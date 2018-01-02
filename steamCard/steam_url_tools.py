# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests

class SteamUrlTools:
    @classmethod
    def getProfileUrl(cls, steam_id):
        return "http://steamcommunity.com/profiles/%s" % (steam_id,)

    @classmethod
    def getStatUrl(cls, steam_id, app_id):
        return "http://steamcommunity.com/profiles/%s/stats/%d" % (steam_id, app_id)

    @classmethod
    def getStoreUrl(cls, app_id):
        return "http://store.steampowered.com/app/%d" % (app_id)

    @classmethod
    def getAppImgUrl(cls, app_id, img_url):
        return "http://media.steampowered.com/steamcommunity/public/images/apps/%d/%s.jpg" % (app_id, img_url)

    @classmethod
    def getAppLogoUrl(cls, app_id, logo_url):
        return "http://media.steampowered.com/steamcommunity/public/images/apps/%d/%s.jpg" % (app_id, logo_url)
