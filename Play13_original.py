#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 29 18:36:01 2021

@author: gary
"""
import sys
import random
import numpy as np
import pandas as pd
import itertools
from itertools import product
import more_itertools
import math

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
        
    # A=14, and suit first
    def show(self):
        suits = {"H":"♡", "S":"♠", "D":"♢", "C":"♣"}
        values = {**{i:str(i) for i in range(2,11)}, 
                 **{ 11:'J',12:'Q', 13:'K', 14:'A'}}
        return suits[self.suit]+values[self.value]
    
    def letter(self):
        return(self.value)
    
    def suit(self):
        return(self.suit)
    
    def isBlack():
        return self.suit == "C" or self.suit=="S"
    
    def isRed():
        return self.suit == "D" or self.suit=="H"

class Deck(object):
    def __init__(self):
        self.cards = []
        self.build()

    # Display all cards in the deck
    def show(self):
        i=0
        for card in self.cards:
            i+=1
            print (card.show())
            if i%13==0 :
                print ('\n')

    # Generate 52 cards
    def build(self):
        self.cards = []
        numbers=list(range(2,15))
        suits = ['C','D','H','S']
        deck = []
        for i in numbers:
            for s in suits:
                #card = "{:0>2d}".format(i)+s
                self.cards.append(Card(suit, i))
    
        #for suit in ['C', 'D', 'H', 'S']:
        #    for val in range(1,14):
        #        self.cards.append(Card(suit, val))

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

    # Return the top card
    def deal(self):
        return self.cards.pop() #取出list最後一個元素並且移除
    
class Player(object):
    def __init__(self, name, hand=[]):
        self.name = name
        self.hand = hand

    def sayHello(self):
        print ('Hi! My name is {}'.format(self.name))
        return self

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

    # Display all the cards in the players hand
    def showHand(self):
        print ("{}'s hand: {}".format(self.name, self.hand))
        return self

    def discard(self):
        return self.hand.pop()

#object for a general hand of cards
class Hand(object):
    def __init__(self,hand):
        self.hand = sorted(hand)
        self.handsize = len(hand)
        self.letters = [hand[i].letter() for i in range(self.handsize)]
        self.numbers = [hand[i].number() for i in range(self.handsize)]
        self.rnum = [ self.numbers.count(i) for i in self.numbers]
        self.rlet = [ self.letters.count(i) for i in self.letters]
        self.dif = max(self.numbers) - min(self.numbers)

    def show(self):
        s = [ i.show() for i in self.hand ]
        #s = [ showcard(i[2:], int(i[:2])) for i in hand] 
        return(s)
    
    def isAllBlack(self):
        bb = [ i.isBlack() for i in self.hand ]
        return(all(bb))
    
    def isAllRed(self):
        rr = [ i.isRed() for i in self.hand ]
        return(all(rr))
    
    
#專屬13支一手牌的object
class Hand13(object):
    def __init__(self, hand):
        self.hand = hand
        self.htop = hand[0]
        self.hmid = hand[1]
        self.hbot = hand[2]
        self.specialhand = chk_special()
    
    def show(): #there's 3 list in hand
    for hh in self.hand:
        ss=[]
        s = [ i.show() for i in hh] 
        ss.append(s)
        return(ss)
    
    def specialhand():
        return('ok')
        
    

########################################
    
#out list of string
def build_deck():
    numbers=list(range(2,15))
    suits = ['C','D','H','S']
    deck = []
    for i in numbers:
        for s in suits:
            card = "{:0>2d}".format(i)+s
            deck.append(card)
    return deck
        
def suffle_deck(deck):
    random.shuffle(deck)
    return deck
    
def distribute_deck(deck): #return an array of 4 x 13
    phands = [deck[:13],deck[13:26], deck[26:39], deck[39:]]
    return phands

def showcard(suit, value):
    suits = {"H":"♡", "S":"♠", "D":"♢", "C":"♣"}
    values = {**{i:str(i) for i in range(2,11)}, 
    **{ 11:'J',12:'Q', 13:'K', 14:'A'}}
    #print(values[self.value]+suits[self.suit])
    return (suits[suit]+values[value])

def convert_cardnum(value):
    values = {**{i:str(i) for i in range(2,11)}, 
    **{ 11:'J',12:'Q', 13:'K', 14:'A'}}
    
    return(values[value]) 
    
def showhand(hand):
    #s=[]
    hand = sorted(hand)
    s = [ showcard(i[2:], int(i[:2])) for i in hand] 
    #for i in hand:
       #print(i[:2], i[2:])
       #ss =showcard('H',14)
    #   ss = showcard( i[2:], int(i[:2])) # get the suit & number for each card in the hand
    #   s.append(ss)
    return(s)

def showhand13(hand): #there's 3 list in hand
    #htop = hand[0]
    #hmid = hand[1]
    #hbot = hand[2]
    #print(hand)
    #input('wait')
    ss = []
    for hh in hand:
        s = [ showcard(i[2:], int(i[:2])) for i in hh] 
        ss.append(s)
    #for i in hand:
       #print(i[:2], i[2:])
       #ss =showcard('H',14)
    #   ss = showcard( i[2:], int(i[:2])) # get the suit & number for each card in the hand
    #   s.append(ss)
    return(ss)
    
def combinations(arr, n):
    arr = np.asarray(arr)
    t = np.dtype([('', arr.dtype)]*n)
    result = np.fromiter(itertools.combinations(arr, n), t)
    return result.view(arr.dtype).reshape(-1, n)

def check_four_of_a_kind(hand,letters,numbers,rnum,rlet):
    for i in numbers:
            if numbers.count(i) == 4:
                four = i
            elif numbers.count(i) == 1:
                card = i
    score = 105 + four # + card/100 ＃也不必看第五張牌
    return score

def check_full_house(hand,letters,numbers,rnum,rlet):
    for i in numbers:
        if numbers.count(i) == 3:
            full = i
        elif numbers.count(i) == 2:
            p = i
    score = 90 + full  # +  p/100  full house won't need to differentiate the pair card
    return score

def check_three_of_a_kind(hand,letters,numbers,rnum,rlet):
    cards = []
    for i in numbers:
        if numbers.count(i) == 3:
            three = i   #是哪個號碼的三條
        else: 
            cards.append(i) #剩下哪兩張牌
    #print('cards',cards) 
    score = 45 + three + max(cards)/100 +min(cards)/1000
    #print(hand, 'score :',score)
    return score

def check_three_of_a_kind2(hand,letters,numbers,rnum,rlet):
    cards = []
    for i in numbers:
        if numbers.count(i) == 3:
            three = i
        else: 
            cards.append(i)
    score = 45 + three # theres no 4th cards + max(cards)/100 +min(cards)/1000
    return score

def check_three_of_a_kind22(hand,letters,numbers,rnum,rlet):
    cards = []
    for i in numbers:
        if numbers.count(i) == 3:
            three = i
        else: 
            cards.append(i)
    score = 120 + three # theres no 4th cards + max(cards)/100 +min(cards)/1000
    return score

def check_two_pair(hand,letters,numbers,rnum,rlet):
    pairs = []
    cards = []
    for i in numbers:
        if numbers.count(i) == 2:
            pairs.append(i)
        elif numbers.count(i) == 1:
            cards.append(i)
            cards = sorted(cards,reverse=True)
    score = 30 + max(pairs) + min(pairs)/100 + cards[0]/1000
    return score

def check_pair(hand,letters,numbers,rnum,rlet):    
    pair = []
    cards  = []
    for i in numbers:
        if numbers.count(i) == 2:
            pair.append(i)
        elif numbers.count(i) == 1:    
            cards.append(i)
            cards = sorted(cards,reverse=True)
    score = 15 + pair[0] + cards[0]/100 + cards[1]/1000 + cards[2]/10000
    return score

def check_pair2(hand,letters,numbers,rnum,rlet):    
    pair = []
    cards  = []
    for i in numbers:
        if numbers.count(i) == 2:
            pair.append(i)
        elif numbers.count(i) == 1:    
            cards.append(i)
            cards = sorted(cards,reverse=True)
    score = 15 + pair[0] + cards[0]/100 #+ cards[1]/1000 + cards[2]/10000
    return score

#check pair for 3 cards
# score 27 - 63
def check_pair22(hand,letters,numbers,rnum,rlet):    
    pair = []
    cards  = []
    for i in numbers:
        if numbers.count(i) == 2:
            pair.append(i)
        elif numbers.count(i) == 1:    
            cards.append(i)
            cards = sorted(cards,reverse=True)
    score = 27 + (pair[0]-2)*3 + cards[0]/100 #+ cards[1]/1000 + cards[2]/10000
    return score

"""
#135 同花大順 - 10000
#120 同花順 - 999987 - 999998
#105 鐵支 - 9997 - 999986
#90 葫蘆 - 9983 - 9997
#75 同花 - 9963-9983
#65 順 - 9940-9963
#45 三條 - 9717-9936
#30 兩對 - 9242-9716
#15 一對 - 5017-9241, 每格差 3.35%
#2..14 亂- 5016
#royal flush = 0.000154%
#straight flush = 0.00139%
#four of a kind = 0.024%
#full house = 0.1441%
#flush = 0.1965%
#straight = 0.3925%
#three of a kind = 2.1118%
#two pair = 4.7539%
#pair = 42.2569%
#high card= 50.1177%
"""

def score_hand(hand):
    
    #letters = [hand[i][:1] for i in range(5)] # We get the suit for each card in the hand
    #numbers = [int(hand[i][1:]) for i in range(5)]  # We get the number for each card in the hand
    letters = [hand[i][2:] for i in range(5)] # We get the suit for each card in the hand
    numbers = [int(hand[i][:2]) for i in range(5)]  # We get the number for each card in the hand
    
    rnum = [numbers.count(i) for i in numbers]  # We count repetitions for each number
    rlet = [letters.count(i) for i in letters]  # We count repetitions for each letter
    dif = max(numbers) - min(numbers) # The difference between the greater and smaller number in the hand
    handtype = ''
    score = 0
    if 5 in rlet: #花色數目=5=同花
        if numbers ==[14,13,12,11,10]: #why already sorted?
            handtype = 'royal_flush'
            score = 135
            #print('this hand is a %s:, with score: %s' % (handtype,score)) 
        elif dif == 4 and max(rnum) == 1: #大小只差4, 每個數字又只出現一次
            handtype = 'straight_flush'
            score = 120 + max(numbers)
            #print('this hand is a %s:, with score: %s' % (handtype,score)) 
        elif 4 in rnum:
            handtype == 'four of a kind'
            score = check_four_of_a_kind(hand,letters,numbers,rnum,rlet)
        # will these code ever gonna run ?? under the flush category
            print('BBBB!!! this hand is a %s:, with score: %s' % (handtype,score)) 
        elif sorted(rnum) == [2,2,3,3,3]:
            handtype == 'full house'
            score = check_full_house(hand,letters,numbers,rnum,rlet)
            print('BBBB !!! this hand is a %s:, with score: %s' % (handtype,score)) 
        elif 3 in rnum:
            handtype = 'three of a kind'
            score = check_three_of_a_kind(hand,letters,numbers,rnum,rlet)
            print('BBBB !!! this hand is a %s:, with score: %s' % (handtype,score)) 
        elif rnum.count(2) == 4:
            handtype = 'two pair'
            score = check_two_pair(hand,letters,numbers,rnum,rlet)
            print('BBBB !!! this hand is a %s:, with score: %s' % (handtype,score)) 
        elif rnum.count(2) == 2:
            handtype = 'pair'
            score = check_pair(hand,letters,numbers,rnum,rlet)
            print('BBBB !!! this hand is a %s:, with score: %s' % (handtype,score)) 
        else:
            handtype = 'flush'
            #score = 75 + max(numbers) #/100 ?? this is a big mistake
            n = sorted(numbers,reverse=True)
            score = 75+ n[0] + n[1]/100 + n[2]/1000 + n[3]/10000 + n[4]/100000
            #print('this hand is a %s:, with score: %s' % (handtype,score)) 
    elif 4 in rnum:
        handtype = 'four of a kind'
        score = check_four_of_a_kind(hand,letters,numbers,rnum,rlet)
        #print('this hand is a %s:, with score: %s' % (handtype,score)) 
    elif sorted(rnum) == [2,2,3,3,3]:
       handtype = 'full house'
       score = check_full_house(hand,letters,numbers,rnum,rlet)
       #print('this hand is a %s:, with score: %s' % (handtype,score)) 
    elif 3 in rnum:
        handtype = 'three of a kind' 
        score = check_three_of_a_kind(hand,letters,numbers,rnum,rlet)
        #print('this hand is a %s:, with score: %s' % (handtype,score)) 
    elif rnum.count(2) == 4:
        handtype = 'two pair'
        score = check_two_pair(hand,letters,numbers,rnum,rlet)
        #print('this hand is a %s:, with score: %s' % (handtype,score)) 
    elif rnum.count(2) == 2:
        handtype = 'pair'
        score = check_pair(hand,letters,numbers,rnum,rlet)
        #print('this hand is a %s:, with score: %s' % (handtype,score)) 
    elif dif == 4:
        handtype = 'straight'
        score = 65 + max(numbers)
        #print('this hand is a %s:, with score: %s' % (handtype,score)) 

    else:
        handtype= 'high card'
        n = sorted(numbers,reverse=True)
        score = n[0] + n[1]/100 + n[2]/1000 + n[3]/10000 + n[4]/100000
        #print('this hand is a %s:, with score: %s' % (handtype,score)) 
    sss =[ score, handtype, handtype_val(handtype)] 
    return(sss)


def score_hand3(hand):
    #3張 除了特殊牌型外 沒有順沒有同花
    #只有 三條，一對，亂
    # percentile: 
        #三條:997602 - 997783
        #一對: '2'pair: 829276 - 985656 (985656 to 997602 for A pair)
        # 842308, 855339, 868371, 881403, 894434, 907466, 920466, 920498
        # 933529, 946561, 959593, 972624, 985656
        
        # 從 '2' pair 開始，每上一個號碼的 pair 增 percentile 1.3% from 82.93
        #亂：2851 to 828190 (234 to QKA)
    
    letters = [hand[i][2:] for i in range(3)] # We get the suit for each card in the hand
    numbers = [int(hand[i][:2]) for i in range(3)]  # We get the number for each card in the hand
    rnum = [numbers.count(i) for i in numbers]  # We count repetitions for each number
    rlet = [letters.count(i) for i in letters]  # We count repetitions for each letter
    dif = max(numbers) - min(numbers) # The difference between the greater and smaller number in the hand
    handtype = ''
    score = 0
    if 3 in rnum:
        handtype = 'three of a kind' 
        score = check_three_of_a_kind2(hand,letters,numbers,rnum,rlet)
        #print('this hand is a %s:, with score: %s' % (handtype,score)) 
    elif rnum.count(2) == 2:
        handtype = 'pair'
        score = check_pair2(hand,letters,numbers,rnum,rlet)
        #print('this hand is a %s:, with score: %s' % (handtype,score)) 
    elif dif == 2:
        handtype = 'high card' #staight in 3 cards
        #與 high card 算法一樣
        #score = 65 + max(numbers)
        n = sorted(numbers,reverse=True)
        score = n[0] + n[1]/100 + n[2]/1000
        
        #print('this hand is a %s:, with score: %s' % (handtype,score)) 
    else:
        handtype= 'high card'
        n = sorted(numbers,reverse=True)
        score = n[0] + n[1]/100 + n[2]/1000
        #print('this hand is a %s:, with score: %s' % (handtype,score)) 
    sss =[score,  handtype, handtype_val(handtype)]
    #print(sss)
    return(sss)

def score_hand32(hand):
    #3張 除了特殊牌型外 沒有順沒有同花
    #只有 三條，一對，亂
    # percentile: 
        #三條:997602 - 997783
        #一對: '2'pair: 829276 - 985656 (985656 to 997602 for A pair)
        # 842308, 855339, 868371, 881403, 894434, 907466, 920466, 920498
        # 933529, 946561, 959593, 972624, 985656
        
        # 從 '2' pair 開始，每上一個號碼的 pair 增 percentile 1.3% from 82.93
        #亂：2851 to 828190 (234 to QKA)
    
    letters = [hand[i][2:] for i in range(3)] # We get the suit for each card in the hand
    numbers = [int(hand[i][:2]) for i in range(3)]  # We get the number for each card in the hand
    rnum = [numbers.count(i) for i in numbers]  # We count repetitions for each number
    rlet = [letters.count(i) for i in letters]  # We count repetitions for each letter
    dif = max(numbers) - min(numbers) # The difference between the greater and smaller number in the hand
    handtype = ''
    score = 0
    if 3 in rnum:
        handtype = 'three of a kind' 
        score = check_three_of_a_kind22(hand,letters,numbers,rnum,rlet)
        #print('this hand is a %s:, with score: %s' % (handtype,score)) 
    elif rnum.count(2) == 2:
        handtype = 'pair'
        score = check_pair22(hand,letters,numbers,rnum,rlet)
        #print('this hand is a %s:, with score: %s' % (handtype,score)) 
    elif dif == 2:
        handtype = 'high card' #staight in 3 cards
        #與 high card 算法一樣
        #score = 65 + max(numbers)
        n = sorted(numbers,reverse=True)
        score = n[0] + n[1]/100 + n[2]/1000
        
        #print('this hand is a %s:, with score: %s' % (handtype,score)) 
    else:
        handtype= 'high card'
        n = sorted(numbers,reverse=True)
        score = n[0] + n[1]/100 + n[2]/1000
        #print('this hand is a %s:, with score: %s' % (handtype,score)) 
    sss =[score,  handtype, handtype_val(handtype)]
    #print(sss)
    return(sss)

def handvalues(combi):
    #scores = dictionary of hand : value
    scores=[]
    tt=0
    #scores =[{"hand": i, "value": score_hand(i)[0]} for i in combi] # We iterate over all combinations scoring them
    for i in combi:
        shand =score_hand(i)
        scores.append({"hand": i, "value": shand[0], "handtype": shand[2] })
        #print(i, shand)
        #if tt==10:
        #    break
        tt+=1
    #print("done")
    scores = sorted(scores, key = lambda k: k['value'],reverse=True) # We sort hands by score
    return scores

def handvalues3(combi):
    #scores = dictionary of hand : value
    scores=[]
    #scores =[{"hand": i, "value": score_hand3(i)[0]} for i in combi] # We iterate over all combinations scoring them
    for i in combi:
        shand =score_hand3(i)
        scores.append({"hand": i, "value": shand[0], "handtype": shand[2] })
    
    #print("done")
    scores = sorted(scores, key = lambda k: k['value'],reverse=True) # We sort hands by score
    return scores



## break 13 cards into i, j, rest3
#13C3 = 286, 10C5 = 252, total = 286*252= 72072 
#13C5 = 1287 => 8C5 = 56, 1287*56 = 72072
# return N * [ [3] [5] [5] ]
def arr_allcomb13(hand):
    comb = itertools.combinations(sorted(hand), 3)
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
            #print (ii,jj, i, j, rest3)
            hh2.append(list(i))
            hh2.append(list(j))
            hh2.append(rest3)
            hh1.append(hh2)
        #print(hh2)        
    #print(len(hh1))
    return hh1

def handtype_val(handtype):
    hh = {"high card":0, "pair":1, "two pair":2, "three of a kind":3, "straight":4,"flush":5, "full house":6, "four of a kind":7, "straight_flush":8, "royal_flush":9}
    return (hh[handtype])

def getscore3(hand3,tab33):
    ll = tab33.loc[(tab33['hand'] == hand3)]
    return (ll.score.values[0])

def getscore5(hand5, tab55):
    ll = tab55.loc[(tab55['hand'] == hand5)]
    return (ll.score.values[0])

#資料檔牌的順序：號碼優先從小到大，同大則 CDHS 順序
#sorted 不能用 因為會先排字母
def arrange_str(cards):
    return sorted(cards)

def eval_attack(s1,s2,s3):
    return(s1*4+s2*2+s3)

def eval_defense(s1,s2,s3):
    return(s1*2+s2+s3)

def eval_CanAttack(s1,s2,s3):
    CanAttack = s1>=14.11 and s2>41 and s3>80 #218, but should be 3rows and stmt
    return(CanAttack)
    

def arrange13(hh): #return list of [3,5,5]
    #ahand = [hh[:3],hh[3:8],hh[8:13]] 
    allcomb = arr_allcomb13(hh)
    #tab33 = pd.read_csv('data13_3.csv')
    #tab55 = pd.read_csv('data13_5.csv')
    #print(len(allcomb))
    #score_arr=[0]*len(allcomb)
    ss_attack=0
    ss_defense=0
    tt=0
    valid_arrange=0
    bestscore_attack=[0,0] #the best score & the location index attack
    bestscore_defense=[0,0]
    for i in allcomb:
        tt+=1
        #print('\n combination ',tt)
        htop = i[0] #str(tuple(sorted(i[0])))
        hmid =i[1] #str(tuple(sorted(i[1])))
        hbot = i[2] #str(tuple(sorted(i[2])))
        #print(htop, hmid, hbot)
        
        s1=score_hand3(htop)
        s2=score_hand(hmid)
        s3=score_hand(hbot)
        
        #ss2=getscore5(str(tuple(sorted(hmid))),tab55) #score_hand(i[1])
        #s3=getscore5(hbot,tab55) #score_hand(i[2])
        
        if s1[0]>s2[0] or s1[0]>s3[0] or s2[0]>s3[0] : # score must be weak to strong
            ss=0
            #print("drop ", tt, "th combination")
        else:
            #s1 = score_hand32(htop)
            valid_arrange+=1
   #this is strength of the hand itself, not considering relationship with between 3 subset
   # and also the difference between 3 cards set & 5 cards set
            ss_attack=eval_attack(s1[0],s2[0],s3[0])
            ss_defense=eval_defense(s1[0],s2[0],s3[0])
            #ss1=getscore3(str(tuple(sorted(htop))),tab33) #score_hand3(i[0])
            #print(htop, hmid, hbot)
            
        if ss_attack>bestscore_attack[0] :    
            bestscore_attack[0] = ss_attack
            bestscore_attack[1] = tt-1
        
        if ss_defense>bestscore_defense[0]:
            bestscore_defense[0]=ss_defense
            bestscore_defense[1]= tt-1
            #print('\n best score now: ', bestscore[0], 'index at:', bestscore[1], ' total score = ',ss)
            #print(s1,i[0])
            #print(s2,i[1])
            #print(s3,i[2])            
            #print(s1[0]*4,s2[0]*2,s3[0], ' Total = ', bestscore[0])
            #input('press any key to continue')
        #if tt==50:
        #    break
        #score_arr[tt-1]=ss
        
    print('# of valid_arrangement :', valid_arrange)
    df = pd.DataFrame(allcomb,columns=['top', 'mid', 'bot'])
    df['score']=score_arr
    df =df[df['score'] !=0]
    print(df)
    df = df.sort_values(by='score', ascending=False)
    print(df.head(3))
    df.to_csv(r'handcombi.csv', header=None, index=None, sep=' ', mode='a')
    #sss =[{"hand": i, "value": score_arr(i)} for i in combi] # We iterate over all combinations scoring them
    print("done")
    #scores = sorted(scores, key = lambda k: k['value'],reverse=True) 
    #max_score=0
    #max_score = df['score'].idxmax
    #print(max_score)
    #ahand = list(df.iloc[max_score])
    i=allcomb[bestscore_attack[1]]
    htop = i[0] #str(tuple(sorted(i[0])))
    hmid =i[1] #str(tuple(sorted(i[1])))
    hbot = i[2] #str(tuple(sorted(i[2])))
        #print(htop, hmid, hbot)
        
    s1=score_hand3(htop)
    s2=score_hand(hmid)
    s3=score_hand(hbot)
    if eval_CanAttack(s1[0],s2[0],s3[0]):
        ahand = i
    else:
        ahand = allcomb[bestscore_defense[1]]
    #show_hand_details(i)
    #show_hand_details(allcomb[bestscore_defense[1]])
    #input('wait')
    return ahand

def show_hand_details(hand):
      htop = hand[0] #str(tuple(sorted(i[0])))
      hmid = hand[1] #str(tuple(sorted(i[1])))
      hbot = hand[2] #str(tuple(sorted(i[2])))
        
      #info in score_hand -- [score,  handtype, handtype_val(handtype)]
      s1=score_hand3(htop)
      s2=score_hand(hmid)
      s3=score_hand(hbot)
      ss=eval_attack(s1[0],s2[0],s3[0])
    
      print('My best arrangement : ', showhand13(hand), '\n')
      if eval_CanAttack(s1[0],s2[0],s3[0]):
          print('Hand: Attack, Score: ', ss,'\n')
      else:
          ss=eval_defense(s1[0],s2[0],s3[0])
          print('Hand: Defense, Score: ', "{:.2f}".format(ss),'\n')          
      print(hand_dscp3(htop))
      print(hand_dscp5(hmid))
      print(hand_dscp5(hbot))
      print(showhand(htop), ', 分數：', "{:.2f}".format(s1[0]))
      print(showhand(hmid), ', 分數：', "{:.2f}".format(s2[0]))
      print(showhand(hbot), ', 分數：', "{:.2f}".format(s3[0]))
      sss=''
      return(sss)
     
def hand_dscp3(rr):
    #print('rr =',rr)
    #input('wait')
    letters = [rr[i][2:] for i in range(3)] # We get the suit for each card in the hand
    numbers = [int(rr[i][:2]) for i in range(3)]  # We get the number for each card in the hand
    rnum = [numbers.count(i) for i in numbers]  # We count repetitions for each number
    rlet = [letters.count(i) for i in letters]  # We count repetitions for each letter
    dif = max(numbers) - min(numbers) # The difference between the greater and smaller number in the hand
    handtype = ''
    score = 0
    if 3 in rnum:
        handtype = 'three of a kind' 
        for i in numbers:
            if numbers.count(i) == 3:
                three = i
        sss=convert_cardnum(three) + ' 衝三'
    elif rnum.count(2) == 2:
        handtype = 'pair'
        score = check_pair2(rr,letters,numbers,rnum,rlet)
        sss = convert_cardnum((math.floor(score) - 15))+' Pair'
        
    elif dif == 2:
        handtype = 'high card' #staight in 3 cards
        #與 high card 算法一樣
        #score = 65 + max(numbers)
        n = sorted(numbers,reverse=True)
        score = n[0] + n[1]/100 + n[2]/1000
        sss = '亂 ['+convert_cardnum(n[0])+' '+convert_cardnum(n[1])+' '+convert_cardnum(n[2])+']'
        
    else:
        handtype= 'high card'
        n = sorted(numbers,reverse=True)
        score = n[0] + n[1]/100 + n[2]/1000
        sss = '亂 ['+convert_cardnum(n[0])+' '+convert_cardnum(n[1])+' '+convert_cardnum(n[2])+']'
        
    return(sss)

def hand_dscp5(rr):
    letters = [rr[i][2:] for i in range(5)] # We get the suit for each card in the hand
    numbers = [int(rr[i][:2]) for i in range(5)]  # We get the number for each card in the hand
    rnum = [numbers.count(i) for i in numbers]  # We count repetitions for each number
    rlet = [letters.count(i) for i in letters]  # We count repetitions for each letter
    dif = max(numbers) - min(numbers) # The difference between the greater and smaller number in the hand
    handtype = ''
    score = 0
    sss = ''
    if 5 in rlet: #花色數目=5=同花
        if numbers ==[14,13,12,11,10]: #why already sorted?
            handtype = 'royal_flush'
            #score = 135
            sss = '同花大順'
        elif dif == 4 and max(rnum) == 1: #大小只差4, 每個數字又只出現一次
            handtype = 'straight_flush'
            #score = 120 + max(numbers)
            sss = str(max(numbers)-4)+' 同花順'
        else:
            handtype = 'flush'
            #score = 75 + max(numbers) #/100 ?? this is a big mistake
            n = sorted(numbers,reverse=True)
            score = 75+ n[0] + n[1]/100 + n[2]/1000 + n[3]/10000 + n[4]/100000
            sss = '同花 ['+convert_cardnum(n[0])+' '+convert_cardnum(n[1])+' '+convert_cardnum(n[2])+' '+convert_cardnum(n[3])+' '+convert_cardnum(n[4])+']'
    elif 4 in rnum:
        handtype = 'four of a kind'
        for i in numbers:
            if numbers.count(i) == 4:
                four = i
        sss= convert_cardnum(four)+' 鐵支'
       
    elif sorted(rnum) == [2,2,3,3,3]:
       handtype = 'full house'
       for i in numbers:
        if numbers.count(i) == 3:
            full = i
        #elif numbers.count(i) == 2:
        #    p = i
       sss = convert_cardnum(full)+' 葫蘆'
    elif 3 in rnum:
        handtype = 'three of a kind' 
        #score = check_three_of_a_kind(hand,letters,numbers,rnum,rlet)
        for i in numbers:
            if numbers.count(i) == 3:
                three = i
        
        sss=convert_cardnum(three)+' 三條'
        
    elif rnum.count(2) == 4:
        handtype = 'two pair'
        #score = check_two_pair(hand,letters,numbers,rnum,rlet)
        pairs = []
        cards = []
        for i in numbers:
            if numbers.count(i) == 2:
                pairs.append(i)
            elif numbers.count(i) == 1:
                cards.append(i)
                cards = sorted(cards,reverse=True)
        score = 30 + max(pairs) + min(pairs)/100 + cards[0]/1000
        sss=convert_cardnum(max(pairs))+'/'+ convert_cardnum(min(pairs))+' Pair'
    elif rnum.count(2) == 2:
        handtype = 'pair'
        score = check_pair(rr,letters,numbers,rnum,rlet)
        sss = convert_cardnum(math.floor(score) - 15)+' Pair'
        
    elif dif == 4:
        handtype = 'straight'
        #score = 65 + max(numbers)
        sss = str(max(numbers)-4)+' 順'

    else:
        handtype= 'high card'
        n = sorted(numbers,reverse=True)
        #score = n[0] + n[1]/100 + n[2]/1000 + n[3]/10000 + n[4]/100000
        sss = '亂 '+convert_cardnum(n[0])+' '+convert_cardnum(n[1])+' '+convert_cardnum(n[2])+' '+convert_cardnum(n[3])+' '+convert_cardnum(n[4])+']'
        #print('this hand is a %s:, with score: %s' % (handtype,score)) 
     
    return(sss)
   
def Compete_hands(hands):
    #comb = itertools.combinations(hands, 2)
    #for cc in comb:
    #    Compete_2hands(cc[0],cc[1])        
    #plyrs=[0,0,0,0,false]*3
    #plyrs[0]=Compete_2hands(cc[0],cc[1])
    
        
"""
################################

