import json
from django.http.response import HttpResponse

from django.http.multipartparser import MultiPartParser
from django.middleware.common import MiddlewareMixin


class MiddlewareChange(MiddlewareMixin):
    def process_request(self, request):
        method = request.method
        if "application/json" in request.content_type:
            try:
                data = json.loads(request.body.decode())
                files = None
            except Exception as e:
                return HttpResponse(
                    json.dumps({
                        "status": 422,
                        "msg": "参数错误",

                    }), content_type="application/json")
        elif "multipart/form-data" in request.content_type:
            data, files = MultiPartParser(request.META, request, request.upload_handlers).parse()
        else:
            data = request.GET
            files = None
        if "HTTP_X_METHOD" in request.META:
            method = request.META["HTTP_X_METHOD"].upper()
            setattr(request, "method", method)
        if files:
            setattr(request, "{method}_FILES".format(method=method), files)
        setattr(request, method, data)
