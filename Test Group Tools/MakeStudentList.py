import configparser

config = configparser.ConfigParser()
config = config.read('TestData.ini')

def get_students_in_band(start, end):
    start, end = start.lower(), end.lower()
    ran = tuple(chr(ord(start) + i) for i in range(0, ord(end)-ord(start)+1))

    students = []

    with open('../Current Students.csv', 'r') as f:
        f.readline()

        for line in f.readlines():
            if not line[1:].lower().startswith(ran):
                continue

            student = line.split(",")[0:-1]

            student = [student[i].lstrip().rstrip().lstrip('"').rstrip('"') for i in range(4)]

            student[0], student[1] = student[1], student[0]

            students.append(student)

    return students

data = dict(config['rooms'])
meta = dict(config['metadata'])

with open('student_list.tex', 'w') as f:
    f.write(r"""\documentclass{article}

\usepackage[margin=1in]{geometry}
\usepackage{booktabs}
\usepackage{longtable}

\begin{document}
""")
    for room, name_range in data.items():
        students = get_students_in_band(*name_range)

        student_data = ""
        for student in students:
            student_data += ' ' * 8 + ' & '.join(student) + ' & \\\\\n'

        n = len(students)

        f.write(r"    \begin{center}" + "\n")
        f.write(r"        {\Huge\textbf{" + meta['test_building'] + "-" + room + f" ({n} students)" + r"}} " + "\n")
        f.write(r"    \end{center}" + "\n")

        f.write(r"""    \begin{longtable}{c|@{~~}c|c|c|c|c}
        \toprule
        \textbf{First Name} & \textbf{Last Name} & \textbf{UPI} & \textbf{Student ID} & \textbf{Has ID?} & \textbf{Notes} \\
        \midrule
        \endhead
        \bottomrule
        \endfoot
""")

        f.write(student_data.rstrip())

        f.write(r"""
        \bottomrule
    \end{longtable}

    \newpage

""")

    f.write(r"\end{document}")

with open('student_rooms.tex', 'w') as f:
    f.write(r"""\documentclass{article}

\usepackage[landscape]{geometry}
\usepackage{fancyhdr}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}

\pagestyle{empty}

\begin{document}
    \fontsize{48pt}{48pt}\selectfont
    \bfseries
""")

    for room, people in data.items():
        f.write(r"""
    \begin{center}
        \vspace*{\fill}
        ASTRO 100 TEST \\
        \vspace{3cm}
        """ + meta['test_building'] + "-" + room + r""" \\
        \vspace{3cm}
        """ + f"{people[0]}-{people[1]}" + r"""
        \vspace*{\fill}
    \end{center}

    \newpage
    """)

    f.write("\n" + r"\end{document}")

# with open('in_use.tex', 'w') as f:
#     f.write(r"""\documentclass{article}

# \usepackage[landscape]{geometry}
# \usepackage{fancyhdr}
# \usepackage[utf8]{inputenc}
# \usepackage[T1]{fontenc}

# \pagestyle{empty}

# \begin{document}
#     \fontsize{56pt}{56pt}\selectfont
#     \bfseries
# """)

#     for room, people in data.items():
#         f.write(r"""
#     \begin{center}
#         \vspace*{\fill}
#         Test in progress
#         \vspace*{\fill}
#     \end{center}

#     \newpage
#     """)

#     f.write("\n" + r"\end{document}")