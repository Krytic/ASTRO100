import configparser
import os

import numpy as np
import pandas as pd
import os

config = configparser.ConfigParser()

config.read('LabData.ini')

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

metadata = dict(config['metadata'])

days = [metadata['day1'], metadata['day2'], metadata['day3']]
n_groups = int(metadata['n_groups'])
switches = dict(config['switches'])

group_nums = range(1, n_groups+1)

students = pd.read_csv('../Current Students.csv')

print(f'Streaming {len(students)} students into {n_groups} groups across {len(days)} days')

days = dict(enumerate(days))

group_cntrs = {
    day: 0
    for day in days.values()
}

with open('Student_List.tex', 'w') as file:
    file.write(fr"""\documentclass{{article}}

\usepackage[margin=1in]{{geometry}}
\usepackage{{booktabs}}
\usepackage{{longtable}}

\begin{{document}}
    \begin{{center}}
        {{\Huge\textbf{{ASTRO 100 Lab Groups}}}}

        {{\Large\textsc{{{len(students)} Students}}}}
    \end{{center}}
    \begin{{longtable}}{{@{{~~}}c|@{{~~}}c|c|c|c|c|c}}
        \toprule
        \textbf{{First Name}} & \textbf{{Last Name}} & \textbf{{Lab Group}} & \textbf{{Week 3}} & \textbf{{Week 5}} & \textbf{{Week 7}} & \textbf{{Week 9}} \\
        \midrule
        \endhead
        \bottomrule
        \endfoot
""")

    for i, row in students.iterrows():
        parts = row['sections'].split(" ")

        if row['login_id'] not in switches.keys():
            lab_day_code = [part for part in parts if part.startswith("B")][0]
        else:
            lab_day_code = switches[row['login_id']]

        lab_day_as_str = lab_day_code[1:3]

        lab_day = days[int(lab_day_as_str)-1]

        group_cntrs[lab_day] += 1

        student_group = lab_day + str(group_cntrs[lab_day])

        students.loc[i, 'group_name'] = student_group

        lastname, firstname = row['name'].split(',')

        start = group_cntrs[lab_day]
        for i in range(4):
            locals()[f'week{3+2*i}'] = (start-1+i)%4+1

        file.write(f"        {firstname} & {lastname} & {student_group} & {week3} & {week5} & {week7} & {week9} \\\\\n")

        if group_cntrs[lab_day] == n_groups:
            group_cntrs[lab_day] = 0

    file.write(r"""        \bottomrule
    \end{longtable}
\end{document}
""")

group_names = [k1+str(k2) for k1 in days.values() for k2 in group_nums]

df_summary = pd.DataFrame.from_dict({
    k: [0] for k in group_names
})

for group in group_names:
    with open(f'groups/{group}', 'w') as file:
        pass

upis = {g: '' for g in group_names}

for i, row in students.iterrows():
    upis[row['group_name']] += (row['login_id'] + "@aucklanduni.ac.nz; ")

    df_summary[row['group_name']] += 1

for group, upi in upis.items():
    upis[group] = upi.rstrip("; ")

for group in group_names:
    day = group[:-1]
    expt = group[-1]

    with open('email_template', 'r') as f:
        message_body = (f.read().replace('|group|', group)
                                .replace('|day|', day)
                                .replace('|expt|', expt))

    with open(f'groups/{group}', 'a') as file:
        file.write(rf'''{upis[group]}

{message_body}''')

students.to_csv('Lab Groups -- computed.csv', index=False)

print(len(students), 'students')

print("Done. Now run latexmk Student_List.tex to render the student list.")