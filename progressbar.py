#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 23:15:45 2021

@author: user
"""

from time import sleep

temp = 0
total = 1000

for n in range(1000):
    temp += 1
    print('\r' + '[Progress]:[%s%s]%.2f%%;' % (
    '█' * int(temp*20/total), ' ' * (20-int(temp*20/total)),
    float(temp/total*100)), end='')
    sleep(0.01)
    
from time import sleep
from tqdm import tqdm, trange

for i in tqdm(range(1000)):
    sleep(0.01)