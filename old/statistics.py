from scipy import stats

def average(data):
    return sum(data) / len(data)

def pearson(x,y):
    return stats.pearsonr(x,y)