with open("dict_1.log", "r") as f:
    l_1 = f.readlines()

l_c = []

for i in l_1:
    l_c.append(i.split(",")[0][1:])

#print(l_c)

dict_1 = {}
for dex, i in enumerate(l_1):
    dict_1[i.split(",")[0][1:]] = [dex]

#print(dict_1)


with open("dict_4.log", "r") as f:
    l_4 = f.readlines()

for dex, i in enumerate(l_4):
    if dict_1.get(i.split(",")[0][1:]):
        dict_1[i.split(",")[0][1:]].append(dex)
        #dict_1[i.split(",")[0][1:]] = [0]
        #print(dict_1[i.split(",")[0][1:]])
        #dict_1[i.split(",")[0][1:]].append(dex)
        #print(dict_1[i.split(",")[0][1:]])

dict_2 = {}
for k,v in dict_1.items():
    try:
        dict_2[k] = v[1] - v[0]
    except Exception as e:
        if l_c.index(k) < 100:
            print(k)
        

ll = sorted(dict_2.items(), key=lambda x:x[1], reverse=True)
for i in ll:
    #print(l_1)
    if (i[1] > 0) and (l_c.index(i[0]) < 100):
        print(i, l_c.index(i[0]))
    #print(i)
