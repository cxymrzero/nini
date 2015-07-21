# Created by cxy on 2014-12-25
# -*- coding: utf-8 -*-
from os import environ


class Config:
    SECRET_KEY = 'your secret key'
    SCHOOL_REL = {
        'hust': u'华中科技大学',
        'neau': u'东北农业大学',
        # 还有20余个分站点
    }
    SCHOOL_ADMIN = {
        'hust': ('hust', '2333'),
        'neau': ('neau', '2333'),
        # 密码是错的，不用试了
    }

    WECHAT_REL = {
        'hust': u'华科学习帝',
        'neau': u'吃在东农',
    }

class LocalConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost/nini_hust'
    SQLALCHEMY_DATABASE_URI_BASE = 'mysql://root:password@localhost/nini_'
    SERVER_NAME = 'nini.local.com'

class ProductConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost/nini_hust'
    SQLALCHEMY_DATABASE_URI_BASE = 'mysql://root:password@localhost/nini_'
    SERVER_NAME = 'nini.hustonline.net'

# 通过环境变量$USER来判断是否为线上环境
if environ.get('USER') == 'mrzero':
    config = LocalConfig()
else:
    config = ProductConfig()