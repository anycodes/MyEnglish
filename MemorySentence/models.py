from django.db import models

# Create your models here.


class Sentence(models.Model):
    sid = models.AutoField(primary_key=True)
    content = models.TextField(verbose_name="英文句子", unique=True)
    wav = models.CharField(max_length=150, verbose_name="音频路径")
    chinese = models.CharField(max_length=150, verbose_name="中文翻译")
    date = models.DateTimeField(auto_now_add=True, verbose_name="存入时间")
    remark = models.CharField(max_length=150, verbose_name="备注说明", blank=True, null=True)


    class Meta:
        verbose_name = "句子背诵"
        verbose_name_plural = verbose_name
        ordering = ["-sid"]

    def __str__(self):
        return self.content