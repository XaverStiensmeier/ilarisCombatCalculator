#!/usr/bin/env python3

class IlarisCharacter():
    def __init__(self, name="Alrik", ws=6, wss=6, koloss=0, tp=(3,6,5), at=12, vt=12, actions=1, wounds=0, ini=3):
        self.name = name
        self.ws=ws
        self.wss=wss
        self.koloss=koloss
        self.tp=tp # (x,y,z)=xDy+z (in z the KK/strength bonus is included)
        self.at=at
        self.vt=vt
        self.actions=actions
        self.wounds=wounds
        self.ini=ini

    def isDead(self):
        return self.wounds>8
    
    def __str__(self):
         return f"{self.name} WS/WS* {self.ws}/{self.wss} with AT {self.at} VT {self.vt} TP {self.tp[0]}W{self.tp[1]}+{self.tp[2]} and INI {self.ini}"
