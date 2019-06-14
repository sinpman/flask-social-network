a=int('1')
a1=[]
count=int(0)
for i in 'abcab':
    a1.append(i)

for i in a1:
     count=count+1


for i in range(count):
    # for j in range(count,0):
    print(a1[i])
    if(i!=1):
        if(a1[i]==a1[0]):
            print(a1[0])

    # print(i)