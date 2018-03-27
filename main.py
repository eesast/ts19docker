#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time
import os
import sys
import copy
import gamemain
import unit
import communication


# 以下为两个将building，solider转化为字典函数，便于写入文件（在通信未完成之前）
def building2dict(std):
    return {"flag": std.Flag, "type": str(std.BuildingType),
            "HP": std.HP, "Maintain": std.Is_Maintain,
            "Pos": std.Position, "id": std.Unit_ID}


def unit2dict(std):
    return {"flag": std.Flag, "type": str(std.Solider_Name), "HP": std.HP,
            "Pos": std.Position}


def BuildingType2Str(std):
    return str(std)


def SoliderName2Str(std):
    return str(std)

def logist_platform(server,game,turn):
    #game处进行操作 把这几个状态给出来
    status=game.status
    status[0]['money']=int(status[0]['money'])
    status[1]['money']=int(status[1]['money'])
    building=copy.deepcopy(game.buildings)
    building[0]['mainbase'] = [game.main_base[0]]
    building[1]['mainbase'] = [game.main_base[1]]
    units=copy.deepcopy(game.units)
    winner=copy.deepcopy(game.winner)
    #units[0]=[Solider(4,100,unit.Position(7,7),1,100)]
    #units[1]=units[0]
   # building[0]=[Building(BuildingType.Hawkin,unit.Position(9,9),1,4,0,3,unit.Position(22,22))]
    '''print(status)
    print(building)
    print(units)
    print(winner)'''
    player_0,player_1=server.send_state(turn,status,building,units,winner)
    command,player_0,player_1=server.recv_command()
   # print(command[0])
    # print(len(command[0]))
    for flag in range(2):
        if len(command[flag])==0:
            continue
        if command[flag][0] == 0:
            game.raw_instruments[flag]['update_age'] = True
        for i in range(1,len(command[flag])):
            command_now = command[flag][i]
            if command_now['commandid'] == 1:
                game.raw_instruments[flag]['construct'].append([ command_now['unitid'],
                [command_now['buildp'].x,command_now['buildp'].y],
                [command_now['soliderp'].x,command_now['soliderp'].y] ])
            if command_now['commandid'] == 2:
                game.raw_instruments[flag]['upgrade'].append(command_now['unitid'])
            if command_now['commandid'] == 3:
                game.raw_instruments[flag]['sell'].append(command_now['unitid'])
            if command_now['commandid'] == 4:
                game.raw_instruments[flag]['maintain'].append(command_now['unitid'])


  #  print("player0:",player_0,"player1:",player_1)
    if player_0 == 0 and player_1 != 0:
        game.winner = 1
    if player_1 == 0 and player_0 != 0:
        game.winner = 0
    if player_0 == player_1 == 0:
        game.turn_num = 1001
    #game在这里处理命令command





############################################################################

filename = "ts19" + time.strftime("%m%d%H%M%S") + ".txt"  # 将来改成rpy
if len(sys.argv) > 1:
    filename = sys.argv[1]

#read_file = open("test.txt", 'r')
game = gamemain.GameMain()
server=communication.MainServer('127.0.0.1',9999)
map=game._map
game.map_save()
print('Waiting for connecting···')
server.start_connection(map)


#print('start')
file = []
while game.winner == 2:
    # 由于未写通信模块，故每回合指令写入txt中，随后自动逐行读取
    # print("server turns:", game.turn_num)
    # line = read_file.readline()
    # if line:
    #     game.raw_instruments = json.loads(line)
    # else:
    #    game.raw_instruments = [{
    #        'construct': [],  # (BuildingType,(BuildingPos.x,BuildingPos.y),(SoldierPos.x,SoldierPos.y))
    #        'maintain': [],  # id
    #        'upgrade': [],  # id
    #        'sell': [],  # id
    #        'update_age': False,
    #    } for _ in range(2)]
    logist_platform(server, game, game.turn_num)
    game.next_tick()
    if game.turn_num>10:
        break
status=game.status
status[0]['money']=int(status[0]['money'])
status[1]['money']=int(status[1]['money'])
building=game.buildings
units=game.units
winner=game.winner
turn=game.turn_num
player_0, player_1 = server.send_state(turn, status, building, units, winner)



with open(filename, 'w') as f:
    #f.writelines(file)
    f.write(str(game.turn_num)+" ")
    f.write(str(game.winner))

