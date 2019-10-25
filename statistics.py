from scipy import stats
import numpy

def average(data):
    return sum(data) / len(data)

def pearson(x,y):
    return stats.pearsonr(x,y)

def z_test_right(a,b):
    a_ave = average(a)
    b_ave = average(b)

    #alpha of 0.05 from z table
    z_critical = .4801

    a_std = numpy.std(a)
    b_std = numpy.std(b)

    z = a_ave - b_ave

    #z-test formula
    div = ((a_std**2)/len(a))+((b_std**2)/len(b))
    div = div**0.5
    z = z/div

    #if z is greater than z_critical than a is significantly greater than b
    if(z > z_critical):
        #if false than a is greater than b
        return False
    return True

