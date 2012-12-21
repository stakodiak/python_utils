import random
from math import *

def mean(xs):
    return sum(xs)/float(len(xs))

def median(xs):
    mp = int(len(xs)/2)
    if len(xs) % 2 == 1:
        return sorted(xs)[mp]
    else:
        return mean(sorted(xs)[mp-1:mp+1])
    
def variance(xs,correct=True):
    n = len(xs)
    correction = n/float(n-1) if correct else 1
    return correction * mean([x**2 for x in xs]) - mean(xs) ** 2    

def zipWith(f,xs,ys):
    return map(lambda(x,y):f(x,y),zip(xs,ys))

def transpose(xxs):
    return zip(*xxs)

def normalize(xs):
    total = float(sum(xs))
    return [x/total for x in xs]

def frequencies(xs):
    length = float(len(xs))
    return [xs.count(x)/length for x in set(xs)]

def verbose_gen(xs,modulus=1):
    for i,x in enumerate(xs):
        if not i % modulus:
            print i
        yield x
        
def h(ps):
    return -sum([p * log2(p) for p in ps])
print "loaded utils"

def safe_log2(x):
    """Implements log2, but defines log2(0) = 0"""
    return math.log(x,2) if x > 0 else 0

def group_by(xs,n):
    return [xs[i:i+n] for i in range(0,len(xs),n)]
    
def split_on(xs, pred):
    """Split xs into a list of lists each beginning with the next x
    satisfying pred, except possibly the first"""
    indices = [i for (i,v) in enumerate(xs) if pred(v)]
    return [xs[i:j] for (i,j) in zip([0]+indices,indices+[len(xs)]) if i != j]

def separate(pred, lst):
    """separates lst into a list of elements satisfying pred and a list of 
    elements not satisfying it.
    """
    sheep = []
    goats = []
    for elem in lst:
        if pred(elem):
            sheep.append(elem)
        else:
            goats.append(elem)
    return (sheep, goats)

def nmers(n):
    if n == 1:
        return ["A","C","G","T"]
    else:
        return sum([map(lambda(b):b+c,nmers(n-1)) for c in base_pair_ordering],[])

def complement(base):
    return {"A":"T","T":"A","G":"C","C":"G"}[base]
    
def wc(word):
    return "".join(map(complement, word[::-1]))

def pprint(x):
    for row in x:
        print row

def choose2(xs,gen=False):
    """return list of choose(xs, 2) pairs, retaining ordering on xs"""
    if gen:
        return ((x1, x2) for i, x1 in enumerate(xs) for x2 in xs[i+1:])
    else:
        return [(x1, x2) for i, x1 in enumerate(xs) for x2 in xs[i+1:]]

def pairs(xs):
    return zip(xs[:-1],xs[1:])

def partition(pred, xs):
    part = []
    appended = False
    for x in xs:
        appended = False
        for p in part:
            if pred(x,p[0]):
                p.append(x)
                appended = True
                break
        if not appended:
            part.append([x])
    return part

def foldl(f,z,xs):
    if not xs:
        return z
    else: 
        return foldl(f,f(z,xs[0]),xs[1:])

def foldl1(f,xs):
    return foldl(f,xs[0],xs[1:])

def choose(n,k):
    return factorial(n)/(factorial(k) * factorial(n-k))

def concat(xxs):
    return sum(xxs,[])

def mmap(f,xxs):
    return [map(f,xs) for xs in xxs]

# naive implementation borrowed from stack overflow

def levenshtein(seq1, seq2):
    oneago = None
    thisrow = range(1, len(seq2) + 1) + [0]
    for x in xrange(len(seq1)):
        twoago, oneago, thisrow = oneago, thisrow, [0] * len(seq2) + [x + 1]
        for y in xrange(len(seq2)):
            delcost = oneago[y] + 1
            addcost = thisrow[y - 1] + 1
            subcost = oneago[y - 1] + (seq1[x] != seq2[y])
            thisrow[y] = min(delcost, addcost, subcost)
    return thisrow[len(seq2) - 1]

def sample(n,xs,replace=True):
    if replace:
        return [random.choice(xs) for i in range(n)]
    else:
        ys = xs[:]
        samp = []
        for i in range(n):
            y = random.choice(ys)
            samp.append(y)
            ys.remove(y)
        return samp

def fast_sample(n,xs):
    """Sample without replacement for large xs"""
    samp = []
    while len(samp) < n:
        x = random.choice(xs)
        if not x in samp:
            samp.append(x)
    return samp

def matrix_mult(A,B):
    """Given two row-major matrices as nested lists, return the matrix
    product"""
    return [[sum(A[i][k] * B[k][j] for k in range(len(A[0])))
             for j in range(len(B[0]))]
            for i in range(len(A))]

def iterate(f,x,n):
    if n == 0:
        return x
    else:
        return iterate(f,f(x),n-1)

def iterate_list(f,x,n):
    if n == 0:
        return [x]
    else:
        return  [x] + iterate_list(f,f(x),n-1)
    
