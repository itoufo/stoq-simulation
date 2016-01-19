from thinkbayes import Pmf
from thinkbayes import Suite
import thinkbayes
import random

print '\n *** Stoq **** '
class Question(Pmf):

    def __init__(self):
        self.rate = random.random()
        print "Rate", self.rate

    def lookup(self, x):
        p = self.rate
        result =  float((1.0-p) * x + (3.0 * p -1.0)/2.0)
        return float(result)
    def reverse(self, y):
        p = self.rate
        result =  float((2.0*y - 3.0*p + 1.0)/(2.0 * (1.0-p)))
        return float(result)
    def a(self):
        p = self.rate
        return(1.0-p)
    def b(self):
        p = self.rate
        return (3.0 * p -1.0)/2.0

class User(Suite):
    def __init__(self):
        Suite.__init__(self, xrange(0, 101))
        # for x in xrange(1, 101):
        #     self.Set(x, 1)
        # self.Normalize()
        self.real_val = thinkbayes.Beta().Random()

    def Likelihood(self, data, hypos):
        question = data["question"]
        result = data["result"]
        if result:
            like = question.lookup(hypos/100.0)
        else:
            like = 1.0 - question.lookup(hypos/100.0)
        print "like,", like
        return like


user = User()

print "Actual,", user.real_val
print "Mean,", user.Mean()
print 'Median,', user.MaximumLikelihood()
print 'CI,', user.CredibleInterval(95)

for i in range(1, 1001):
    question = Question()
    print question.rate
    print "question, a=", question.a(), "b=",question.b(), "p=", question.rate
    rand = thinkbayes.Beta().Random()
    result = (rand < question.lookup(user.real_val))
    print result
    data = dict(result=result,  question=question)
    user.Update(data)
    print "Actual,", user.real_val
    print "Mean,", user.Mean()
    print 'Median,', user.MaximumLikelihood()
    print 'CI,', user.CredibleInterval(95)