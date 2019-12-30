import sys
import copy
class Board:
    def __init__(self,aiSide,humanSide):
        #initialy we set the board to this state and this becomes the current state
        white={"rook":[[0,0],[7,0]],"knight":[[1,0],[6,0]],"bishop":[[2,0],[5,0]],"queen":[[3,0]],"pawn":[[i,1] for i in range(8)],"king":[[4,0]]}
        black={"rook":[[0,7],[7,7]],"knight":[[1,7],[6,7]],"bishop":[[2,7],[5,7]],"queen":[[3,7]],"pawn":[[i,6] for i in range(8)],"king":[[4,7]]}
        self.human=humanSide
        self.ai=aiSide
        self.chance="white"
        self.currentState=State(True,{"white":white,"black":black},self.chance)
    def changeCurrentState(self,piece,initial_cord,final_cord):
        if self.chance=="white":
            self.chance="black"
        else:
            self.chance="white"
        castle,pieces=self.currentState.getNextState(piece,initial_cord,final_cord)
        self.currentState=State(castle,pieces,self.chance)
    def checkMate(self):
        if len(self.currentState.pieces[self.currentState.side]["king"])==0:
            return True
        else:
            return False

class State:
    def __init__(self,castle,pieces,chance):
        self.pieces=pieces
        self.mat = [["" for i in range(8)] for j in range(8)]
        for side in self.pieces:
            for piece in self.pieces[side]:
                for cord in self.pieces[side][piece]:
                    self.mat[cord[0]][cord[1]]=side+" "+piece
        self.castle=castle
        self.side=chance
        self.pieceSquareTable={}
        self.pieceSquareTable["pawn"]=[[0,5,5,0,5,10,50,0],[0,10,-5,0,5,10,50,0],[0,10,-10,0,10,20,50,0],[0,-20,0,20,25,30,50,0],[0,-20,0,20,25,30,50,0],[0,10,-10,0,10,20,50,0],[0,10,-5,0,5,10,50,0],[0,5,5,0,5,10,50,0]]
        self.pieceSquareTable["knight"]=[[-50,-40,-30,-30,-30,-30,-40,-50],[-40,-20,5,0,5,0,-20,-40],[-30,0,10,15,15,10,0,-30],[-30,5,15,20,20,15,0,-30],[-30,5,15,20,20,15,0,-30],[-30,0,10,15,15,10,0,-30],[-40,-20,5,0,5,0,-20,-40],[-50,-40,-30,-30,-30,-30,-40,-50]]
        self.pieceSquareTable["bishop"]=[[-20,-10,-10,-10,-10,-10,-10,-20],[-10,5,10,0,5,0,0,-10],[-10,0,10,10,5,5,0,-10],[-10,0,10,10,10,10,0,-10],[-10,0,10,10,10,10,0,-10],[-10,0,10,10,5,5,0,-10],[-10,5,10,0,5,0,0,-10],[-20,-10,-10,-10,-10,-10,-10,-20]]
        self.pieceSquareTable["rook"]=[[0,-5,-5,-5,-5,-5,5,0],[0,0,0,0,0,0,10,0],[0,0,0,0,0,0,10,0],[5,0,0,0,0,0,10,0],[5,0,0,0,0,0,10,0],[0,0,0,0,0,0,10,0],[0,0,0,0,0,0,10,0],[0,-5,-5,-5,-5,-5,5,0]]
        self.pieceSquareTable["queen"]=[[-20,-10,-10,0,-5,-10,-10,-20],[-10,0,5,0,0,0,0,-10],[-10,5,5,5,5,5,0,-10],[-5,0,5,5,5,5,0,-5],[-5,0,5,5,5,5,0,-5],[-10,0,5,5,5,5,0,-10],[-10,0,0,0,0,0,0,-10],[-20,-10,-10,-5,-5,-10,-10,-20]]
        self.pieceSquareTable["king"]=[]
        self.pieceSquareTable["king"].append([[20,20,-10,-20,-30,-30,-30,-30],[30,20,-20,-30,-40,-40,-40,-40],[15,0,-20,-30,-40,-40,-40,-40],[0,0,-20,-40,-50,-50,-50,-50],[0,0,-20,-40,-50,-50,-50,-50],[10,0,-20,-30,-40,-40,-40,-40],[30,20,-20,-30,-40,-40,-40,-40],[20,20,-10,-20,-30,-30,-30,-30]])
        self.pieceSquareTable["king"].append([[-50,-30,-30,-30,-30,-30,-30,-50],[-30,-30,-10,-10,-10,-10,-20,-40],[-30,0,20,30,30,20,-10,-30],[-30,0,30,40,40,30,0,-20],[-30,0,30,40,40,30,0,-20],[-30,0,20,30,30,20,-10,-30],[-30,-30,-10,-10,-10,-10,-20,-40],[-50,-30,-30,-30,-30,-30,-30,-50]])
    def getStateScore(self):
        scoreWhite=0
        scoreBlack=0
        #piece difference
        sums={}
        for side in self.pieces:
            sum=0
            for piece in self.pieces[side]:
                if piece=="rook":
                    sum=sum+len(self.pieces[side][piece])*5000
                elif piece=="knight":
                    sum=sum+len(self.pieces[side][piece])*3200
                elif piece=="bishop":
                    sum=sum+len(self.pieces[side][piece])*3300
                elif piece=="queen":
                    sum=sum+len(self.pieces[side][piece])*9000
                elif piece=="pawn":
                    sum=sum+len(self.pieces[side][piece])*1000
                elif piece=="king":
                    sum=sum+len(self.pieces[side][piece])*200000
            sums[side]=sum
        scoreWhite=scoreWhite+sums["white"]-sums["black"]
        scoreBlack=scoreBlack+sums["black"]-sums["white"]
        if len(self.pieces["black"]["king"])==0 or len(self.pieces["white"]["king"])==0:
            return scoreWhite,scoreBlack
        pieceSquareTableScoreWhite=0
        pieceSquareTableScoreBlack=0
        for side in self.pieces:
            for piece in self.pieces[side]:
                for cord in self.pieces[side][piece]:
                    if side=="white":
                        if piece!="king":
                            pieceSquareTableScoreWhite=pieceSquareTableScoreWhite+self.pieceSquareTable[piece][cord[0]][cord[1]]
                        elif len(self.pieces["black"]["queen"])==0 or len(self.pieces["black"]["rook"])+len(self.pieces["black"]["bishop"])+len(self.pieces["black"]["knight"])<1:
                                pieceSquareTableScoreWhite=pieceSquareTableScoreWhite+self.pieceSquareTable[piece][1][cord[0]][cord[1]]
                    else:
                        if piece!="king":
                            pieceSquareTableScoreBlack=pieceSquareTableScoreBlack+self.pieceSquareTable[piece][cord[0]][7-cord[1]]
                        elif len(self.pieces["white"]["queen"])==0 or len(self.pieces["black"]["rook"])+len(self.pieces["black"]["bishop"])+len(self.pieces["black"]["knight"])<1:
                                pieceSquareTableScoreBlack=pieceSquareTableScoreBlack+self.pieceSquareTable[piece][1][cord[0]][7-cord[1]]
        scoreWhite=scoreWhite+pieceSquareTableScoreWhite
        scoreBlack=scoreBlack+pieceSquareTableScoreBlack
        #pawn structure
        hash=[0 for i in range(8)]
        for cord in self.pieces["white"]["pawn"]:
            if hash[cord[0]]<1:
                hash[cord[0]]=hash[cord[0]]+1
            else:
                scoreWhite=scoreWhite-5
        for i,_ in enumerate(hash):
            if i-1>=0 and hash[i-1]==0 and i+1<8 and hash[i+1]==0:
                scoreWhite=scoreWhite-5
        hash=[0 for i in range(8)]        
        for cord in self.pieces["black"]["pawn"]:
            if hash[cord[0]]<1:
                hash[cord[0]]=hash[cord[0]]+1
            else:
                scoreBlack=scoreBlack-5
        for i,_ in enumerate(hash):
            if i-1>=0 and hash[i-1]==0 and i+1<8 and hash[i+1]==0:
                scoreBlack=scoreBlack-5
        #open file rook
        open=True
        for cord in self.pieces["white"]["rook"]:
            for i in range(8):
                if self.mat[cord[0]][i] not in ["","white rook"]:
                    open=False
            if open:
                scoreWhite=scoreWhite+5
        open=True
        for cord in self.pieces["black"]["rook"]:
            for i in range(8):
                if self.mat[cord[0]][i] not in ["","black rook"]:
                    open=False
            if open:
                scoreBlack=scoreBlack+5
        #pins on king
        x=self.pieces["black"]["king"][0][0]
        y=self.pieces["black"]["king"][0][1]
        countBlack=0
        countWhite=0
        pin=False
        for i in range(x+1,8):
            if self.mat[i][y].split(" ")[0] == "black":
                countBlack=countBlack+1
                pin=True
            if pin and self.mat[i][y] in ["white rook","white queen"]:
                countWhite=countWhite+1
        if countBlack==1 and countWhite>0:
            scoreWhite=scoreWhite+countWhite*5
        countBlack=0
        countWhite=0
        pin=False
        for i in reversed(range(0,x)):
            if self.mat[i][y].split(" ")[0] == "black":
                countBlack=countBlack+1
                pin=True
            if pin and self.mat[i][y] in ["white rook","white queen"]:
                countWhite=countWhite+1
        if countBlack==1 and countWhite>0:
            scoreWhite=scoreWhite+countWhite*5
        countBlack=0
        countWhite=0
        pin=False
        for j in reversed(range(0,y)):
            if self.mat[x][j].split(" ")[0] == "black":
                countBlack=countBlack+1
                pin=True
            if pin and self.mat[x][j] in ["white rook","white queen"]:
                countWhite=countWhite+1
        if countBlack==1 and countWhite>0:
            scoreWhite=scoreWhite+countWhite*5
        countBlack=0
        countWhite=0
        pin=False
        for j in range(y+1,8):
            if self.mat[x][j].split(" ")[0] == "black":
                countBlack=countBlack+1
                pin=True
            if pin and self.mat[x][j] in ["white rook","white queen"]:
                countWhite=countWhite+1
        if countBlack==1 and countWhite>0:
            scoreWhite=scoreWhite+countWhite*5
        countBlack=0
        countWhite=0
        pin=False
        for i,j in zip(range(x+1,8),range(y+1,8)):
            if self.mat[i][j].split(" ")[0] == "black":
                countBlack=countBlack+1
                pin=True
            if pin and self.mat[i][j] in ["white bishop","white queen"]:
                countWhite=countWhite+1
        if countBlack==1 and countWhite>0:
            scoreWhite=scoreWhite+countWhite*5
        countBlack=0
        countWhite=0
        pin=False
        for i,j in zip(range(x+1,8),reversed(range(0,y))):
            if self.mat[i][j].split(" ")[0] == "black":
                countBlack=countBlack+1
                pin=True
            if pin and self.mat[i][j] in ["white bishop","white queen"]:
                countWhite=countWhite+1
        if countBlack==1 and countWhite>0:
            scoreWhite=scoreWhite+countWhite*5
        countBlack=0
        countWhite=0
        pin=False
        for i,j in zip(reversed(range(0,x)),range(y+1,8)):
            if self.mat[i][j].split(" ")[0] == "black":
                countBlack=countBlack+1
                pin=True
            if pin and self.mat[i][j] in ["white bishop","white queen"]:
                countWhite=countWhite+1
        if countBlack==1 and countWhite>0:
            scoreWhite=scoreWhite+countWhite*5
        countBlack=0
        countWhite=0
        pin=False
        for i,j in zip(reversed(range(0,x)),reversed(range(0,y))):
            if self.mat[i][j].split(" ")[0] == "black":
                countBlack=countBlack+1
                pin=True
            if pin and self.mat[i][j] in ["white bishop","white queen"]:
                countWhite=countWhite+1
        if countBlack==1 and countWhite>0:
            scoreWhite=scoreWhite+countWhite*5


        x=self.pieces["white"]["king"][0][0]
        y=self.pieces["white"]["king"][0][1]
        countBlack=0
        countWhite=0
        pin=False
        for i in range(x+1,8):
            if self.mat[i][y].split(" ")[0] == "white":
                countWhite=countWhite+1
                pin=True
            if pin and self.mat[i][y] in ["black rook","black queen"]:
                countBlack=countBlack+1
        if countWhite==1 and countBlack>0:
            scoreBlack=scoreBlack+countBlack*5
        countBlack=0
        countWhite=0
        pin=False
        for i in reversed(range(0,x)):
            if self.mat[i][y].split(" ")[0] == "white":
                countWhite=countWhite+1
                pin=True
            if pin and self.mat[i][y] in ["black rook","black queen"]:
                countBlack=countBlack+1
        if countWhite==1 and countBlack>0:
            scoreBlack=scoreBlack+countBlack*5
        countBlack=0
        countWhite=0
        pin=False
        for j in reversed(range(0,y)):
            if self.mat[x][j].split(" ")[0] == "white":
                countWhite=countWhite+1
                pin=True
            if pin and self.mat[i][y] in ["black rook","black queen"]:
                countBlack=countBlack+1
        if countWhite==1 and countBlack>0:
            scoreBlack=scoreBlack+countBlack*5
        countBlack=0
        countWhite=0
        pin=False
        for j in range(y+1,8):
            if self.mat[x][j].split(" ")[0] == "white":
                countWhite=countWhite+1
                pin=True
            if pin and self.mat[i][y] in ["black rook","black queen"]:
                countBlack=countBlack+1
        if countWhite==1 and countBlack>0:
            scoreBlack=scoreBlack+countBlack*5
        countBlack=0
        countWhite=0
        pin=False
        for i,j in zip(range(x+1,8),range(y+1,8)):
            if self.mat[i][j].split(" ")[0] == "white":
                countWhite=countWhite+1
                pin=True
            if pin and self.mat[i][j] in ["black bishop","black queen"]:
                countBlack=countBlack+1
        if countWhite==1 and countBlack>0:
            scoreBlack=scoreBlack+countBlack*5
        countBlack=0
        countWhite=0
        pin=False
        for i,j in zip(range(x+1,8),reversed(range(0,y))):
            if self.mat[i][j].split(" ")[0] == "white":
                countWhite=countWhite+1
                pin=True
            if pin and self.mat[i][j] in ["black bishop","black queen"]:
                countBlack=countBlack+1
        if countWhite==1 and countBlack>0:
            scoreBlack=scoreBlack+countBlack*5
        countBlack=0
        countWhite=0
        pin=False
        for i,j in zip(reversed(range(0,x)),range(y+1,8)):
            if self.mat[i][j].split(" ")[0] == "white":
                countWhite=countWhite+1
                pin=True
            if pin and self.mat[i][j] in ["black bishop","black queen"]:
                countBlack=countBlack+1
        if countWhite==1 and countBlack>0:
            scoreBlack=scoreBlack+countBlack*5
        countBlack=0
        countWhite=0
        pin=False
        for i,j in zip(reversed(range(0,x)),reversed(range(0,y))):
            if self.mat[i][j].split(" ")[0] == "white":
                countWhite=countWhite+1
                pin=True
            if pin and self.mat[i][j] in ["black bishop","black queen"]:
                countBlack=countBlack+1
        if countWhite==1 and countBlack>0:
            scoreBlack=scoreBlack+countBlack*5
        return scoreWhite,scoreBlack

    def getLeagleMoves(self):
        total_possible_move = {}
        for piece in self.pieces[self.side]:
            total_possible_move[piece]={}
            for cordIndex,cord in enumerate(self.pieces[self.side][piece]):
                possible_move_perpiece=[]
                if piece == "rook":
                    for i in range(cord[0]+1,8):
                        if self.mat[i][cord[1]] == "":
                            possible_move_perpiece.append([i,cord[1]])
                        else:
                            if self.mat[i][cord[1]].split(" ")[0]==self.side:
                                break
                            else:
                                possible_move_perpiece.append([i,cord[1]])
                                break
                    for i in reversed(range(0,cord[0])):
                        if self.mat[i][cord[1]] == "":
                            possible_move_perpiece.append([i,cord[1]])
                        else:
                            if self.mat[i][cord[1]].split(" ")[0]==self.side:
                                break
                            else:
                                possible_move_perpiece.append([i,cord[1]])
                                break
                    for j in range(cord[1]+1,8):
                        if self.mat[cord[0]][j] == "":
                            possible_move_perpiece.append([cord[0],j])
                        else:
                            if self.mat[cord[0]][j].split(" ")[0]==self.side:
                                break
                            else:
                                possible_move_perpiece.append([cord[0],j])
                                break
                    for j in reversed(range(0,cord[1])):
                        if self.mat[cord[0]][j] == "":
                            possible_move_perpiece.append([cord[0],j])
                        else:
                            if self.mat[cord[0]][j].split(" ")[0]==self.side:
                                break
                            else:
                                possible_move_perpiece.append([cord[0],j])
                                break
                elif piece == "knight":
                    if cord[0]+2<8 and cord[1]+1<8:    
                        if self.mat[cord[0]+2][cord[1]+1]=="":
                            possible_move_perpiece.append([cord[0]+2,cord[1]+1])
                        else: 
                            if self.mat[cord[0]+2][cord[1]+1].split(" ")[0]!=self.side:
                                possible_move_perpiece.append([cord[0]+2,cord[1]+1])
                    if cord[0]+2<8 and cord[1]-1>=0:    
                        if self.mat[cord[0]+2][cord[1]-1]=="":
                            possible_move_perpiece.append([cord[0]+2,cord[1]-1])
                        else: 
                            if self.mat[cord[0]+2][cord[1]-1].split(" ")[0]!=self.side:
                                possible_move_perpiece.append([cord[0]+2,cord[1]-1])
                    if cord[0]-2>=0 and cord[1]+1<8:    
                        if self.mat[cord[0]-2][cord[1]+1]=="":
                            possible_move_perpiece.append([cord[0]-2,cord[1]+1])
                        else: 
                            if self.mat[cord[0]-2][cord[1]+1].split(" ")[0]!=self.side:
                                possible_move_perpiece.append([cord[0]-2,cord[1]+1])                    
                    if cord[0]-2>=0 and cord[1]-1>=0:    
                        if self.mat[cord[0]-2][cord[1]-1]=="":
                            possible_move_perpiece.append([cord[0]-2,cord[1]-1])
                        else: 
                            if self.mat[cord[0]-2][cord[1]-1].split(" ")[0]!=self.side:
                                possible_move_perpiece.append([cord[0]-2,cord[1]-1])
                    if cord[0]+1<8 and cord[1]+2<8:    
                        if self.mat[cord[0]+1][cord[1]+2]=="":
                            possible_move_perpiece.append([cord[0]+1,cord[1]+2])
                        else: 
                            if self.mat[cord[0]+1][cord[1]+2].split(" ")[0]!=self.side:
                                possible_move_perpiece.append([cord[0]+1,cord[1]+2])
                    if cord[0]+1<8 and cord[1]-2>=0:    
                        if self.mat[cord[0]+1][cord[1]-2]=="":
                            possible_move_perpiece.append([cord[0]+1,cord[1]-2])
                        else: 
                            if self.mat[cord[0]+1][cord[1]-2].split(" ")[0]!=self.side:
                                possible_move_perpiece.append([cord[0]+1,cord[1]-2])
                    if cord[0]-1>=0 and cord[1]+2<8:    
                        if self.mat[cord[0]-1][cord[1]+2]=="":
                            possible_move_perpiece.append([cord[0]-1,cord[1]+2])
                        else: 
                            if self.mat[cord[0]-1][cord[1]+2].split(" ")[0]!=self.side:
                                possible_move_perpiece.append([cord[0]-1,cord[1]+2])                    
                    if cord[0]-1>=0 and cord[1]-2>=0:    
                        if self.mat[cord[0]-1][cord[1]-2]=="":
                            possible_move_perpiece.append([cord[0]-1,cord[1]-2])
                        else: 
                            if self.mat[cord[0]-1][cord[1]-2].split(" ")[0]!=self.side:
                                possible_move_perpiece.append([cord[0]-1,cord[1]-2])
                elif piece == "bishop":
                    i=cord[0]+1
                    j=cord[1]+1
                    while i<8 and j<8:
                        if self.mat[i][j] == "":
                            possible_move_perpiece.append([i,j])
                        else:
                            if self.mat[i][j].split(" ")[0]==self.side:
                                break
                            else:
                                possible_move_perpiece.append([i,j])
                                break
                        i=i+1
                        j=j+1
                    i=cord[0]+1
                    j=cord[1]-1
                    while i<8 and j>=0:
                        if self.mat[i][j] == "":
                            possible_move_perpiece.append([i,j])
                        else:
                            if self.mat[i][j].split(" ")[0]==self.side:
                                break
                            else:
                                possible_move_perpiece.append([i,j])
                                break
                        i=i+1
                        j=j-1
                    i=cord[0]-1
                    j=cord[1]+1
                    while i>=0 and j<8:
                        if self.mat[i][j] == "":
                            possible_move_perpiece.append([i,j])
                        else:
                            if self.mat[i][j].split(" ")[0]==self.side:
                                break
                            else:
                                possible_move_perpiece.append([i,j])
                                break
                        i=i-1
                        j=j+1
                    i=cord[0]-1
                    j=cord[1]-1
                    while i>=0 and j>=0:
                        if self.mat[i][j] == "":
                            possible_move_perpiece.append([i,j])
                        else:
                            if self.mat[i][j].split(" ")[0]==self.side:
                                break
                            else:
                                possible_move_perpiece.append([i,j])
                                break
                        i=i-1
                        j=j-1
                elif piece == "queen":
                    for i in range(cord[0]+1,8):
                        if self.mat[i][cord[1]] == "":
                            possible_move_perpiece.append([i,cord[1]])
                        else:
                            if self.mat[i][cord[1]].split(" ")[0]==self.side:
                                break
                            else:
                                possible_move_perpiece.append([i,cord[1]])
                                break
                    for i in reversed(range(0,cord[0])):
                        if self.mat[i][cord[1]] == "":
                            possible_move_perpiece.append([i,cord[1]])
                        else:
                            if self.mat[i][cord[1]].split(" ")[0]==self.side:
                                break
                            else:
                                possible_move_perpiece.append([i,cord[1]])
                                break
                    for j in range(cord[1]+1,8):
                        if self.mat[cord[0]][j] == "":
                            possible_move_perpiece.append([cord[0],j])
                        else:
                            if self.mat[cord[0]][j].split(" ")[0]==self.side:
                                break
                            else:
                                possible_move_perpiece.append([cord[0],j])
                                break
                    for j in reversed(range(0,cord[1])):
                        if self.mat[cord[0]][j] == "":
                            possible_move_perpiece.append([cord[0],j])
                        else:
                            if self.mat[cord[0]][j].split(" ")[0]==self.side:
                                break
                            else:
                                possible_move_perpiece.append([cord[0],j])
                                break
                    i=cord[0]+1
                    j=cord[1]+1
                    while i<8 and j<8:
                        if self.mat[i][j] == "":
                            possible_move_perpiece.append([i,j])
                        else:
                            if self.mat[i][j].split(" ")[0]==self.side:
                                break
                            else:
                                possible_move_perpiece.append([i,j])
                                break
                        i=i+1
                        j=j+1
                    i=cord[0]+1
                    j=cord[1]-1
                    while i<8 and j>=0:
                        if self.mat[i][j] == "":
                            possible_move_perpiece.append([i,j])
                        else:
                            if self.mat[i][j].split(" ")[0]==self.side:
                                break
                            else:
                                possible_move_perpiece.append([i,j])
                                break
                        i=i+1
                        j=j-1
                    i=cord[0]-1
                    j=cord[1]+1
                    while i>=0 and j<8:
                        if self.mat[i][j] == "":
                            possible_move_perpiece.append([i,j])
                        else:
                            if self.mat[i][j].split(" ")[0]==self.side:
                                break
                            else:
                                possible_move_perpiece.append([i,j])
                                break
                        i=i-1
                        j=j+1
                    i=cord[0]-1
                    j=cord[1]-1
                    while i>=0 and j>=0:
                        if self.mat[i][j] == "":
                            possible_move_perpiece.append([i,j])
                        else:
                            if self.mat[i][j].split(" ")[0]==self.side:
                                break
                            else:
                                possible_move_perpiece.append([i,j])
                                break
                        i=i-1
                        j=j-1
                elif piece == "king":
                    if cord[0]+1<8 and cord[1]+1<8:    
                        if self.mat[cord[0]+1][cord[1]+1]=="":
                            possible_move_perpiece.append([cord[0]+1,cord[1]+1])
                        else: 
                            if self.mat[cord[0]+1][cord[1]+1].split(" ")[0]!=self.side:
                                possible_move_perpiece.append([cord[0]+1,cord[1]+1])
                    if cord[0]+1<8:    
                        if self.mat[cord[0]+1][cord[1]]=="":
                            possible_move_perpiece.append([cord[0]+1,cord[1]])
                        else: 
                            if self.mat[cord[0]+1][cord[1]].split(" ")[0]!=self.side:
                                possible_move_perpiece.append([cord[0]+1,cord[1]])
                    if cord[0]+1<8 and cord[1]-1>=0:    
                        if self.mat[cord[0]+1][cord[1]-1]=="":
                            possible_move_perpiece.append([cord[0]+1,cord[1]-1])
                        else: 
                            if self.mat[cord[0]+1][cord[1]-1].split(" ")[0]!=self.side:
                                possible_move_perpiece.append([cord[0]+1,cord[1]-1])                    
                    if cord[1]-1>=0:    
                        if self.mat[cord[0]][cord[1]-1]=="":
                            possible_move_perpiece.append([cord[0],cord[1]-1])
                        else: 
                            if self.mat[cord[0]][cord[1]-1].split(" ")[0]!=self.side:
                                possible_move_perpiece.append([cord[0],cord[1]-1])
                    if cord[0]-1>=0 and cord[1]-1>=0:    
                        if self.mat[cord[0]-1][cord[1]-1]=="":
                            possible_move_perpiece.append([cord[0]-1,cord[1]-1])
                        else: 
                            if self.mat[cord[0]-1][cord[1]-1].split(" ")[0]!=self.side:
                                possible_move_perpiece.append([cord[0]-1,cord[1]-1])
                    if cord[0]-1>=0:    
                        if self.mat[cord[0]-1][cord[1]]=="":
                            possible_move_perpiece.append([cord[0]-1,cord[1]])
                        else: 
                            if self.mat[cord[0]-1][cord[1]].split(" ")[0]!=self.side:
                                possible_move_perpiece.append([cord[0]-1,cord[1]])
                    if cord[0]-1>=0 and cord[1]+1<8:    
                        if self.mat[cord[0]-1][cord[1]+1]=="":
                            possible_move_perpiece.append([cord[0]-1,cord[1]+1])
                        else: 
                            if self.mat[cord[0]-1][cord[1]+1].split(" ")[0]!=self.side:
                                possible_move_perpiece.append([cord[0]-1,cord[1]+1])                    
                    if cord[1]+1<8:    
                        if self.mat[cord[0]][cord[1]+1]=="":
                            possible_move_perpiece.append([cord[0],cord[1]+1])
                        else: 
                            if self.mat[cord[0]][cord[1]+1].split(" ")[0]!=self.side:
                                possible_move_perpiece.append([cord[0],cord[1]+1])
                    count=0
                    if self.side == "white":
                            for cord in self.pieces["white"]["rook"]:
                                if cord not in [[0,0],[0,7]]:
                                    count=count+1
                    if count==2:
                        self.castle=False
                    count=0
                    if self.side == "black":
                            for cord in self.pieces["black"]["rook"]:
                                if cord not in [[7,0],[7,7]]:
                                    count=count+1
                    if self.castle:
                        if self.side == "white":
                            i=cord[0]
                            j=cord[1]
                            castle=True
                            while i>=cord[0]-2:
                                if self.mat[i][j]!="" and self.mat[i][j]!="white king":
                                    castle=False
                                    break
                                a=i
                                b=j
                                while a<8 and b<8:
                                    if self.mat[a][b]!="" and self.mat[a][b].split(" ")[0]!=self.side and self.mat[a][b].split(" ")[1] in ["queen","bishop"]:
                                        castle=False
                                        break
                                    elif self.mat[a][b]!="" and self.mat[a][b].split(" ")[0]==self.side:
                                        break
                                    a=a+1
                                    b=b+1
                                if not castle:
                                    break
                                a=i
                                b=j
                                while a>=0 and b<8:
                                    if self.mat[a][b]!="" and self.mat[a][b].split(" ")[0]!=self.side and self.mat[a][b].split(" ")[1] in ["queen","bishop"]:
                                        castle=False
                                        break
                                    elif self.mat[a][b]!="" and self.mat[a][b].split(" ")[0]==self.side:
                                        break
                                    a=a-1
                                    b=b+1
                                if not castle:
                                    break
                                a=i
                                b=j
                                while b<8:
                                    if self.mat[a][b]!="" and self.mat[a][b].split(" ")[0]!=self.side and self.mat[a][b].split(" ")[1] in ["queen","rook"]:
                                        castle=False
                                        break
                                    elif self.mat[a][b]!="" and self.mat[a][b].split(" ")[0]==self.side:
                                        break
                                    b=b+1
                                if not castle:
                                    break
                                a=i
                                b=j
                                if a+2<8 and b+1<8 and self.mat[a+2][b+1]!="" and self.mat[a+2][b+1].split(" ")[0]!=self.side and self.mat[a+2][b+1].split(" ")[1]=="knight":
                                    castle=False
                                    break
                                elif a+1<8 and b+2<8 and self.mat[a+1][b+2]!="" and self.mat[a+1][b+2].split(" ")[0]!=self.side and self.mat[a+1][b+2].split(" ")[1]=="knight":
                                    castle=False
                                    break
                                elif a-1>=0 and b+2<8 and self.mat[a-1][b+2]!="" and self.mat[a-1][b+2].split(" ")[0]!=self.side and self.mat[a-1][b+2].split(" ")[1]=="knight":
                                    castle=False
                                    break
                                elif a-2>=0 and b+1<8 and self.mat[a-2][b+1]!="" and self.mat[a-2][b+1].split(" ")[0]!=self.side and self.mat[a-2][b+1].split(" ")[1]=="knight":
                                    castle=False
                                    break
                                i=i-1
                            if castle:
                                possible_move_perpiece.append([cord[0]-2,cord[1]])
                            #right rook    
                            i=cord[0]
                            castle=True
                            while i<=cord[0]+2:
                                if self.mat[i][j]!=""  and self.mat[i][j]!="white king":
                                    castle=False
                                    break
                                a=i+1
                                b=j+1
                                while a<8 and b<8:
                                    if self.mat[a][b]!="" and self.mat[a][b].split(" ")[0]!=self.side and self.mat[a][b].split(" ")[1] in ["queen","bishop"]:
                                        castle=False
                                        break
                                    elif self.mat[a][b]!="" and self.mat[a][b].split(" ")[0]==self.side:
                                        break
                                    a=a+1
                                    b=b+1
                                if not castle:
                                    break
                                a=i-1
                                b=j+1
                                while a>=0 and b<8:
                                    if self.mat[a][b]!="" and self.mat[a][b].split(" ")[0]!=self.side and self.mat[a][b].split(" ")[1] in ["queen","bishop"]:
                                        castle=False
                                        break
                                    elif self.mat[a][b]!="" and self.mat[a][b].split(" ")[0]==self.side:
                                        break
                                    a=a-1
                                    b=b+1
                                if not castle:
                                    break
                                a=i
                                b=j+1
                                while b<8:
                                    if self.mat[a][b]!="" and self.mat[a][b].split(" ")[0]!=self.side and self.mat[a][b].split(" ")[1] in ["queen","rook"]:
                                        castle=False
                                        break
                                    elif self.mat[a][b]!="" and self.mat[a][b].split(" ")[0]==self.side:
                                        break
                                    b=b+1
                                if not castle:
                                    break
                                a=i
                                b=j
                                if a+2<8 and b+1<8 and self.mat[a+2][b+1]!="" and self.mat[a+2][b+1].split(" ")[0]!=self.side and self.mat[a+2][b+1].split(" ")[1]=="knight":
                                    castle=False
                                    break
                                elif a+1<8 and b+2<8 and self.mat[a+1][b+2]!="" and self.mat[a+1][b+2].split(" ")[0]!=self.side and self.mat[a+1][b+2].split(" ")[1]=="knight":
                                    castle=False
                                    break
                                elif a-1>=0 and b+2<8 and self.mat[a-1][b+2]!="" and self.mat[a-1][b+2].split(" ")[0]!=self.side and self.mat[a-1][b+2].split(" ")[1]=="knight":
                                    castle=False
                                    break
                                elif a-2>=0 and b+1<8 and self.mat[a-2][b+1]!="" and self.mat[a-2][b+1].split(" ")[0]!=self.side and self.mat[a-2][b+1].split(" ")[1]=="knight":
                                    castle=False
                                    break
                                i=i+1
                            if castle:
                                possible_move_perpiece.append([cord[0]+2,cord[1]])
                        else:
                            i=cord[0]
                            j=cord[1]
                            castle=True
                            while i>=cord[0]-2:
                                if self.mat[i][j]!="" and self.mat[i][j]!="black king":
                                    castle=False
                                    break
                                a=i-1
                                b=j-1
                                while a>=0 and b>=0:
                                    if self.mat[a][b]!="" and self.mat[a][b].split(" ")[0]!=self.side and self.mat[a][b].split(" ")[1] in ["queen","bishop"]:
                                        castle=False
                                        break
                                    elif self.mat[a][b]!="" and self.mat[a][b].split(" ")[0]==self.side:
                                        break
                                    a=a-1
                                    b=b-1
                                if not castle:
                                    break
                                a=i+1
                                b=j-1
                                while a<8 and b>=0:
                                    if self.mat[a][b]!="" and self.mat[a][b].split(" ")[0]!=self.side and self.mat[a][b].split(" ")[1] in ["queen","bishop"]:
                                        castle=False
                                        break
                                    elif self.mat[a][b]!="" and self.mat[a][b].split(" ")[0]==self.side:
                                        break
                                    a=a+1
                                    b=b-1
                                if not castle:
                                    break
                                a=i
                                b=j-1
                                while b>=0:
                                    if self.mat[a][b]!="" and self.mat[a][b].split(" ")[0]!=self.side and self.mat[a][b].split(" ")[1] in ["queen","rook"]:
                                        castle=False
                                        break
                                    elif self.mat[a][b]!="" and self.mat[a][b].split(" ")[0]==self.side:
                                        break
                                    b=b-1
                                if not castle:
                                    break
                                a=i
                                b=j
                                if a+2<8 and b-1>=0 and self.mat[a+2][b-1]!="" and self.mat[a+2][b-1].split(" ")[0]!=self.side and self.mat[a+2][b-1].split(" ")[1]=="knight":
                                    castle=False
                                    break
                                elif a+1<8 and b-2>=0 and self.mat[a+1][b-2]!="" and self.mat[a+1][b-2].split(" ")[0]!=self.side and self.mat[a+1][b-2].split(" ")[1]=="knight":
                                    castle=False
                                    break
                                elif a-1>=0 and b-2>=0 and self.mat[a-1][b-2]!="" and self.mat[a-1][b-2].split(" ")[0]!=self.side and self.mat[a-1][b-2].split(" ")[1]=="knight":
                                    castle=False
                                    break
                                elif a-2>=0 and b-1>=0 and self.mat[a-2][b-1]!="" and self.mat[a-2][b-1].split(" ")[0]!=self.side and self.mat[a-2][b-1].split(" ")[1]=="knight":
                                    castle=False
                                    break
                                i=i-1
                            if castle:
                                possible_move_perpiece.append([cord[0]-2,cord[1]])
                            #right rook    
                            i=cord[0]
                            castle=True
                            while i<=cord[0]+2:
                                if self.mat[i][j]!="" and self.mat[i][j]!="black king":
                                    castle=False
                                    break
                                a=i-1
                                b=j-1
                                while a>=0 and b>=0:
                                    if self.mat[a][b]!="" and self.mat[a][b].split(" ")[0]!=self.side and self.mat[a][b].split(" ")[1] in ["queen","bishop"]:
                                        castle=False
                                        break
                                    elif self.mat[a][b]!="" and self.mat[a][b].split(" ")[0]==self.side:
                                        break
                                    a=a-1
                                    b=b-1
                                if not castle:
                                    break
                                a=i+1
                                b=j-1
                                while a<8 and b>=0:
                                    if self.mat[a][b]!="" and self.mat[a][b].split(" ")[0]!=self.side and self.mat[a][b].split(" ")[1] in ["queen","bishop"]:
                                        castle=False
                                        break
                                    elif self.mat[a][b]!="" and self.mat[a][b].split(" ")[0]==self.side:
                                        break
                                    a=a+1
                                    b=b-1
                                if not castle:
                                    break
                                a=i
                                b=j-1
                                while b>=0:
                                    if self.mat[a][b]!="" and self.mat[a][b].split(" ")[0]!=self.side and self.mat[a][b].split(" ")[1] in ["queen","rook"]:
                                        castle=False
                                        break
                                    elif self.mat[a][b]!="" and self.mat[a][b].split(" ")[0]==self.side:
                                        break
                                    b=b-1
                                if not castle:
                                    break
                                a=i
                                b=j
                                if a+2<8 and b-1>=0 and self.mat[a+2][b-1]!="" and self.mat[a+2][b-1].split(" ")[0]!=self.side and self.mat[a+2][b-1].split(" ")[1]=="knight":
                                    castle=False
                                    break
                                elif a+1<8 and b-2>=0 and self.mat[a+1][b-2]!="" and self.mat[a+1][b-2].split(" ")[0]!=self.side and self.mat[a+1][b-2].split(" ")[1]=="knight":
                                    castle=False
                                    break
                                elif a-1>=0 and b-2>=0 and self.mat[a-1][b-2]!="" and self.mat[a-1][b-2].split(" ")[0]!=self.side and self.mat[a-1][b-2].split(" ")[1]=="knight":
                                    castle=False
                                    break
                                elif a-2>=0 and b-1>=0 and self.mat[a-2][b-1]!="" and self.mat[a-2][b-1].split(" ")[0]!=self.side and self.mat[a-2][b-1].split(" ")[1]=="knight":
                                    castle=False
                                    break
                                i=i+1
                            if castle:
                                possible_move_perpiece.append([cord[0]+2,cord[1]])
                elif piece == "pawn":
                    if self.side=="white":    
                        if cord[1]==1:
                            if self.mat[cord[0]][cord[1]+1]=="":
                                possible_move_perpiece.append([cord[0],cord[1]+1])
                                if self.mat[cord[0]][cord[1]+2]=="":
                                    possible_move_perpiece.append([cord[0],cord[1]+2])
                        elif cord[1]+1<8 and self.mat[cord[0]][cord[1]+1]=="":
                                possible_move_perpiece.append([cord[0],cord[1]+1])
                        if cord[0]+1<8 and cord[1]+1<8 and self.mat[cord[0]+1][cord[1]+1]!="" and self.mat[cord[0]+1][cord[1]+1].split(" ")[0]!=self.side:
                            possible_move_perpiece.append([cord[0]+1,cord[1]+1])
                        if cord[0]-1>=0 and cord[1]+1<8 and self.mat[cord[0]-1][cord[1]+1]!="" and self.mat[cord[0]-1][cord[1]+1].split(" ")[0]!=self.side:
                            possible_move_perpiece.append([cord[0]-1,cord[1]+1])
                    elif self.side=="black":
                        if cord[1]==6:
                            if self.mat[cord[0]][cord[1]-1]=="":
                                possible_move_perpiece.append([cord[0],cord[1]-1])
                                if self.mat[cord[0]][cord[1]-2]=="":
                                    possible_move_perpiece.append([cord[0],cord[1]-2])
                        elif cord[1]-1>=0 and self.mat[cord[0]][cord[1]-1]=="":
                                possible_move_perpiece.append([cord[0],cord[1]-1])
                        if cord[0]+1<8 and self.mat[cord[0]+1][cord[1]-1]!="" and self.mat[cord[0]+1][cord[1]-1].split(" ")[0]!=self.side:
                            possible_move_perpiece.append([cord[0]+1,cord[1]-1])
                        if cord[0]-1>=0 and self.mat[cord[0]-1][cord[1]-1]!="" and self.mat[cord[0]-1][cord[1]-1].split(" ")[0]!=self.side:
                            possible_move_perpiece.append([cord[0]-1,cord[1]-1])
                total_possible_move[piece][cordIndex]=possible_move_perpiece
        return total_possible_move

    def getNextState(self,piece,initial_cord,final_cord):
        ret=copy.deepcopy(self.pieces)
        castle=self.castle
        for i,_ in enumerate(ret[self.side][piece]):
            if ret[self.side][piece][i] == initial_cord:
                if self.mat[final_cord[0]][final_cord[1]]!="" and self.mat[final_cord[0]][final_cord[1]].split(" ")[0]!=self.side:
                    if self.side=="white":
                        ret["black"][self.mat[final_cord[0]][final_cord[1]].split(" ")[1]].remove(final_cord)
                    if self.side=="black":
                        ret["white"][self.mat[final_cord[0]][final_cord[1]].split(" ")[1]].remove(final_cord)
                #castle
                if piece == "king": 
                    if (initial_cord[0]-final_cord[0])**2==4:
                        if final_cord[0]>initial_cord[0]:
                            for j,cord in enumerate(ret[self.side]["rook"]):
                                if cord[0]>initial_cord[0]:
                                    ret[self.side]["rook"][j][0]=initial_cord[0]+1
                                    
                        elif final_cord[0]<initial_cord[0]:
                            for j,cord in enumerate(ret[self.side]["rook"]):
                                if cord[0]<initial_cord[0]:
                                    ret[self.side]["rook"][j][0]=initial_cord[0]-1
                    castle=False
                ret[self.side][piece][i]=final_cord
                if piece == "pawn":
                    if final_cord[1]==0 and final_cord[1]==7:
                        ret[self.side][piece].remove(final_cord)
                        ret[self.side]["queen"].append(final_cord)    
                break
        return castle,ret

