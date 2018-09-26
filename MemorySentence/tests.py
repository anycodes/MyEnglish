from django.test import TestCase
import base64
import binascii
import hashlib
import hmac
import random
import sys
import time
import json
import urllib.request
# Create your tests here.


def translationFun(textData):
    # 设置参数
    param = {}
    # 公共参数
    # Nonce最好是随机数
    param["Nonce"] = random.randint(1, sys.maxsize)
    # Timestamp最好是当前时间戳
    param["Timestamp"] = int(time.time())
    param["Region"] = "ap-guangzhou"
    param["SecretId"] = "AKID1ynRAoVcoqrDUbwR9RbcS7mKrOl1q0kK"
    param["Action"] = "TextTranslate"
    param["Version"] = "2018-03-21"
    param["SourceText"] = textData
    param["Source"] = "en"
    param["Target"] = "zh"
    param["ProjectId"] = "1"

    # 生成待签名字符串
    sign_str = "GETtmt.tencentcloudapi.com/?"
    sign_str += "&".join("%s=%s" % (k, param[k]) for k in sorted(param))

    # 生成签名
    secret_key = "cCoJncN0BHLG2jGvcAYlXWRI5kFZj5Oa"
    if sys.version_info[0] > 2:
        sign_str = bytes(sign_str, "utf-8")
        secret_key = bytes(secret_key, "utf-8")
    hashed = hmac.new(secret_key, sign_str, hashlib.sha1)
    signature = binascii.b2a_base64(hashed.digest())[:-1]
    if sys.version_info[0] > 2:
        signature = signature.decode()

    requestStr = "https://" + sign_str.decode("utf-8")[3:] + "&Signature=" + signature
    responseData = urllib.request.urlopen(requestStr).read().decode("utf-8")
    jsonData = json.loads(responseData)["Response"]["TargetText"]
    return jsonData


def textToVoiceFun(textData):
    # 设置参数
    param = {}
    # 公共参数
    # Nonce最好是随机数
    param["Nonce"] = random.randint(1, sys.maxsize)
    # Timestamp最好是当前时间戳
    param["Timestamp"] = int(time.time())
    param["Region"] = "ap-guangzhou"
    param["SecretId"] = "AKID1ynRAoVcoqrDUbwR9RbcS7mKrOl1q0kK"
    param["Action"] = "TextToVoice"
    param["Version"] = "2018-05-22"
    param["Text"] = textData
    param["SessionId"] = param["Nonce"]
    param["ModelType"] = "1"

    # 生成待签名字符串
    sign_str = "GETaai.tencentcloudapi.com/?"
    sign_str += "&".join("%s=%s" % (k, param[k]) for k in sorted(param))

    # 生成签名
    secret_key = "cCoJncN0BHLG2jGvcAYlXWRI5kFZj5Oa"
    if sys.version_info[0] > 2:
        sign_str = bytes(sign_str, "utf-8")
        secret_key = bytes(secret_key, "utf-8")
    hashed = hmac.new(secret_key, sign_str, hashlib.sha1)
    signature = binascii.b2a_base64(hashed.digest())[:-1]
    if sys.version_info[0] > 2:
        signature = signature.decode()
    requestStr = "https://" + sign_str.decode("utf-8")[3:] + "&Signature=" + signature
    responseData = urllib.request.urlopen(requestStr).read().decode("utf-8")
    jsonData = json.loads(responseData)["Response"]["Audio"]
    return jsonData

with open("test.wav","wb") as f:
    wavData = base64.b64decode(textToVoiceFun("what are you doing?"))
    f.write(wavData)