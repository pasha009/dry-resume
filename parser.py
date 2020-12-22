import os
import re
import sys
import subprocess
import toml

with open("data.toml") as f:
    parsed_toml = toml.load(f)

# print(parsed_toml)
in_file_name = sys.argv[1]
base_dir = os.path.dirname(in_file_name)
splitted = in_file_name.split(".")
out_file_name = "".join(splitted[:-1]) + "_out." + splitted[-1]

print(base_dir)
print(in_file_name)
print(out_file_name)

with open(in_file_name) as f:
    test_string = f.read()

def replacer(mo: re.Match):
    mtext = mo.group(0)
    # remove delimiter << and >>
    mtext = mtext[2:]
    mtext = mtext[:-2]
    if mtext[0] == "<":
        mtext = mtext[1:]
        fields = re.findall("~(.*?)~", mtext, flags=re.S)
        category = fields[0]
        fields = fields[1:]
        mtext = re.sub("~(.*?)~", "", mtext, count=1, flags=re.S)
        # mtext = re.sub("~(.*?)~", "{}", mtext, flags=re.S)
        # print(mtext)
        ret = []
        for obj in parsed_toml[category]:
            values = [obj[field] for field in fields]
            i = 0

            def sweepvalues(_: re.Match):
                nonlocal i
                rt = values[i]
                i += 1
                return str(rt)

            ret.append(re.sub("~(.*?)~", sweepvalues, mtext, flags=re.S))
            # print(ret)
        return "\n".join(ret)
    return parsed_toml[mtext]


test_string = re.sub("<<(.*?)>>", replacer, test_string, flags=re.S)

with open(out_file_name, "w") as f:
    f.write(test_string)

out_file_name = os.path.basename(out_file_name)
subprocess.run(["pdflatex", out_file_name], cwd=base_dir)
