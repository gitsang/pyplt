#!/usr/bin/python

ls = ['a', 'b', 'c', 'd', 'e']
print(ls)
for name in ls:
    print(name)
    print(f'{name} good')

for name in ls:
    print(f'{name} is my')

for value in range(1, 5):  # range用来生成系列数（到最后一个数时终止， 所以是不包括最后一个， 只有1,2,3,4
    for value2 in range(11, 15):
        print(f'{value}{value2}')

numbers = list(range(1, 3))
print(numbers)

even_numbers=list(range(2,11,2))
print(even_numbers)

dig_lists = [1, 2, 3, 4, 5, 6, 7, 8]
print(min(dig_lists))
print(max(dig_lists))
print(sum(dig_lists))
print(dig_lists[0:2])
print(dig_lists[:3])
print(dig_lists[0:])
print(dig_lists[-1:])
