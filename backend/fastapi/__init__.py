class Response:
    """Simple response object mimicking FastAPI's TestClient return."""
    def __init__(self, json_data, status_code=200):
        self._json = json_data
        self.status_code = status_code
    def json(self):
        return self._json

class FastAPI:
    """Very small subset of FastAPI used for tests."""
    def __init__(self, title=None):
        self.title = title
        self.routes = {}

    async def __call__(self, scope, receive, send):
        """Minimal ASGI callable so ``uvicorn`` can run this stub."""
        if scope["type"] != "http":
            raise NotImplementedError("Only HTTP scope supported")
        handler = self.routes.get((scope["method"], scope["path"]))
        if handler is None:
            status = 404
            body = b"not found"
        else:
            try:
                result = handler({}) if handler.__code__.co_argcount else handler()
            except HTTPException as exc:
                status = exc.status_code
                body = exc.detail.encode()
            else:
                import json
                body = json.dumps(result).encode()
                status = 200
        await send({"type": "http.response.start", "status": status, "headers": []})
        await send({"type": "http.response.body", "body": body})

    def get(self, path):
        def decorator(func):
            self.routes[("GET", path)] = func
            return func
        return decorator

    def post(self, path):
        def decorator(func):
            self.routes[("POST", path)] = func
            return func
        return decorator


class Depends:
    def __init__(self, dependency):
        self.dependency = dependency


class HTTPException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
