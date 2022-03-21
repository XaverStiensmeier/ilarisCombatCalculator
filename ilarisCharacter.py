#!/usr/bin/env python3

class IlarisCharacter():
    def __init__(self, name="Alrik", ws=4, wss=4, tp=(1,6,4), at=8, vt=8, bTP=0, ini=3):
        self.name = name
        self.ws=ws
        self.wss=wss
        self.tp=tp # (x,y,z)=xWy+z
        self.at=at
        self.vt=vt
        self.bTP=bTP
        self.wounds=0
        self.ini=ini

    def isDead(self):
        return self.wounds>8
    
    def __str__(self):
         return f"{self.name} WS/WS* {self.ws}/{self.wss} with AT {self.at} VT {self.vt} TP {self.tp[0]} W+{self.tp[2]}+{self.bTP} and INI {self.ini}"
