from django.db import models


class Category (models.Model):
    ''' Categories for links in the "nettguide" '''
    name =  models.CharField (max_length=100)
    #comment = model.TextField (help_text='For internal use. Not shown on webpage.')
    def __unicode__ (self):
        return self.name


''' Nettguide '''
class Guide (models.Model):
    category = models.ForeignKey (Category)
    name =     models.CharField (max_length=255)
    url =      models.URLField()
    text =     models.TextField ('description', blank=True)
    lang =     models.CharField (max_length=2, blank=True)
    comment =  models.TextField (blank=True, help_text='For internal use. Not shown on webpage.')
    def __unicode__ (self):
        return self.name
