from django.http import JsonResponse


def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/post/:post_id',
        'GET /api/comment/:comment_id',
    ]
    return JsonResponse(routes, safe=False)
