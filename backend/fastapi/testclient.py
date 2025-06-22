from . import Response, Depends
import inspect

class TestClient:
    """Very small stub for fastapi.testclient.TestClient."""
    def __init__(self, app):
        self.app = app

    def _call(self, handler, json):
        sig = inspect.signature(handler)
        kwargs = {}
        for name, param in sig.parameters.items():
            default = param.default
            if isinstance(default, Depends):
                dep = default.dependency
                val = dep()
                val = next(val) if hasattr(val, '__iter__') else val
                kwargs[name] = val
            elif json and name in json:
                kwargs[name] = json[name]
        if json and not kwargs and len(sig.parameters) == 1:
            # if single body parameter, pass entire json
            param_name = next(iter(sig.parameters))
            kwargs[param_name] = json
        return handler(**kwargs)

    def get(self, path):
        handler = self.app.routes.get(("GET", path))
        if handler is None:
            return Response(None, status_code=404)
        result = self._call(handler, None)
        return Response(result, status_code=200)

    def post(self, path, json=None):
        handler = self.app.routes.get(("POST", path))
        if handler is None:
            return Response(None, status_code=404)
        result = self._call(handler, json or {})
        return Response(result, status_code=200)


