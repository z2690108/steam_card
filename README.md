# Steam Card

Show your steam profile. Unofficial.

[![GitHub release](https://img.shields.io/github/release/z2690108/steam_card.svg)](https://github.com/z2690108/steam_card)

## 简介
- 在个人网站或博客展示你的 [Steam](http://store.steampowered.com/ "steam") 账号；
- 基于 Steam 页面以及 [Steam Web API](https://developer.valvesoftware.com/wiki/Steam_Web_API "Steam Web API") 。

## 使用
在html中添加：
```html
<div class="steam-card" data-id="76561198096800938" data-lang="zh" data-width="270"></div>
<script src="//cdn.jsdelivr.net/gh/z2690108/steam_card@latest/jsdelivr/widget.js"></script>
```
- data-id: Steam 64位id。你可以在 [steamid.io](https://steamid.io/) 通过你的 Steam 个人页面 URL 查询到你的 **steamID64**；
- data-width: 卡片的宽度。单位是 **px** ；
- data-lang: [Language code](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)，影响卡片显示语言。仅限 Steam 支持的语言，默认为 en 。

## 例子
```html
<div class="steam-card" data-id="76561198096800938" data-lang="zh" data-width="270"></div>
<script src="//cdn.jsdelivr.net/gh/z2690108/steam_card@latest/jsdelivr/widget.js"></script>
```
[![steam_card_example](https://raw.githubusercontent.com/z2690108/steam_card/master/readme/steam_card_example.png "steam_card_example")](http://cdn.igiari.moe/steamCard?id=76561198096800938&identity=stcard-76561198096800938-1&lang=zh&width=270 "steam_card_example")

