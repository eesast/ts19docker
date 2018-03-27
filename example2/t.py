import os
import time

# EXECUTE_PATH = '/home/ubuntu/team19/game/teamstyle19new/src/'
# TEAM_PATH = '/home/ubuntu/team19/team/'
EXECUTE_PATH = '/code/media/platform/'
TEAM_PATH = '/code/media/team/'
#
team1 = 'test'
team2 = 'lxh'
old_path = os.getcwd()
# .chdir(EXECUTE_PATH)
# print(os.getcwd())
# os.system('nohup python3 ' + 'main.py ' + team1 + team2 + '.txt &')#运行环境
os.chdir(TEAM_PATH + team1)
print(os.getcwd())
os.system('nohup ./' + team1 + '.exe &')
os.chdir(TEAM_PATH + team2)
print(os.getcwd())
os.system('nohup ./' + team2 + '.exe &')
os.chdir(old_path)
print(os.getcwd())
initial_time = time.time()

while time.time() - initial_time < 10:
    index = os.listdir(EXECUTE_PATH)
    goal = team1 + team2 + '.txt'
    if goal in index:
        print('got it')
        os.system('rm ' + EXECUTE_PATH + goal + ' nohup.out')
        os.system('rm ' + TEAM_PATH + team1 + '/nohup.out')
        os.system('rm ' + TEAM_PATH + team2 + '/nohup.out')
        break
