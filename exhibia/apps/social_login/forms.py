import re

from django import forms
from django.forms.util import ErrorDict
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.translation import ugettext_lazy as _, ugettext

from django.contrib import messages
from django.contrib.auth.models import User

from emailconfirmation.models import EmailAddress

from pinax.apps.account.utils import perform_login



alnum_re = re.compile(r"^\w+$")


# @@@ might want to find way to prevent settings access globally here.
REQUIRED_EMAIL = getattr(settings, "ACCOUNT_REQUIRED_EMAIL", False)
EMAIL_VERIFICATION = getattr(settings, "ACCOUNT_EMAIL_VERIFICATION", False)
EMAIL_AUTHENTICATION = getattr(settings, "ACCOUNT_EMAIL_AUTHENTICATION", False)
UNIQUE_EMAIL = getattr(settings, "ACCOUNT_UNIQUE_EMAIL", False)

class GroupForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.group = kwargs.pop("group", None)
        super(GroupForm, self).__init__(*args, **kwargs)


class SignupForm(GroupForm):

    username = forms.CharField(
        label = _("Username"),
        max_length = 30,
        widget = forms.TextInput()
    )
    social_username = forms.CharField(
        label = _("Social Username"),
        max_length = 30,
        widget = forms.TextInput(),
        required = False,
    )
    password1 = forms.CharField(
        label = _("Password"),
        widget = forms.PasswordInput(render_value=False)
    )
    password2 = forms.CharField(
        label = _("Password (again)"),
        widget = forms.PasswordInput(render_value=False)
    )
    email = forms.EmailField(widget=forms.TextInput())
    agree_with_terms = forms.BooleanField(label = _("I reviewed and accept the terms and conditions"),
                                          widget = forms.CheckboxInput())
    confirmation_key = forms.CharField(
        max_length = 40,
        required = False,
        widget = forms.HiddenInput()
    )
    backend = forms.CharField(
        max_length = 255,
        required = False,
        widget = forms.HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        if REQUIRED_EMAIL or EMAIL_VERIFICATION or EMAIL_AUTHENTICATION:
            self.fields["email"].label = ugettext("Email")
            self.fields["email"].required = True
        else:
            self.fields["email"].label = ugettext("Email (optional)")
            self.fields["email"].required = False

    def clean_username(self):
        if not alnum_re.search(self.cleaned_data["username"]):
            raise forms.ValidationError(_("Usernames can only contain letters, numbers and underscores."))
        try:
            user = User.objects.get(username__iexact=self.cleaned_data["username"])
        except User.DoesNotExist:
            return self.cleaned_data["username"]
        raise forms.ValidationError(_("This username is already taken. Please choose another."))

    def clean_email(self):
        value = self.cleaned_data["email"]
        if UNIQUE_EMAIL or EMAIL_AUTHENTICATION:
            try:
                User.objects.get(email__iexact=value)
            except User.DoesNotExist:
                return value
            raise forms.ValidationError(_("A user is registered with this email address."))
        return value

    def is_valid_for_backend(self):
        self.cleaned_data = {}
        self._errors = ErrorDict()
        fields = ['username', 'agree_with_terms']
        is_valid = True
        for name in fields:
            field = self.fields[name]
            value = field.widget.value_from_datadict(self.data, self.files, self.add_prefix(name))
            try:
                value = field.clean(value)
                self.cleaned_data[name] = value
                if hasattr(self, 'clean_%s' % name):
                    value = getattr(self, 'clean_%s' % name)()
                    self.cleaned_data[name] = value
            except ValidationError, e:
                self._errors[name] = self.error_class(e.messages)
                is_valid = False
        return is_valid

    def get_agree_with_terms(self):
        self._errors = ErrorDict()
        field = self.fields['agree_with_terms']
        value = field.widget.value_from_datadict(self.data, self.files, self.add_prefix('agree_with_terms'))
        try:
            value = field.clean(value)
            is_valid = True
        except ValidationError, e:
            self._errors['agree_with_terms'] = self.error_class(e.messages)
            is_valid = False
        return value, is_valid

    def del_errors(self):
        self._errors = ErrorDict()

    def clean(self):
        if "password1" in self.cleaned_data and "password2" in self.cleaned_data:
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                raise forms.ValidationError(_("You must type the same password each time."))
        return self.cleaned_data

    def create_user(self, username=None, commit=True):
        user = User()
        if username is None:
            raise NotImplementedError("SignupForm.create_user does not handle "
                "username=None case. You must override this method.")
        user.username = username
        user.email = self.cleaned_data["email"].strip().lower()
        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        if commit:
            user.save()
        return user

    def login(self, request, user):
        # nasty hack to get get_user to work in Django
        user.backend = "django.contrib.auth.backends.ModelBackend"
        perform_login(request, user)

    def save(self, request=None):
        # don't assume a username is available. it is a common removal if
        # site developer wants to use email authentication.
        username = self.cleaned_data.get("username")
        email = self.cleaned_data["email"]

        if self.cleaned_data["confirmation_key"]:
            from friends.models import JoinInvitation # @@@ temporary fix for issue 93
            try:
                join_invitation = JoinInvitation.objects.get(confirmation_key=self.cleaned_data["confirmation_key"])
                confirmed = True
            except JoinInvitation.DoesNotExist:
                confirmed = False
        else:
            confirmed = False

        # @@@ clean up some of the repetition below -- DRY!

        if confirmed:
            if email == join_invitation.contact.email:
                new_user = self.create_user(username)
                join_invitation.accept(new_user) # should go before creation of EmailAddress below
                if request:
                    messages.add_message(request, messages.INFO,
                        ugettext(u"Your email address has already been verified")
                    )
                # already verified so can just create
                EmailAddress(user=new_user, email=email, verified=True, primary=True).save()
            else:
                new_user = self.create_user(username)
                join_invitation.accept(new_user) # should go before creation of EmailAddress below
                if email:
                    if request:
                        messages.add_message(request, messages.INFO,
                            ugettext(u"Confirmation email sent to %(email)s") % {
                                "email": email,
                            }
                        )
                    EmailAddress.objects.add_email(new_user, email)
        else:
            new_user = self.create_user(username)
            if email:
                if request and not EMAIL_VERIFICATION:
                    messages.add_message(request, messages.INFO,
                        ugettext(u"Confirmation email sent to %(email)s") % {
                            "email": email,
                        }
                    )
                EmailAddress.objects.add_email(new_user, email)

        if EMAIL_VERIFICATION:
            new_user.is_active = False
            new_user.save()

        self.after_signup(new_user)

        return new_user

    def after_signup(self, user, **kwargs):
        """
        An extension point for subclasses.
        """
        pass
