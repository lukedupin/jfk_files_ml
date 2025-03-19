import sys

for idx, line in enumerate(sys.stdin.readlines()):
    print(f'[{idx%2},"{line.strip()}"]')