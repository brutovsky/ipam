from .urls import pages, sidebar_navigation


def navigation_middleware(get_response):
    def middleware(request):
        paths = request.path.split('/')[:-1]

        if len(paths) > 1 and paths[1] != 'api' and paths[1] != 'admin':
            navigation = []
            for path in paths:
                navigation.append(pages[path])
            request.navigation = navigation[:-1]

            if paths[1] == 'users':
                request.current_component = 'Users Component'

            if paths[1] == 'ipam':
                request.current_component = 'IPAM Component'

            request.last_link = navigation[-1]
            request.title = navigation[-1][2]

        request.sidebar_navigation = sidebar_navigation

        response = get_response(request)

        return response

    return middleware