class AI:
    def __init__(self,depth):
        self.depth=depth
        self.alphaSide=""
    def alphaBeta(self,currentState,alpha,beta,depth):
        global totalNodesSearched
        if depth==self.depth:
            white,black=currentState.getStateScore()
            if self.alphaSide=="white":
                return white
            else:
                return black
        else:
            if currentState.side==self.alphaSide:
                candidateMoves=currentState.getLeagleMoves()
                for piece in candidateMoves:
                    for cordIndex in candidateMoves[piece]:
                        for final_cord in candidateMoves[piece][cordIndex]:
                            #print(depth,currentState.side,piece,currentState.pieces[currentState.side][piece][cordIndex],final_cord)
                            castle,pieces=currentState.getNextState(piece,currentState.pieces[currentState.side][piece][cordIndex],final_cord)
                            if currentState.side=="white":
                                newState=State(castle,pieces,"black")
                            else:
                                newState=State(castle,pieces,"white")
                            alpha=max(self.alphaBeta(newState,alpha,beta,depth+1),alpha)
                            if alpha>=beta :
                                return beta
                return alpha
            else:
                candidateMoves=currentState.getLeagleMoves()
                for piece in candidateMoves:
                    for cordIndex in candidateMoves[piece]:
                        for final_cord in candidateMoves[piece][cordIndex]:
                            #print(depth,currentState.side,piece,currentState.pieces[currentState.side][piece][cordIndex],final_cord)
                            castle,newPieces=currentState.getNextState(piece,currentState.pieces[currentState.side][piece][cordIndex],final_cord)
                            if currentState.side=="white":
                                newState=State(castle,newPieces,"black")
                            else:
                                newState=State(castle,newPieces,"white")
                            beta=min(self.alphaBeta(newState,alpha,beta,depth+1),beta)
                            if alpha>=beta :
                                return alpha
                return beta  
        
    def getMove(self,alphaState):
        alpha=-sys.maxsize
        beta=sys.maxsize
        value=alpha
        self.alphaSide=alphaState.side
        candidateMoves=alphaState.getLeagleMoves()
        for piece in candidateMoves:
            for cordIndex in candidateMoves[piece]:
                for final_cord in candidateMoves[piece][cordIndex]:
                    castle,newPieces=alphaState.getNextState(piece,alphaState.pieces[alphaState.side][piece][cordIndex],final_cord)
                    if alphaState.side=="white":
                        newState=State(castle,newPieces,"black")
                    else:
                        newState=State(castle,newPieces,"white")
                    x=self.alphaBeta(newState,alpha,beta,0)
                    print(alphaState.side,piece,alphaState.pieces[alphaState.side][piece][cordIndex],final_cord,x)
                    if value<x:
                        value=x
                        movePiece=piece
                        moveInitialCord=alphaState.pieces[alphaState.side][piece][cordIndex]
                        moveFinalCord=final_cord
                    
        return movePiece,moveInitialCord,moveFinalCord
                        