# enum & sort for all possible combination, for most precise scoring.
# Make datafile for score lookup
# top 3 cards first. 52C3 = 22100
# e.g. pair of 2 in 3 cards = item 3797, score 829276

# in 22100, category of value total 455 = [2851.0, 5747.0, 8643.0, 11538.0, ..., 999412.0, 999593.0, 999774.0,
#                            1000000.0]
#資料檔牌的順序：號碼優先從小到大，同大則 CDHS 順序
# 3 card 沒有去掉 duplicate, 方便直接查出牌
"""

def generate_3cards_prob(deck):
    deck0=sorted(deck)
    comb = itertools.combinations(sorted(deck0), 3)
    hand_values = handvalues3(comb)
    #print(hand_values[10])
    arr_size = len(hand_values)
    print(arr_size)
    scorerank = [0]*arr_size
    scorerank[0] = 1000000
    prevval = hand_values[0]['value']
    #print(hand_values[22099]['value'])

    for i in range(1,arr_size) :
        curval = hand_values[i]['value']
        if curval==prevval:         #same score, same ranking
            scorerank[i]=scorerank[i-1]
        else:
            scorerank[i] = round((1-(i+1)/arr_size)*1000000,0)
            prevval = curval
    #print(i, curval ,scorerank[i],prevval)

# panda file read and write
    df = pd.DataFrame(hand_values, columns= ['hand', 'value', 'handtype'])
    df['score']=scorerank
    print(df)
    #df=df.drop_duplicates(subset = "value")
    df.to_csv (r'data13_3.csv', index = False, header=True)


"""
A value is trying to be set on a copy of a slice from a DataFrame

