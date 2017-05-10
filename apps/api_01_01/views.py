# -*- coding: utf-8 -*-
# __author__: taohu

# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")

from flask import render_template, request
from . import api
from apps.models import Project, Info, db_session
from sqlalchemy import and_
import json
import sys
import datetime


def convert(data):
    if sys.version.split('.')[0] == '3':
        data = str(data, encoding='utf-8')
    elif sys.version.split('.')[0] == '2':
        data = str(data)
    return data


CURRENT_DATE = datetime.date.today()
OFFERSET_DAYS = datetime.timedelta(days=3)
START_DATE = (CURRENT_DATE - OFFERSET_DAYS).strftime("%Y-%m-%d")


@api.route('/center/', methods=['GET'])
def page_center():
    res_obj = db_session.query(Project).filter(Project.type == 'Center')
    return render_template('show/center.html', obj=res_obj)


@api.route('/center/detail/', methods=['GET'])
@api.route('/center/detail/<num>/', methods=['GET'])
def center_detail(num):
    res = db_session.query(Info).filter(
        and_(Info.project_id == num), Info.agent_date > START_DATE).order_by(-Info.agent_date)
    return render_template('show/projects_detail.html', obj=res)


@api.route('/projects/')
def page_projects():
    projects = db_session.query(Project).filter(Project.type == 'PRO')
    # projects = Project.query.all()
    # for i in projects:
    #     print(i.memo)
    return render_template('show/projects.html', obj=projects)


@api.route('/projects/detail/')
@api.route('/projects/detail/<num>/')
def projects_detail(num):
    res = db_session.query(Info).filter(
        and_(Info.project_id == num), Info.agent_date > START_DATE).order_by(-Info.agent_date)
    # query_obj = db_session.query(Info).filter(and_(Info.project_id.like(num)), Info.port.like('23007')).all()
    # r = db_session.query(Info).filter(and_(Info.project_id == num), and_(Info.port == '23007'), Project.type == 'PRO')
    for item in res:
        print(item.ctime, item.project_id, item.project_obj.name)
    return render_template('show/projects_detail.html', obj=res)


@api.route('/data_post/', methods=['POST'])
def data_post():
    # python3, 版本选择取决于 agent 端的 python 版本, 而不是 server 端运行环境的 python 版本
    post_data = json.loads(convert(request.data))
    info = post_data.get('info', 0)
    # python2, 版本选择取决于 agent 端的 python 版本, 而不是 server 端运行环境的 python 版本
    # post_data = request.values.to_dict()
    # info = eval(post_data.get('info', 0))
    host = post_data.get('host', 0)
    port = post_data.get('port', 0)
    tactics = post_data.get('tactics', 0)
    date = post_data.get('date', 0)
    ctime = post_data.get('datetime', 0)
    pro_name = post_data.get('pro_name', 0)
    pro_type = post_data.get('pro_type', 0)

    # 把数据保存到 MySQL
    pro_obj = db_session.query(Project).filter(Project.name == pro_name).first()
    if not pro_obj:
        pro_obj = Project(name=pro_name, memo='xx', type=pro_type)
        db_session.add(pro_obj)
        db_session.flush()

    base_dict = {
        'host': host,
        'port': port,
        'tactics': tactics,  # 备份策略
        'agent_date': date,  # agent 执行备份的日期，区分一天多备
        'ctime': ctime,  # 备份执行时间
        'project_id': pro_obj.id
    }

    info_list = []
    for item in info:
        tmp_list = list(item.items())[0]
        tmp_dict = {'db_name': tmp_list[0], 'size': tmp_list[1]}
        tmp_dict.update(base_dict)
        info_list.append(tmp_dict)

    # 多条插入
    db_session.execute(
        Info.__table__.insert(),
        info_list
    )
    db_session.commit()

    # 插入单条
    # info_obj = Info(tactics='', db_name='', size='', ctime='', project_id=project_obj.id)
    # db_session.add(info_obj)
    # db_session.commit()
    return 'OK'
