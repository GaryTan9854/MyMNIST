import random
import pandas as pd
import numpy as np
import itertools
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
        
    def show(self):
        suits = {"H":"♡", "S":"♠", "D":"♢", "C":"♣"}
        values = {**{i:str(i) for i in range(2,10)}, 
        **{1:'A', 10:'T', 11:'J',12:'Q', 13:'K', }}
        #print(values[self.value]+suits[self.suit])
        return values[self.value]+suits[self.suit]
    
        if self.value == 1:
            val = "A"
        elif self.value == 11:
            val = "J"
        elif self.value == 12:
            val = "Q"
        elif self.value == 13:
            val = "K"
        else:
            val = self.value
        return "{}{}".format(val, suits[self.suit])

        if self.value == 1:
            val = "Ace"
        elif self.value == 11:
            val = "Jack"
        elif self.value == 12:
            val = "Queen"
        elif self.value == 13:
            val = "King"
        else:
            val = self.value

        return "{} of {}".format(val, self.suit)
    
    def show2(self):
        suits = {"h":"♡", "s":"♠", "d":"♢", "c":"♣"}
        values = {**{i:str(i) for i in range(2,10)}, 
        **{10:'T', 11:'J',12:'Q', 13:'K', 14:'A'}}
        return values[self.value] + suits[self.suit]

class Deck(object):
    def __init__(self):
        self.cards = []
        self.build()

    # Display all cards in the deck
    def show(self):
        i=0
        for card in self.cards:
            #for i in range(13):
            #   print(card[i], end =" ")
            i+=1
            print (card.show())
            if i%13==0 :
                print ('\n')

    # Generate 52 cards
    def build(self):
        self.cards = []
        #for suit in ['Hearts', 'Clubs', 'Diamonds', 'Spades']:
        for suit in ['H', 'C', 'D', 'S']:
            for val in range(1,14):
                self.cards.append(Card(suit, val))

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

    # Return the top card
    def deal(self):
        return self.cards.pop()


class Player(object):
    def __init__(self, name):
        self.name = name
        self.hand = []

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
        print ('{}s hand: {}'.format(self.name, self.hand))
        return self

    def discard(self):
        return self.hand.pop()

class Hand13(object):
    
    def __init__(self, hand):
        self.hand = []
        self.rtop = self.hand[1:3]
        self.rmid = self.hand[4:8]
        self.rbottom = self.hand[9:13]
                        

    def __unicode__(self):
        return self.show()
    def __str__(self):
        return self.show()
    def __repr__(self):
        return self.show()
    
    def show(self):
        return self.rtop.show()+' // '+self.rmid.show()+' // '+self.rbottom.show()
    
    def Arrange13(self):
        return self.hand
        
def build_deck():
    numbers=list(range(2,15))
    suits = ['H','S','C','D']
    deck = []
    for i in numbers:
        for s in suits:
            card = s+str(i)
            deck.append(card)
    return deck
        
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
    score = 105 + four + card/100
    return score

def check_full_house(hand,letters,numbers,rnum,rlet):
    for i in numbers:
        if numbers.count(i) == 3:
            full = i
        elif numbers.count(i) == 2:
            p = i
    score = 90 + full + p/100  
    return score

def check_three_of_a_kind(hand,letters,numbers,rnum,rlet):
    cards = []
    for i in numbers:
        if numbers.count(i) == 3:
            three = i
        else: 
            cards.append(i)
    score = 45 + three + max(cards) + min(cards)/1000
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
        
#135 同花大順
#120 同花順
#105 鐵支
#90 葫蘆
#75 同花
#65 順
#45 三條
#30 兩對
#15 一對
#2..14 亂

