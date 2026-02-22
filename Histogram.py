#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 19 09:30:27 2021

@author: user
"""

from itertools import zip_longest

Suits = {"H":"♡", "S":"♠", "D":"♢", "C":"♣"}
Values = {**{i:str(i) for i in range(0,11)}, **{ 11:'J',12:'Q', 13:'K', 14:'A'}}

HandCat={'亂':0, '一對':1, '兩對':2, '三條':3, '順':4, '同花':5,
         '葫蘆':6, '鐵支':7, '同花順':8, '同花次大順':9, '同花大順':10}

HandName = {v : k for k, v in HandCat.items()}
HandScor = {0:0, 1:15, 2:30, 3:45, 4:65, 5:75, 6:90, 7:105, 8:120, 9:130, 10:135 }
def convert_cardnum(value):
    return(Values[value]) 

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
    
class Hand(list):
    def __init__(self,hand=[]):
        list.__init__([])
        if str(type(hand[0]))=="<class '__main__.Card'>":
            #Card object
            self.handlist = sorted( [ i.cardstr() for i in hand ])
            #self = sorted(hand)  # sorted by __eq__ & __lt__
            for i in sorted(hand):      #strange- need to re-append by for loop
                self.append(i)
            #print('Card Object')
        else:
            #List of String:['02D','03H'...]
            self.handlist = sorted(hand)
            print(self.handlist)
            for i in self.handlist:
                cc = Card(i[2:], int(i[:2])) # number then suit 
                self.append(cc)
            #print('Lists')
        
        self.handsize = len(self)
        self.numbers = [ i.value for i in self]
        #print(self.numbers)
        
    def show(self):
        #s = [ i.show() for i in self.hand ]
        s='[ '
        for i in self:
            s=s+i.show()+' '
        return(s+']')
    
    def chk_flush(self):
        suits = [ i.suit for i in self]
        for i in suits[1:]:
            if i!=suits[0] :
                return False
        return True
    

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
            if need != have: return False
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
        return self.check_sets(3, 2)
    
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
            
    def check_pair2(self):    
        pair = 0
        for i in self.numlist:
            if self.numlist.count(i) == 2:
                pair=i
            else:
                ll = i
        score = 15 + pair + ll/100 #+ cards[1]/1000 + cards[2]/10000
        
        return score
    
def chk_flush(f):
    for i in f[1:]:
        if i!=f[0] :
            return False
    return True

class Hand3(Hand):
    def __init__(self,hand):
        super(Hand3, self).__init__(hand)
        self.handtype = ''
        self.handtype_val=0
        self.score=0
        self.p=[0,0,0]
        self.sss=self.score_hand()
    
    def score_hand(self):
    #3張 除了特殊牌型外 沒有順沒有同花
    #只有 三條，一對，亂
        x = Hist_Cards(self.numbers)
        cat = x.hand_category()
        self.handtype_val = cat
        self.handtype = HandName[cat]
        if cat == 3:
            self.score = self.check_three_of_a_kind()
        elif cat ==1:
            self.score = self.check_pair()
        elif cat ==0:
            self.score = self.check_highcard()
        sss =[self.score,  self.handtype, self.handtype_val]
        return(sss)
    
    def check_three_of_a_kind(self):
        three = self.numbers[0]
        score = HandScor[3] + three 
        self.p[0]=three
        return score
    
    def check_pair(self):    
        pair = 0
        for i in self.numbers:
            if self.numbers.count(i) == 2:
                pair=i
            else:
                ll = i
        score = HandScor[1] + pair + ll/100
        self.p[0]=pair
        self.p[1]=ll
        return score
    
    def check_highcard(self):
        #n = sorted(self.numbers,reverse=True)
        self.p=self.numbers
        score = self.p[2] + self.p[1]/100 + self.p[0]/1000
        return score
    
    def hand_dscp(self):
        ht = self.handtype
        print(ht, self.handtype_val, self.p)
        sss=''
        if ht== '三條':
            sss=convert_cardnum(self.p[0]) + ' 衝三'
        elif ht =='一對':
            sss = convert_cardnum(self.p[0])+' Pair'
        elif ht== '亂': #staight in 3 cards
            sss = '亂 ['+convert_cardnum(self.p[0])+' '+convert_cardnum(self.p[1])+' '+convert_cardnum(self.p[2])+']'
        
        return(sss)
    
class Hand5(Hand):
    def __init__(self,hand):
        super(Hand5, self).__init__(hand)
        self.handtype = ''
        self.handtype_val=0
        self.score=0
        self.p=[0,0,0,0,0]
        self.sss=self.score_hand()
        
        
    def check_four_of_a_kind(self):
        for i in self.numbers:
            if self.numbers.count(i) == 4:
                four = i
            elif self.numbers.count(i) == 1:
                card = i
        score = HandScor[7] + four # + card/100 ＃也不必看第五張牌
        self.p[0]=four
        self.p[1]=card
        return score

    def check_full_house(self):
        for i in self.numbers:
            if self.numbers.count(i) == 3:
                full = i
            elif self.numbers.count(i) == 2:
                p = i
        score = HandScor[6] + full  # +  p/100  full house won't need to differentiate the pair card
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
        score = HandScor[3] + three 
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
        score = HandScor[2] + max(pairs) + min(pairs)/100 + cards[0]/1000
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
        score = HandScor[1] + pair[0] + cards[0]/100 + cards[1]/1000 + cards[2]/10000
        self.p[0]=pair[0]
        self.p[1:]=cards
                
        return score
    
    def check_straight(self):
        m1=min(self.numbers)
        m2=max(self.numbers)
        if m2==14: #got A, either A-5 or 10-A
            nn = 1 if m1==2 else 10
        else:
            nn=m1
        self.p[0]=nn
        self.p[1]=nn+4
        if nn==1:
            return HandScor[4]+13.5 # A-5 straight 比較大
        return HandScor[4]+self.p[1] 
    
    
    def check_highcard(self):
        n = sorted(self.numbers,reverse=True)
        score = n[0] + n[1]/100 + n[2]/1000 + n[3]/10000 + n[4]/100000
        self.p=n
        return score
    
#    HandCat={'亂':0, '一對':1, '兩對':2, '三條':3, '順':4, '同花':5,
#         '葫蘆':6, '鐵支':7, '同花順':8, '同花次大順':9, '同花大順':10}

    def score_hand(self):
        self.flush=self.chk_flush()
        x = Hist_Cards(self.numbers)
        cat = x.hand_category(self.flush)
        self.handtype_val = cat
        self.handtype = HandName[cat]
        
        if cat >8: #同花順
            self.p=self.numbers
        elif cat ==8:    
            self.score = HandScor[cat] + max(self.numbers)
            self.p[0]=min(self.numbers)
            self.p[1]=max(self.numbers)  
        elif cat ==7:
            self.score = self.check_four_of_a_kind()
        elif cat == 6:
            self.score = self.check_full_house()
        elif cat == 5:
            ss=self.check_highcard()
            self.score = HandScor[cat]+ ss
        elif cat == 4:
            self.score = self.check_straight()
        elif cat == 3:
            self.score = self.check_three_of_a_kind()
        elif cat == 2:
            self.score = self.check_two_pair()
        elif cat == 1:
            self.score = self.check_pair()
        elif cat ==0:
            self.score = self.check_highcard()
        sss =[self.score,  self.handtype, self.handtype_val]
        return(sss)
    
    
    def hand_dscp(self):
        hh = self.handtype
        sss=hh
        if hh=='同花順':
            sss = str(self.p[0])+' 同花順'
        elif hh=='同花':
            sss = '同花 ['+convert_cardnum(self.p[0])+' '+convert_cardnum(self.p[1])+' '+convert_cardnum(self.p[2])+' '+convert_cardnum(self.p[3])+' '+convert_cardnum(self.p[4])+']'
        elif hh=='鐵支':
            sss = convert_cardnum(self.p[0])+' 鐵支'
        elif hh=='葫蘆':
            sss = convert_cardnum(self.p[0])+' 葫蘆'
        elif hh=='三條' :
            sss=convert_cardnum(self.p[0])+' 三條'
        elif hh=='兩對':
            sss=convert_cardnum(self.p[0])+'/'+ convert_cardnum(self.p[1])+' Pair'
        elif hh=='一對':
            sss = convert_cardnum(self.p[0])+' Pair'
        elif hh=='順':
            if self.p[1]==14:
                sss = str(self.p[0])+'-'+'A 順'
            else:
                sss = str(self.p[0])+'-'+str(self.p[1])+' 順'
        elif hh=='亂':
            sss = '亂 ['+convert_cardnum(self.p[0])+' '+ convert_cardnum(self.p[1])+' '+convert_cardnum(self.p[2])+' '+convert_cardnum(self.p[3])+' '+convert_cardnum(self.p[4])+']'
        return sss
    
#專屬13支一手牌的object
class Hand13(Hand):
    def __init__(self, hand):
        super(Hand13, self).__init__(hand)
        self.handtype = ''
        self.handtype_val=0
        self.score=0
        
        self.specialhand = 'normal' 
        self.CanAttack = False
        self.attack_score =0
        self.defense_score=0
        self.htop = []
        self.hmid = []
        self.hbot = []
        self.ss= [0,0,0]
        self.score = 0
        self.totalscore = 0
        
        #print(self[:3],self[3:8],self[8:13],self.handlist)
        
        self.eval()
        #print(ss)
    
    def eval(self):
        self.htop = Hand3(self.handlist[:3]) #['02C','02D','02H']) #
        self.hmid = Hand5(self.handlist[3:8]) #['03C', '03D', '03H', '04C', '04D']) #
        self.hbot = Hand5(self.handlist[8:13]) #['04H', '04S', '05C', '11C', '11S']) #
        self.ss = [self.htop.score,self.hmid.score,self.hbot.score]
        self.score = sum(self.ss)
        self.totalscores = self.score
        
        
    def show355(self):
        ss= self.htop.show() + self.hmid.show()+self.hbot.show()
        return ss
        


x = Hist_Cards([1,2,3,4,5])

t=[3,2]
print(t, x.sets, zip(t, x.sets))
p2 = True
for need, have in zip_longest(t, x.sets): #這招特別 因為sort過
    if need != have: 
        p2=False

print(p2)    
print(HandName[x.hand_category()])
print(x.numlist)
print(x)
print(x.values())
#h = Hand(['02D','05C','14H','10S','11D'])
#sample2= ['02C', '02D', '02H', '11S', '03C', '03D', '03H', '11C', '04C', '04D', '04H', '04S', '05C'] 
#h = Hand13(sample2)
#h2= Hand3(['03H', '13C', '13H'])
#h3 = Hand3([Card('C',8),Card('D',3),Card('D',12)])
#print(h2.hand_dscp())
      
         
#print(chk_flush(['C','C','C','C','C']))
#xx = x.hand_category(1)
#print(xx)
#xx = x.hand_category()
#print(xx)

#print(HandName[xx])