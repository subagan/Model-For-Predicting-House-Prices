import csv
import copy

ss_res = 'ss-res'
r_sq = 'r-sq'
r_sq_adj = 'r-sq-adj'
c = 'c'
aic = 'aic'
id = 'id'

DATA = []
with open('export.csv') as f:
    raw = csv.reader(f, delimiter=',')
    for i, row in enumerate(raw):
        if i == 0:
            continue

        DATA.append({
            id: i,
            r_sq: float(row[2]),
            r_sq_adj: float(row[3]),
            c: float(row[4]),
            aic: float(row[5])
        })

def merge(this, other, access=lambda x: x):
    this_index = 0
    other_index = 0
    res = []
    while True:
        this_out_of_range = this_index >= len(this)
        other_out_of_range = other_index >= len(other)

        if this_out_of_range and other_out_of_range:
            break
        this_candidate = not this_out_of_range and access(this[this_index])
        other_candidate = not other_out_of_range and access(other[other_index])
        if other_out_of_range:
            res.append(this[this_index])
            this_index += 1
        elif this_out_of_range:
            res.append(other[other_index])
            other_index += 1
        elif this_candidate < other_candidate:
            res.append(this[this_index])
            this_index += 1
        else:
            res.append(other[other_index])
            other_index += 1
    return res

def mergeSort(this, access=lambda x: x):
    if len(this) == 1:
        res = this
    else:
        half = len(this) // 2
        first = mergeSort(this[:half], access=access)
        second = mergeSort(this[half:], access=access)
        res = merge(first, second, access=access)
    return res

def rSqRanks():
    data = copy.deepcopy(DATA)
    return mergeSort(data, access=lambda x: x[r_sq])

def rSqAdjRanks():
    data = copy.deepcopy(DATA)
    return mergeSort(data, access=lambda x: x[r_sq_adj])

def cRanks():
    data = copy.deepcopy(DATA)
    return mergeSort(data, access=lambda x: x[c])

def aicRanks():
    data = copy.deepcopy(DATA)
    return mergeSort(data, access=lambda x: x[aic])

def countScore():
    scores = dict()

    for i in range (1, 8193):
        scores[i] = 0

    rank = 0
    current = 1

    lst = rSqRanks()
    lst.reverse()
    for ele in lst:
        if ele[r_sq] < current:
            current = ele[r_sq]
            rank += 1
        scores[ele[id]] += rank

    rank = 0
    current = 1
    lst = rSqAdjRanks()
    lst.reverse()
    for ele in lst:
        if ele[r_sq_adj] < current:
            current = ele[r_sq_adj]
            rank += 1
        scores[ele[id]] += rank

    rank=0
    current = 1
    lst = cRanks()
    print(lst)

    rank = 0


countScore()
