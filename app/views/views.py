# Powered by cxy on 2014/12/25
# -*- coding: utf-8 -*-
from app import app
from flask import request, render_template, abort
from app.models import Model
from datetime import datetime
from helpers import order_teacher_by_cmt_num, order_cmts_by_up_vote, \
    order_cmts_by_time, get_unique_cmts


@app.route('/', subdomain='<school>')
def get_random_teacher(school):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI_BASE'] + school
    wechat = app.config['WECHAT_REL'][school]
    return render_template('index.html', teachers=Model.get_random_teacher(), wechat=wechat)


@app.route('/teacher/add', methods=['GET', 'POST'], subdomain='<school>')
def add_teacher(school):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI_BASE'] + school
    timestamp = datetime.now()
    if request.method == 'GET':
        m = Model()
        depts = m.get_dept_lst()
        depts = m.get_dept_list_new()
        school_name = app.config['SCHOOL_REL'][school]
        # print school_name
        return render_template('add.html', depts=depts, timestamp=timestamp, school=school_name)
    if request.method == 'POST':
        name = request.form['name']
        name = name.strip(' ')
        if name == '':
            return 'name invalid'
        school = request.form['school']
        dept_id = request.form['dept_name']
        m = Model()
        t_id = m.teacher_exist(name, school, dept_id)
        if t_id:
            return 'teacher exists'
        else:
            m.add_teacher(name, school, dept_id)
            t_id = m.teacher_exist(name, school, dept_id)  # 获得新插入老师id
            print request.remote_addr
            return str(t_id)


@app.route('/teacher/<int:t_id>', methods=['GET', 'POST'], subdomain='<school>')
def teacher_detail(t_id, school):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI_BASE'] + school
    model = Model()
    timestamp = datetime.now()
    if request.method == 'GET':
        teacher = model.get_teacher_detail(t_id)
        ip = request.remote_addr
        if not teacher:
            return render_template('404.html', timestamp=timestamp)
        cmts = model.get_teacher_cmts(teacher.id)
        pop_cmts = order_cmts_by_up_vote(cmts) if cmts else []
        new_cmts = order_cmts_by_time(cmts) if cmts else []
        pop_cmts = get_unique_cmts(pop_cmts)
        new_cmts = get_unique_cmts(new_cmts)
        pop_cmts_methods = [model.get_vote_method(ip, cmt.id) for cmt in pop_cmts]
        new_cmts_methods = [model.get_vote_method(ip, cmt.id) for cmt in new_cmts]
        return render_template('info.html', teacher=teacher, pop_cmts=pop_cmts,
                               new_cmts=new_cmts, pop_cmts_methods=pop_cmts_methods,
                               new_cmts_methods=new_cmts_methods, timestamp=timestamp)

    if request.method == 'POST':
        # 添加关于这个教师的评论
        ip = request.remote_addr
        content = request.form['content'].strip(' ')
        if len(content) > 340:
            return 'long'  # content longer than 340
        point = request.form['point']
        point = int(point)
        current_time = datetime.now()
        res = model.add_cmt(content, current_time, point, t_id, ip)
        if not res:
            return 'not exist'  # teacher not exist
        return 'ok'


# 用名字搜索老师
@app.route('/teacher/search', methods=['GET'], subdomain='<school>')
def search_teacher(school):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI_BASE'] + school
    model = Model()
    timestamp = datetime.now()
    name = request.args.get('search-content', '')
    name = name.strip(' ')
    # 当作姓名搜索
    teachers_by_name = model.get_teachers_by_name(name)
    # 当作院系搜索
    teachers_by_dept = model.get_teacher_by_dept_name(name)
    teachers_by_dept = order_teacher_by_cmt_num(teachers_by_dept)
    teachers = teachers_by_dept + teachers_by_name
    return render_template('result.html', teachers=teachers,
                           timestamp=timestamp)


# 评论详情
@app.route('/comment/<int:cmt_id>', subdomain='<school>')
def cmt_detail(cmt_id, school):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI_BASE'] + school
    model = Model()
    timestamp = datetime.now()
    ip = request.remote_addr
    cmt = model.get_cmt_by_id(cmt_id)
    if not cmt:
        abort(404)
    method = model.get_vote_method(ip, cmt_id)
    teacher_id = model.get_teacher_by_cmt_id(cmt_id)
    return render_template('comment.html', cmt=cmt, method=method, teacher_id=teacher_id, timestamp=timestamp)


@app.route('/comment/vote', subdomain='<school>')
def vote_cmt(school):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI_BASE'] + school
    cmt_id = request.args.get("cmt_id", 0)
    method = request.args.get("method", "error")
    # 获取用户ip，每个ip只能投一票
    ip = request.remote_addr
    model = Model()
    if model.ip_exist(ip, cmt_id):
        return 'already voted'
    model.add_ip(ip, cmt_id, method)
    cmt = model.get_cmt_by_id(cmt_id)
    if not cmt:
        return 'comment not exist'
    model.change_vote(method, cmt)
    return "ok"


@app.route('/pop/', subdomain='<school>')
def pop(school):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI_BASE'] + school
    teachers = Model.get_pop_teachers(20)
    return render_template("pop.html", teachers=teachers)


@app.route('/high/', subdomain='<school>')
def high(school):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI_BASE'] + school
    teachers = Model.get_high_score_teachers(20)
    return render_template("high_score.html", teachers=teachers)


@app.route('/low/', subdomain='<school>')
def low(school):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI_BASE'] + school
    teachers = Model.get_low_score_teachers(20)
    return render_template("low.html", teachers=teachers)


@app.route('/copyright', subdomain='<school>')
def copyright(school):
    return render_template('copyright.html')


@app.route('/sad', subdomain='<school>')
def so_sad(school):
    if school == 'hust':
        # return u'so sad, 匿匿遇到了一点儿麻烦, 谢谢大家支持, 以后还会再见哦...'
        # return render_template('sad.html')
        return render_template('soonback.html')
    return "I'm ok now"


@app.errorhandler(404)
def render_404(error):
    timestamp = datetime.now()
    return render_template('404.html', timestamp=timestamp), 404