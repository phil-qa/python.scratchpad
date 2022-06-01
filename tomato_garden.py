import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
'''
given a garden with crops and days per crop available and the number of tomatoes needed to make soup, how long before you can make soup'''

crops, tomatoes, delay = [int(i) for i in input().split()]
garden = [int(i) for i in input()]
garden=[i-delay for i in garden]
if sum(1 for i in garden if i<=0)>=tomatoes:
    print(f"YOU_CAN_MAKE_A_SOUP_IN_{delay}_DAYS")
else:
    print(f"YOU_CANNOT_MAKE_A_SOUP_IN_{delay}_DAYS")