See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
  df['handvalue'][i]= score_hand(df['hand'][i])[2]
  
"""

def generate_5cards_prob(deck):
# 5 cards  # 52C5 = 2598960
# Categories (7363, float64)
    print('hihihi')
    deck0=sorted(deck)
    comb = itertools.combinations(deck0, 5)
    hand_values = handvalues(comb)
    arr_size = len(hand_values)
    print(arr_size)
    scorerank = [0]*arr_size
    scorerank[0] = 1000000
    prevval = hand_values[0]['value']

    for i in range(1,arr_size) :
        curval = hand_values[i]['value']
        if curval==prevval:         #same score, same ranking
            scorerank[i]=scorerank[i-1]
        else:
            scorerank[i] = round((1-(i+1)/arr_size)*1000000,0)
            prevval = curval
    #print(i, curval ,scorerank[i],prevval)

# panda file read and write
    df = pd.DataFrame(hand_values, columns= ['hand', 'value', 'handtype'])
    df['score']=scorerank
    print(df)
    df=df.drop_duplicates(subset = "value")
    print (df)
    df.to_csv (r'data13_5.csv', index = False, header=True)


################## Main Program #####################

""" Method 1: Deck & Player Object
myDeck = Deck()
myDeck.shuffle()
#myDeck.show()

