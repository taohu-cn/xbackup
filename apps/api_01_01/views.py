# -*- coding: utf-8 -*-
# __author__: taohu

# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")

from flask import render_template, request
from . import api
from apps.models import Project, Info, db_session
import json
import sys


def convert(data):
    if sys.version.split('.')[0] == '3':
        data = str(data, encoding='utf-8')
    elif sys.version.split('.')[0] == '2':
        data = str(data)
    return data


@api.route('/center/', methods=['GET'])
def page_center():
    return render_template('show/center.html')


@api.route('/projects/')
def page_projects():
    project_objs = Project.query.all()
    # for i in project_objs:
    #     print(i.memo)
    return render_template('show/projects.html', obj=project_objs)


@api.route('/projects/detail/')
@api.route('/projects/detail/<num>/')
def projects_detail(num):
    # num = request.args.get('num')
    query_obj = db_session.query(Info).filter(Info.project_id == num).all()
    # for item in query_obj:
    #     print(item.ctime, item.project_id, item.project_obj.name)
    return render_template('show/projects_detail.html', obj=query_obj)


@api.route('/data_post/', methods=['POST'])
def data_post():
    post_data = json.loads(convert(request.data))
    info = post_data.get('info', 0)
    host = post_data.get('host', 0)
    port = post_data.get('port', 0)
    tactics = post_data.get('tactics', 0)
    datetime = post_data.get('datetime', 0)
    project_flag = post_data.get('project_flag', 0)

    # 把数据保存到 MySQL
    project_obj = db_session.query(Project).filter(Project.name == project_flag).first()
    if not project_obj:
        project_obj = Project(name=project_flag, memo='xx')
        db_session.add(project_obj)
        db_session.flush()

    base_dict = {'host': host, 'port': port, 'tactics': tactics, 'ctime': datetime, 'project_id': project_obj.id}

    info_list = []
    for item in info:
        tmp_list = list(item.items())[0]
        tmp_dict = {'db_name': tmp_list[0], 'size': tmp_list[1]}
        tmp_dict.update(base_dict)
        info_list.append(tmp_dict)

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
