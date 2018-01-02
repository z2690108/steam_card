# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
from django.shortcuts import render
from .steam_card import SteamCard

def getSteamCard(request):
  context = {}
  if request.method == "GET":
    steam_id = request.GET['id']
    language = request.GET['lang'] if 'lang' in request.GET else 'en'
    width = request.GET['width'] if 'width' in request.GET else 280
    identity = request.GET['identity'] if 'identity' in request.GET else '*'

    m_card = SteamCard(steam_id, language)
    context['info'] = m_card.getSteamCard()

    context['info']['width'] = str(width) + 'px'
    context['info']['identity'] = identity

    print "card info: "
    print context['info']

  return render(request, 'steamCard/base.html', context)
