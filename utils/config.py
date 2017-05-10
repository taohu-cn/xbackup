# -*- coding: utf-8 -*-
# __author__: taohu

# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")

SERVER_API = '127.0.0.1:5001/api/data_post/'

# mysql server ip address
HOST = '172.16.81.62'

# mysql server port
PORT = 23006

# mysql user & password for backup
USER = 'backer'
PASWD = 'Bker.!.'

# mysql backup commond (tip: xtra for innobackupex and dumpall for mysqldump -A, dump for single db)
TACTICS = 'dumpall'
CMD = '/usr/bin/mysqldump'
# TACTICS = 'xtra'
# CMD = '/usr/bin/innobackupex'

# mysql config file, it's necessary if you backup using innobackupex
CNF = '/i02/mysql/23006/run/23006.cnf'

# dbnames which need to be backuped, end by ',' <comma > ( only supported by dump mode )
DBS = ['xguardian', 'xmonitor', 'career', ]

# position to store the data, Attention: must end with '/' !!!  ( eg: /i01/bak_mysql/172.16.10.11/)
DEST_DIR = '/tmp/'

# project name
NAME = 'test'

# project type
TYPE = 'Center'
