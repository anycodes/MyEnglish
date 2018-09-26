from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import MemorySentence.models
import base64
import binascii
import hashlib
import hmac
import random
import sys
import time
import json
import urllib.request
import urllib.parse
from django.core.paginator import *
# Create your views here.

def translationFun(textData):
    # 设置参数
    param = {}
    # 公共参数
    # Nonce最好是随机数
    param["Nonce"] = random.randint(1, sys.maxsize)
    # Timestamp最好是当前时间戳
    param["Timestamp"] = int(time.time())
    param["Region"] = "ap-guangzhou"
    param["SecretId"] = ""
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
    secret_key = ""
    if sys.version_info[0] > 2:
        sign_str = bytes(sign_str, "utf-8")
        secret_key = bytes(secret_key, "utf-8")
    hashed = hmac.new(secret_key, sign_str, hashlib.sha1)
    signature = binascii.b2a_base64(hashed.digest())[:-1]
    if sys.version_info[0] > 2:
        signature = signature.decode()

    requestStr = "https://" + sign_str.decode("utf-8")[3:] + "&Signature=" + urllib.parse.quote(signature)
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
    param["SecretId"] = ""
    param["Action"] = "TextToVoice"
    param["Version"] = "2018-05-22"
    param["Text"] = textData
    param["SessionId"] = param["Nonce"]
    param["ModelType"] = "1"

    # 生成待签名字符串
    sign_str = "GETaai.tencentcloudapi.com/?"
    sign_str += "&".join("%s=%s" % (k, param[k]) for k in sorted(param))

    # 生成签名
    secret_key = ""
    if sys.version_info[0] > 2:
        sign_str = bytes(sign_str, "utf-8")
        secret_key = bytes(secret_key, "utf-8")
    hashed = hmac.new(secret_key, sign_str, hashlib.sha1)
    signature = binascii.b2a_base64(hashed.digest())[:-1]
    if sys.version_info[0] > 2:
        signature = signature.decode()
    requestStr = "https://" + sign_str.decode("utf-8")[3:] + "&Signature=" + urllib.parse.quote(signature)
    responseData = urllib.request.urlopen(requestStr).read().decode("utf-8")
    jsonData = json.loads(responseData)["Response"]["Audio"]
    return jsonData

def index(request):

    pageNum = request.GET.get("page",1)

    dataList = MemorySentence.models.Sentence.objects.all().order_by("-sid")
    paginator = Paginator(dataList, 10)
    # 对传递过来的页面进行判断，页码最小为1，最大为分页器所得总页数
    if pageNum < 0:
        pageNum = 1
    if pageNum > paginator.num_pages:
        pageNum = paginator.num_pages
    # 分页器获得当前页面的数据内容
    pageList = paginator.page(pageNum)

    return render(request, "index.html", locals())


@csrf_exempt
def input(request):

    if request.GET.get("token") != "mytoken123":
        return JsonResponse({
                "code":"-1",
                "message":"No Sign!"
            })

    if request.method == "POST":
        inputText = request.POST.get("text")

        for eveLine in inputText.split("\n"):
            englishSentence = eveLine.strip()
            if englishSentence:
                chinese = translationFun(englishSentence)
                voice = textToVoiceFun(englishSentence)

                hl = hashlib.md5()
                hl.update(voice.encode(encoding='utf-8'))
                name = hl.hexdigest()

                with open( "wavFile/" + name + ".wav", "wb") as f:
                    wavData = base64.b64decode(voice)
                    f.write(wavData)

                '''
                sid = models.AutoField(primary_key=True)
                content = models.TextField(verbose_name="英文句子")
                wav = models.CharField(max_length=150, verbose_name="音频路径")
                chinese = models.CharField(max_length=150, verbose_name="中文翻译")
                date = models.DateTimeField(auto_now_add=True, verbose_name="存入时间")
                remark = models.CharField(max_length=150, verbose_name="备注说明")
               '''
                try:
                    MemorySentence.models.Sentence.objects.create(
                        content = englishSentence,
                        chinese = chinese,
                        wav = name,
                    )
                except:
                    pass

    return render(request, "input.html", locals())
