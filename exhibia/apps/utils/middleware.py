__author__ = 'vh5'
class MemberMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            try:
                member = request.user.get_profile()
            except:
                member = None
        else:
            try:
                member = request.user.get_profile()
            except:
                member = None
        request.member = member
