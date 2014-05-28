jQuery(document).ready(function($) {

    //button-top
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('#go-up').show();
        } else {
            $('#go-up').hide();
        }
    });

    $('#go-up').click(function () {
        $('.header').ScrollTo(0);
    });

    function display_form_errors(errors, captcha, $form) {
        if(captcha) {
            $('.captcha').closest('tr').empty().append(captcha);
        }
        for (var k in errors) {
            $form.find('label.error[for="id_' + k + '"]').append(errors[k]).show()
        }

    }

    $('body').on('click', '.ajax-submit', function () {
        var id = $(this).attr('id');
        $('#' + id + '-form').ajaxSubmit({
            success: function (data, statusText, xhr, $form) {
                // Удаляем ошибки если были
                $form.find('.error').empty().hide();
                if (data['result'] == 'success') {
                    if (data.hasOwnProperty('next')) {
                        next = data['next'];
                        window.location.href = next;
                    }
                    else {
                        window.location.reload();
                    }
                }
                else if (data['result'] == 'error') {
                    display_form_errors(data['response'], data['captcha'], $form);
                }
            },
            dataType: 'json'
        });
    });
});