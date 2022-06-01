global here_is_a_value



def add_one():
    here_is_a_value = 1
    here_is_a_value += 1
    return (here_is_a_value)

print(add_one())
print(here_is_a_value)