def score_hand(hand):
    letters = [hand[i][:1] for i in range(5)] # We get the suit for each card in the hand
    numbers = [int(hand[i][1:]) for i in range(5)]  # We get the number for each card in the hand
    rnum = [numbers.count(i) for i in numbers]  # We count repetitions for each number
    rlet = [letters.count(i) for i in letters]  # We count repetitions for each letter
    dif = max(numbers) - min(numbers) # The difference between the greater and smaller number in the hand
    handtype = ''
    score = 0
    if 5 in rlet: #花色數目=5=同花
        if numbers ==[14,13,12,11,10]: #why already sorted?
            handtype = 'royal_flush'
            score = 135
            print('this hand is a %s:, with score: %s' % (handtype,score)) 
        elif dif == 4 and max(rnum) == 1: #大小只差4, 每個數字又只出現一次
            handtype = 'straight_flush'
            score = 120 + max(numbers)
            print('this hand is a %s:, with score: %s' % (handtype,score)) 
        elif 4 in rnum:
            handtype == 'four of a kind'
            score = check_four_of_a_kind(hand,letters,numbers,rnum,rlet)
            print('this hand is a %s:, with score: %s' % (handtype,score)) 
        elif sorted(rnum) == [2,2,3,3,3]:
            handtype == 'full house'
            score = check_full_house(hand,letters,numbers,rnum,rlet)
            print('this hand is a %s:, with score: %s' % (handtype,score)) 
        elif 3 in rnum:
            handtype = 'three of a kind'
            score = check_three_of_a_kind(hand,letters,numbers,rnum,rlet)
            print('this hand is a %s:, with score: %s' % (handtype,score)) 
        elif rnum.count(2) == 4:
            handtype = 'two pair'
            score = check_two_pair(hand,letters,numbers,rnum,rlet)
            print('this hand is a %s:, with score: %s' % (handtype,score)) 
        elif rnum.count(2) == 2:
            handtype = 'pair'
            score = check_pair(hand,letters,numbers,rnum,rlet)
            print('this hand is a %s:, with score: %s' % (handtype,score)) 
        else:
            handtype = 'flush'
            score = 75 + max(numbers)/100
            print('this hand is a %s:, with score: %s' % (handtype,score)) 
    elif 4 in rnum:
        handtype = 'four of a kind'
        score = check_four_of_a_kind(hand,letters,numbers,rnum,rlet)
        print('this hand is a %s:, with score: %s' % (handtype,score)) 
    elif sorted(rnum) == [2,2,3,3,3]:
       handtype = 'full house'
       score = check_full_house(hand,letters,numbers,rnum,rlet)
       print('this hand is a %s:, with score: %s' % (handtype,score)) 
    elif 3 in rnum:
        handtype = 'three of a kind' 
        score = check_three_of_a_kind(hand,letters,numbers,rnum,rlet)
        print('this hand is a %s:, with score: %s' % (handtype,score)) 
    elif rnum.count(2) == 4:
        handtype = 'two pair'
        score = check_two_pair(hand,letters,numbers,rnum,rlet)
        print('this hand is a %s:, with score: %s' % (handtype,score)) 
    elif rnum.count(2) == 2:
        handtype = 'pair'
        score = check_pair(hand,letters,numbers,rnum,rlet)
        print('this hand is a %s:, with score: %s' % (handtype,score)) 
    elif dif == 4:
        handtype = 'straight'
        score = 65 + max(numbers)
        print('this hand is a %s:, with score: %s' % (handtype,score)) 

    else:
        handtype= 'high card'
        n = sorted(numbers,reverse=True)
        score = n[0] + n[1]/100 + n[2]/1000 + n[3]/10000 + n[4]/100000
        print('this hand is a %s:, with score: %s' % (handtype,score)) 
        
    return score


def handvalues(combinations):
    scores =[{"hand": i, "value": score_hand(i)} for i in combi] # We iterate over all combinations scoring them
    scores = sorted(scores, key = lambda k: k['value'],reverse=True) # We sort hands by score
    return scores

    
deck = build_deck() # We create our deck
sample=['H10', 'S12', 'D11', 'S09', 'C07', 'D14', 'S14', 'H08', 'C03', 'D09', 'S03', 'D06', 'H14']
sample_len = len(sample)
print('sample len =', str(sample_len))
nCr = math.comb(sample_len,5)
print("total ", str(nCr), " combinations")

combi = combinations(sample,5) # We create an array containing all possible 5 cards combinations
hand_values = handvalues(combi) #sorted table of hand & value
for i in range(nCr):
    print(hand_values[i])
    
    
#convert into data dictionary of hands and values
#x = [i.get("hand","") for i in hand_values] # making a list of hands
#y = [i.get("value","") for i in hand_values] #making a list of values

#data = {'hands':x, 'value':y} # making a dictionary of hands and values
#df = pd.DataFrame(data) # making a pandas dataframe with hands and values



#################################
# Test making a Card
# card = Card('Spades', 6)
# print card

# Test making a Deck
#myDeck = Deck()
#myDeck.shuffle()
#myDeck.show()

#Players = [Player('Ian'),Player('Gary'),Player('Jack'),Player('Glory')]
#for i in range(0,4) :
#    Players[i].sayHello()
#    Players[i].draw(myDeck, 13)
#    Players[i].showHand()
#    #hh = Hand13(Players[i].hand)
    #print(hh)
    
    