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
from .models import SteamKey

proxies = {
            "http":"socks5://127.0.0.1:1080",
            "https":"socks5://127.0.0.1:1080"
          }

class SteamApi:
    def __init__(self, steam_id, language="en"):
        self.steam_id = steam_id
        self.key = SteamKey.objects.get(admin_id = 1).api_key
        self.language = language

        self.profiles_url = SteamUrlTools.getProfileUrl(self.steam_id,)

    '''
        return:
            info: basic information of steam account.
                steam_id: steam id.
                persona_name: name of steam.
                avatar: the URL of avator.
                avatar_m: the URL of mediume size avator.
                avatar_f: the URL of full size avator.
                visibility_state: whether the profile is visible or not. 1 - Private, 3 - Public.
    '''

    def getBasicInfo(self):
        try:
            param = {'key':self.key, 'steamids':self.steam_id}
            r = requests.get('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/', params = param)
            players = r.json()['response']['players']
            player = players[0] if len(players) else {}

            info = {}
            if player:
                info['steam_id']            = player['steamid'] if 'steamid' in player else None
                info['persona_name']        = player['personaname'] if 'personaname' in player else None
                info['avatar']              = player['avatar'] if 'avatar' in player else None
                info['avatar_m']            = player['avatarmedium'] if 'avatarmedium' in player else None
                info['avatar_f']            = player['avatarfull'] if 'avatarfull' in player else None
                info['visibility_state']    = player['communityvisibilitystate'] if 'communityvisibilitystate' in player else None
            
            return info

        except Exception, e:
            print 'Get basic info from steam failed. steamid: ', self.steam_id, ' Exception: ', e
            return {}

    '''
        return:
            info: profile information of steam account.
                level: steam level.
                desc: profile summary.
                badges_count: the total amount of badges.
                badges_link_total: the URL of badges page of user.
                badges: a list of badge.
                    badge: badge info.
                        desc: description of badge.
                        link: the URL of badge's page.
                        img: the URL of badge image's page.
    '''

    def getProfileInfo(self):
        try:
            headers = {'Accept-Language': self.language}
            r = requests.get(self.profiles_url, headers = headers)
            tree = html.fromstring(r.text)

            level_list              = tree.xpath('//div[@class="profile_header_badgeinfo_badge_area"]//span[@class="friendPlayerLevelNum"]/text()')
            desc_list               = tree.xpath('//div[@class="profile_summary" or @class="profile_summary noexpand"]//text()')
            badges_count_list       = tree.xpath('//div[@class="profile_badges"]//span[@class="profile_count_link_total"]/text()')
            badges_link_total_list  = tree.xpath('//div[@class="profile_badges"]//div[@class="profile_count_link ellipsis"]//@href')
            badges_desc_list        = tree.xpath('//div[@class="profile_badges"]//div[@class="profile_badges_badge " or @class="profile_badges_badge last"]/@data-community-tooltip')
            badges_link_list        = tree.xpath('//div[@class="profile_badges"]//div[@class="profile_badges_badge " or @class="profile_badges_badge last"]//@href')
            badges_img_list         = tree.xpath('//div[@class="profile_badges"]//div[@class="profile_badges_badge " or @class="profile_badges_badge last"]//img/@src')

            profile_item_list       = tree.xpath('//div[@class="profile_item_links"]/div[@class="profile_count_link ellipsis"]/a')
            item_link_list          = [x.xpath('@href') for x in profile_item_list]
            item_title_list         = [x.xpath('span[@class="count_link_label"]//text()') for x in profile_item_list]
            item_count_list         = [x.xpath('span[@class="profile_count_link_total"]//text()') for x in profile_item_list]

            info = {}
            info['profiles_url'] = self.profiles_url or ''
            info['level'] = level_list[0] if len(level_list) else ''

            def getFrameLevel(level_str):
                if level_str and level_str.isdigit():
                    level = int(level_str)
                    return min(level / 10 * 10 if level < 100 else level / 100 * 100, 3000) if level > 0 else 0
                else:
                    return 0

            info['frame_level'] = getFrameLevel(info['level'])

            desc = []
            for v in desc_list:
                if v.strip():
                    desc.append(v.strip())
            info['desc']  = '\n'.join(desc).strip() if len(desc) else ''

            badges_count_str = badges_count_list[0].strip() if len(badges_count_list) else ''
            badges_count_digit_str = badges_count_str.replace(',', '')
            info['badges_count'] = int(badges_count_digit_str) if badges_count_digit_str.isdigit() else 0
            info['badges_count_str'] = badges_count_str

            info['badges_link_total'] = badges_link_total_list[0] if len(badges_link_total_list) else ''

            info['badges'] = []
            for i in xrange(len(badges_desc_list)):
                badge = {}
                badge['desc'] = badges_desc_list[i].replace('<br>', '').replace('<br />', '') if i < len(badges_desc_list) else ''
                badge['link'] = badges_link_list[i] if i < len(badges_link_list) else ''
                badge['img']  = badges_img_list[i] if i < len(badges_img_list) else ''
                info['badges'].append(badge)

            undisplay_badges_count = info['badges_count'] - len(info['badges'])
            info['undisplay_badges_count'] = undisplay_badges_count if undisplay_badges_count > 0 else 0

            info['items'] = []
            for i in xrange(len(item_title_list)):
                item = {}
                if (item_count_list[i]):
                    count_str = item_count_list[i][0].strip()
                    digit_str = count_str.replace(',', '')
                    if digit_str.isdigit() and int(digit_str) > 0:
                        item['link'] = item_link_list[i][0] if i < len(item_link_list) and len(item_link_list[i]) else ''
                        item['title'] = item_title_list[i][0].strip() if i < len(item_title_list) and len(item_title_list[i]) else ''
                        item['count'] = count_str

                        info['items'].append(item)

            return info

        except Exception, e:
            print 'Get profile info from steam failed. steamid: ', self.steam_id, ' Exception: ', e
            return {}

    def getOwnedGames(self, order_by_playtime_2weeks=True):
        try:
            param = {'key':self.key, 'steamid':self.steam_id, 'include_played_free_games':1, 'include_appinfo':1, 'format':'json'}
            r = requests.get('http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/', params = param)

            game_count = r.json()['response']['game_count']
            games = r.json()['response']['games']

            def w2cmp(g1, g2):
                ftime1 = g1['playtime_forever'] if 'playtime_forever' in g1 else 0
                ftime2 = g2['playtime_forever'] if 'playtime_forever' in g2 else 0

                wtime1 = g1['playtime_2weeks'] if 'playtime_2weeks' in g1 else 0
                wtime2 = g2['playtime_2weeks'] if 'playtime_2weeks' in g2 else 0

                return cmp(ftime1, ftime2) if cmp(wtime1, wtime2) == 0 else cmp(wtime1, wtime2)

            if order_by_playtime_2weeks:
                games = sorted(games, cmp=w2cmp, reverse=True)
            else:
                games = sorted(games, key=lambda g:g['playtime_forever'] if 'playtime_forever' in g else 0, reverse=True)

            for game in games:
                game['img_icon_url'] = "http://media.steampowered.com/steamcommunity/public/images/apps/%d/%s.jpg" % (game['appid'], game['img_icon_url'])
                game['img_logo_url'] = "http://media.steampowered.com/steamcommunity/public/images/apps/%d/%s.jpg" % (game['appid'], game['img_logo_url'])

                if game['has_community_visible_stats']:
                    game['stats_url'] = "http://steamcommunity.com/profiles/%s/stats/%d" % (self.steam_id, game['appid'])
                # if no stats page, return store page.
                else:
                    game['stats_url'] = "http://store.steampowered.com/app/%d" % (game['appid'],)
                
                game['store_url'] = "http://store.steampowered.com/app/%d" % (game['appid'],)

            return games

        except Exception, e:
            print 'Get owned games of ', self.steam_id, ' failed. Exception: ', e
            return {}

    def getRecentlyGames(self):
        try:
            param = {'key':self.key, 'steamid':self.steam_id, 'count':30, 'format':'json'}
            r = requests.get('http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/', params = param)

            total_count = r.json()['response']['total_count']
            games = r.json()['response']['games']

            games = sorted(games, key=lambda g:g['playtime_2weeks'] if 'playtime_2weeks' in g else 0, reverse=True)

            for game in games:
                game['img_icon_url'] = "http://media.steampowered.com/steamcommunity/public/images/apps/%d/%s.jpg" % (game['appid'], game['img_icon_url'])
                game['img_logo_url'] = "http://media.steampowered.com/steamcommunity/public/images/apps/%d/%s.jpg" % (game['appid'], game['img_logo_url'])

                game['stats_url'] = "http://steamcommunity.com/profiles/%s/stats/%d" % (self.steam_id, game['appid'])
                game['store_url'] = "http://store.steampowered.com/app/%d" % (game['appid'],)

            return games

        except Exception, e:
            print 'Get recently played games of ', self.steam_id, ' failed. Exception: ', e
            return {}
