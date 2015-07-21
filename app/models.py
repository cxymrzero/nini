# Created by cxy on 2014-12-25
# -*- coding: utf-8 -*-
# from . import db
from sqlalchemy import desc
import random
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Teacher(db.Model):
    __tablename__ = 'teacher'
    __table_args__ = {'mysql_charset': 'utf8'}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    school = db.Column(db.String(16), nullable=False)
    dept_name = db.Column(db.String(32), nullable=False)
    dept_id = db.Column(db.Integer, nullable=False)
    avg = db.Column(db.Float, nullable=False, default=0)
    cmt_num = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, name, school, dept_name, dept_id):
        self.name = name
        self.school = school
        self.dept_name = dept_name
        self.dept_id = dept_id

    def __repr__(self):
        s = '<Teacher name: %s school: %s dept_id: %s>'
        return s % (self.name, self.school, self.dept_id)


class Dept(db.Model):
    __tablename__ = 'dept'
    __table_args__ = {'mysql_charset': 'utf8'}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)

    def __init__(self, name):
        self.name = name


class Cmt(db.Model):
    __tablename__ = 'cmt'
    __table_args__ = {'mysql_charset': 'utf8'}
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(400), nullable=False)
    up = db.Column(db.SmallInteger, nullable=False, default=0)
    cmt_time = db.Column(db.DateTime, nullable=False)
    point = db.Column(db.SmallInteger)  # 这条评论给教师的评分
    teacher_id = db.Column(db.Integer, nullable=False)

    def __init__(self, content, cmt_time, point, t_id):
        self.content = content
        self.cmt_time = cmt_time
        self.point = point
        self.teacher_id = t_id


# 限制一个ip同一评论只能评价一次
class Ip_cmt_rel(db.Model):
    __tablename__ = 'ip_cmt_rel'
    __table_args__ = {'mysql_charset': 'utf8'}
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(32), nullable=False)
    cmt_id = db.Column(db.Integer, nullable=False)
    method = db.Column(db.String(4), nullable=False)

    def __init__(self, ip, cmt_id, method):
        self.ip = ip
        self.cmt_id = cmt_id
        self.method = method


class Ip_teacher_rel(db.Model):
    __tablename__ = 'ip_teacher_rel'
    __table_args__ = {'mysql_charset': 'utf8'}
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(32), nullable=False)
    teacher_id = db.Column(db.Integer, nullable=False)

    def __init__(self, ip, teacher_id):
        self.ip = ip
        self.teacher_id = teacher_id

