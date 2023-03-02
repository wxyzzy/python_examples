# real-world use of re (regex) and yield
# parts courtesy of Henrik Tunedal


import re


def parse_ranges(text):
    "interpret comma separated intervals and whole numbers."
    pat = re.compile(r"^ *([0-9]+) *(- *[0-9]+)? *$")
    for r in text.strip(", ").split(","):
        m = pat.match(r)
        if not m:
            raise ValueError("Incorrect format: " + repr(r.strip()))
        start = int(m.group(1))
        end = int(m.group(2)[1:]) if m.group(2) else start
        if (start > end):
            raise ValueError("Incorrect ordering of interval: " + r.strip())
        for i in range(start, end + 1):
            yield i


def parse_and_print(text):
    print(', '.join([str(i) for i in parse_ranges(text)]))


print('Enter ranges separated by commas (1-3, 7, 8)')
done = False
while not done:
    text = input(': ')
    if text == '':
        done = True
    else:
        try:
            parse_and_print(text)
        except Exception as e:
            print(e)
print('done')