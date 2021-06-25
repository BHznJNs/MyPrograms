origin_list = [3, 8, 51, 60, 7, 31, 25, 59, 15, 40]

for i in range(1, len(origin_list)):
    for j in range(0, len(origin_list) - i):
        if origin_list[j] > origin_list[j+1]:
            origin_list[j], origin_list[j+1] = origin_list[j+1], origin_list[j]
print(origin_list)  
