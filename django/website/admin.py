# XXX Hack to modify flatpage form
# https://djangosnippets.org/snippets/1035/
# http://stackoverflow.com/questions/1833287/change-field-in-django-flatpages-admin

# Note: This file is loaded from website/urls.py, since it have to come
#       after autodiscover, because we can't unregister FlatPage until
#       it's already been registered.

#from django import forms
from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
#from django.contrib.flatpages.admin import FlatPageAdmin, FlatpageForm
from django.contrib.flatpages.admin import FlatPageAdmin

from tinymce4.widgets import TinyMCE


from django.db import models
class MyFlatPageAdmin (FlatPageAdmin):
    formfield_overrides = {
        models.TextField: { 'widget': TinyMCE },
        #models.TextField: { 'widget': TinyMCE (attrs={'cols': 20, 'rows': 20}) },
    }


#from django.utils.translation import ugettext_lazy as _
#class MyFlatpageForm (FlatpageForm):
#    content = forms.CharField (label = _(u'content'), required=False,
#                               widget = TinyMCE())
#
#class MyFlatPageAdmin (FlatPageAdmin):
#    form = MyFlatpageForm


admin.site.unregister (FlatPage)
admin.site.register (FlatPage, MyFlatPageAdmin)
