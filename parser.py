import toml
import re
import os

with open("data.toml") as f:
    parsed_toml = toml.load(f)

# print(parsed_toml)

for file_name in os.listdir("templates"):
    with open("templates/{}".format(file_name)) as f:
        test_string = f.read()

    # test_string = r"""
    # \usepackage[top=0.5in, bottom=0.5in, left=0.5in, right=0.5in]{geometry}
    # \usepackage{enumitem}

    # <<< ~Education~ ~institute~ ~location~
    # >>
    # \begin{document}
    # \begin{center}
    # \thispagestyle{empty}
    # \large \textbf{ <<name>> \\}
    # \normalsize <<email>> $\mid$ <<phone>> $\mid$ <<website>>    \\
    # \hrulefill
    # \end{center}
    # """

    # print(test_string)

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
                def sweepvalues(mo: re.Match):
                    nonlocal i
                    rt = values[i]
                    i += 1
                    return str(rt)
                ret.append(re.sub("~(.*?)~", sweepvalues, mtext, flags=re.S))
                # print(ret)
            return "\n".join(ret)
        return parsed_toml[mtext]

    test_string = re.sub("<<(.*?)>>", replacer, test_string, flags=re.S)

    with open("outputs/{}".format(file_name), "w") as f:
        f.write(test_string)
