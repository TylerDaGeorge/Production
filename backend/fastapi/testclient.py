from . import Response

class TestClient:
    """Very small stub for fastapi.testclient.TestClient."""
    def __init__(self, app):
        self.app = app

    def get(self, path):
        handler = self.app.routes.get(("GET", path))
        if handler is None:
            return Response(None, status_code=404)
        result = handler()
        return Response(result, status_code=200)

    def post(self, path, json=None):
        handler = self.app.routes.get(("POST", path))
        if handler is None:
            return Response(None, status_code=404)
        if json is None:
            result = handler()
        else:
            result = handler(json)
        return Response(result, status_code=200)
