from collections import Counter
l=[1,1,2,2,2,3,3,3]
unique_list=[]
for i in l:
    if i not in unique_list:
        unique_list.append(i)

print([[x,l.count(x)] for x in set(l)])