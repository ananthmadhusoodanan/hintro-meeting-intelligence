from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    request = context.get('request')
    trace_id = getattr(request, 'trace_id', None)

    if response is not None:
        # Get a clean error message
        if isinstance(response.data, dict):
            message = response.data.get('detail', str(response.data))
        else:
            message = str(response.data)

        response.data = {
            "traceId": trace_id,
            "success": False,
            "error": {
                "code": _get_error_code(response.status_code),
                "message": message
            }
        }
    return response


def _get_error_code(status_code):
    codes = {
        400: "VALIDATION_ERROR",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        500: "INTERNAL_SERVER_ERROR",
    }
    return codes.get(status_code, "ERROR")
