import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--file')

args = parser.parse_args()

new_file_lines = []

with open(f"{args.file}.tex", 'r') as f:
    for line in f.readlines():
        # line = line.strip()
        if line.strip().endswith(r'\printanswers'):
            if line.strip().startswith("%"):
                # disable it
                line = line.strip()[1:].strip()
            else:
                # enable it
                line = f"% {line.strip()}"

        new_file_lines.append(line.rstrip())
    new_file = "\n".join(new_file_lines)

    # print(new_file)

with open(f"{args.file}.tex", 'w') as f:
    f.seek(0)
    f.write(new_file)