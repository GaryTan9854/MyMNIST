#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 12 16:37:49 2021

@author: user
"""

# mutual exclusion
mutex = Semaphore(1)
counter = 0

## Thread code

mutex.wait()
# critical section
counter += 1
mutex.signal()