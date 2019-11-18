from scipy import stats

def average(data):
    return sum(data) / len(data)

def pearson(x,y):
    return stats.pearsonr(x,y)


def ZoTtest(a,b):
    if len(a) > 100:
        return t_test(a,b)
    else:
        return z_test_right(a,b)

def t_test(a,b):
    if len(a) > len(b):
        N = len(b)
    else:
        N = len(a)
    sum = 0
    for i in range(N):
        diff = a[i] - b[i]
        sum = sum +diff
        square = square + diff**2

    numerator = sum/N
    bottom_d = (N-1)*N
    top_d = square - ((sum**2)/N)
    denominator = bottom_d/top_t
    denominator = denominator**0.5
    t = numerator/denominator
    return t

def z_test_right(a,b):
    a_ave = average(a)
    b_ave = average(b)

    #alpha of  0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1,  from z table
    z_critical = [0.496, 0.4920, 0.4880, 0.4840, 0.4801, 0.4761, 0.4721, 0.4681, 0.4641, 0.4602 ]

    a_std = numpy.std(a)
    b_std = numpy.std(b)

    z = a_ave - b_ave

    #z-test formula
    div = ((a_std**2)/len(a))+((b_std**2)/len(b))
    div = div**0.5
    z = z/div
    i = 0
    found = False
    #if z is greater than z_critical than a is significantly greater than b
    while (i < len(z_critical and found is False)):
        if z > z_critical:
            found = True
        else:
            i = i + 1
    if found == False:
        return -1
    else:
        if i < 11:
            reutrn (i+1)/100
        return 0.1