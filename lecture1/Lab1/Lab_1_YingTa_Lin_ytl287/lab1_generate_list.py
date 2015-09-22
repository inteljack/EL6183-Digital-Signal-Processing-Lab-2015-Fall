import random
import sorting

pool = range(1,101)
alist = random.sample(pool,9)
print(alist)
alist1 = alist
sorting.insertionSort(alist1)
print "insertion sort:",alist1
alist2 = alist
sorting.bubbleSort(alist2)
print "bubble sort:", alist2
