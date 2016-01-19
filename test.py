"""This file contains code for use with "Think Bayes",
by Allen B. Downey, available from greenteapress.com

Copyright 2012 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

from thinkbayes import Pmf
from thinkbayes import Suite
import thinkbayes


print '\n *** Monty **** '
class Monty(Suite):
    def Likelihood(self, data, hypo):
        if hypo == data:
            return 0
        elif hypo == 'A':
            return 0.5
        else:
            return 1

suite = Monty('ABC')
suite.Update('B')
suite.Print()


print '\n *** MM **** '
class MM(Suite):
    mixes = {
        '1994': dict(brown=0.3, yellow=0.2, red=0.2, green=0.1, orange=0.1, tan=0.1),
        '1996': dict(brue=0.24, green=0.2, orange=0.16, yellow=0.14, red=0.13, brown=0.13)
    }
    def Likelihood(self, data, hypo):
        mix = self.mixes[hypo]
        p = mix.get(data,0)
        return p

hypos = ['1994', '1996']
suite = MM(hypos)
suite.Update('yellow')
suite.Print()



print '\n *** Dice **** '
class Dice(Suite):
    def Likelihood(self, data, hypo):
        if data <= 0:
            return 0
        elif data > hypo:
            return 0
        else:
            return 1.0/hypo


hypos = [4,6,8,12,20]
suite = Dice(hypos)
for roll in [1,6,3,7,7,9]:
    suite.Update(roll)
suite.Print()


print '\n *** Train **** '
class Train(Suite):
    def Likelihood(self, data, hypo):
        if data <= 0:
            return 0
        elif data > hypo:
            return 0
        else:
            return 1.0/hypo
    def __init__(self, hypos, alpha=1.0):
        Pmf.__init__(self)
        for hypo in hypos:
            self.Set(hypo, hypo**(-alpha))
        self.Normalize()

hypos = xrange(1, 1001)
suite = Train(hypos)
for num in [60, 30, 90, 20, 12]:
    suite.Update(num)
print suite.Mean()
interval = thinkbayes.Percentile(suite, 5.0), thinkbayes.Percentile(suite, 95.0)
print interval


print '*** Euro1 ****'
class Euro1(Suite):
    def Likelihood(self, data, hypo):
        x = hypo / 100.
        if data == 'H':
            return x
        else:
            return 1 - x

suite = Euro1(xrange(0,101))
dataset = 'H' * 140 + 'T' * 110
for data in dataset:
    suite.Update(data)

print "Mean", suite.Mean()
print 'Median', suite.MaximumLikelihood()
print 'CI', suite.CredibleInterval(95)


print '\n*** Euro2 ****'
class Euro2(Suite):
    def Likelihood(self, data, hypo):
        x = hypo / 100.0
        head, tail = data
        return x**head * (1-x)**tail

suite = Euro2(xrange(0,101))
data = (140, 110)
suite.Update(data)
print "Mean", suite.Mean()
print 'Median', suite.MaximumLikelihood()
print 'CI', suite.CredibleInterval(95)


print '\n*** Euro3 ****'
bata = thinkbayes.Beta()
bata.Update((140, 110))

print "Mean", bata.Mean()
print 'CI', suite.CredibleInterval(95)


# print '\n *** SToQ **** '
# class Stoq(Suite):
#     def Likelihood(self, data,hypo):

print '\n *** Coin practice ****'
class Coin(Suite):
    def Likelihood(self, data, hypo):
        y = 50/100.0
        x = hypo / 100.0
        if data == 'H':
            return x * (1- y) + (1-x)*y
        else:
            return (1 - x) * (1 - y) + x*y

suite = Coin(xrange(0,101))
dataset = 'H' * 140 + 'T' * 110
for data in dataset:
    suite.Update(data)

print "Mean", suite.Mean()
print 'Median', suite.MaximumLikelihood()
print 'CI', suite.CredibleInterval(95)


class Die(thinkbayes.Pmf):
    def __init__(self, sides):
        thinkbayes.Pmf.__init__(self)
        for x in xrange(1, sides+1):
            self.Set(x,1)
        self.Normalize()
d6 = Die(6)
dice = [d6] * 3
three = thinkbayes.SampleSum(dice, 10000)
for hypo, prob in three.Items():
    print hypo, prob
