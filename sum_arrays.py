import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
'''
n = int(input())
figs = [map(int(), input().split())]
print (figs)
'''


# Write an answer using print
# To debug: print("Debug messages...", file=sys.stderr, flush=True)



import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

n = int(input())
# for i in input().split():
#     number = int(i)

# Write an answer using print
# To debug: print("Debug messages...", file=sys.stderr, flush=True)

print(sum(sum(int(j) for j in str(i)) for i in input().split()))

