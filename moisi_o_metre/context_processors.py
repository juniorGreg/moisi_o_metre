from django.conf import settings

def debug_processor(request):
    return {"debug": settings.DEBUG}
