import json

from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse


class Rest:
    def __init__(self, name=None):
        self.name = name or __class__.__name__.lower()

    def enter(self, request, *args, **kwargs):
        method = request.method
        if method == "GET":
            return self.get(request, *args, **kwargs)
        elif method == "DELETE":
            return self.delete(request, *args, **kwargs)
        elif method == "PUT":
            return self.put(request, *args, **kwargs)
        elif method == "POST":
            return self.post(request, *args, **kwargs)
        else:
            return HttpResponse("不支持其他方法")

    def get(self, request, *args, **kwargs):
        data = {
            "msg": "方法不支持"
        }
        return HttpResponse(json.dumps(data), content_type="application/json", status=405)

    def delete(self, request, *args, **kwargs):
        data = {
            "msg": "方法不支持"
        }
        return HttpResponse(json.dumps(data), content_type="application/json", status=405)

    def put(self, request, *args, **kwargs):
        data = {
            "msg": "方法不支持"
        }
        return HttpResponse(json.dumps(data), content_type="application/json", status=405)

    def post(self, request, *args, **kwargs):
        data = {
            "msg": "方法不支持"
        }
        return HttpResponse(json.dumps(data), content_type="application/json", status=405)


class Register:
    def __init__(self, version="v1"):
        self.name = version
        self.resources = []

    def regist(self, resource):
        self.resources.append(resource)

    @property
    def urls(self):
        urlpatterns = [
            url(r"{version}/{name}$".format(version=self.name, name=obj.name), csrf_exempt(obj.enter)) for obj in
            self.resources
        ]
        return urlpatterns