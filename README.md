# MyEnglish

## 基本描述
这是一个背单词的软件，参考地址：http://word.0duzhan.com

## 使用方法
* 上传程序到服务器
* 同步数据库
* 在MemorySentence/views.py中配置自己的腾讯云云API密钥，分别在27,40，63,75
* 记住自己的token，在文件MemorySentence/views.py中第111行：if request.GET.get("token") != "mytoken123":
* 通过页面/input/?token=你设定的token，默认为mytoken123,录入英文句子，每行一个，点击提交即可
* 通过/admin页面来管理已经录入的句子
* 通过首页/index来学习背诵，点击英文句子，可以朗读

## 说明
* 本工具，用到了腾讯云云API中的tmt和aai
* 部分代码来自腾讯云云API的explorer

## 作者想说
因为我这段时间在准备英语考试，所以在背单词，朋友建议我，通过例句来背单词，但是我太笨了，没找到类似的背单词软件，所以就自己写了这样一个工具，来辅助自己背单词，主要特色就是，录入英文，自动翻译中文，自动生成音频，然后自己就可以每天看，每天背诵，不会的看英文，不会读的听音频，祝自己英语考试顺利。
* 联系邮箱：service@52exe.cn
* 个人主页：http://www.0duzhan.com
