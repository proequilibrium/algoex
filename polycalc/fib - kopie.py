def fibonacci(limit):
    a = 0
    b = 1
    count = 0
    while b < limit:
        yield b
        count += 1
        a, b = b, a + b
    return count

def fib_annotated():
    count = (yield from fibonacci(10))
    print('LOG: Generated {} numbers'.format(count))

for value in fib_annotated():
    print('Got', value)
