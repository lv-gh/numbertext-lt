# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, sys, re
import timeit
import random
import doctest
import argparse

from threading import Timer, RLock
from cachetools import TTLCache, cached

root = os.path.dirname(__file__)
sys.path.append(os.path.join(root, 'org', 'Numbertext'))
import Soros
import places

digits = range(0, 10)
teens = range(11, 20)
tens = range(10, 100, 10)
miniset = [0, 1, 2, 3, 4, 5,
           10, 11, 12, 13, 14, 15,
           20, 21, 30, 31, 40, 41, 50, 51,
           66, 77, 88, 99]

Args = None
conv = None

def _get_converter():
    global Args
    
    try:
        mod = __import__(os.path.splitext(Args.patterns)[0])
    except:
        raise

    conv = Soros.compile(mod.__doc__)
    if Args.cached:
        conv.lock = RLock()
        conv.cache = TTLCache(maxsize=10**5, ttl=60)
        conv._run = cached(cache=conv.cache, lock=conv.lock)(conv._run)
    return conv


def moneytext(num, curr):
    """
    >>> for n in digits:
    ...     print moneytext(n, 'LTL~')
    nulis litų
    vienas litas
    du litai
    trys litai
    keturi litai
    penki litai
    šeši litai
    septyni litai
    aštuoni litai
    devyni litai

    >>> for n in teens:
    ...     print moneytext(n, 'LTL~')
    vienuolika litų
    dvylika litų
    trylika litų
    keturiolika litų
    penkiolika litų
    šešiolika litų
    septyniolika litų
    aštuoniolika litų
    devyniolika litų


    >>> for n in tens:
    ...     print moneytext(n, 'LTL~')
    dešimt litų
    dvidešimt litų
    trisdešimt litų
    keturiasdešimt litų
    penkiasdešimt litų
    šešiasdešimt litų
    septyniasdešimt litų
    aštuoniasdešimt litų
    devyniasdešimt litų


    >>> for n in [21, 31, 41, 51, 61, 71, 81, 91]:
    ...     print moneytext(n, 'LTL~')
    dvidešimt vienas litas
    trisdešimt vienas litas
    keturiasdešimt vienas litas
    penkiasdešimt vienas litas
    šešiasdešimt vienas litas
    septyniasdešimt vienas litas
    aštuoniasdešimt vienas litas
    devyniasdešimt vienas litas


    >>> for n in [22, 33, 44, 55, 66, 77, 88, 99]:
    ...     print moneytext(n, 'LTL~')
    dvidešimt du litai
    trisdešimt trys litai
    keturiasdešimt keturi litai
    penkiasdešimt penki litai
    šešiasdešimt šeši litai
    septyniasdešimt septyni litai
    aštuoniasdešimt aštuoni litai
    devyniasdešimt devyni litai


    >>> for n in [1.10, 2.20, 3.30, 4.40, 5.50, 6.60, 7.70, 8.80, 9.90]:
    ...     print moneytext(n, 'LTL~')
    vienas litas dešimt centų
    du litai dvidešimt centų
    trys litai trisdešimt centų
    keturi litai keturiasdešimt centų
    penki litai penkiasdešimt centų
    šeši litai šešiasdešimt centų
    septyni litai septyniasdešimt centų
    aštuoni litai aštuoniasdešimt centų
    devyni litai devyniasdešimt centų


    >>> for n in miniset:
    ...     print moneytext(n, 'USD~')
    nulis dolerių
    vienas doleris
    du doleriai
    trys doleriai
    keturi doleriai
    penki doleriai
    dešimt dolerių
    vienuolika dolerių
    dvylika dolerių
    trylika dolerių
    keturiolika dolerių
    penkiolika dolerių
    dvidešimt dolerių
    dvidešimt vienas doleris
    trisdešimt dolerių
    trisdešimt vienas doleris
    keturiasdešimt dolerių
    keturiasdešimt vienas doleris
    penkiasdešimt dolerių
    penkiasdešimt vienas doleris
    šešiasdešimt šeši doleriai
    septyniasdešimt septyni doleriai
    aštuoniasdešimt aštuoni doleriai
    devyniasdešimt devyni doleriai


    >>> for n in miniset:
    ...     print moneytext(n, 'UAH~')
    nulis grivinų
    viena grivina
    dvi grivinos
    trys grivinos
    keturios grivinos
    penkios grivinos
    dešimt grivinų
    vienuolika grivinų
    dvylika grivinų
    trylika grivinų
    keturiolika grivinų
    penkiolika grivinų
    dvidešimt grivinų
    dvidešimt viena grivina
    trisdešimt grivinų
    trisdešimt viena grivina
    keturiasdešimt grivinų
    keturiasdešimt viena grivina
    penkiasdešimt grivinų
    penkiasdešimt viena grivina
    šešiasdešimt šešios grivinos
    septyniasdešimt septynios grivinos
    aštuoniasdešimt aštuonios grivinos
    devyniasdešimt devynios grivinos


    >>> for n in [0.0, 0.01, 1.01, 2.02, 3.10, 4.11, 21.21, 60.66]:
    ...     print moneytext(n, 'RUB~')
    nulis rublių nulis kapeikų
    nulis rublių viena kapeika
    vienas rublis viena kapeika
    du rubliai dvi kapeikos
    trys rubliai dešimt kapeikų
    keturi rubliai vienuolika kapeikų
    dvidešimt vienas rublis dvidešimt viena kapeika
    šešiasdešimt rublių šešiasdešimt šešios kapeikos
    

    >>> for n in [0.0, 0.01, 1.01, 2.02, 3.10, 4.11, 21.21, 60.66]:
    ...     print moneytext(n, 'KZT')
    nulis Kazachstano tengių nulis tiyn
    nulis Kazachstano tengių vienas tiyn
    viena Kazachstano tengė vienas tiyn
    dvi Kazachstano tengės du tiyn
    trys Kazachstano tengės dešimt tiyn
    keturios Kazachstano tengės vienuolika tiyn
    dvidešimt viena Kazachstano tengė dvidešimt vienas tiyn
    šešiasdešimt Kazachstano tengių šešiasdešimt šeši tiyn


    >>> for n in [0.0, 0.01, 1.01, 2.02, 3.10, 4.11, 21.21, 60.66]:
    ...     print moneytext(n, 'SEK')
    nulis Švedijos kronų nulis erių
    nulis Švedijos kronų viena erė
    viena Švedijos krona viena erė
    dvi Švedijos kronos dvi erės
    trys Švedijos kronos dešimt erių
    keturios Švedijos kronos vienuolika erių
    dvidešimt viena Švedijos krona dvidešimt viena erė
    šešiasdešimt Švedijos kronų šešiasdešimt šešios erės

    
    >>> for n in [1.01, 1.5, 2.21, 3.31, 4.41, 5.51, 6.61, 7.71, 8.81, 9.91]:
    ...     print moneytext(n, 'ZAR')
    vienas Pietų Afrikos Respublikos randas vienas centas
    vienas Pietų Afrikos Respublikos randas penkiasdešimt centų
    du Pietų Afrikos Respublikos randai dvidešimt vienas centas
    trys Pietų Afrikos Respublikos randai trisdešimt vienas centas
    keturi Pietų Afrikos Respublikos randai keturiasdešimt vienas centas
    penki Pietų Afrikos Respublikos randai penkiasdešimt vienas centas
    šeši Pietų Afrikos Respublikos randai šešiasdešimt vienas centas
    septyni Pietų Afrikos Respublikos randai septyniasdešimt vienas centas
    aštuoni Pietų Afrikos Respublikos randai aštuoniasdešimt vienas centas
    devyni Pietų Afrikos Respublikos randai devyniasdešimt vienas centas
    """
    
    global conv

    if curr == None:
        outcurr = ""
    else:
        outcurr = curr + " "

    if isinstance(num, float):
        num = format(num, '.2f')

    return get_numbertext(outcurr + str(num), conv)

