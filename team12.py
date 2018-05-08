import sys
import random
import signal
import time
import copy
import math
from numpy import Inf

class Team12:
    def __init__(self):
        self.optimalMoves = []
        self.originalBoard = []

    def move(self, board, old_move, key):
        self.optimalMoves = []
        self.originalBoard = board
        valid_moves = []
        val_list = []
        maxD = 1
        has_moved = False
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(15)
        alpha = -Inf
        beta = Inf
        answer = -Inf
        if(old_move == (-1, -1)):
            return (random.randrange(16), random.randrange(16))
        if(key == 'x'):
            otherkey = 'o'
        else:
            otherkey = 'x'

        try:
            while(maxD):
                temp_board = copy.deepcopy(board)
                actions = self.getNextMoves(temp_board, old_move)
                for action in actions:
                    temp_board.update(old_move, action, key)
                    curr_val = self.minimax(temp_board, False, 0, maxD, action, key, otherkey, alpha, beta)
                    valid_moves.append(action)
                    val_list.append(curr_val)
                    temp_board.board_status[action[0]][action[1]] = '-'
                    temp_board.block_status[action[0] / 4][action[1] / 4] = '-'
                    if curr_val >= answer:
                        answer = curr_val
                        self.optimalMoves.append(action)

                if answer == -Inf:
                    curr_max = val_list[0]
                    for a in range(len(actions)):
                        if cur-r_max < val_list[a]:
                            curr_max = val_list[a]
                            self.optimalMoves.append(valid_moves[a])
                maxD += 1

        except TimedOutExc:
            return self.optimalMoves[-1]

        return self.optimalMoves[-1]

    def minimax(self, temp_board, maxi, curr_depth, max_depth, old_move, key, otherkey, alpha, beta):

        heuristic_val = self.heuristic_function(temp_board, old_move, key, otherkey)
        if curr_depth == max_depth - 1:
            return heuristic_val

        actions = self.getNextMoves(temp_board, old_move)
        if maxi:
            answer = -Inf
            for action in actions:
                temp_board.update(old_move, action, key)
                val = self.minimax(temp_board, False, curr_depth + 1, max_depth, action, key, otherkey, alpha, beta)
                temp_board.board_status[action[0]][action[1]] = '-'
                temp_board.block_status[action[0] / 4][action[1] / 4] = '-'
                if val >= answer:
                    answer = val
                #if answer >= beta:
                 #   return answer
                alpha = max(alpha, answer)


                if beta <= alpha:
                    break
            return (1.3*answer + heuristic_val)

        else:
            answer = Inf
            for action in actions:
                temp_board.update(old_move, action, otherkey)
                val = self.minimax(temp_board, True, curr_depth + 1, max_depth, action, key, otherkey, alpha, beta)
                temp_board.board_status[action[0]][action[1]] = '-'
                temp_board.block_status[action[0] / 4][action[1] / 4] = '-'

                if answer >= val:
                    answer = val

                #if answer <= alpha:
                 #   return answer


                beta = min(beta, answer)
                if beta <= alpha:
                    break
            return (1.3*answer + heuristic_val)

    def getNextMoves(self, board, old_move):
        return board.find_valid_move_cells(old_move)

    # Heuristic function for 4*4*4*4 Extreme Tic-Tac-Toe.
    def heuristic_function(self,temp_board,old_move,flag,oldflag):

        x = old_move[0]/4
        y = old_move[1]/4

        hrow = hcol = hdiam = 0

        stat=temp_board.board_status

        #checking block status if it has multiple places to win the give prioprity to place where it will win the game.
        cnt_x=0
        cnt_o=0
        blk = temp_board.block_status
        hblock=0
        trans_blk = zip(*blk)
        diam1 = [blk[0][1],blk[1][0],blk[1][2],blk[2][1]]
        diam2 = [blk[0][2],blk[1][1],blk[1][3],blk[2][2]]
        diam3 = [blk[1][1],blk[2][0],blk[2][2],blk[3][1]]
        diam4 = [blk[1][2],blk[2][1],blk[2][3],blk[3][2]]

        if(diam1.count(flag) == 4 or diam2.count(flag) == 4 or diam3.count(flag) == 4 or diam4.count(flag) == 4):
            hdiam += 1000000
        if((diam1.count(flag) == 1 and diam1.count(oldflag) == 3)):
            hdiam += 150000/4
        if((diam2.count(flag) == 1 and diam2.count(oldflag) == 3)):
            hdiam += 150000/4
        if((diam3.count(flag) == 1 and diam3.count(oldflag) == 3)):
            hdiam += 150000/4
        if((diam4.count(flag) == 1 and diam4.count(oldflag) == 3)):
            hdiam += 150000/4

        if((diam1.count(flag) == 3 and diam1.count(oldflag) == 0)):
            hdiam += 100000/4
        if((diam2.count(flag) == 3 and diam2.count(oldflag) == 0)):
            hdiam += 100000/4
        if((diam3.count(flag) == 3 and diam3.count(oldflag) == 0)):
            hdiam += 100000/4
        if((diam4.count(flag) == 3 and diam4.count(oldflag) == 0)):
            hdiam += 100000/4

        if((diam1.count(flag) == 2 and diam1.count(oldflag) == 0)):
            hdiam += 15000/4
        if((diam2.count(flag) == 2 and diam2.count(oldflag) == 0)):
            hdiam += 15000/4
        if((diam3.count(flag) == 2 and diam3.count(oldflag) == 0)):
            hdiam += 15000/4
        if((diam4.count(flag) == 2 and diam4.count(oldflag) == 0)):
            hdiam += 15000/4
     
        if((diam1.count(flag) == 2 and diam1.count(oldflag) == 1)):
            hdiam += 10000/4
        if((diam2.count(flag) == 2 and diam2.count(oldflag) == 1)):
            hdiam += 10000/4
        if((diam3.count(flag) == 2 and diam3.count(oldflag) == 1)):
            hdiam += 10000/4
        if((diam4.count(flag) == 2 and diam4.count(oldflag) == 1)):
            hdiam += 10000/4

        if(diam1.count(oldflag) == 4 or diam2.count(oldflag) == 4 or diam3.count(oldflag) == 4 or diam4.count(oldflag) == 4):
            hdiam -= 1000000

        if((diam1.count(oldflag) == 1 and diam1.count(flag) == 3)):
            hdiam -= 150000/4
        if((diam2.count(oldflag) == 1 and diam2.count(flag) == 3)):
            hdiam -= 150000/4
        if((diam3.count(oldflag) == 1 and diam3.count(flag) == 3)):
            hdiam -= 150000/4
        if((diam4.count(oldflag) == 1 and diam4.count(flag) == 3)):
            hdiam -= 150000/4

        if((diam1.count(oldflag) == 3 and diam1.count(flag) == 0)):
            hdiam -= 100000/4
        if((diam2.count(oldflag) == 3 and diam2.count(flag) == 0)):
            hdiam -= 100000/4
        if((diam3.count(oldflag) == 3 and diam3.count(flag) == 0)):
            hdiam -= 100000/4
        if((diam4.count(oldflag) == 3 and diam4.count(flag) == 0)):
            hdiam -= 100000/4

        if((diam1.count(oldflag) == 2 and diam1.count(flag) == 0)):
            hdiam -= 15000/4
        if((diam2.count(oldflag) == 2 and diam2.count(flag) == 0)):
            hdiam -= 15000/4
        if((diam3.count(oldflag) == 2 and diam3.count(flag) == 0)):
            hdiam -= 15000/4
        if((diam4.count(oldflag) == 2 and diam4.count(flag) == 0)):
            hdiam -= 15000/4

        if((diam1.count(oldflag) == 2 and diam1.count(flag) == 1)):
            hdiam -= 10000/4
        if((diam2.count(oldflag) == 2 and diam2.count(flag) == 1)):
            hdiam -= 10000/4
        if((diam3.count(oldflag) == 2 and diam3.count(flag) == 1)):
            hdiam -= 10000/4
        if((diam4.count(oldflag) == 2 and diam4.count(flag) == 1)):
            hdiam -= 10000/4

        total_o =0
        total_x =0
        for i in range(4):
            cnt_x = blk[i].count(flag)
            cnt_o = blk[i].count(oldflag)
            total_x += cnt_x 
            total_o += cnt_o
            if(cnt_x == 4 and cnt_o == 0):
                hblock += 1000000
            if(cnt_o == 3 and cnt_x == 1):
                hblock += 150000
            if(cnt_x == 3 and cnt_o == 0):
                hblock += 100000
            if(cnt_o == 2 and cnt_x == 1):
                hblock += 15000
            if(cnt_x == 2 and cnt_o == 0):
                hblock += 10000
                # if(i==1 or i==2) and (blk[i][1]==flag or blk[i][2]==flag):
                #     hblock += 10000
                # elif(i==1 or i==2):
                #     hblock += 9000
                # if(i==0 or i==3) and (blk[i][0]==flag or blk[i][3]==flag):
                #     hblock += 10000
                # elif(i==0 or i==3):
                #     hblock += 9000

            if(cnt_x == 0 and cnt_o == 4):
                hblock -= 1000000
            if(cnt_x == 0 and cnt_o == 3):
                hblock -= 150000
            if(cnt_x == 0 and cnt_o == 2):
                hblock -= 10000
                # if(i==1 or i==2) and (blk[i][1]==oldflag or blk[i][2]==oldflag):
                #     hblock -= 10000
                # elif(i==1 or i==2):
                #     hblock -= 9000
                # if(i==0 or i==3) and (blk[i][0]==oldflag or blk[i][3]==oldflag):
                #     hblock -= 10000
                # elif(i==0 or i==3):
                #     hblock -= 9000


            cnt_x = trans_blk[i].count(flag)
            cnt_o = trans_blk[i].count(oldflag)
            if(cnt_x == 4 and cnt_o == 0):
                hblock += 1000000
            if(cnt_o == 3 and cnt_x == 1):
                hblock += 150000
            if(cnt_x == 3 and cnt_o == 0):
                hblock += 100000
            if(cnt_o == 2 and cnt_x == 1):
                hblock += 15000
            if(cnt_x == 2 and cnt_o == 0):
                hblock += 10000
                # if(i==1 or i==2) and (trans_blk[i][1]==flag or trans_blk[i][2]==flag):
                #     hblock += 10000
                # elif(i==1 or i==2):
                #     hblock += 9000
                # if(i==0 or i==3) and (trans_blk[i][0]==flag or trans_blk[i][3]==flag):
                #     hblock += 10000
                # elif(i==0 or i==3):
                #     hblock += 9000

            if(cnt_x == 0 and cnt_o == 4):
                hblock -= 1000000
            if(cnt_x == 0 and cnt_o == 3):
                hblock -= 150000
            if(cnt_x == 0 and cnt_o == 2):
                hblock -= 10000
                # if(i==1 or i==2) and (trans_blk[i][1]==oldflag or trans_blk[i][2]==oldflag):
                #     hblock -= 10000
                # elif(i==1 or i==2):
                #     hblock -= 9000
                # if(i==0 or i==3) and (trans_blk[i][0]==oldflag or trans_blk[i][3]==oldflag):
                #     hblock -= 10000
                # elif(i==0 or i==3):
                #     hblock -= 9000
        # if(total_o > total_x):
        #     hblock += 1000

        for i1 in range(0,13,4):
            arr = stat[i1:i1+4]
            for i2 in range(0,13,4):
                req_arr = []
                for j in range(4):
                    req_arr.append([])
                    tmp = arr[j][i2:i2+4]
                    req_arr[j] = tmp
                trans_stat = zip(*req_arr)

                diam1 = [req_arr[0][1],req_arr[1][0],req_arr[1][2],req_arr[2][1]]
                diam2 = [req_arr[0][2],req_arr[1][1],req_arr[1][3],req_arr[2][2]]
                diam3 = [req_arr[1][1],req_arr[2][0],req_arr[2][2],req_arr[3][1]]
                diam4 = [req_arr[1][2],req_arr[2][1],req_arr[2][3],req_arr[3][2]]

                if(diam1.count(flag) == 4 or diam2.count(flag) == 4 or diam3.count(flag) == 4 or diam4.count(flag) == 4):
                    hdiam += 10000
                if((diam1.count(flag) == 1 and diam1.count(oldflag) == 3)):
                    hdiam += 9000/4
                if((diam2.count(flag) == 1 and diam2.count(oldflag) == 3)):
                    hdiam += 9000/4
                if((diam3.count(flag) == 1 and diam3.count(oldflag) == 3)):
                    hdiam += 9000/4
                if((diam4.count(flag) == 1 and diam4.count(oldflag) == 3)):
                    hdiam += 9000/4

                if((diam1.count(flag) == 3 and diam1.count(oldflag) == 0)):
                    hdiam += 8800/4
                if((diam2.count(flag) == 3 and diam2.count(oldflag) == 0)):
                    hdiam += 8800/4
                if((diam3.count(flag) == 3 and diam3.count(oldflag) == 0)):
                    hdiam += 8800/4
                if((diam4.count(flag) == 3 and diam4.count(oldflag) == 0)):
                    hdiam += 8800/4

                if((diam1.count(flag) == 2 and diam1.count(oldflag) == 0)):
                    hdiam += 800/4
                if((diam2.count(flag) == 2 and diam2.count(oldflag) == 0)):
                    hdiam += 800/4
                if((diam3.count(flag) == 2 and diam3.count(oldflag) == 0)):
                    hdiam += 800/4
                if((diam4.count(flag) == 2 and diam4.count(oldflag) == 0)):
                    hdiam += 800/4
             
                if((diam1.count(flag) == 2 and diam1.count(oldflag) == 1)):
                    hdiam += 80/4
                if((diam2.count(flag) == 2 and diam2.count(oldflag) == 1)):
                    hdiam += 80/4
                if((diam3.count(flag) == 2 and diam3.count(oldflag) == 1)):
                    hdiam += 80/4
                if((diam4.count(flag) == 2 and diam4.count(oldflag) == 1)):
                    hdiam += 80/4

                if(diam1.count(oldflag) == 4 or diam2.count(oldflag) == 4 or diam3.count(oldflag) == 4 or diam4.count(oldflag) == 4):
                    hdiam -= 10000

                if((diam1.count(oldflag) == 1 and diam1.count(flag) == 3)):
                    hdiam -= 9000/4
                if((diam2.count(oldflag) == 1 and diam2.count(flag) == 3)):
                    hdiam -= 9000/4
                if((diam3.count(oldflag) == 1 and diam3.count(flag) == 3)):
                    hdiam -= 9000/4
                if((diam4.count(oldflag) == 1 and diam4.count(flag) == 3)):
                    hdiam -= 9000/4

                if((diam1.count(oldflag) == 3 and diam1.count(flag) == 0)):
                    hdiam -= 8800/4
                if((diam2.count(oldflag) == 3 and diam2.count(flag) == 0)):
                    hdiam -= 8800/4
                if((diam3.count(oldflag) == 3 and diam3.count(flag) == 0)):
                    hdiam -= 8800/4
                if((diam4.count(oldflag) == 3 and diam4.count(flag) == 0)):
                    hdiam -= 8800/4

                if((diam1.count(oldflag) == 2 and diam1.count(flag) == 0)):
                    hdiam -= 800/4
                if((diam2.count(oldflag) == 2 and diam2.count(flag) == 0)):
                    hdiam -= 800/4
                if((diam3.count(oldflag) == 2 and diam3.count(flag) == 0)):
                    hdiam -= 800/4
                if((diam4.count(oldflag) == 2 and diam4.count(flag) == 0)):
                    hdiam -= 800/4

                if((diam1.count(oldflag) == 2 and diam1.count(flag) == 1)):
                    hdiam -= 80/4
                if((diam2.count(oldflag) == 2 and diam2.count(flag) == 1)):
                    hdiam -= 80/4
                if((diam3.count(oldflag) == 2 and diam3.count(flag) == 1)):
                    hdiam -= 80/4
                if((diam4.count(oldflag) == 2 and diam4.count(flag) == 1)):
                    hdiam -= 80/4

                for i in range(4):
                    #for rows
                    cnt_x = req_arr[i].count(flag)
                    cnt_o = req_arr[i].count(oldflag)
                    if (cnt_x == 4):
                        hrow += 10000
                    if (cnt_o == 3 and cnt_x == 1):
                        hrow += 950
                    if (cnt_x == 3 and cnt_o == 0):
                        hrow += 900
                    if (cnt_x == 2 and cnt_o == 0):
                        hrow += 80
                        # if(i==1 or i==2):
                        #     hrow += 80
                        # else:
                        #     hrow += 75
                    if(cnt_x == 1 or cnt_o == 2):
                        hrow += 8

                    if (cnt_o == 4):
                        hrow -= 10000
                    if (cnt_x == 3 and cnt_o == 1):
                        hrow -= 950
                    if (cnt_o == 3 and cnt_x == 0):
                        hrow -= 900
                    if (cnt_o == 2 and cnt_x == 0):
                        hrow -= 80
                        # if(i==1 or i==2):
                        #     hrow -= 80
                        # else:
                        #     hrow -= 75
                    if(cnt_o == 1 or cnt_x == 2):
                        hrow -= 8

                    #for columns

                    cnt_x = trans_stat[i].count(flag)
                    cnt_o = trans_stat[i].count(oldflag)
                    if (cnt_x == 4):
                        hcol += 10000
                    if (cnt_o == 3 and cnt_x == 1):
                        hcol += 950
                    if (cnt_x == 3 and cnt_o == 0):
                        hcol += 900
                    if (cnt_x == 2 and cnt_o == 0):
                        hcol += 80
                        # if(i==1 or i==2):
                        #     hcol += 80
                        # else:
                        #     hcol += 75
                    if(cnt_x == 1 or cnt_o == 2):
                        hcol += 8

                    if (cnt_o == 4):
                        hcol -= 10000
                    if (cnt_x == 3 and cnt_o == 1):
                        hcol -= 950
                    if (cnt_o == 3 and cnt_x == 0):
                        hcol -= 900
                    if (cnt_o == 2 and cnt_x == 0):
                        hcol -= 80
                        # if(i==1 or i==2):
                        #     hcol -= 80
                        # else:
                        #     hcol -= 75
                    if(cnt_o == 1 or cnt_x == 2):
                        hcol -= 8


        hsum = hdiam + hrow + hcol + hblock
        return hsum



class TimedOutExc(Exception):
    pass

def handler(signum, frame):
    raise TimedOutExc()

