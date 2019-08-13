# -*- coding: utf-8 -*-

from http.server import BaseHTTPRequestHandler
from time import sleep
import cgi
import os
import time
import socket
import datetime
import zipfile
import psutil
import shutil

exists_path = os.path.exists('store new release path')
if not exists_path:
    os.makedirs('store new release path')


class PostHandler(BaseHTTPRequestHandler):
    def _do_post(self):
        print('*')
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     }
        )
        self.send_response(200)
        self.end_headers()
        self.wfile.write(('Client: %sn' % str(self.client_address)).encode('utf-8'))
        self.wfile.write(('User-agent: %sn' & str(self.headers['User-agent'])).encode('utf-8'))
        self.wfile.write(('Path: %sn' % self.path).encode('utf-8'))
        self.wfile.write('Form data: n'.encode('utf-8'))
        get_param = form.keys()

        if "CopyFrom" in get_param:
            print(u"此脚本为复制脚本，非部署脚本")
            copy_from = str(form['copy_from'].value)
            copy_to = str(form['copy_to'].value)
            print(u"需要复制的路径：" + copy_from + "\t" + u"目标路径：" + copy_to)

            if os.path.exists(copy_to):
                print(u"文件存在，需要先执行删除操作，删除中。。。。。")
                shutil.rmtree(copy_to)
                for index in range(5):
                    if os.path.exists(copy_to):
                        print(u"等待文件删除完成，10秒")
                        sleep(10)
                    else:
                        print(u"删除完成")
                        break
            print(u"拷贝中。。。。。" + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            shutil.copytree(copy_from, copy_to)
            print(u"文件拷贝完成" + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            return 0

        #  接收完整的新应用
        file_item = form['file']
        if file_item.filename:
            fn = os.path.basename(file_item.filname)

            with open('store new release path' + fn, 'wb') as f:
                f.write(file_item.file.read())
                print('File save sucess')
                f.close()

        day_time = datetime.datetime.now().strftime('%Y%m%d')  # get time
        bak_dir = ('back up location' + day_time)  # backup dir
        bak_path = os.path.exists(bak_dir)

        # create backup dir
        if not bak_path:
            os.makedirs(bak_dir)
        sleep(10)

        # unzip new release
        print('start unzip new release')
        zip_file_loc = zipfile.ZipFile('new release location', 'r')

        try:
            for names in zip_file_loc.namelist():
                zip_file_loc.extract(names, path='new release dir')
        except Exception as e:
            print(e)
        finally:
            zip_file_loc.close()
        print('unzip ok')

        #  stop running session
        print('kill session now')
        java_proc = 'javaw.exe'
        check_proc = [psutil.Process(i).name() for i in psutil.pids()]
        kill_session = 'kill session file location'
        if java_proc in check_proc:
            os.chdir('old program dir')
            os.sysconf(kill_session)
            os.chdir('change dir to anywhere for move old program folder')
            print('session killed')
            sleep(10)
        else:
            print('session not running')

        #  backup old program
        print('backup start')
        shutil.move('old program folder', str(bak_dir + 'folder name'))
        print('backup ok')
        sleep(5)

        #  start new program
        start_session = 'start session file location'
        print('start new program now')
        shutil.move('new release dir', 'program dir')
        os.chdir('program dir')
        os.system(start_session)
        sleep(10)
        if java_proc in check_proc:
            print('program running')
            os.chdir('anywhere')
        else:
            print('program starting failed')


if __name__ == '__main__':
    from http.server import HTTPServer
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    monitor_server = HTTPServer((str(host_ip), 23333), PostHandler)
    print(monitor_server)
    print('monitor running, do not stop')
    monitor_server.serve_forever()