Players = [Player('Ian'),Player('Gary'),Player('Jack'),Player('Glory')]
for i in range(4) :
    Players[i].sayHello()
    Players[i].draw(myDeck, 13)
    Players[i].showHand()
    hh = arrange13(Players[i].hand)
    print(hh, '\n')
"""    

# retrieve data and check value
#df33 = pd.read_csv('data13_3.csv')
#df=df33.astype("category")
#print(df['score'])

#df55= pd.read_csv('data13_5.csv')
#df=df55.astype("category")
#print(df['score'])
#sys.exit()

#sample=['H10', 'S12', 'D11', 'S09', 'C07', 'D14', 'S14', 'H08', 'C03', 'D09', 'S03', 'D06', 'H14']
#sample = ['C02', 'D02', 'H02', 'S02', 'C03', 'D03', 'H03', 'S03', 'C04', 'D04', 'H04', 'S04', 'C05'] 
#s3 = str(( '07D', '07H','13S')) 
#s4= ('03C', '04D', '12H')
#s43 = ['04C', '12H', '03D']
#print(score_hand3(s43))

# Debug
#myh1=('06C', '03S', '03D', '07D', '03H')	
#myh2=('06C', '05S', '04C', '04D', '04H')
#print(myh1, score_hand(myh1))
#print(myh2, score_hand(myh2))
#sys.exit()
#print(s43, arrange_str(s43))

#print(s4, s43, set(s4)==set(s43))
#s42= str(tuple(sorted(['04C', '14C', '12C'])))
#s5 = str(tuple(sorted(['05D', '06D', '08D', '10D', '13D'])))

#ss1 = df33.loc[df33['hand']==str(tuple(sorted(s43)))]
#ss1=getscore3(str(tuple(sorted(s43))), df33)
#ss2=getscore5(s5, df55)
#print(s43, ss1)
#print(s5, ss2)
#print(ss1>ss2)
#sys.exit()
# What else:
    # 1. show shape of suits => ok
    # 2. 特殊牌型
    # 3. make sure within same handtype, scoring is consistent with strength 
    # 4. normalize scoring of htop to 5 cards valuation
    # 5. rewrite handvalue() & handvalue3() for handtype dict => ok
    # 6. 條件機率：中間：給13張，前三要比較小、後五要比較大的情形下 的機率
        #         後面 : 給13張，前三中五要比較小 情形下的機率

#case1
 #My hand is : ['♢2', '♠2', '♠4', '♣5', '♢6', '♢8', '♣9', '♢9', '♡9', '♠10', '♡J', '♠Q', '♣A']
 #my best score : 130.089

 #my best arrangement is: 
 #[['♠4', '♢6', '♣A'], ['♢2', '♠2', '♣5', '♣9', '♢9'], ['♢8', '♡9', '♠10', '♡J', '♠Q']]

#case 2
 #My hand is : ['♠3', '♣6', '♡6', '♠6', '♣8', '♡8', '♡9', '♠9', '♢10', '♠10', '♣J', '♡J', '♡K']
#my best score : 162.223

 #my best arrangement is: 
 #[['♢10', '♠10', '♡K'], ['♠3', '♡9', '♠9', '♣J', '♡J'], ['♣6', '♡6', '♠6', '♣8', '♡8']]

#case 3
# [['♡9', '♠10', '♡K'], ['♣3', '♡4', '♠4', '♣7', '♠7'], ['♢2', '♢6', '♢8', '♢10', '♢A']]

### Method 2

deck0 = build_deck() # We create our deck
deck = suffle_deck(deck0)
#print(deck0, '\n')
hands = distribute_deck(deck0) #distribute deck into 13*4playes
#print('My hand is :', hands[0],'\n')

#generate_5cards_prob(deck0)

for hhh in hands:
    special = chk_special(hhh)
        show_hand_special(hhh)
    if hhh>0 :
        continue
    myplay = arrange13(hhh)
    print('============================================================================================= \n')
    print('My hand is :', showhand(hhh),'\n')
    show_hand_details(myplay)
Compete_hands(hands)
    
### Compete each other, scoring system
### max expected value
