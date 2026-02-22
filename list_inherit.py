#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 20:33:22 2021

@author: user
"""

class myList(list):
    def __init__(self, ll=[]):
        list.__init__([])
        #self = ll
        #self = [x for x in ll]
        for i in ll:
            self.append(i)        
        print(self)
        
mm = myList([3,4,6,2,8])
print(mm)
