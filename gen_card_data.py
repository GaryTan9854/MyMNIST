#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 11:55:36 2021

@author: user
"""

import random
import csv
from itertools import zip_longest
from tqdm import tqdm 

HandCat={'亂':0, '一對':1, '兩對':2, '三條':3, '順':4, '同花':5,
         '葫蘆':6, '鐵支':7, '同花順':8, '同花次大順':9, '同花大順':10}

HandName = {v : k for k, v in HandCat.items()}

#因為是 dict 所以可以查字典
#本 class 只適合 5 cards
class Hist_Cards(dict):
    """A map from each item (x) to its frequency."""

    def __init__(self, seq):
        "Creates a new histogram starting with the items in seq."
        self.numlist = sorted(seq)
        for x in seq:
            self.count(x)
        self.sets = list(self.values())  
        self.sets.sort(reverse=True)  #重覆個數的sorted list

        # way to get max freq 代表的數 max(stats, key=stats.get)
        #max(stats.items(), key=operator.itemgetter(1))[0]

    def count(self, x, f=1):
        "Increments the counter associated with item x."
        self[x] = self.get(x, 0) + f
        if self[x] == 0:
            del self[x]

    def check_sets(self, *t):
        for need, have in zip(t, self.sets): #這招特別 因為sort過
            if need > have: return False
        return True
    
    #for precise match of *t not >
    def check_sets2(self, *t):
        for need, have in zip_longest(t, self.sets): #這招特別 因為sort過
            if need != have: return False
        return True
    
    def no_pair(self):
        return max(self.values())==1
    
    def has_pair(self):
        """Checks whether this hand has a pair."""
        return self.check_sets(2)
    
    def has_onepair(self):
        return self.check_sets(2,1)
    
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
        return self.check_sets2(3, 2)
    
    def no_straight(self):
        t= self.chk_straight()
        return t<2
    
    def chk_straight(self):
        sdict = { '大順':10, '次順':9, '順':4, '亂':0}
        if not self.no_pair():
            return 0
        m1= max(self)
        m2=min(self)
        if m1-m2==4: #2-14 是順
            return sdict['大順'] if m2==10 else sdict['順']
        if m1==14: #有 A
            m1=max(self.numlist[:-1]) #except last item (A)
            #print(m1,m2, self.numlist[:-1])
            if m1==5:
                return sdict['次順']
        return sdict['亂']    
    


    def hand_category(self, is_flush=0):
        if is_flush:
            ss = self.chk_straight()
            if ss==0:
                return HandCat['同花']
            if ss==10:
                return HandCat['同花大順']
            elif ss==9:
                return HandCat['同花次大順']
            elif ss==4:
                return HandCat['同花順']
        if self.has_fourkind():
            return HandCat['鐵支']
        if self.has_fullhouse():
            return HandCat['葫蘆']
        if self.has_threekind():
            return HandCat['三條']
        if self.has_twopair():
            return HandCat['兩對']
        if self.has_onepair():
            return HandCat['一對']
        if self.chk_straight():
            return HandCat['順']
        return HandCat['亂']
            

def gen_3card(n):
    res = []
    for i in range(n):
        arr = []
        for j in range(3):
            arr.append(random.randint(2,14))
        ll = []
        for k in arr:
            ll.append(arr.count(k))
        same_num = max(ll)
        r=3 if same_num==3 else (2 if same_num==2 else 1)
        arr.append(r)
    res.append(arr)
    return res

def gen_5card(n):
    res = []
    for i in tqdm(range(n)):
        arr = []
        for j in range(5):
            arr.append(random.randint(2,14))
        ll = []
        #for k in arr:
        #    ll.append(arr.count(k))
        #same_num = max(ll)
        x = Hist_Cards(arr)
        r = x.hand_category()
        arr.append(r)
        #print(arr)
        #r=3 if same_num==3 else (2 if same_num==2 else 1)
        res.append(arr)
    print(len(res))
    return res

def write_f(fn, res):
    with open(fn, 'w', newline='') as csvfile:
        # 建立 CSV 檔寫入器
        writer = csv.writer(csvfile)
        n= len(res)
        for i in tqdm(range(n)):
            writer.writerow(res[i])
    return n

#x = Hist_Cards([9,9,9,9,9])
#print(HandName[x.hand_category(0)])
#dat = gen_5card(300000)
#write_f('card5train.csv',dat)
ll = [9,9,8,2,4,6,5,1,10,15,4,23]
for i in tqdm(ll):
    print(ll)
