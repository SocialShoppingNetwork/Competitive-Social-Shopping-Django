def member(request):
    try:
        member = request.user.get_profile()
    except Exception, e:
        member = None
    return {'member': member}
