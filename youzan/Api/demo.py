import random

from django.contrib.auth.models import User
from django.http.response import HttpResponse
from Api.resources import Rest
import json

from interapp.models import UC


class Demo(Rest):
    def get(self, request, *args, **kwargs):
        data = request.GET
        username = data.get("username", "")
        password = data.get("password", "")
        entu_password = data.get("entu_password", "")
        category = data.get("category", "")
        if password != entu_password:
            data = {
                "msg": "两次密码要一致"
            }
            return HttpResponse(json.dumps(data), content_type="application/json", status=200)
        elif not username:
            data = {
                "msg": "用户名不允许为空"
            }
            return HttpResponse(json.dumps(data), content_type="application/json", status=200)
        user = User()
        user.username = username
        user.set_password(password)
        user.save()
        if category == "customer":
            uc = UC()
            uc.user = user
            uc.stack_ID = "9527"
            uc.save()
        data_return = {
            "msg": "ok"
        }
        return HttpResponse(json.dumps(data_return), content_type="application/json", status=200)


def post(self, request, *args, **kwargs):
    return HttpResponse(json.dumps("name"), content_type="application/json", status=200)
