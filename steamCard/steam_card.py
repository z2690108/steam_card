# -*- coding: utf-8 -*-

# ---------------------------------------------------------------
#
# check steam web API from: https://developer.valvesoftware.com
#
# ---------------------------------------------------------------

from __future__ import unicode_literals

from lxml import html
import requests

from .steam_url_tools import SteamUrlTools
from .steam_api import SteamApi

class SteamCard:
    def __init__(self, steam_id, language="en"):
        self.steam_id = steam_id
        self.steam_api = SteamApi(steam_id, language)

    def getSteamCard(self, show_games=False, order_by_2week_games=True):
        try:
            card = {}
            card['basic_info'] = self.steam_api.getBasicInfo()
            card['profile_info'] = self.steam_api.getProfileInfo()

            if show_games:
                card['games'] = self.steam_api.getOwnedGames(order_by_2week_games)

            return card

        except Exception, e:
            print 'Get steam card of ', self.steam_id, ' failed. Exception: ', e
            return {}




