def my_iter():
    for i in range(5):
        yield i, i**2


print(list(zip(*my_iter())))

left, right = zip(*my_iter())
print(f"left: {left}")
print(f"right: {right}")