class Admin(db.Model):
    __tablename__ = 'admin'
    __table_args__ = {'mysql_charset': 'utf8'}
    id = db.Column(db.SmallInteger, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    pwd = db.Column(db.String(32), nullable=False)

    def __init__(self, name, pwd):
        self.name = name
        self.pwd = pwd


class Model():
    def __init__(self):
        self.session = db.session

    def add_teacher(self, name, school, dept_id):
        dept = Dept.query.get(dept_id)
        t = Teacher(name, school, dept.name, dept_id)
        t.cmt_num = 0
        self.session.add(t)
        return self.session.commit()

    @staticmethod
    def teacher_exist(name, school, dept_id):
        t = Teacher.query.filter_by(name=name, school=school, dept_id=dept_id).first()
        if t:
            return t.id
        return False

    @staticmethod
    def get_cmt_by_id(c_id):
        cmt = Cmt.query.get(c_id)
        return cmt

    @staticmethod
    def get_teacher_detail(t_id):
        t = Teacher.query.filter_by(id=t_id).first()
        if not t:
            return None
        return t

    @staticmethod
    def get_dept_name(dept_id):
        d = Dept.query.filter_by(id=dept_id).first()
        return d.name

    @staticmethod
    def get_cmt_detail(cmt_id):
        c = Cmt.query.filter_by(id=cmt_id).first()
        return c

    @staticmethod
    def get_pop_teachers(num):
        teachers = Teacher.query.order_by(desc(Teacher.cmt_num)).limit(num).all()
        return teachers

    @staticmethod
    def get_high_score_teachers(num):
        teachers = Teacher.query.filter(Teacher.cmt_num>3).order_by(desc(Teacher.avg)).\
            order_by(desc(Teacher.cmt_num)).limit(num).all()
        return teachers

    @staticmethod
    def get_low_score_teachers(num):
        teachers = Teacher.query.filter(Teacher.cmt_num>3).order_by(Teacher.avg).\
            order_by(desc(Teacher.cmt_num)).limit(num).all()
        return teachers

    @staticmethod
    def get_random_teacher():
        # 将评论数排名前5的老师随机选出两位加入结果列表
        top_teachers = Model.get_pop_teachers(5)
        res = []
        print len(top_teachers)
        if len(top_teachers) < 5:
            return res
        while len(res) < 2:
            teacher = random.choice(top_teachers)
            if teacher not in res:
                res.append(teacher)
        # 将评论数排名前20的老师随机选出四位加入结果列表
        # pop_teachers = Teacher.query.filter(Teacher.cmt_num>5).all()
        top_20 = Model.get_pop_teachers(30)
        if len(top_20) < 6:
            return res
        while len(res) < 6:
            teacher = random.choice(top_20)
            if teacher not in res:
                res.append(teacher)
        return res

    @staticmethod
    def get_teachers_by_name(name):
        # pattern = ''.join(['%', name, '%'])
        pattern = '%' + '%'.join([i for i in name]) + '%'
        teachers = Teacher.query.filter(Teacher.name.like(pattern)).\
            order_by(desc(Teacher.cmt_num)).all()
        return teachers

    @staticmethod
    def get_teacher_cmts(t_id):  # 通过教师id获得教师评论列表
        cmt_lst = Cmt.query.filter_by(teacher_id=t_id).order_by(Cmt.point).all()
        return cmt_lst

    @staticmethod
    def get_pop_cmts(t_id, limit):
        cmt_lst = Cmt.query.filter_by(teacher_id=t_id).order_by(desc(Cmt.up)).limit(limit).all()
        if not cmt_lst:
            return False
        return cmt_lst

    @staticmethod
    def get_new_cmts(t_id, limit):
        cmt_lst = Cmt.query.filter_by(teacher_id=t_id).order_by(desc(Cmt.cmt_time)).limit(limit).all()
        if not cmt_lst:
            return False
        return cmt_lst

    @staticmethod
    def ip_exist(ip, cmt_id):
        ip_exist = Ip_cmt_rel.query.filter_by(ip=ip, cmt_id=cmt_id).first()
        if ip_exist:
            return True
        return False

    def add_ip(self, ip, cmt_id, method):
        rel = Ip_cmt_rel(ip, cmt_id, method)
        self.session.add(rel)
        return self.session.commit()

    def add_cmt(self, content, cmt_time, point, t_id, ip):
        # 判断是否给老师打过分, 若打过分前端不作处理将分数置为-1
        if Model.has_point_teacher(ip, t_id):
            print Model.has_point_teacher(ip, t_id)
            commit_point = -1
        else:
            commit_point = point
            rel = Ip_teacher_rel(ip, t_id)
            self.session.add(rel)
            self.session.commit()
        cmt = Cmt(content, cmt_time, point=commit_point, t_id=t_id)
        cmt.up = 0
        print cmt.point
        self.session.add(cmt)
        # 将此条评论评分计入老师总分
        t = Teacher.query.get(t_id)
        if not t_id:
            return False
        elif commit_point != -1:  # 分数为-1表示未评价
            point_sum = t.avg * t.cmt_num
            t.cmt_num += 1
            point_sum += point
            t.avg = point_sum / t.cmt_num
            self.session.commit()
        else:
            self.session.commit()
        return True


    def delete_comment_by_id(self, comment_id):
        comment = Cmt.query.get(comment_id)
        if not comment:
            return False
        self.session.delete(comment)
        self.session.commit()
        return True


    def delete_teacher_by_id(self, teacher_id):
        teacher = Teacher.query.get(teacher_id)
        if not teacher:
            return False
        self.session.delete(teacher)
        self.session.commit()
        return True

    @staticmethod
    def has_point_teacher(ip, teacher_id):
        res = Ip_teacher_rel.query.filter_by(ip=ip, teacher_id=teacher_id).first()
        if res:
            return True
        return False

    @staticmethod
    def get_cmt_by_id(c_id):
        c = Cmt.query.get(c_id)
        return c

    def delete_cmt(self, c_id=0, cmt=None):
        # 通过id删除评论
        if c_id != 0:
            c = Cmt.query.get(c_id)
            if c:
                self.session.delete(c)
                self.session.commit()
            else:
                return 'comment does not exist'
        elif cmt:
            self.session.delete(cmt)
            return self.session.commit()
        return 'delete comment error'

    def change_vote(self, method, cmt):
        if method == 'up':
            cmt.up += 1
            return self.session.commit()
        elif method == 'down':
            cmt.up -= 1
            if cmt.up <= -5:
                return self.delete_cmt(cmt=cmt)
            return self.session.commit()

    @staticmethod
    def get_dept_lst():
        items = Dept.query.all()
        return items

    def get_dept_list_new(self):
        dept_list = Dept.query.filter().all()
        return dept_list

    @staticmethod
    def get_vote_method(ip, cmt_id):
        rel = Ip_cmt_rel.query.filter_by(ip=ip, cmt_id=cmt_id).first()
        if not rel:
            return None
        return rel.method

    @staticmethod
    def get_teacher_by_cmt_id(cmt_id):
        cmt = Cmt.query.filter_by(id=cmt_id).first()
        teacher_id = cmt.teacher_id
        return teacher_id

    @staticmethod
    def get_teacher_by_dept_name(dept_name):
        # pattern = '%' + dept_name + '%'
        pattern = '%' + '%'.join([i for i in dept_name]) + '%'
        depts = Dept.query.filter(Dept.name.like(pattern)).all()
        res = []

        if not depts:
            return res
        for dept in depts:
            dept_id = dept.id
            res += Teacher.query.filter_by(dept_id=dept_id).all()
        return res