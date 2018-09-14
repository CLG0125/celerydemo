import hashlib
import random
import time

from django.contrib.auth.models import User
from django.http.response import HttpResponse

from Api.addtoken import encrypt, get_payload
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
        data = request.POST
        username = data.get("username", "")
        password = data.get("password", "")
        obj = User.objects.filter(username=username).first()
        if obj and obj.check_password(password):
            HEADER = {"NAME": 'big'}
            header = encrypt(HEADER)
            en_data = {'username': obj.username, "stack_id": obj.uc.stack_ID, "expiry_time": time.time() + 3}
            payload = encrypt(en_data)
            md5 = hashlib.md5()
            md5.update("{header}.{payload}".format(header=header, payload=payload).encode())
            signature = md5.hexdigest()
            token = "{header}.{payload}.{signature}".format(header=header, payload=payload, signature=signature)
            return_content = {
                "token": token,
                "msg": "ok",
            }
            return HttpResponse(json.dumps(return_content), content_type="application/json", status=200)
        else:
            return_content = {
                "msg": "用户名不存在"
            }
            return HttpResponse(json.dumps(return_content), content_type="application/json", status=200)

    def put(self, request, *args, **kwargs):
        data = request.PUT
        token = data.get("token")
        try:
            expiry_time = get_payload(token)["expiry_time"]
        except:
            return_content = {
                "msg": "token错误"
            }
            return HttpResponse(json.dumps(return_content), content_type="application/json", status=403)
        if expiry_time >= time.time():
            return_content = {
                "msg": "可以执行接下来的操作"
            }
            return HttpResponse(json.dumps(return_content), content_type="application/json", status=200)
        else:
            return HttpResponse(json.dumps({"msg": "您的token已经过期请重新登录"}), content_type="application/json", status=403)
