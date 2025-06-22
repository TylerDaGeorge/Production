from . import Response, Depends
import inspect

class TestClient:
    """Very small stub for fastapi.testclient.TestClient."""
    def __init__(self, app):
        self.app = app

    def _call(self, handler, json, path_params=None):
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
            elif path_params and name in path_params:
                kwargs[name] = path_params[name]
        if json and not kwargs and len(sig.parameters) == 1:
            # if single body parameter, pass entire json
            param_name = next(iter(sig.parameters))
            kwargs[param_name] = json
        return handler(**kwargs)

    def get(self, path):
        handler, params = self.app._match_route("GET", path)
        if handler is None:
            return Response(None, status_code=404)
        result = self._call(handler, None, params)
        return Response(result, status_code=200)

    def post(self, path, json=None):
        handler, params = self.app._match_route("POST", path)
        if handler is None:
            return Response(None, status_code=404)
        result = self._call(handler, json or {}, params)
        return Response(result, status_code=200)


