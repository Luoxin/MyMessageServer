SERVERHOST = "127.0.0.1"  # 消息推送服务的域名
SERVERPORT = 9090  # 消息推送服务的端口

BASE_URL = "http://127.0.0.1:1200/"  # 获取的站点信息
BASE_PROXY_URL = " https://rsshub.app/"  # 一些需要翻墙的站点的,或需要借助第三方的站点


RSSLIST = {
    # "果壳网科学人":{
    #     'base_url': BASE_URL,
    #     'url_routing':  "/guokr/scientific",
    #     'analyze_rule': {
    #         "标题": "//rss/channel/item/title/text()",
    #         "简介": "//rss/channel/item/description/text()",
    #         "发布时间": "//rss/channel/item/pubDate/text()",
    #         "详情地址": "//rss/channel/item/link/text()",
    #         "id": "//rss/channel/item/guid/text()"
    #     }
    # },
    "广州市停水": {
        "base_url": BASE_URL,
        "url_routing": "tingshuitz/guangzhou",
        "analyze_rule": {
            "标题": "//rss/channel/item/title/text()",
            "简介": "//rss/channel/item/description/text()",
            "详情地址": "//rss/channel/item/link/text()",
            "id": "//rss/channel/item/guid/text()",
        },
    },
    "地震信息": {
        "base_url": BASE_URL,
        "url_routing": "/earthquake",
        "analyze_rule": {
            "标题": "//rss/channel/item/title/text()",
            "简介": "//rss/channel/item/description/text()",
            "发布时间": "//rss/channel/item/pubDate/text()",
            "详情地址": "//rss/channel/item/link/text()",
            "id": "//rss/channel/item/guid/text()",
        },
    },
    "微信公众号-果壳": {
        "base_url": BASE_URL,
        "url_routing": "/wechat/wasi/5b575dac58e5c4583338daaf",
        "analyze_rule": {
            "标题": "//rss/channel/item/title/text()",
            "简介": "//rss/channel/item/description/text()",
            "发布时间": "//rss/channel/item/pubDate/text()",
            "详情地址": "//rss/channel/item/link/text()",
            "id": "//rss/channel/item/guid/text()",
        },
    },
    "微信公众号-十五言": {
        "base_url": BASE_URL,
        "url_routing": "/wechat/wasi/5b73ebec244d4e49fb24d26c",
        "analyze_rule": {
            "标题": "//rss/channel/item/title/text()",
            "简介": "//rss/channel/item/description/text()",
            "发布时间": "//rss/channel/item/pubDate/text()",
            "详情地址": "//rss/channel/item/link/text()",
            "id": "//rss/channel/item/guid/text()",
        },
    },
    "微博热搜": {
        "base_url": BASE_URL,
        "url_routing": "/weibo/search/hot",
        "analyze_rule": {
            "标题": "//rss/channel/item/title/text()",
            "简介": "//rss/channel/item/description/text()",
            "详情地址": "//rss/channel/item/link/text()",
            "id": "//rss/channel/item/guid/text()",
        },
    },
    # "知乎热榜":{
    #     'base_url': BASE_URL,
    #     'url_routing':  "/zhihu/hotlist",
    #     'analyze_rule': {
    #         "标题": "//rss/channel/item/title/text()",
    #         "简介": "//rss/channel/item/description/text()",
    #         "发布时间": "//rss/channel/item/pubDate/text()",
    #         "详情地址": "//rss/channel/item/link/text()",
    #         "id": "//rss/channel/item/guid/text()"
    #     }
    # },
    "豆瓣-正在上映的电影": {
        "base_url": BASE_URL,
        "url_routing": "/douban/movie/playing",
        "analyze_rule": {
            "标题": "//rss/channel/item/title/text()",
            "简介": "//rss/channel/item/description/text()",
            "详情地址": "//rss/channel/item/link/text()",
            "id": "//rss/channel/item/guid/text()",
        },
    },
    # "InfoQ推荐":{
    #     'base_url': BASE_URL,
    #     'url_routing':  "/infoq/recommend",
    #     'analyze_rule': {
    #         "标题": "//rss/channel/item/title/text()",
    #         "简介": "//rss/channel/item/description/text()",
    #         "发布时间": "//rss/channel/item/pubDate/text()",
    #         "详情地址": "//rss/channel/item/link/text()",
    #         "id": "//rss/channel/item/guid/text()"
    #     }
    # },
}
