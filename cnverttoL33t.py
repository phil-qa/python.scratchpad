import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

s = input()
a = dict(O='0', L='1', Z='2', E='3', A='4', S='5', G='6', T='7', B='8', Q='9')
# Write an answer using print
# To debug: print("Debug messages...", file=sys.stderr, flush=True)


b = ''
for i in s:
    if i.capitalize() in a:
        b = b + a[i.capitalize()]
    else:
        b = b + i
print(b)