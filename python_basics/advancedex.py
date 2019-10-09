

def sortt(list):
    #for all elements in the list
    for i in range(len(list)-1, 0, -1):
        for j in range(i):
            if list[j] > list[j+1]:
                temp = list[j]
                list[j] = list[j+1]
                list[j+1] = temp


list = [1, 4, 5, 2, 8, 3]

sortt(list)

print(list)