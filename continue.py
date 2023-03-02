# This demonstrates continue, break, and return


def print_even():
    for i in range(10000):
        if i % 2 == 1:
            continue
        print(i)
        if i >= 20:
            #break
            return

print_even()
