target_fibonnaci = int(input())

# Write an answer using print
# To debug: print("Debug messages...", file=sys.stderr, flush=True)


a = b = 1
fibonacci_position = 1

while a != target_fibonnaci:
    a, b = b, a+b
    print(a,b)
    fibonacci_position += 1
print(f"{fibonacci_position} is value {a}")

