# Created by cxy on 15/1/15 with PyCharm
# -*- coding: utf-8 -*-
from operator import attrgetter
from functools import wraps
from flask import session, request, redirect, url_for, flash, current_app
from hashlib import md5
from config import config


def order_teacher_by_cmt_num(teacher_lst):
    res = sorted(teacher_lst, key=attrgetter('cmt_num'), reverse=True)
    return res


def order_cmts_by_time(cmts):
    res = sorted(cmts, key=attrgetter('cmt_time'), reverse=True)
    return res


def order_cmts_by_up_vote(cmts):
    res = sorted(cmts, key=attrgetter('up'), reverse=True)
    return res


def get_unique_cmts(cmts):
    if not cmts:
        return cmts
    res = []
    content_lst = []
    for cmt in cmts:
        content = cmt.content
        if content not in content_lst:
            res.append(cmt)
            content_lst.append(content)
    return res


def hashed_username(user_name):
    return md5(user_name).hexdigest()


def get_school_data(school):
    data = config.SCHOOL_ADMIN[school]
    return data[0], data[1]


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        school = kwargs['school']
        name = get_school_data(school)[0]
        if not ((hashed_username(name) == session.get('user')) and session.get('logged')):
            return redirect(url_for('admin.login', school=school))
        return func(*args, **kwargs)
    return wrapper


def change_dbconn(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        school = kwargs['school']
        current_app.config['SQLALCHEMY_DATABASE_URI'] += school
        return func(*args, **kwargs)
    return wrapper