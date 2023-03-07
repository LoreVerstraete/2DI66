# queue = [[],[],[]]
# queue[0].append(1)
# print(queue)
# print(len(queue[0]))

CustomerINFO= {0: [4,1,5, 'cash'], 1: [9, 6, 15, 'card'], 2: [12, 2, 14, 'card']}
sorted_customer_info = sorted(CustomerINFO.items(),key=lambda item: (item[1][2]))

# print(type(sorted_customer_info[1]))
print(sorted_customer_info)
print(sorted_customer_info[1][0])
# kkey = list(sorted_customer_info.keys())
# print(kkey[1])
# print(sorted_customer_info[0][1].append(5454))
# # sorted_customer_info[2].append(5454545)
# print(sorted_customer_info)