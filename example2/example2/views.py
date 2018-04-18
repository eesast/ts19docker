from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, StreamingHttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt

import os
import time
import subprocess
# import re
import threading

DOCKER_PATH = '/code/media/'
EXECUTE_PATH = '/code/media/platform/'
TEAM_PATH = '/code/media/team/'
SAVE_PATH = '/code/media/battle/'


def run_battle(id1, id2, battle_id):
    # TODO: It seems that starting a new thread is not recommended in Django,
    # a better practice might be using Celery.

    PLATFORM_TIMEOUT = 3600

    # 运行环境
    platform = subprocess.Popen(['python3', 'main.py', battle_id + '.txt',
                                 os.path.join(SAVE_PATH, battle_id + '.zip')],
                                stdout=subprocess.PIPE, cwd=EXECUTE_PATH)
    while b'Waiting for connecting' not in platform.stdout.readline():
        if platform.poll() is not None:
            raise Exception('platform exited before starting player')

    player1 = subprocess.Popen(['./' + id1 + '.exe'],
                               cwd=os.path.join(TEAM_PATH, id1))

    while b'connect successfully!' not in platform.stdout.readline():
        if platform.poll() is not None:
            raise Exception('platform exited before starting second player')

    player2 = subprocess.Popen(['./' + id2 + '.exe'],
                               cwd=os.path.join(TEAM_PATH, id2))

    try:
        print('Battle', battle_id, 'started')
        platform.communicate(timeout=PLATFORM_TIMEOUT)
    except subprocess.TimeoutExpired:
        raise Exception('platform TLE, time limit = %d' % PLATFORM_TIMEOUT)
    finally:
        print('Start killing procs')
        platform.kill()
        player1.kill()
        player2.kill()
        print('SIGKILL sent')
        platform.wait()
        player1.wait()
        player2.wait()
        print('Kill done')


@csrf_exempt
# 运行main.py，指定输出文件，依次运行两个exe，监测输出文件
def battle(request):
    if request.method == 'GET':
        path = os.getcwd()
        file1 = os.listdir(path)
        return JsonResponse({'path': path, 'file': file1})
    elif request.method == 'POST':
        # team1 = request.POST['team1']
        # team2 = request.POST['team2']
        id1 = request.POST['id1']
        id2 = request.POST['id2']
        battle_id = request.POST['battleid']
        """ # Test input fields
        try:
            int(id1)
            int(id2)
        except ValueError:
            return JsonResponse({'success': False, 'message': 'id failed input test'})
        if re.fullmatch('[0-9a-f]{8}', battleid) is None:
            return JsonResponse({'success': False, 'message': 'battleid failed input test'})
        """
        for x in id1, id2:
            exe = os.path.join(TEAM_PATH, x, x + '.exe')
            if not os.path.isfile(exe) or not os.access(exe, os.X_OK):
                return JsonResponse(
                    {'success': False, 'message': "请保证对战双方均已上传AI！"})
        threading.Thread(target=run_battle, args=(id1, id2, battle_id)).start()
        return JsonResponse({'success': True})


@csrf_exempt
def Inquire(request):
    if request.method == 'POST':
        the_battle_id = request.POST['battleid']
        goal = the_battle_id + '.txt'
        if os.path.isfile(os.path.join(EXECUTE_PATH, goal)):
            print("i got it ")
            with open(os.path.join(EXECUTE_PATH, goal), 'r') as f:
                content = f.readlines()[0].split(' ')
            total_round, battle_result = content[:2]
            os.chdir(EXECUTE_PATH)
            try:
                os.system('rm ' + goal)
            except:
                print("====================\nFail to remove the txt file!!!!\n=====================")
            return JsonResponse({'success': True, 'total_round': total_round,
                                 'result': battle_result})
        else:
            index = os.listdir(EXECUTE_PATH)
            return JsonResponse({'success': False,
                                 'message': 'Still in battle!' + goal
                                            + str(index)})
    elif request.method == 'GET':
        '''team1 = request.POST['team1']
        team2 = request.POST['team2']
        old_path = os.getcwd()
        os.chdir(EXECUTE_PATH)
        os.system('nohup python3 ' + 'main.py ' + team1 + team2 + '.txt &')'''
        return JsonResponse({'success': False, 'message': 'stupid man!!!'})


@csrf_exempt
def compile(request):  # 编译报错
    if request.method == 'GET':
        path = os.getcwd()
        file1 = os.listdir(path)
        return JsonResponse({'path': path, 'file': file1})
    elif request.method == 'POST':
        teamname, filename = os.path.split(request.POST['name'])
        teamname = os.path.basename(teamname)
        # teamid = request.POST['id']
        cmd = ['g++', 'main.cpp', teamname + '.cpp', 'api_player.cpp',
               'communication.cpp', '-pthread', '-std=c++11', '-o',
               os.path.join('/code/media/team', teamname, teamname + '.exe')]
        the_cwd = '/code/media/compile'
        r = subprocess.Popen(
            cmd,
            cwd=the_cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        output = r.stdout.readlines()
        output = [s.decode('utf-8') for s in output]
        error = r.stderr.readlines()
        print(error)
        try:
            error = [s.decode('utf-8') for s in error]
        except UnicodeDecodeError:
            return JsonResponse(
                {'success': False, 'message': '含有中文字符的代码行出现错误！'})
        if any('error' in e for e in error):
            return JsonResponse({'success': False, 'message': str(error)})
        else:
            return JsonResponse({'success': True, 'message': str(output)})
