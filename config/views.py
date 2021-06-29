from django.shortcuts import render


def about(request):
    template_page = 'about.html'
    return render(request, template_page)


def page_not_found(request, exception):
    title = 'Ошибка 404'
    return render(
        request,
        'misc/404.html',
        {'path': request.path, 'title': title},
        status=404
    )


def server_error(request):
    title = 'Ошибка 500'
    return render(
        request,
        'misc/500.html',
        {'title': title},
        status=500
    )
