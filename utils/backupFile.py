# -*- coding: utf-8 -*-
# __author__: taohu

# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")

import os
import sys
import subprocess
import time
from utils.config import *

current_date = time.strftime("%Y-%m-%d")
current_time = time.strftime("%H-%M-%S")


class Backup(object):
    def __init__(self):
        self.url = SERVER_API
        self.host = HOST
        self.port = PORT
        self.user = USER
        self.paswd = PASWD
        self.dbs = DBS
        self.dest_dir = DEST_DIR
        self.cnf = CNF
        self.mth = MTH
        self.cmd = CMD
        self.sign = TAG
        self.back_cmd()

    def create_dir(self):
        """
        :return: self.dest_dir/current_date
        """
        this_dir = os.path.join(self.dest_dir, current_date)

        if not os.path.exists(this_dir):
            os.makedirs(this_dir)
        return this_dir

    def back_cmd(self):
        """
        生成备份命令列表
        :return: []
        """
        cmd_list = []
        if self.mth == 'xtra':
            this_cmd = "{0} --user={1} --password={2} --defaults-file={3} {4}/{5}_xtra --no-timestamp".format(
                self.cmd,
                self.user,
                self.paswd,
                self.cnf,
                self.create_dir(),
                current_time
            )
            cmd_list.append(this_cmd)

        elif self.mth == 'dumpall':
            this_cmd = "{0} -h{1} -P{2} -u{3} -p'{4}' -A -R --single-transaction --master-data=2 > {5}/{6}".format(
                self.cmd,
                self.host,
                self.port,
                self.user,
                self.paswd,
                self.create_dir(),
                current_time + '_dumpall.sql'
            )
            cmd_list.append(this_cmd)

        else:
            for db in self.dbs:
                this_cmd = "{0} -h{1} -P{2} -u{3} -p'{4}' {5} -R --single-transaction --master-data=2 > {6}/{7}".format(
                    self.cmd,
                    self.host,
                    self.port,
                    self.user,
                    self.paswd,
                    db,
                    self.create_dir(),
                    current_time + '_' + db + '.sql'
                )
                cmd_list.append(this_cmd)

        return cmd_list

    def exe_backup(self):
        """
        执行备份
        """
        for i in self.back_cmd():
            print(i)
            result = execute(i)
            result.wait()

    def post(self):
        data = {}
        if self.mth is not False:
            tmp_list = []
            result = execute("cd {0}/{1} && du -s *".format(self.dest_dir, current_date))
            result.wait()
            for i in result.stdout:
                size, name = i.split()
                tmp_list.append({name: size + 'K'})
            data.update({
                'host': self.host,
                'port': self.port,
                'info': tmp_list,
                'tactics': self.mth,
                'datetime': current_date + ' ' + current_time.replace('-', ':'),
                'project_flag': self.sign
            })
        print(data)

        if sys.version.split('.')[0] == '3':
            import urllib.request
            import urllib.parse

            url = self.url
            data = urllib.parse.urlencode(data)
            data = data.encode('utf-8')
            request = urllib.request.Request(url=url)
            request.add_header("Content-Type", "application/x-www-form-urlencoded;charset=utf-8")
            f = urllib.request.urlopen(request, data)
            callback_msg = f.read().decode('utf-8')
            # print(callback_msg)
            return callback_msg

        elif sys.version.split('.')[0] == '2':
            import urllib
            import urllib2

            url = self.url
            data_encode = urllib.urlencode(data)
            req = urllib2.Request(url=url, data=data_encode)
            res_data = urllib2.urlopen(req, timeout=30)
            callback_msg = res_data.read()
            # print('\033[1;33m %s \033[0m' % __file__, type(callback_msg), callback_msg)
            return callback_msg


def execute(cmd):
    return subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )


if __name__ == '__main__':
    print(current_date, current_time)
    backer = Backup()
    print(backer.back_cmd())
    # backer.exe_backup()
    # backer.post()
    pass
