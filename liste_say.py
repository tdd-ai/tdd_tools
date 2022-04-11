from collections import Counter
listem = ["ve", "bir", "bir", "üç"]
print(Counter(listem))

var_sayi = [[x,listem.count(x)] for x in set(listem)]
print (var_sayi)