from django.db import models

# Create your models here.


class Paste(models.Model):
    text = models.TextField()
    name = models.CharField(max_length=40, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name or str(self.id)

    @models.permalink
    def get_absolute_url(self):
        return ('pastebin_paste_detail', [self.id])

