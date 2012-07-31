def member(request):
    try:
        member = request.user.get_profile()
    except Exception, e:
        member = None
    return {'member': member}

def settings(request):
    import settings
    return {'SOCKETIO_SERVER':settings.SOCKETIO_SERVER}