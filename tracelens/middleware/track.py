from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from tracelens.logging.writer import LogWriter
from tracelens.core.recorder import Recorder
from tracelens.core.config.model import TraceLensConfig
from tracelens.core.hasher import hash_endpoint
from tracelens.logging.writer import LogWriter

class TraceLensMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        config: TraceLensConfig,
        writer: LogWriter | None = None,
    ):
        super().__init__(app)
        self._config = config
        self._writer = writer or LogWriter(config)
        self._recorder = Recorder(config, self._writer)

    async def dispatch(self, request: Request, call_next):
        if not self._config.enabled:
            return await call_next(request)

        start_time = self._recorder.start_timer()

        response = None
        error = None

        try:
            response = await call_next(request)
            

        except Exception as exc:
            error = exc
            raise

        finally:
            try:
                endpoint = request.url.path
                if self._config.hash_endpoints:
                    endpoint = hash_endpoint(endpoint)

                status_code = (
                    response.status_code if response is not None else 500
                )

                self._recorder.record(
                    start_time=start_time,
                    endpoint=endpoint,
                    method=request.method,
                    status_code=status_code,
                    error=str(error) if error else None,
                )

            except Exception as e:
                return
            
            return response