# Created by cxy on 15/2/7 with PyCharm
# -*- coding: utf-8 -*-
from flask import Blueprint, request, render_template, \
    redirect, g, url_for, session, flash, current_app
from helpers import hashed_username, login_required, get_school_data, change_dbconn
from ..models import Model


admin = Blueprint('admin', __name__, subdomain='<school>')


@admin.route('/', methods=['GET'])
@login_required
def admin_route(school):
    return redirect(url_for('admin.manage', school=school))


@admin.route('/login', methods=['GET', 'POST'])
def login(school):
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        admin_name, admin_pwd = get_school_data(school)
        name = request.form['name']
        pwd = request.form['pwd']
        if name == admin_name and pwd == admin_pwd:
            session.permanent = True
            session['user'] = hashed_username(admin_name)
            session['logged'] = True
            # flash('you are %s' % admin_name)
            return redirect(url_for('admin.manage', school=school))
        error = u'用户名或密码错误'
        flash(error)
        return redirect(url_for('admin.login', school=school))


@admin.route('/welcome', methods=['GET'])
@login_required
def hello(school):
    # admin_data = config.SCHOOL_ADMIN[school]
    # if session.get('user') == md5(admin_data[0]).hexdigest() and session.get('logged'):
    #     flash('haha, you have cookie!')
    return render_template('hello.html')


@admin.route('/manage', methods=['GET'])
@login_required
def manage(school):
    return render_template('manage.html')


@admin.route('/dt', methods=['POST'])
@login_required
def delete_teacher(school):
    current_app.config['SQLALCHEMY_DATABASE_URI'] = current_app.config['SQLALCHEMY_DATABASE_URI_BASE'] + school
    url_str = request.form.get('teacher_url', '')
    url_str = url_str.strip(' ').strip('/')
    teacher_id = int(url_str.split('/')[-1])
    model = Model()
    try:
        result = model.delete_teacher_by_id(teacher_id)
        if result:
            return '删除成功'
    except:
        pass
    return '输入链接错误, 请重新确认'


@admin.route('/dc', methods=['POST'])
@login_required
def delete_comment(school):
    current_app.config['SQLALCHEMY_DATABASE_URI'] = current_app.config['SQLALCHEMY_DATABASE_URI_BASE'] + school
    url_str = request.form.get('comment_url', '')
    url_str = url_str.strip(' ').strip('/')
    comment_id = int(url_str.split('/')[-1])
    model = Model()
    try:
        result = model.delete_comment_by_id(comment_id)
        if result:
            return '删除成功'
    except:
        pass
    return '输入链接错误, 请重新确认'


@admin.route('/test', methods=['POST'])
@login_required
def test(school):
    # teacher_url = request.form['teacher_url']
    # if teacher_url:
    #     return str(request.form)
    # return 'error'
    # flash(teacher_url)
    # return render_template('hello.html')
    return str(request.form)