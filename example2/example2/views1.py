from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, StreamingHttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt

import os
import time
import subprocess

DOCKER_PATH = '/code/media/'
EXECUTE_PATH = '/code/media/platform/'
TEAM_PATH = '/code/media/team/'
SAVE_PATH = '/code/media/battle/'

@csrf_exempt
#运行main.py，指定输出文件，依次运行两个exe，监测输出文件
def battle(request):
    if request.method == 'GET':
        path = os.getcwd()
        file1 = os.listdir(path)
        return JsonResponse({'path':path,'file':file1})
    elif request.method == 'POST':
        team1 = request.POST['team1']
        team2 = request.POST['team2']
        id1 = request.POST['id1']
        id2 = request.POST['id2']
        if (team1 + '.exe') not in os.listdir(TEAM_PATH + team1) or (team2 + '.exe') not in os.listdir(TEAM_PATH + team2):
            return JsonResponse({'success':False,'message':"请保证对战双方均已上传AI！"})
        old_path = os.getcwd()
        result_text = request.POST['battleid'] + '.txt'
        save_route = SAVE_PATH+ request.POST['battleid'] + '.zip'
        os.chdir(EXECUTE_PATH)
        os.system('nohup python3 ' + 'main.py ' + result_text + ' ' + save_route + ' &')#运行环境
        the_time = time.time()
        while time.time() - the_time < 3:
            pass
        os.chdir(TEAM_PATH + team1)
        os.system('nohup ./' + team1 + '.exe &')
        os.chdir(TEAM_PATH + team2)
        os.system('nohup ./' + team2 + '.exe &')
        os.chdir(old_path)
        return JsonResponse({'success':True})
        '''initial_time = time.time()
        while time.time() - initial_time < 30:
            index = os.listdir(EXECUTE_PATH)
            goal = team1 + team2 + '.txt'
            if goal in index:
                print("i got it ")
                f = open(EXECUTE_PATH + goal,'r')
                #except:
                    #return HttpResponse(index)
                content = f.readlines()[0].split(' ')
                total_round = content[0]
                if content[1] == "1":
                    result = {'winner':team1,'loser':team2}
                elif content[1] == "2":
                    result = {'winner':team2,'loser':team1}
                f.close()
                os.system('rm ' + EXECUTE_PATH + goal + ' nohup.out')
                os.system('rm ' + TEAM_PATH + team1 + '/nohup.out')
                os.system('rm ' + TEAM_PATH + team2 + '/nohup.out')
                os.system('rm /code/nohup.out')
                return JsonResponse({'success':True,'total_round':total_round,'result':result})
        if time.time() - initial_time > 30:
            return JsonResponse({'success':False,'message':'RunTimeError!'})'''

@csrf_exempt
def Inquire(request):
    if request.method == 'POST':
        the_battle_id = request.POST['battleid']
        index = os.listdir(EXECUTE_PATH)
        goal = the_battle_id + '.txt'
        if goal in index:
            print("i got it ")
            f = open(EXECUTE_PATH + goal,'r')
            content = f.readlines()[0].split(' ')
            total_round = content[0]
            battle_result = content[1]
            f.close()
            os.system('rm /code/nohup.out')
            os.system('rm ' + EXECUTE_PATH + goal + ' nohup.out')
            return JsonResponse({'success':True,'total_round':total_round,'result':battle_result})
        else:
            return JsonResponse({'success':False,'message':'Still in battle!' + goal + str(index)})
    elif request.method == 'GET':       
        '''team1 = request.POST['team1']
        team2 = request.POST['team2']
        old_path = os.getcwd()
        os.chdir(EXECUTE_PATH)
        os.system('nohup python3 ' + 'main.py ' + team1 + team2 + '.txt &')'''
        return JsonResponse({'success':False,'message':'stupid man!!!'})

        '''path = os.getcwd()
        file1 = os.listdir(path)
        initial_time = time.time()
        while time.time() - initial_time < 30:
            index = os.listdir(EXECUTE_PATH)
            goal = team1 + team2 + '.txt'
            if goal in index:
                print("i got it ")
                f = open(EXECUTE_PATH + goal,'r')
                #except:
                    #return HttpResponse(index)
                content = f.readlines()[0].split(' ')
                total_round = content[0]
                if content[1] == "1":
                    result = {'winner':team1,'loser':team2}
                elif content[1] == "2":
                    result = {'winner':team2,'loser':team1}
                f.close()
                os.system('rm ' + EXECUTE_PATH + goal + ' nohup.out')
                os.system('rm ' + TEAM_PATH + team1 + '/nohup.out')
                os.system('rm ' + TEAM_PATH + team2 + '/nohup.out')
                os.system('rm /code/nohup.out')
                return JsonResponse({'success':True,'total_round':total_round,'result':result})
        if time.time() - initial_time > 30:
            return JsonResponse({'success':False,'message':'RunTimeError!'})
        return JsonResponse({'path':path,'file':file1})'''
 
@csrf_exempt
def compile(request):#编译报错
    if request.method == 'GET':
        path = os.getcwd()
        file1 = os.listdir(path)
        return JsonResponse({'path':path,'file':file1})
    elif request.method == 'POST':
        teamname = request.POST['name'].split('/')[-2]
        filename = request.POST['name'].split('/')[-1]
        old_path = os.getcwd()
        os.chdir('/code/media/compile')
        execute = '/code/media/team/' + teamname + '/' + teamname + '.exe'
        source = '/code/media/team/%s/%s'%(teamname,filename)
        #cmd = "g++ main.cpp %s.cpp api_player.cpp communication.cpp -pthread -std=c++11 -o"%'test' + execute
        #cmd = "python -c 'import os;print(os.listdir(os.getcwd())'"
        cmd = ['g++','main.cpp','%s.cpp'%str(teamname),'api_player.cpp','communication.cpp','-pthread','-std=c++11','-o' + execute]
        #cmd = ['g++','main.cpp','test.cpp','api_player.cpp','communication.cpp','-pthread','-std=c++11','-o' + execute]        
        #os.system('cp /code/media/compile/test.exe ' + execute)
        #os.system('rm %s.cpp'%teamname)
        the_cwd = '/code/media/compile'
        r = subprocess.Popen(
            cmd,
            cwd = the_cwd,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE
            )
        #os.system('rm %s.cpp'%teamname)
        os.chdir(old_path)
        output = r.stdout.readlines()
        output = [s.decode('utf-8') for s in output]
        error = r.stderr.readlines()
        print(error)
        try:
            error = [s.decode('utf-8') for s in error]
        except:
            return JsonResponse({'success':False,'message': '含有中文字符的代码行出现错误！' })
        flag = True
        for e in error:
            if 'error' in e:
                flag = False
                break

        if flag == True:
            return JsonResponse({'success':True,'message': str(output) })
        else:
            return JsonResponse({'success':False,'message': str(error) })

        #os.system('g++ main.cpp' + filename + 'api_player.cpp communication.cpp -pthread -std=c++11 -o ' + execute + '>log.txt')
        #os.system('python3 -c "import os;print(os.listdir(os.getcwd()))"')

