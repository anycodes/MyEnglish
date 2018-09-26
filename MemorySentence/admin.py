from django.contrib import admin
import MemorySentence.models
# Register your models here.

class SentenceAdmin(admin.ModelAdmin):
    list_display = ('sid','content','chinese')

admin.site.register(MemorySentence.models.Sentence,SentenceAdmin)