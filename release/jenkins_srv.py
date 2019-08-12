# -*- coding utf8 -*-

from time import sleep
import os
import requests


def get_env():
    modules_name = os.getenv('plat_windows_server')
    ip_list = modules_name.split(',')
    return ip_list


if __name__ == '__main__':
    target_server = get_env()
    source_code_path = str('')
    zip_path = str('')
    zip_dir = str('')
    os.chdir(zip_dir)
    os.system('rm' + ' ' + '-f' + ' ' + '*')
    sleep(5)
    os.chdir(source_code_path)
    do_zip = ('zip -r' + ' ' + zip_path + ' ' + '*')
    os.system(do_zip)

    for i in target_server:
        print(i)
        monitor_port = str(':23333')
        monitor_url = ('http://' + str(i) + monitor_port)
        target_files = {'file': open(zip_path, 'rb')}
        remote = requests.post(str(monitor_url), files=target_files)
        print(remote.url, remote.request, remote.headers, remote.history)
        remote.close()

