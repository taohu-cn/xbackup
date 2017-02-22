# -*- coding: utf-8 -*-
# __author__: taohu

"""Documentation"""


# db configuration
class DBConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql://xbackup:xbackup@172.16.81.62:23006/xbackup?charset=utf8'

# 静态文件路径，默认为`/static/`: 表示使用flask发布网站时的`http://ip:port/static/`目录
# 也可指定为固定地址的静态文件url, 例如: "http://172.16.10.10:5000/static/"
# 注意, 使用其他域名的静态文件时有可能引起跨域问题
STATIC_ROOT = "/static/"

if __name__ == "__main__":
    pass
