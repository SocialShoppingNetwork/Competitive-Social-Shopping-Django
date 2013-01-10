__author__ = 'vh5'
class MemberMiddleware(object):
    def process_request(self, request):
        member = None
        if request.user.is_authenticated():
            try:
                member = request.user.get_profile()
            except: pass
        request.member = member
