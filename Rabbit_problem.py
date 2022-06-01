import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

r = int(input())
D = int(input())
B = int(input())

a,b,c,d=0,0,0,r
for _ in ' '*(D-1):
    a,b,c,d=b,c,d,(b+c)*B
print(a+b+c+d)


'''
import sys
import math

rabbits between 2-3 days reproduce the number of babies

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

rabbit = int(input())
day = int(input())
babies = int(input())

rabbits =[]
for i in range(rabbit):
    rabbits.append(1)
count = len(rabbits)
while rabbits:
    #print(rabbits)
    if rabbits.count(4) > 0:
        rabbits.remove(4)
    reproductive = rabbits.count(2)+rabbits.count(3)
    for newrabbits in range(reproductive): 
        for multiplier in range(babies):
            rabbits.append(0)
            count += 1
    rabbits = [n+1 for n in rabbits]
    
# Write an answer using print
# To debug: print("Debug messages...", file=sys.stderr, flush=True)

print(count)

'''