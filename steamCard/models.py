# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class SteamKey(models.Model):
    # id
    admin_id = models.IntegerField(primary_key=True, blank=False)
    # steam api key
    api_key = models.CharField(blank=False, max_length=36)  
    # remark
    remark = models.CharField(blank=False, max_length=36)  
    
    def __unicode__(self):  
        return self.admin_id
