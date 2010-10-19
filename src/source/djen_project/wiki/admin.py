from django.contrib import admin

from models import Article, Edit

class EditInline(admin.StackedInline):
    model = Edit
    extra = 1
    exclude = ['editor']

class ArticleAdmin(admin.ModelAdmin):
    inlines = (EditInline,)


admin.site.register(Article, ArticleAdmin)

