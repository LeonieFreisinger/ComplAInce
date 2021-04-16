with open('gifts_raw.md', 'r') as file:
    raw = file.read()

raw = raw.split('\n')
raw = [el for el in raw if not el == '']
print(len(raw))

for el in raw:
    # check if line is headline
    if el[0] == '#':
        