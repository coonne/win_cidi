# -*- coding:UTF-8 -*-

import os
import sys
import logging
import commands

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    datefmt='%Y %b %d %H:%M:%S'
                    )

APP_PATH = "/app.path/"
BACK_PATCH = "/app.back.path/"
START_SHELL = "/app startup sh/"

reload(sys)
sys.setdefaultencoding('utf-8')


#  定义JENKINS环境字典  #
def _get_env():
    get_jen_env = {}
    target_ip = os.getenv('IP')
    action = os.getenv('ACTION')
    get_jen_env['app_name'] = os.getenv('APPNAME')
    get_jen_env['work_space'] = os.getenv('WORKSPACE')
    get_jen_env['target_user'] = os.getenv('USER')
    get_jen_env['pkg_svn'] = os.getenv('SVN_URL')
    get_jen_env['order_id'] = os.getenv('orderID')
    get_jen_env['target_ip_list'] = target_ip.split(',')
    get_jen_env['action_list'] = action.split(",")
    return get_jen_env


get_env = _get_env()


#  定义执行语句统一部分，用于简化后面的操作  #
def _ssh_cmd(action_cmd):
    for i in get_env['target_ip_list']:
        remote_ip = str(i)
        ssh_cmd = "ssh -o StrictHostKeyChecking=no -q  " + get_env['target_user'] + "@" + remote_ip + " " + action_cmd
        return ssh_cmd


#  定义文件复制语句，以备调用  #
def _scp_cmd():
    for i in get_env['target_ip_list']:
        remote_ip = str(i)
        scp_cmd = "scp -r " + get_env['work_space'] + "/" + get_env['app_name'] + ' ' + get_env['target_user'] + "@" + remote_ip + ":" + APP_PATH
        return scp_cmd


#  定义查询进程PID方法，以备调用  #
def _check_pid():
    check_cmd = "ps -ef |grep Bootstrap|grep -v grep|awk  \'{print $2}\'"
    run_check_pid = (_ssh_cmd(check_cmd))
    return run_check_pid


#  定义停止进程方法，以备调用  #
def _kill_pid(now_pid):
    kill_cmd = 'kill -9 ' + now_pid
    run_kill_sh = (_ssh_cmd(kill_cmd))
    return run_kill_sh


#  定义备份应用方法，以备调用  #
def _back_pkg():
    back_pkg_cmd = "mv" + ' ' + APP_PATH + get_env['app_name'] + ' ' + BACK_PATCH
    back_pkg_sh = (_ssh_cmd(back_pkg_cmd))
    return back_pkg_sh


#  定义启服务方法，以备调用  #
def _start_session():
    run_start_sh = (_ssh_cmd(START_SHELL))
    return run_start_sh


#  定义清空CACHE方法，以备调用  #
def _clear_cache():
    clear_cmd = 'rm -rf' + ' ' + APP_PATH + '*'
    run_clear_sh = (_ssh_cmd(clear_cmd))
    return run_clear_sh


#  定义回滚方法，以备调用  #
def _rollback_pkg():
    rollback_cmd = "mv" + ' ' + BACK_PATCH + get_env['app_name'] + ' ' + APP_PATH
    rollback__sh = (_ssh_cmd(rollback_cmd))
    return rollback__sh


for j in get_env['action_list']:
    if j == 'check':    # 调用查询进程功能
        stat, result_id = commands.getstatusoutput(_check_pid())
        print stat, result_id

    elif j == 'stop':   # 调用停止进程功能
        stat, result_id = commands.getstatusoutput(_check_pid())
        print stat, result_id
        kill_stat, kill_result = commands.getstatusoutput(_kill_pid(result_id))
        print kill_stat, kill_result

    elif j == 'start':  # 调用单次启动服务功能
        start_stat, start_result = commands.getstatusoutput(_start_session())
        print start_stat, start_result

    elif j == 'deploy':  # 调用完成服务部署功能
        stat, result_id = commands.getstatusoutput(_check_pid())
        print stat, result_id

        kill_stat, kill_result = commands.getstatusoutput(_kill_pid(result_id))
        print kill_stat, kill_result

        back_stat, back_result = commands.getstatusoutput(_back_pkg())
        print back_stat, back_result

        clear_stat, clear_result = commands.getstatusoutput(_clear_cache())
        print clear_stat, clear_result

        scp_new_sh = (_scp_cmd())
        print scp_new_sh
        scp_stat, scp_result = commands.getstatusoutput(scp_new_sh)
        print scp_stat, scp_result

        start_stat, start_result = commands.getstatusoutput(_start_session())
        print start_stat, start_result

    elif j == 'rollback':  # 调用应用回滚功能
        stat, result_id = commands.getstatusoutput(_check_pid())
        print stat, result_id

        kill_stat, kill_result = commands.getstatusoutput(_kill_pid(result_id))
        print kill_stat, kill_result

        clear_stat, clear_result = commands.getstatusoutput(_clear_cache())
        print clear_stat, clear_result

        rollback_stat, rollback_result = commands.getstatusoutput(_rollback_pkg())
        print rollback_stat, rollback_result

        start_stat, start_result = commands.getstatusoutput(_start_session())
        print start_stat, start_result

    elif j == 'backup':  # 调用单次备份应用功能
        back_stat, back_result = commands.getstatusoutput(_back_pkg())
        print back_stat, back_result
# todo 1.添加备份目录日期。2.把BATCH应用包整合进这个脚本。
