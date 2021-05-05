from .urls import pages


def navigation_middleware(get_response):
    def middleware(request):
        paths = request.path.split('/')[:-1]

        if len(paths) > 1 and paths[1] != 'api' and paths[1] != 'admin':
            navigation = []
            for path in paths:
                navigation.append(pages[path])
            request.navigation = navigation

            request.title = navigation[-1][2]

        response = get_response(request)

        return response

    return middleware