def numbertext(num):
    """
    >>> for n in digits:
    ...     print numbertext(str(n))
    nulis
    vienas
    du
    trys
    keturi
    penki
    šeši
    septyni
    aštuoni
    devyni

    >>> for n in teens:
    ...     print numbertext(n)
    vienuolika
    dvylika
    trylika
    keturiolika
    penkiolika
    šešiolika
    septyniolika
    aštuoniolika
    devyniolika

    >>> for n in tens:
    ...     print numbertext(n)
    dešimt
    dvidešimt
    trisdešimt
    keturiasdešimt
    penkiasdešimt
    šešiasdešimt
    septyniasdešimt
    aštuoniasdešimt
    devyniasdešimt

    >>> for n in [k*10 for k in tens]:
    ...     print numbertext(n)
    vienas šimtas
    du šimtai
    trys šimtai
    keturi šimtai
    penki šimtai
    šeši šimtai
    septyni šimtai
    aštuoni šimtai
    devyni šimtai

    # Exponentials (case nominative, singular) and boundary
    >>> for n in [10**3, 10**6, 10**9, 10**12, 10**15, 10**18, 10**21]:
    ...     print numbertext(n)
    vienas tūkstantis
    vienas milijonas
    vienas milijardas
    vienas trilijonas
    vienas kvadrilijonas
    vienas kvintilijonas
    1000000000000000000000

    # Exponentials (case nominative, plural)
    >>> for n in [2*10**3, 2*10**6, 2*10**9, 2*10**12, 2*10**15, 2*10**18]:
    ...     print numbertext(n)
    du tūkstančiai
    du milijonai
    du milijardai
    du trilijonai
    du kvadrilijonai
    du kvintilijonai

    # Exponentials (case genitive, plural)
    >>> for n in [11*10**3, 11*10**6, 11*10**9, 11*10**12, 11*10**15, 11*10**18]:
    ...     print numbertext(n)
    vienuolika tūkstančių
    vienuolika milijonų
    vienuolika milijardų
    vienuolika trilijonų
    vienuolika kvadrilijonų
    vienuolika kvintilijonų

    # Exponentials (case genitive, plural)
    >>> for n in [120*10**3, 230*10**6, 340*10**9, 450*10**12, 560*10**15, 670*10**18]:
    ...     print numbertext(n)
    vienas šimtas dvidešimt tūkstančių
    du šimtai trisdešimt milijonų
    trys šimtai keturiasdešimt milijardų
    keturi šimtai penkiasdešimt trilijonų
    penki šimtai šešiasdešimt kvadrilijonų
    šeši šimtai septyniasdešimt kvintilijonų


    # random
    >>> for n in [50361, 276522, 972450, 82543063, 3443855901]:
    ...     print numbertext(n)
    penkiasdešimt tūkstančių trys šimtai šešiasdešimt vienas
    du šimtai septyniasdešimt šeši tūkstančiai penki šimtai dvidešimt du
    devyni šimtai septyniasdešimt du tūkstančiai keturi šimtai penkiasdešimt
    aštuoniasdešimt du milijonai penki šimtai keturiasdešimt trys tūkstančiai šešiasdešimt trys
    trys milijardai keturi šimtai keturiasdešimt trys milijonai aštuoni šimtai penkiasdešimt penki tūkstančiai devyni šimtai vienas
    """
    global conv
    return get_numbertext(str(num), conv)

