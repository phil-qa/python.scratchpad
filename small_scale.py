'''
convert string list to integer list
'''
test_list = ['1', '4', '3', '6', '7']

# Printing original list
print("Original list is : " + str(test_list))

# using map() to
# perform conversion
test_list = list(map(int, test_list))

# Printing modified list
print("Modified list is : " + str(test_list))

test_list = list(map(float, test_list))
print("Modified list to float : " + str(test_list))

# cast to list a map of floats against a target list

'''
Average of a list 
'''
number_list = [45, 34, 10, 36, 12, 6, 80]
avg = sum(number_list)/len(number_list)
print("The average is ", round(avg,2))


'''
list comprehension
'''
# Iterate over a string using list comprehension
h_letters = [ letter for letter in 'human' ]
print( h_letters)

# same thing with lambda
letters = list(map(lambda x: x, 'human'))
print(letters)

# or
f = (lambda x: list(x))
print(f('human'))

'''
Remove all digits from a string'''
s = "T4ex5t w9ith 9numerals"
print("".join(filter(lambda x: not x.isdigit(), s)))

'''
convert and load to positions as integers this is an unpack and needs exact mapping
'''
values = '100 200'
n,m = map(int,values.split())
print (n, m)

''' 
Search in list for item in class return the first
'''
next((x for x in test_list if x.value == value), None)