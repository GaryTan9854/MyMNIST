# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 10:30:17 2021

@author: user
"""

import sys
import random
import numpy as np
#import pandas as pd
import itertools
#from itertools import product
#import more_itertools
#import math
from datetime import datetime
from tqdm import tqdm 
from time import sleep

Suits = {"H":"♡", "S":"♠", "D":"♢", "C":"♣"}
Values = {**{i:str(i) for i in range(2,11)}, **{ 11:'J',12:'Q', 13:'K', 14:'A'}}

SpecialHand = {"normal":9999,"high card":0, "pair":1, "two pair":2, "three of a kind":3,
              "straight":4,"flush":5, "full house":6,
              "four of a kind":7, "straight flush":8, "royal flush":9,
              "三同花": 500, "三順子":510, "六對半":520,
              "全黑一張紅":530,"全紅一張黑":540, "全大":550, "全小":560, 
              "單pair":570, "雙pair無花無順": 580, "單三條":590, 
              "大全小":700, "大全大":710,
              "六對半帶葫蘆":760, "全黑一點紅A":740, "全紅一點黑A":745,
              "全紅":750, "全黑":755, "四套三條":800,"三分天下":810, "三同花順":820, "十二皇族":830, 
              "一條龍":900, "清龍":1000}
    
def handtype_text(handtxt):
    return (SpecialHand[handtxt])
    
def convert_cardnum(value):
    #values = {**{i:str(i) for i in range(2,11)}, 
    #          **{ 11:'J',12:'Q', 13:'K', 14:'A'}}
    return(Values[value]) 

class Hist(dict):
    """A map from each item (x) to its frequency."""

    def __init__(self, seq=[]):
        "Creates a new histogram starting with the items in seq."
        for x in seq:
            self.count(x)

    def count(self, x, f=1):
        "Increments the counter associated with item x."
        self[x] = self.get(x, 0) + f
        if self[x] == 0:
            del self[x]
    
class Card(object):
    def __init__(self, suit, val):
        self.suit = suit
        self.value = val

    # Implementing build in methods so that you can print a card object
    def __unicode__(self):
        return self.show()
    def __str__(self):
        return self.show()
    def __repr__(self):
        return self.show()
    
    def __eq__(self, other):
        return self.value == other.value and self.suit == other.suit

    def __lt__(self, other):
        return self.value < other.value

    def cardstr(self):
        return "{:0>2d}".format(self.value)+self.suit
            
    def show(self):    
        return Suits[self.suit]+Values[self.value]
    
    def isBlack(self):
        return self.suit == "C" or self.suit=="S"
    
    def isRed(self):
        return self.suit == "D" or self.suit=="H"

# Card object in Deck
class Deck(object):
    def __init__(self):
        self.cards = []
        self.build()

    # Display all cards in the deck
    def show(self):
        phands = [self.cards[:13],self.cards[13:26], self.cards[26:39], self.cards[39:]]
        for cc in phands: 
            print(cc)
        return(str(phands))
            

    # Generate 52 cards
    def build(self):
        self.cards = []
        numbers=list(range(2,15))
        suits = ['C','D','H','S']
        for i in numbers:
            for s in suits:
                self.cards.append(Card(s, i)) #<= Card object append here
        
        
    # Shuffle the deck
    def shuffle(self, num=1):
        length = len(self.cards)
        for _ in range(num):
            # This is the fisher yates shuffle algorithm
            for i in range(length-1, 0, -1):
                randi = random.randint(0, i)
                if i == randi:
                    continue
                self.cards[i], self.cards[randi] = self.cards[randi], self.cards[i]
    
    # You can also use the build in shuffle method
    # random.shuffle(self.cards)
    def shuffle2(self,num=1):
        random.shuffle(self.cards)

    def distribute(self): #return an array of 4 x 13
        self.shuffle(3)
        phands = [self.cards[:13],self.cards[13:26], self.cards[26:39], self.cards[39:]]
        return phands

    # Return the top card
    def deal(self):
        return self.cards.pop() #取出list最後一個元素並且移除
    

        
        
#object for a general hand of cards
#hand = list of Cards, not list of string
#initiate with list of string
class Hand(object):
    def __init__(self,hand):
        if str(type(hand[0]))=="<class '__main__.Card'>":
            #Card object
            self.handlist = sorted( [ i.cardstr() for i in hand ])
            self.hand = sorted(hand)  # sorted by __eq__ & __lt__
        else:
            #List of String:['02D','03H'...]
            self.handlist = sorted(hand)
            self.hand=[]
            for i in self.handlist:
                cc = Card(i[2:], int(i[:2])) # number then suit 
                self.hand.append(cc)
            
        #print(self.handlist)
        #print(self.hand)
        #input('wait')
        
        self.handsize = len(hand)
        self.handtype = ''
        self.handtype_val=0
        self.score=0
        self.suits = [ self.hand[i].suit for i in range(self.handsize)]
        self.numbers = [ self.hand[i].value for i in range(self.handsize)]
        self.rnum = [ self.numbers.count(i) for i in self.numbers]
        self.rlet = [ self.suits.count(i) for i in self.suits]
        self.dif = max(self.numbers) - min(self.numbers)
        self.p=[0,0,0,0,0] #parameters for different handtypes
        
        self.suithist = Hist()
        self.numhist = Hist()
        
        
        for c in self.hand:
            self.suithist.count(c.suit)
            self.numhist.count(c.value)

        self.sets = list(self.numhist.values())  #dict 的函數
        self.sets.sort(reverse=True)
        self.suitset = list(self.suithist.values())
        self.suitset.sort(reverse=True)
        
    def show(self):
        #s = [ i.show() for i in self.hand ]
        s='[ '
        for i in self.hand:
            s=s+i.show()+' '
        return(s+']')
    
    def isAllBlack(self):
        bb = [ i.isBlack() for i in self.hand ]
        return(all(bb))
    
    def isAllRed(self):
        rr = [ i.isRed() for i in self.hand ]
        return(all(rr))
    
    def isAllButOneBlack(self):
        rr=0
        cc=0
        for i in self.hand:
            if i.isRed():
                rr+=1
            else:
                cc=i.value    
        if rr==self.handsize-1 :
            return cc
        else:
            return 0
        
    def isAllButOneRed(self):
        rr=0
        cc=0
        for i in self.hand:
            if i.isBlack():
                rr+=1
            else:
                cc=i.value    
        if rr==self.handsize-1 :
            return cc
        else:
            return 0
    
    def check_sets(self, *t):
        for need, have in zip(t, self.sets): #這招特別 因為sort過
            if need > have: return False
        return True
    
    #for precise match of *t not >
    def check_sets2(self, *t):
        for need, have in zip(t, self.sets): #這招特別 因為sort過
            if need != have: return False
        return True
    
    def check_suitset(self, *t):
        for need, have in zip(t, self.suitset): #這招特別 因為sort過
            if need > have: return False
        return True
    
    def has_pair(self):
        """Checks whether this hand has a pair."""
        return self.check_sets(2)
        
    def has_twopair(self):
        """Checks whether this hand has two pair."""
        return self.check_sets(2, 2)
    
    def has_threekind(self):
        """Checks whether this hand has three of a kind."""
        return self.check_sets(3)
        
    def has_fourkind(self):
        """Checks whether this hand has four of a kind."""
        return self.check_sets(4)

    def has_fullhouse(self):
        """Checks whether this hand has a full house."""
        return self.check_sets(3, 2)

    def has_flush(self):
        """Checks whether this hand has a flush."""
        for val in self.suitshist.values():
            if val >= 5:
                return True
        return False
    
    def no_flush(self):
        for val in self.suithist.values():
            if val < 5:
                return True
        return False
    
    #wrong algo
    def no_straight(self):
        return( not self.has_straight())
           
    #5-K or 6-A
    def chk_allbig(self):
        bb = (max(self.numbers)<=13 and min(self.numbers)>=5) or (max(self.numbers)<=14 and min(self.numbers)>=6)
        return(bb)
    
    #8-A
    def chk_bigallbig(self):
        bb = max(self.numbers)<=14 and min(self.numbers)>=8
        return(bb)
    
    #2-8
    def chk_bigallsmall(self):
        r = self.numbers
        bb = max(r)<=8 and min(r)>=2
        return(bb)
       
    #1-9 or 2-10
    def chk_allsmall(self):
        ranks = self.numhist.copy()
        ranks[1] = ranks.get(14, 0) #把 A 調到前面當 1
        ranks.pop(14, None)
        if ranks[1]==0:
            ranks.pop(1,None)
        bb = (max(ranks)<=9 and min(ranks)>=1) or (max(ranks)<=10 and min(ranks)>=2)
        return(bb)
            
        
    def has_straight(self):
        """Checks whether this hand has a straight."""
        # make a copy of the rank histogram before we mess with it
        ranks = self.numhist.copy()
        ranks[1] = ranks.get(14, 0) #把 A 調到前面當 1
        # see if we have 5 in a row
        return self.in_a_row(ranks, 5)
    
    
    def in_a_row(self, ranks, n=5):
        """Checks whether the histogram has n ranks in a row.
        hist: map from rank to frequency
        n: number we need to get to
        """
        count = 0
        for i in range(1, 15):
            if ranks.get(i, 0):
                count += 1
                if count == n:
                    return i  #return highest num of the straight
            else:
                count = 0
        return 0
    
    
    
class Hand3(Hand):
    def __init__(self,hand):
        super(Hand3, self).__init__(hand)
        self.sss=self.score_hand()
        
    def check_three_of_a_kind(self):
        cards = []
        for i in self.numbers:
            if self.numbers.count(i) == 3:
                three = i
            else: 
                cards.append(i)
        score = 45 + three 
        self.p[0]=three
        self.p[1:]=cards
        return score
    
    def check_pair(self):    
        pair = []
        cards  = []
        for i in self.numbers:
            if self.numbers.count(i) == 2:
                pair.append(i)
            elif self.numbers.count(i) == 1:    
                cards.append(i)
                cards = sorted(cards,reverse=True)
        score = 15 + pair[0] + cards[0]/100 #+ cards[1]/1000 + cards[2]/10000
        self.p[0]=pair[0]
        self.p[1:]=cards
        return score
    
    def check_highcard(self):
        n = sorted(self.numbers,reverse=True)
        score = n[0] + n[1]/100 + n[2]/1000
        self.p=n
        return score
        
    
    def score_hand(self):
    #3張 除了特殊牌型外 沒有順沒有同花
    #只有 三條，一對，亂
        if 3 in self.rnum:
            self.handtype = 'three of a kind' 
            self.score = self.check_three_of_a_kind()
        elif self.rnum.count(2) == 2:
            self.handtype = 'pair'
            self.score = self.check_pair()
        elif self.dif == 2:
            self.handtype = 'high card' #staight in 3 cards
            self.score = self.check_highcard()
        else:
            self.handtype= 'high card'
            self.score = self.check_highcard()
        self.handtype_val=handtype_text(self.handtype)
        sss =[self.score,  self.handtype, self.handtype_val]
        return(sss)
    
    def hand_dscp(self):
        ht = self.handtype
        sss=''
        if ht== 'three of a kind':
            sss=convert_cardnum(self.p[0]) + ' 衝三'
        elif ht =='pair':
            sss = convert_cardnum(self.p[0])+' Pair'
        elif ht== 'high card': #staight in 3 cards
            sss = '亂 ['+convert_cardnum(self.p[0])+' '+convert_cardnum(self.p[1])+' '+convert_cardnum(self.p[2])+']'
        
        return(sss)
    
class Hand5(Hand):
    def __init__(self,hand):
        super(Hand5, self).__init__(hand)
        self.sss=self.score_hand()
        
    def check_four_of_a_kind(self):
        for i in self.numbers:
            if self.numbers.count(i) == 4:
                four = i
            elif self.numbers.count(i) == 1:
                card = i
        score = 105 + four # + card/100 ＃也不必看第五張牌
        self.p[0]=four
        self.p[1]=card
        return score

    def check_full_house(self):
        for i in self.numbers:
            if self.numbers.count(i) == 3:
                full = i
            elif self.numbers.count(i) == 2:
                p = i
        score = 90 + full  # +  p/100  full house won't need to differentiate the pair card
        self.p[0]=full
        self.p[1]=p
        return score

    def check_three_of_a_kind(self):
        cards = []
        for i in self.numbers:
            if self.numbers.count(i) == 3:
                three = i
            else: 
                cards.append(i)
        score = 45 + three 
        self.p[0]=three
        self.p[1:]=cards
        return score
    
    def check_two_pair(self):
        pairs = []
        cards = []
        for i in self.numbers:
            if self.numbers.count(i) == 2:
                pairs.append(i)
            elif self.numbers.count(i) == 1:
                cards.append(i)
                cards = sorted(cards,reverse=True)
        score = 30 + max(pairs) + min(pairs)/100 + cards[0]/1000
        self.p[0]=max(pairs)
        self.p[1]=min(pairs)
        self.p[2:]=cards
        return score

    def check_pair(self):    
        pair = []
        cards  = []
        for i in self.numbers:
            if self.numbers.count(i) == 2:
                pair.append(i)
            elif self.numbers.count(i) == 1:    
                cards.append(i)
                cards = sorted(cards,reverse=True)
        score = 15 + pair[0] + cards[0]/100 #+ cards[1]/1000 + cards[2]/10000
        self.p[0]=pair[0]
        self.p[1:]=cards
                
        return score
    
    def check_straight(self, nn):
        #if nn==1:
        self.p[0]=nn-4
        self.p[1]=nn
        #self.p[0]=min(self.numbers)
        #self.p[1]=max(self.numbers)        
        if self.p[0]==1:
            return 65+13.5
        return 65+self.p[1] #如果 A-5 straight 比較大則要改此
    
    def check_highcard(self):
        n = sorted(self.numbers,reverse=True)
        score = n[0] + n[1]/100 + n[2]/1000 + n[3]/10000 + n[4]/100000
        self.p=n
        return score
    
    def score_hand(self):
        #print(self.handlist)
        #print(self.numbers)
        #print(self.rnum)
        #print(self.rlet)
        #print(self.dif)
        #print(self.p)
        #input('wait')
        
        if 5 in self.rlet: #花色數目=5=同花
            if self.numbers ==[10,11,12,13,14]: #why already sorted?
                self.handtype = 'royal flush'
                self.score = 135
                self.p=self.numbers
            elif self.numbers ==[2,3,4,5,14]:
                self.handtype = '同花次大順'
                self.score = 130
                self.p=self.numbers
            elif self.dif == 4 and max(self.rnum) == 1: #大小只差4, 每個數字又只出現一次                
                self.handtype = 'straight flush'
                self.score = 120 + max(self.numbers)
                self.p[0]=min(self.numbers)
                self.p[1]=max(self.numbers)  
            else:
                self.handtype = 'flush'
                n = sorted(self.numbers,reverse=True)
                self.score = 75+ n[0] + n[1]/100 + n[2]/1000 + n[3]/10000 + n[4]/100000
                self.p=n                
        elif 4 in self.rnum:
            self.handtype = 'four of a kind'
            self.score = self.check_four_of_a_kind()
        elif sorted(self.rnum) == [2,2,3,3,3]:
            self.handtype = 'full house'
            self.score = self.check_full_house()
        elif 3 in self.rnum:
            self.handtype = 'three of a kind' 
            self.score = self.check_three_of_a_kind()
        elif self.rnum.count(2) == 4:
            self.handtype = 'two pair'
            self.score = self.check_two_pair()
        elif self.rnum.count(2) == 2:
            self.handtype = 'pair'
            self.score = self.check_pair()
        else:
            stt = self.has_straight()
            if stt>0:
                self.handtype = 'straight'
                self.score = self.check_straight(stt)
            else:
                self.handtype= 'high card'
                self.score = self.check_highcard()
        self.handtype_val=handtype_text(self.handtype)
        sss =[self.score,  self.handtype, self.handtype_val]
        return(sss)
    
    def hand_dscp(self):
        hh = self.handtype
        sss=hh
        if hh== 'royal flush':
            sss = '同花大順'
        elif hh== '同花次大順':
            sss = '同花次大順'
        elif hh=='straight flush':
            sss = str(self.p[0])+' 同花順'
        elif hh=='flush':
            sss = '同花 ['+convert_cardnum(self.p[0])+' '+convert_cardnum(self.p[1])+' '+convert_cardnum(self.p[2])+' '+convert_cardnum(self.p[3])+' '+convert_cardnum(self.p[4])+']'
        elif hh=='four of a kind':
            sss = convert_cardnum(self.p[0])+' 鐵支'
        elif hh=='full house':
            sss = convert_cardnum(self.p[0])+' 葫蘆'
        elif hh=='three of a kind' :
            sss=convert_cardnum(self.p[0])+' 三條'
        elif hh=='two pair':
            sss=convert_cardnum(self.p[0])+'/'+ convert_cardnum(self.p[1])+' Pair'
        elif hh=='pair':
            sss = convert_cardnum(self.p[0])+' Pair'
        elif hh=='straight':
            if self.p[1]==14:
                sss = str(self.p[0])+'-'+'A 順'
            else:
                sss = str(self.p[0])+'-'+str(self.p[1])+' 順'
        elif hh=='high card':
            sss = '亂 ['+convert_cardnum(self.p[0])+' '+ convert_cardnum(self.p[1])+' '+convert_cardnum(self.p[2])+' '+convert_cardnum(self.p[3])+' '+convert_cardnum(self.p[4])+']'
        
        return(sss)
    
#專屬13支一手牌的object
class Hand13(Hand):
    def __init__(self, hand):
        super(Hand13, self).__init__(hand)
        self.htop = Hand3(hand[:3]) #Hand3(['♢2', '♢3', '♢4']) # 
        self.hmid = Hand5(hand[3:8]) #Hand5(['♢5', '♢6', '♢7', '♢8', '♢9']) #
        self.hbot = Hand5(hand[8:]) #Hand5(['♢10', '♢J', '♢Q', '♢K', '♢A']) #
        self.ss = [self.htop.score,self.hmid.score,self.hbot.score]
        self.score = sum(self.ss)
        self.totalscores = self.score
        self.specialhand = 'normal' #self.chk_special()
        self.CanAttack = False
        self.attack_score =0
        self.defense_score=0
    
    def show355(self):
        ss= self.htop.show() + self.hmid.show()+self.hbot.show()
        return ss
        
    
    def check_pair(self):    
        pair = []
        cards  = []
        
        for i in self.numbers:
            if self.numbers.count(i) == 2:
                pair.append(i)
            elif self.numbers.count(i) == 1:    
                cards.append(i)
                cards = sorted(cards,reverse=True)
        no_of_pairs=len(pair)/2
        return no_of_pairs
        
    def chk_special(self):
        #self.suits = [ self.hand[i].suit for i in range(self.handsize)]
        #self.numbers = [ self.hand[i].value for i in range(self.handsize)]
        #self.rnum = [ self.numbers.count(i) for i in self.numbers]
        #self.rlet = [ self.suits.count(i) for i in self.suits]
        #self.dif = max(self.numbers) - min(self.numbers)
        #"三同花": 50, "三順子":55, "六對半":60,"四套三條":70 ,
        #      "全黑一張紅":80,"全紅一張黑":81, "全大":200, "全小":201, 
        #      "單pair無花無順": 100, "單三張":101, 
        #      "六對半帶葫蘆":110, "全黑一點紅A":120, "全紅一點黑A":121  
        #      "全紅":250, "全黑":251, "三分天下":300, "三同花順":350, "十二皇族":400, "一條龍":500, "清龍":1000}
        ht = 'normal' 
        if self.dif==12 and len(self.numhist)==13: #龍
            #print(len(self.numhist))
            if max(self.rlet)==13:
                ht = '清龍'
            else:
                ht = '一條龍'
            return(ht)
        if min(self.numbers)==11:
            ht = '十二皇族'
            return(ht)
        if self.isAllBlack():
            ht = '全黑'
            return(ht)
        if self.isAllRed():
            ht = '全紅'
            return(ht)
        br = self.isAllButOneBlack()
        #chk if is A
        if br>0:
            if br== 14:
                ht = '全紅一點黑'
            else:
                ht = '全紅一張黑'
            return(ht)
        
        br = self.isAllButOneRed()
        if br>0:
            if br==14:
                ht = '全黑一點紅'
            else:
                ht = '全黑一張紅'
            return(ht)

        #全大全小: 全大：8-A 全小：2-8 ; 全大：5-K、6~A, 全小：1-9、2-10
        if self.chk_bigallbig():
            ht="大全大"
            return(ht)
        if self.chk_allbig():
            ht="全大"
            return(ht)
        if self.chk_bigallsmall():
            ht="大全小"
            return(ht)
        if self.chk_allsmall():
            ht="全小"            
            return(ht)        
        
        if self.check_sets(2,2,2,2,2,2):
            #chk 有沒有帶葫蘆
            if max(self.rnum)==3:
                ht = '六對半帶葫蘆'
            else:
                ht = '六對半'
            return(ht)
        
        #四套三張
        if self.check_sets2(3, 3, 3, 3): 
            ht="四套三條"
            return(ht)
        
        #三套四=三分天下
        if self.check_sets2(4, 4, 4): 
            ht="三分天下"
            return(ht)
        
        #三同花順＆三順子
        ss= self.has_3straight()
        if ss:
            if self.has_3straightflush(ss):
                ht="三同花順"
            else:
                ht="三順子"
            return(ht)
        
        
        #無順：5P&no10 or 10P&no5 
        #單pair：只能有一個 pair. 一定會有順 有沒有花無所謂 
        #單3張 ：不能有其他pair, 不然就會變葫蘆。有花有順無所謂
        #雙pair無花無順：一定要無花無順 
        
        #單pair
        if self.check_sets2(2,1) and max(self.rnum)==2:  #單pair
            #print(self.numhist.get(5) , self.numhist.get(10))
            #no_straight = if (self.numhist.get(5)=="None" and self.numhist.get(10)==2 ) or (self.numhist.get(10)=="None" and self.numhist.get(5)==2 ):
            ht="單pair"
            return(ht)
        
        #單三張
        if max(self.rnum)==3 and self.check_sets2(3, 1): #and not self.check_sets(3,2):
            ht="單三條"
            return(ht)
        
        #雙pair無花無順
        if max(self.rnum)==2 and self.check_sets2(2,2,1) and self.no_straight() and self.no_flush():
            ht="雙pair無花無順"
            return(ht)
        
        #三同花
        if (self.check_suitset(5,5,3)):
            ht="三同花"
            return(ht)
        

        self.handtype = ht
        self.handtype_val = handtype_text(ht)
        self.totalscores=self.handtype_val
        #print(ht)
        return(ht)
    
    #return 72072 combination of [3,5,5] from 13 cards
    def arr_allcomb13(self):
        hand = self.handlist
        comb = itertools.combinations(hand, 3)
        hh1 = []
        ii=0
        jj=0
        for i in comb:
            ii+=1    
            rest = list(set(hand)-set(i))
            comb2 = itertools.combinations(sorted(rest),5)
            for j in comb2:
                jj+=1
                hh2=[]
                rest3 = sorted(list(set(rest)-set(j)))
                hh2.append(list(i))
                hh2.append(list(j))
                hh2.append(rest3)
                hh1.append(hh2)
        return hh1
    
    def eval_attack(self, s1,s2,s3):
        return(s1*4+s2*2+s3)

    def eval_defense(self, s1,s2,s3):
        return(s1*2+s2+s3)

    def eval_CanAttack(self, s1,s2,s3):
        CanAttack = s1>=14.11 and s2>41 and s3>80 #218, but should be 3rows and stmt
        return(CanAttack)
        
    
    
    def arrange13(self): #return list of [3,5,5]
    
        #self.specialhand = self.chk_special()
        #ht = self.specialhand
        if self.specialhand!='normal':
            self.handtype = ht
            self.handtype_val = handtype_text(ht)
            self.totalscores=self.handtype_val
            #print('特殊牌型 報到！！ ~~~'+ self.specialhand,' ',self.specialhand,' ',self.specialhand+'~~~')
            return self.hand
        
        allcomb = self.arr_allcomb13()
        ss_attack=0
        ss_defense=0
        tt=0
        valid_arrange=0
        bestscore_attack=[0,0] #the best score & the location index attack
        bestscore_defense=[0,0]
        total = 72027
        for i in allcomb:
            tt+=1
            temp=tt
            print('\r' + '[Progress]:[%s%s]%3d%%;' % (
                '█' * int(temp*20/total), ' ' * (20-int(temp*20/total)),
                int(temp/total*100)), end='')
            htop = Hand3(i[0]) #['02C', '03H', '03S']
            hmid = Hand5(i[1]) #str(tuple(sorted(i[1])))
            hbot = Hand5(i[2]) #str(tuple(sorted(i[2])))
                
            s1=htop.score
            s2=hmid.score
            s3=hbot.score
            #print(s1,s2,s3)
            if s1>s2 or s1>s3 or s2>s3 : # score must be weak to strong
                continue
   #this is strength of the hand itself, not considering relationship with between 3 subset
   # and also the difference between 3 cards set & 5 cards set
            ss_attack=self.eval_attack(s1,s2,s3)
            ss_defense=self.eval_defense(s1,s2,s3)
            
            if ss_attack>bestscore_attack[0] :    
               bestscore_attack[0] = ss_attack
               bestscore_attack[1] = tt-1
        
            if ss_defense>bestscore_defense[0]:
               bestscore_defense[0]=ss_defense
               bestscore_defense[1]= tt-1

        
        
        """
        print('# of valid_arrangement :', valid_arrange)
        df = pd.DataFrame(allcomb,columns=['top', 'mid', 'bot'])
        df['score']=score_arr
        df =df[df['score'] !=0]
        print(df)
        df = df.sort_values(by='score', ascending=False)
        print(df.head(3))
        df.to_csv(r'handcombi.csv', header=None, index=None, sep=' ', mode='a')
        print("done")
        """
        
        #### place results into Hand13 attributes
        i=allcomb[bestscore_attack[1]]
        htop = Hand3(i[0]) #str(tuple(sorted(i[0])))
        hmid = Hand5(i[1]) #str(tuple(sorted(i[1])))
        hbot = Hand5(i[2]) #str(tuple(sorted(i[2])))        
        s1=htop.score
        s2=hmid.score
        s3=hbot.score
        if self.eval_CanAttack(s1,s2,s3):
            ahand = i
            self.CanAttack = True
        else:
            ahand = allcomb[bestscore_defense[1]]
            self.CanAttack = False
        
        self.htop = htop
        self.hmid = hmid
        self.hbot = hbot
        self.totalscores=s1+s2+s3
        self.ss = [s1,s2,s3]
        self.attack_score = bestscore_attack[0]
        self.defense_score= bestscore_defense[0]
        
        return ahand
    
    def show_hand_details(self):
      sss=''
      if self.specialhand!='normal':
          print('特殊牌型 報到！！ ~~~'+ self.specialhand,' ',self.specialhand,' ',self.specialhand+'~~~')
          return(sss)    
      print('\r我的排列 : ', self.show355(), '\n')
      ss = '攻擊' if self.CanAttack else '防守'
      print('攻防: '+ss+', 總分: ', "{:.2f}".format(self.totalscores),'\n')
      print(self.htop.hand_dscp())
      print(self.hmid.hand_dscp())
      print(self.hbot.hand_dscp())
      print(self.htop.show(), ', 分數：', "{:.2f}".format(self.ss[0]))
      print(self.hmid.show(), ', 分數：', "{:.2f}".format(self.ss[1]))
      print(self.hbot.show(), ', 分數：', "{:.2f}".format(self.ss[2]))

      return(sss)
  
    #同一號碼可能有多張
    #'♡2', '♠3', '♡4', '♠4', '♣5', '♢5', '♢6', '♠6' =>
    #[['H'], ['S'], ['H', 'S'], ['C', 'D'], ['D', 'S']] 
    #看是否有同花在list 內
    def has_samesuit(self,num, n):
        #選出 號碼 num 的牌
        
        ss = []
        for j in range(n):
            cc = []
            rr = filter(lambda x: x.value == (14 if num+j==1 else num+j), self.hand)
            for i in rr:
                cc.append(i.suit)
            ss.append(cc)
            
        #sort ss by len of list
        ll = list(map(lambda x: len(x) , ss))   #find the max len list of num_of_suits
        
        zz = sorted(zip(ss,ll),key=lambda x:x[1],reverse=True)
        
        #print(ss, ll, zz)
        #input('waitt')
        ans = False
        for suit in zz[0][0]: #['C', 'D']
            match=[]
            for i in zz[1:]: #(['C', 'D'], 2), (['D', 'S'], 2), (['D'], 1)] 除自己外
                match.append(suit in i[0])
            #print('suit ', suit, 'list ', i[0], suit in i[0], match)
            #input('waitt')
                
            if all(match):
                ans = True
                break
        return ans
    
    def has_3straightflush(self, rr):
        # chk same suit for 3,5,5 // 5,3,5 // 5,5,3 
        #if not self.check_suitset(5,5,3):
        #    return False
        
        mode = rr[3]
        if mode==355:
            t1=rr[0]-2
            t2=rr[1]-4
            t3=rr[2]-4
        elif mode==535:
            t2=rr[0]-4
            t1=rr[1]-2
            t3=rr[2]-4
        elif mode==553:
            t2=rr[0]-4
            t3=rr[1]-4
            t1=rr[2]-2
        #print(t1,t2,t3)
        ss1= self.has_samesuit(t1,3) 
        ss2= self.has_samesuit(t2,5) 
        ss3= self.has_samesuit(t3,5)
        #print(ss1,ss2,ss3)
        
        return ss1 and ss2 and ss3
    
    # chk for  3,5,5 //  5,3,5 //  5,5,3 
    # return index & mode #
    def has_3straight(self):
        ranks = self.numhist.copy()
        ranks[1] = ranks.get(14, 0) #把 A 調到前面當 1
        
        
        for hh in range(1, 11):
            count = 0
            count2 = 0
            count3 =0
            jj=hh
            kk=hh
            #print('round ', hh, ranks)
            r1 = ranks.copy()
            for i in range(hh,15):
                gg= r1.get(i,0)
                if gg>0:
                    r1[i]=gg-1
                    if i==1:
                        r1[14]=r1[1]
                    count += 1  #得順往前
                    if r1[i]==0: #下一條順從下個號碼才可能有
                        jj +=1
                        kk +=1
                    #print(r1,i,jj, kk, count)
                    #input('www \n')
                        
                    if count == 3: #得第一個順
                        for j in range(jj,15):
                            if r1.get(j, 0):
                                r1[j]=r1[j]-1 #用掉一個
                                count2 += 1  #得順往前
                                if r1[j]==0: #下一條順從下個號碼才可能有
                                    kk+=1
                                #print(r1, i, j, kk, count2)
                                #input('www2')
                                
                                if count2 == 5: #得第二個順
                                    for k in range(kk,15):
                                        if r1.get(k, 0):
                                            r1[k]=r1[k]-1 #用掉一個
                                            count3 += 1
                                            #print(r1, i, j, k,  count3)
                                            #input('www3')
                                            
                                            if count3 == 5:
                                                #哪三條順：i,j,k
                                                print('三順子：',i,j,k, 355)
                                                return [i,j,k, 355]
                                        else:
                                            count3 = 0
                            else:
                                count2 = 0                                    
                else:
                    
                    count=0 #reset straight counter    
            #failed one round of seek 3,5,5 goto next num and start new round
        for hh in range(1, 11):
            count = 0
            count2 = 0
            count3 =0
            jj=hh
            kk=hh
            #print('round ', hh, ranks)
            r1 = ranks.copy()
            for i in range(hh,15):
                gg= r1.get(i,0)
                if gg>0:
                    r1[i]=gg-1
                    if i==1:
                        r1[14]=r1[1]
                    count += 1  #得順往前
                    if r1[i]==0: #下一條順從下個號碼才可能有
                        jj +=1
                        kk +=1
                    #print(r1,i,jj, kk, count)
                    #input('www \n')
                        
                    if count == 5: #得第一個順
                        for j in range(jj,15):
                            if r1.get(j, 0):
                                r1[j]=r1[j]-1 #用掉一個
                                count2 += 1  #得順往前
                                if r1[j]==0: #下一條順從下個號碼才可能有
                                    kk+=1
                                #print(r1, i, j, kk, count2)
                                #input('www2')
                                
                                if count2 == 3: #得第二個順
                                    for k in range(kk,15):
                                        if r1.get(k, 0):
                                            r1[k]=r1[k]-1 #用掉一個
                                            count3 += 1
                                            #print(r1, i, j, k,  count3)
                                            #input('www3')
                                            
                                            if count3 == 5:
                                                #哪三條順：i,j,k
                                                print('三順子：',i,j,k, 535)
                                                return [i,j,k, 535]
                                        else:
                                            count3 = 0
                            else:
                                count2 = 0                                    
                else:
                    
                    count=0 #reset straight counter    
            
        for hh in range(1, 11):
            count = 0
            count2 = 0
            count3 =0
            jj=hh
            kk=hh
            #print('round ', hh, ranks)
            r1 = ranks.copy()
            for i in range(hh,15):
                gg= r1.get(i,0)
                if gg>0:
                    r1[i]=gg-1
                    if i==1:
                        r1[14]=r1[1]
                    count += 1  #得順往前
                    if r1[i]==0: #下一條順從下個號碼才可能有
                        jj +=1
                        kk +=1
                    #print(r1,i,jj, kk, count)
                    #input('www \n')
                        
                    if count == 5: #得第一個順
                        for j in range(jj,15):
                            if r1.get(j, 0):
                                r1[j]=r1[j]-1 #用掉一個
                                count2 += 1  #得順往前
                                if r1[j]==0: #下一條順從下個號碼才可能有
                                    kk+=1
                                #print(r1, i, j, kk, count2)
                                #input('www2')
                                
                                if count2 == 5: #得第二個順
                                    for k in range(kk,15):
                                        if r1.get(k, 0):
                                            r1[k]=r1[k]-1 #用掉一個
                                            count3 += 1
                                            #print(r1, i, j, k,  count3)
                                            #input('www3')
                                            
                                            if count3 == 3:
                                                #哪三條順：i,j,k
                                                print('三順子：',i,j,k, 553)
                                                return [i,j,k, 553]
                                        else:
                                            count3 = 0
                            else:
                                count2 = 0                                    
                else:
                    
                    count=0 #reset straight counter    
            
    
        return False
    
  
#initiate with list of string  ['♡3', '♢Q', '♠10', '♡6', '♣10', '♣K', '♡J', '♣J', '♡K', '♣2', '♠3', '♣4', '♣A'] 
# convert into a Hand13 object
class Player(object):
    def __init__(self, name, hh):
        self.name = name
        self.hand = Hand13(hh)
        self.res = [0,0,0,0,0] #top mid bot total gun

        
    def sayHello(self):
        print ('\nHi! 我是 {}'.format(self.name))
        return self

    def giveCards(self, hh):
        self.hand = Hand13(hh)
        self.res = [0,0,0,0,0]
        
    # Draw n number of cards from a deck
    # Returns true in n cards are drawn, false if less then that
    def draw(self, deck, num=1):
        for _ in range(num):
            card = deck.deal()
            if card:
                self.hand.append(card)
            else: 
                return False
        return True

    def showhand(self):
        s = self.hand.show()
        print('我的牌是: ', s, '\n')
        
    # Display all the cards in the players hand
    def show2(self):
        print ("{}'s hand: {}".format(self.name, self.hand))
        return self

    def discard(self):
        return self.hand.pop()
    
    def arrange13(self):
        return self.hand.arrange13()


  
class Game(object):
    def __init__(self,name="Game", location="Home", players=['Ian','Gary','Jack','Glory'], no_of_games=1):
        self.name = name
        self.location = location
        self.gametime = datetime.now()
        self.duration = 90
        self.no_of_games = no_of_games
        self.players =  [Player(players[0], sample2),Player(players[1],sample1),
                    Player(players[2], sample45), Player(players[3], sample3)]
        self.gamescore= []    
    
    def startgame(self):
        print("牌局名稱：", self.name)
        print("地點：", self.location)
        now = datetime.now()
        dt_string = now.strftime("%Y.%m.%d")
        print("日期：", dt_string)        
            
        print("牌局時間：", self.duration, "分鐘")
        print("局數：", self.no_of_games)
        
        self.gamescore = []
        for j in range(self.no_of_games):
            gs=self.OnePlay(j)
            self.gamescore.append(gs)
        
        c= np.array(self.gamescore,dtype='i')
        print('\n',c, '\n')
        self.finalscore = c.sum(axis=0)
        for i in range(4):
            print(self.players[i].name, ' 總分：', self.finalscore[i])
        
    def OnePlay(self, j):
        now = datetime.now()
        dt_string = now.strftime("%H:%M:%S")
        print('-'*100)
        print("局次：", j+1)
        print("時間：", dt_string)        
        
        myDeck = Deck()
        hands = myDeck.distribute()
        for i in range(4):
            self.players[i].giveCards(hands[i])
        #self.players =  [ Player(players[0], hands[0]),
        #                  Player(players[1]),hands[1]),
        #                  Player(players[2], hands[2]),
        #                  Player(players[3], hands[3])]
        
        #排牌
        for i in self.players:
            i.sayHello()
            i.showhand()
            i.arrange13()
            i.hand.show_hand_details()  
        print('\n')
        
        gamescore = self.gamecompete()
        return gamescore
            
        
    def splevel(self, h):
        ht = h.handtype_val
        if ht>=1000:
            return 'sp5'
        elif ht>=900:
            return 'sp4'
        elif ht>=800:
            return 'sp3'
        elif ht>=700:
            return 'sp2'
        elif ht>=500:
            return 'sp1'
        else:
            return 'sp0'
        return 'sp0'
            
    def gamecompete(self):
        #比牌
        comb = itertools.combinations(self.players, 2) #4人抓對廝殺的組合
        res=[0,0,0,0,0]
        gun=[] #create a list of [winner, loser, result]
        for i in comb: #每種組合兩兩廝殺
            res = self.compete(i[0].hand,i[1].hand)
            if res[3]>=0:
                gun.append( [i[0].name, i[1].name, res])
            elif res[3]<0:
                gun.append( [i[1].name, i[0].name, list(map(lambda x: -x, res))])
        
        #轉播戰況
        for i in gun:
            res = i[2]  # the res array here
            if res[4]>0:
                print(i[0], '打槍', i[1], res[0:3], '=', res[3])
            elif res[4]<0:
                print(i[1], '打槍', i[0], res[0:3], '=', res[3])
            elif res[3]>0:
                print(i[0], '勝', i[1], res[0:3], '=', res[3])
            elif res[3]<0:
                print(i[0], '勝', i[1], res[0:3], '=', res[3])
            else:
                print(i[0], '平手', i[1], res[0:3], '=', res[3])
        
        #check for 打槍兩家＆全壘打   
        for i in self.players:
            #locate list of each players as winner
            tt=[item for item in gun if item[0] ==i.name ]
            no_of_gun=0
            for x in tt:
                if x[2][4]==1: #打槍
                    no_of_gun+=1
            mul = 2 if no_of_gun==3 else (1.5 if no_of_gun==2 else 1)
            if no_of_gun==3:
                print(i.name, '全壘打！！')
            elif no_of_gun==2:
                print(i.name, '打兩家！！')
            for ww in tt:
                #winner = myself
                mul2 = mul if ww[2][4]==1 else 1 #only mul for gun shot ones

                for j in range(4):
                    i.res[j]= i.res[j]+ww[2][j] * mul2
                #不能用單行寫 會影響紀錄打槍的 res[4] 
                #losers
                #find the loser by name
                ll = [item for item in self.players if item.name==ww[1] ]
                for j in range(4):
                    ll[0].res[j]= ll[0].res[j] - ww[2][j] * mul2
                    
            #for k in self.players:
             #   print(k.name, k.res)
        #現在先簡單紀錄一列最後分數
        gamescore = [ i.res[3] for i in self.players]
        resstr = [(i.name, i.res[3]) for i in self.players]
        print('\n本局比分：', resstr)
        return gamescore
    
    def compete(self, h1, h2):
        res=[0,0,0,0,0] #4th = score, 5th = gun

        if h1.specialhand!='normal':
            if h2.specialhand!='normal':         #兩人報到 等級不同要比強弱
                s1= specialcharge[self.splevel(h1)]
                s2= specialcharge[self.splevel(h2)]
                res[3] = s1 if s1>s2 else (-s2 if s1<s2 else 0)
            else:
                res[3] = specialcharge[self.splevel(h1)] 
            return res
        elif h2.specialhand!='normal':
            res[3] = -specialcharge[self.splevel(h2)] 
            return res


        # 原子頭、中敦葫、中敦鐵、中敦柳、尾敦鐵、尾敦柳、小柳、大柳
        # 打兩家 *1.5, 全壘打 *2
        for i in range(0,3):
            res[i]= 1 if (h1.ss[i] >h2.ss[i]) else (-1 if h1.ss[i]<h2.ss[i] else 0)
            
        #碾壓規則: 兩敦贏一敦平手
        if sorted(res[0:3])==[0,1,1]:
            res[i]=[1,1,1,3,1]
        tot=sum(res)  #要先加原始分數
        #original score 全贏 = 打槍
        mul = 2 if (tot==3 or tot==-3) else 1 
        #打槍或被打槍的標誌
        res[4]= 1 if tot==3 else (-1 if tot==-3 else 0) #打槍或被打槍的標誌
        
        #print(h1.htop.handtype, h1.htop.p[0], h2.htop.handtype)
        i=0
        if h1.htop.handtype=='three of a kind' or h2.htop.handtype=='three of a kind':
            p_whowin = h1.htop.p[0] if res[i]>0 else h2.htop.p[0]
            res[i]=res[i]*(6 if p_whowin==3 else 3)
        
        i=1 #中敦
        if h1.hmid.handtype=='full house' or h2.hmid.handtype=='full house':
            res[i]= res[i]*2
        elif h1.hmid.handtype=='four of a kind' or h2.hmid.handtype=='four of a kind':
            p_whowin=h1.hmid.p[0] if res[i]>0 else h2.hmid.p[0]
            res[i]= res[i]*(16 if p_whowin==4 else 8)
        elif h1.hmid.handtype=='straight flush' or h2.hmid.handtype=='straight flush':
            res[i]= res[i]*10
        elif h1.hmid.handtype=='同花次大順' or h2.hmid.handtype=='同花次大順':
            res[i]= res[i]*12
        elif h1.hmid.handtype=='royal flush' or h2.hmid.handtype=='royal flush':
            res[i]= res[i]*14
        
        i=2 #尾敦
        if h1.hbot.handtype=='four of a kind' or h2.hbot.handtype=='four of a kind':
            p_whowin=h1.hbot.p[0] if res[i]>0 else h2.hbot.p[0]
            res[i]= res[i]*(8 if p_whowin==4 else 4)
        elif h1.hbot.handtype=='straight flush' or h2.hbot.handtype=='straight flush':
            res[i]= res[i]*5
        elif h1.hbot.handtype=='同花次大順' or h2.hbot.handtype=='同花次大順':
            res[i]= res[i]*6
        elif h1.hbot.handtype=='royal flush' or h2.hbot.handtype=='royal flush':
            res[i]= res[i]*7
        
        # calc sum of 3 level score
        res[3]=sum(res[0:3])
        for i in range(len(res)-1):
            res[i]=res[i]*mul

        #print(res)     
        return res
            
            
            


##################### Main ############################

specialcharge = { 'sp0':0, 'sp1': 6, 'sp2':18, 'sp3': 36, 'sp4':40, 'sp5':100 }


#sys.exit()

pp = {'gary':[1,2,3], 'jack':[4,5,6], 'ian':[7,8,9], 'glory':[1,4,2]}
#print(pp['jack'])


s0 = [ ('A','B'), ('C','B'), ('B','D'),('C','A'),('A','D'),('C','D')]
#tt=[item for item in s0 if item[0] =='A']
#if len(tt)==2:
    

ss=['03C', '03H', '14S']
s2 = [Card('C',5), Card('H',9),Card('S',7)]
s5=['12C', '10S', '13S', '14C', '11D']
s6=['02C', '03S', '05S', '04C', '14D']

sample1=['10H', '12S', '11D', '09S', '07C', '14D', '14S', '08H', '03C', '09D', '03S', '06D', '14H']
sample2= ['02C', '02D', '02H', '11S', '03C', '03D', '03H', '11C', '04C', '04D', '04H', '04S', '05C'] 
sample3=['03D', '09C', '09D', '09H', '09S', '05S', '07S', '08D', '12D', '12S', '13D', '13H', '13S'] 
#單三條
sample49=['03D', '03C', '03S', '05H', '06S', '08S', '07D', '04S', '02D', '11S', '13D', '10H', '14S'] 
#四套三條
sample53=['03D', '03C', '03S', '05H', '05S', '08S', '08D', '05S', '02D', '08H', '02C', '02S', '14S'] 
#三套四條
sample54=['03D', '03C', '03S', '05H', '08C', '08S', '08D', '03H', '02D', '08H', '02C', '02S', '02H']         
#單pair
sample51=['03D', '03C', '09S', '11D', '06S', '08S', '07S', '04C', '02C', '05H', '12D', '13H', '14D'] 
#雙pair無花無順
sample52=['03D', '03C', '09S', '11D', '06S', '08C', '07S', '04C', '04S', '02H', '12D', '13H', '14D'] 
#三順子
sample70=['06D', '11C', '07S', '08D', '04S', '04H', '03S', '05C', '06S', '02H', '12D', '13H', '05D'] 
#三同花順
sample73=['03D', '14C', '07S', '11C', '04S', '10C', '03S', '14D', '06S', '02D', '12C', '13C', '05S'] 
        
#一條龍
sample4=['03D', '04C', '02D', '05H', '06S', '08S', '07S', '09D', '12D', '11S', '13D', '10H', '14S'] 
#清龍
sample42=['03D', '04D', '02D', '05D', '06D', '08D', '07D', '09D', '12D', '11D', '13D', '10D', '14D'] 
#全紅
sample43=['09D', '04D', '02H', '05H', '06D', '08D', '07H', '09D', '12D', '11D', '13D', '10D', '14D'] 
#全黑
sample44=['09S', '04S', '02S', '05S', '06S', '08S', '07S', '09S', '12S', '11S', '13S', '10H', '14S'] 
#全黑一張紅
sample45=['09S', '04S', '02S', '06C', '06S', '07C', '07S', '09D', '12S', '11S', '13S', '10S', '14S'] 
#全黑一點紅
sample46=['09S', '04S', '02S', '06C', '06S', '07C', '07S', '09C', '12S', '11S', '13S', '10S', '14H'] 
#全紅一張黑
sample71=['09D', '04D', '02H', '05H', '06D', '08D', '07H', '09S', '12D', '11D', '13D', '10D', '14D'] 
#全紅一點黑
sample72=['09D', '04D', '02H', '05H', '06D', '08D', '07H', '09H', '12D', '11D', '13D', '10D', '14S'] 
        
#六對半
sample47=['09S', '04S', '02S', '05C', '09C', '04C', '02D', '05D', '12S', '11S', '12D', '11H', '14D'] 
#六對半帶葫蘆
sample53=['09S', '04S', '02S', '05C', '09C', '04C', '02D', '05D', '12S', '11S', '12D', '11H', '12C'] 

#十二皇族
sample48=['11S', '12D', '13S', '11C', '12C', '14C', '14S', '13C', '11D', '12S', '13D', '13H', '14H'] 
#大全大
sample60=['11S', '12D', '08S', '09C', '12C', '14C', '10S', '13C', '11D', '12S', '08D', '13H', '14H'] 
#失敗全大1 
sample61=['11S', '05D', '08S', '09C', '12C', '14C', '10S', '13C', '11D', '12S', '08D', '13H', '14H'] 
#成功全大1 
sample62=['11S', '05D', '08S', '09C', '12C', '11C', '10S', '13C', '11D', '12S', '08D', '13H', '06H'] 
#全大2
sample63=['11S', '06D', '08S', '09C', '12C', '14C', '10S', '13C', '11D', '12S', '08D', '13H', '14H'] 
#失敗全大2
sample64=['11S', '06D', '08S', '09C', '12C', '14C', '10S', '13C', '11D', '12S', '08D', '05H', '14H'] 

#大全小
sample65=['14S', '02D', '03S', '04C', '05C', '07C', '06S', '03C', '08D', '08S', '06D', '02H', '06H'] 
#全小
sample66=['14S', '02D', '03S', '04C', '05C', '07C', '06S', '03C', '09D', '08S', '06D', '02H', '06H'] 
#失敗全小
sample67=['14S', '02D', '03S', '10C', '05C', '07C', '06S', '03C', '09D', '08S', '06D', '02H', '06H'] 
#全小2
sample68=['10S', '02D', '03S', '04C', '05C', '07C', '06S', '03C', '09D', '08S', '06D', '02H', '06H'] 
#失敗全小2
sample69=['10S', '14D', '03S', '04C', '05C', '07C', '06S', '03C', '09D', '08S', '06D', '02H', '06H'] 
        
#三同花
sample50=['11S', '02D', '03S', '05S', '06D', '09D', '14S', '13C', '11D', '08H', '13D', '13H', '14H'] 
 
#這是沒排好的 sample       
#[ ♢2 ♣6 ♠6 ♡6 ♢7 ♡10 ♣J ♠J ♡Q ♠K ♣A ♢A ♠A ] 

gg= Game('九月第一場','台北浪漫一生',['Glory','Jack','Ian','Gary'],3)
gg.startgame()

#['♠5', '♠7', '♢8'] , 分數： 8.08
#['♢Q', '♠Q', '♢K', '♡K', '♠K'] , 分數： 103.00
#['♢3', '♣4', '♢4', '♡4', '♠4'] , 分數： 109.00
#h1=Hand3(ss)
#print(h1.show())
#print(h1.has_pair())
#h2=Hand5(s6)
#print(h2.score_hand())
#print(h2.show())
#print(h2.has_pair())
#print(h2.has_twopair())
#sys.exit()
#print(s2)
#print(sorted(s2))
#hh = Hand13(sample1)
#print(hh.show())
#print(hh.has_straight())
#hh.arrange13()
#s = hh.show()
#print('我的牌是: ', s, '\n')
#print(hh.show())

#h1.arrange13()
#h1.show_hand_details()

#print(str(type(ss))=="<class 'list'>")
#hh = Hand5(s5)
#print(hh.hand_dscp())