def get_numbertext(num, conv):
    try:
        n = conv.run(num)
    except:
        return "Conversion error"
    if n == "":
        return num
    return n

def print_cache():
    if hasattr(conv, 'cache'):
        print "cache size:", len(conv.cache)
    
def test1(n, k):
    """{0}: numbertext() called {2} times with random int [1, {1:.0g}]"""
    for i in xrange (1, n):
        num = random.randint(1,k)
        s = numbertext(num)

def test2(n, k):
    """{0}: moneytext() called {2} times with random float [1.00, {1:.3g}]"""
    for i in xrange (1, n):
        num = random.randint(1,k) + random.random()
        s = moneytext(num, 'USD')
    
def test3(n, k):
    """{0}: numbertext() called {2} times with same random int [1, {1:.0g}]"""
    num = str(random.randint(1,k))
    for i in xrange (1, n):
        s = numbertext(num)
        
if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=
    """
    Test numbertext-lt patterns and/or benchmark module (patterns) performance.
    """)
    ap.add_argument('-p', '--patterns', nargs='?', metavar='MOD',
                    default='numbertext_lt_LT.py', help=
                    'pattern module file, default: %(default)s')
    ap.add_argument('-c', '--cached', action='store_true', default=False, help=
                    'turn on caching')
    ap.add_argument('-t', '--timeit', nargs='?', metavar='TEST',
                    const='test1', default=False,
                    choices=['test1', 'test2', 'test3'], help=
                    'run particular test and timeit. '
                    '%(metavar)s: %(choices)s, default: %(const)s')
    ap.add_argument('-l', '--limit', nargs='?', type=int, metavar='10**N',
                    default=18, help=
                    'limit test random number generation to %(metavar)s; '
                    'default: N=%(default)i')
    Args = ap.parse_args()

    conv = _get_converter()
    if Args.timeit:
        test = Args.timeit
        nlim = 10**Args.limit
        thunk = '%s(10000, %i)' % (test, nlim)
        setup = 'from __main__ import %s' % (test)

        print eval(test).__doc__.format(test, nlim, 10000)
        print "took:", timeit.timeit(thunk, number=1, setup=setup)
        print_cache()
    else:
        doctest.testmod(optionflags = doctest.NORMALIZE_WHITESPACE)




