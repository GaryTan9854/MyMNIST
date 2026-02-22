import random
import numpy as np
import itertools
from itertools import product
from math import comb
import sys

p=[0]*5
q=[i for i in range(5,25,5)] 
print(p,q)
p[0]=13
p[1:]=q
print(p,q)
sys.exit()
        

print('Whats your name ?')
#name=input()
#print('good morning ', name)

print('Hello')



for x, y in product(range(1, 10), range(1, 10)):
    print(x, y, x*y)
    
list1 = ['a', 'b']
list2 = ['c', 'd']

for i in product(list1, list2):
    print(i)
    
iterable = (x+x for x in range(5))
print (np.fromiter(iterable, int))
yy = (y*y for y in range(5))
print(np.fromiter(yy,int))

#make a card deck

list3 = ['H','S','D','C']
for x,y in itertools.product(list3,range(2,15)):
    print(x+str(y))


xx = itertools.combinations('ABCD', 2)
yy = itertools.combinations('ABCD', 2)
#print(list(xx))
for i in xx:
    print(i)
print(list(yy))

#############
hand=['H2', 'S2', 'C2', 'D2', 'H3']

print(sorted(hand))

letters = [hand[i][:1] for i in range(5)]

print(letters)
#Out[5]: ['H', 'S', 'C', 'D', 'H']

numbers = [int(hand[i][1:]) for i in range(5)]

print(numbers)
#Out[7]: [2, 2, 2, 2, 3]

rnum = [numbers.count(i) for i in numbers]

print(rnum)
#Out[9]: [4, 4, 4, 4, 1]

rlet = [letters.count(i) for i in letters]

print(rlet)
#Out[11]: [2, 1, 1, 1, 2]

#arr = np.array('ABCD')
#t = np.dtype([('', arr.dtype)]*2)
#result = np.fromiter(itertools.combinations(arr, 2), t)
#print(result)
    #return result.view(arr.dtype).reshape(-1, n)
#print(np.fromiter(xx,t))
    
#for i in itertools.combinations('ABCD',2):
#    print (i)

hand=['H2', 'S2', 'C2', 'D2', 'H3', 'H8', 'H9', 'S10', 'S7', 'D11', 'C11', 'C12','C14']
list = [20, 16, 10, 5]
random.shuffle(hand)
print ("随机排序列表 : ",  hand)

random.shuffle(hand)
print ("随机排序列表 : ",  hand)
print(len(hand))
top = hand[:3]
print(top)
mid = hand[3:8]
print(mid)
bot = hand[8:13]
print(bot)

x= comb(13,3)
y=comb(10,5)
print( x, y, x*y)

sample=['H10', 'S12', 'D11', 'S09', 'C07', 'D14', 'S14', 'H08', 'C03', 'D09', 'S03', 'D06', 'H14']
s2 = ['D11','S09','H08','D09','S03']
print(sample)
print(sorted(sample))
#rest = list(set(sample) - set(s2))
#print(rest)

"""
# panda file read and write
data = {'Product': ['Desktop Computer','Tablet','Printer','Laptop'],
        'Price': [850,200,150,1300]
        }

df = pd.DataFrame(data, columns= ['product', 'price'])

df.to_csv (r'datatest.csv', index = False, header=True)

print (df)
"""

list0=[]
list1=[]
list2=[]
list3=[]
answer1='yes'
answer2='yes'
answer3='yes'

while answer1=='yes':
    item1=input("Please input a list element for your first list:")
    answer1=input("Do you want to continue:")
    list1.append(item1)

while answer2=='yes':
    item2=input("Please input a list element for your second list:")
    answer2=input("Do you want to continue:")
    list2.append(item2)

while answer3=='yes':
    item3=input("Please input a list element for your third list:")
    answer3=input("Do you want to continue:")
    list3.append(item3)

list0.append(list1)
list0.append(list2)
list0.append(list3)

print(list0)