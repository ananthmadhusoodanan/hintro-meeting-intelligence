import uuid
import logging
import time

logger = logging.getLogger(__name__)


class TraceMiddleware:
    """
    Adds a unique trace ID to every request.
    This lets you track a request through all your logs.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Generate trace ID from request header, or create a new one
        trace_id = request.headers.get('X-Trace-Id', str(uuid.uuid4()))
        request.trace_id = trace_id

        start_time = time.time()

        response = self.get_response(request)

        duration_ms = round((time.time() - start_time) * 1000)

        # Log every request with trace ID
        logger.info(
            f"[{trace_id}] {request.method} {request.path} "
            f"→ {response.status_code} ({duration_ms}ms)"
        )

        # Include trace ID in every response header
        response['X-Trace-Id'] = trace_id
        return response