if __name__ == "__main__":
    side = input("Which side do you want to play from?")
    if side == "black" or side=="Black":
        b=Board("white","black")
    else:
        b=Board("black","white")
    ai=AI(3)
    while True:
                    if side=="white":
                        piece=input("piece:  ")
                        x,y=input("from:  ").strip().split()
                        initial_cord=[int(x)-1,int(y)-1]
                        x,y=input("to:  ").strip().split()
                        final_cord=[int(x)-1,int(y)-1]
                        b.changeCurrentState(piece,initial_cord,final_cord)
                        move=ai.getMove(b.currentState)
                        print(move[0],[move[1][0]+1,move[1][1]+1],[move[2][0]+1,move[2][1]+1])
                        b.changeCurrentState(move[0],move[1],move[2])
                    else:
                        move=ai.getMove(b.currentState)
                        print(move[0],[move[1][0]+1,move[1][1]+1],[move[2][0]+1,move[2][1]+1])
                        b.changeCurrentState(move)
                        piece=input("piece")
                        x,y=input("from:  ").strip().split()
                        initial_cord=[int(x),int(y)]
                        x,y=input("to:  ").strip().split()
                        final_cord=[int(x)-1,int(y)-1]
                        b.changeCurrentState(piece,initial_cord,final_cord)
                    if b.checkMate():
                        print("checkMate")
                        break
