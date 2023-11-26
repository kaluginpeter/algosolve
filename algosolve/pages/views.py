from django.shortcuts import render

from http import HTTPStatus


def page_not_found(request, exception):
    return render(
        request,
        'pages/404.html',
        status=HTTPStatus.NOT_FOUND.value)


def csrf_failure(request, reason=''):
    return render(
        request,
        'pages/403csrf.html',
        status=HTTPStatus.FORBIDDEN.value)


def server_error(request):
    return render(
        request,
        'pages/500.html',
        status=HTTPStatus.INTERNAL_SERVER_ERROR.value)
