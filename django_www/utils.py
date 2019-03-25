from django.http import JsonResponse


def resp_err(message, err='', code=400):
    content = {
        "status": False,
        "message": message,
        "err_number": err
    }

    return JsonResponse(content, status=code)


def resp_success(data, code=200):
    content = {
        "status": True,
        "data": data
    }
    return JsonResponse(content, status=code)