def converge(f,x,verbose=False,i=0):
    if verbose:
        print i
    y = f(x)
    if y == x:
        return x
    else:
        return converge(f,y,verbose=verbose,i=i+1)

def converge2(f,x,verbose=False,i=0):
    y = f(x)
    while not y == x:
        if verbose:
            print i
            i += 1
        x = y
        y = f(x)
    return y

def converge_list(f,x):
    y = f(x)
    history = [x,y]
    while not y == x:
        x = y
        y = f(x)
        history.append(y)
    return history

def data2csv(data, filename, sep=", ",header=None,overwrite=False):
    import os
    make_line = lambda row: sep.join([str(field) for field in row]) + "\n"
    if filename in os.listdir('.') and not overwrite:
        print "found ",filename
        pass
    with open(filename, 'w') as f:
        if header:
            f.write(make_line(header))
        f.write("".join([make_line(row) for row in data]))

def dot(u,v):
    return sum(zipWith(lambda x,y:x*y,u,v))

def norm(u):
    return sqrt(dot(u,u))

def cosine_distance(u,v):
    return dot(u,v)/(norm(u)*norm(v))

<<<<<<< HEAD
def l2(xs,ys):
    return sum(zipWith(lambda x,y:(x-y)**2,xs,ys))

def linf(xs,ys):
    return max(zipWith(lambda x,y:abs(x-y),xs,ys))

def takeWhile(p,xs):
    if not xs or not p(xs[0]):
        return []
    else:
        return [xs[0]] + takeWhile(p,xs[1:])

def signum(x):

    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0
    
def bisect_interval(f,xmin,xmax,ymin=None,ymax=None,tolerance=1e-10):
    print xmin,xmax,ymin,ymax
    if ymin is None:
        ymin = f(xmin)
    if ymax is None:
        ymax = f(xmax)
    assert(sign(ymin)!= sign(ymax)), "ymin=%s,ymax=%s" % (ymin,ymax)
    x = (xmin + xmax)/2.0
    y = f(x)
    if abs(y) < tolerance:
        return x
    else:
        if sign(y) == sign(ymin):
            return bisect_interval(f,x,xmax,ymin=y,ymax=ymax,tolerance=tolerance)
        else:
            return bisect_interval(f,xmin,x,ymin=ymin,ymax=y,tolerance=tolerance)

def secant_interval(f,xmin,xmax,ymin=None,ymax=None,tolerance=1e-10):
    #print xmin,xmax,ymin,ymax
    if ymin is None:
        ymin = f(xmin)
    if ymax is None:
        ymax = f(xmax)
    assert(sign(ymin)!= sign(ymax)), "ymin=%s,ymax=%s" % (ymin,ymax)
    m = (ymax - ymin)/(xmax - xmin)
    x = xmax - ymax/m
    y = f(x)
    if abs(y) < tolerance:
        return x
    else:
        if sign(y) == sign(ymin):
            return secant_interval(f,x,xmax,ymin=y,ymax=ymax,tolerance=tolerance)
        else:
            return secant_interval(f,xmin,x,ymin=ymin,ymax=y,tolerance=tolerance)

        
def secant_interval_robust(f,xmin,xmax,ymin=None,ymax=None,tolerance=1e-10,p=0.1):
    #print xmin,xmax,ymin,ymax
    if ymin is None:
        ymin = f(xmin)
    if ymax is None:
        ymax = f(xmax)
    assert(sign(ymin)!= sign(ymax)), "ymin=%s,ymax=%s" % (ymin,ymax)
    if random.random() > p:
        m = (ymax - ymin)/(xmax - xmin)
        x = xmax - ymax/m
    else:
        x = (xmax + xmin)/2.0
    y = f(x)
    if abs(y) < tolerance:
        return x
    else:
        if sign(y) == sign(ymin):
            return secant_interval_robust(f,x,xmax,ymin=y,ymax=ymax,tolerance=tolerance,p=p)
        else:
            return secant_interval_robust(f,xmin,x,ymin=ymin,ymax=y,tolerance=tolerance,p=p)

def percentile(x,xs):
    return len(filter(lambda y:y > x,xs))/float(len(xs))

def normal_model(xs):
    mu = mean(xs)
    sigma = sqrt(variance(xs))
    return [random.gauss(mu,sigma) for x in xs]


def myrange(start,stop,step):
    return map(lambda x: start + (x-start)*step + start,
               range(start,int(stop/step)))

def grad_descent(f,x,y,ep_x=0.0001,ep_y=0.0001):
    "minimize f"
    z = f(x,y)
    best_z = None
    epsilon_shrinkage = 1
    while best_z is None or z <= best_z or True:
        z = best_z 
        choices = [(x + ep_x,y),(x - ep_x,y),(x,y + ep_y),(x,y - ep_y)]
        z_choices = map(lambda (x,y):f(x,y),choices)
        choice = min(zip(choices,z_choices),key=lambda(z,z_ch):z_ch)
        (x,y),best_z = choice
        ep_x *= epsilon_shrinkage
        ep_y *= epsilon_shrinkage
        print x,y,log(best_z),ep_x,ep_y
    return x,y
