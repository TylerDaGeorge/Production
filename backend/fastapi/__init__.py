class Response:
    """Simple response object mimicking FastAPI's TestClient return."""
    def __init__(self, json_data, status_code=200):
        self._json = json_data
        self.status_code = status_code
    def json(self):
        return self._json

class FastAPI:
    """Very small subset of FastAPI used for tests and simple local runs."""

    """Very small subset of FastAPI used for tests."""
    def __init__(self, title=None):
        self.title = title
        self.routes = {}

    def _call(self, handler, json_payload, path_params=None):
        import inspect
        kwargs = {}
        sig = inspect.signature(handler)
        for name, param in sig.parameters.items():
            default = param.default
            if isinstance(default, Depends):
                dep = default.dependency
                val = dep()
                val = next(val) if hasattr(val, "__iter__") else val
                kwargs[name] = val
            elif json_payload and name in json_payload:
                kwargs[name] = json_payload[name]
            elif path_params and name in path_params:
                kwargs[name] = path_params[name]
        if json_payload and not kwargs and len(sig.parameters) == 1:
            param_name = next(iter(sig.parameters))
            kwargs[param_name] = json_payload
        return handler(**kwargs)

    def _match_route(self, method, path):
        handler = self.routes.get((method, path))
        if handler:
            return handler, {}
        for (m, pattern), func in self.routes.items():
            if m != method or "{" not in pattern:
                continue
            p_parts = pattern.strip("/").split("/")
            path_parts = path.strip("/").split("/")
            if len(p_parts) != len(path_parts):
                continue
            params = {}
            matched = True
            for pp, actual in zip(p_parts, path_parts):
                if pp.startswith("{") and pp.endswith("}"):
                    params[pp[1:-1]] = actual
                elif pp != actual:
                    matched = False
                    break
            if matched:
                return func, params
        return None, None

    async def __call__(self, scope, receive, send):
        """Minimal ASGI callable so ``uvicorn`` can run this stub."""
        if scope["type"] != "http":
            raise NotImplementedError("Only HTTP scope supported")

        handler, path_params = self._match_route(scope["method"], scope["path"])
        if handler is None:
            status = 404
            body = b"not found"
        else:
            import json
            raw_body = b""
            while True:
                message = await receive()
                raw_body += message.get("body", b"")
                if not message.get("more_body"):
                    break
            json_payload = json.loads(raw_body.decode() or "null") if raw_body else None
            try:
                result = self._call(handler, json_payload, path_params)
            except HTTPException as exc:
                status = exc.status_code
                body = exc.detail.encode()
            else:
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

    def delete(self, path):
        def decorator(func):
            self.routes[("DELETE", path)] = func
            return func
        return decorator


class Depends:
    def __init__(self, dependency):
        self.dependency = dependency


class HTTPException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
