import configparser
import subprocess

config = configparser.ConfigParser()
config.read('TestData.ini')

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

    students.sort(key=lambda x: x[1].lower())

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
        f.write(r"        {\Huge\textbf{" + meta['test_building'] + "-" + room.upper() + f" ({n} students)" + r"}} " + "\n")
        f.write(r"    \end{center}" + "\n")

        f.write(r"""    \begin{longtable}{c|@{~~}c|c|c|c|p{0.3\textwidth}}
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
    f.write(r"""\documentclass[a4paper]{article}

\usepackage[landscape]{geometry}
\usepackage{fancyhdr}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{anyfontsize}
\usepackage[dvipsnames]{xcolor}
\usepackage{soul}

\pagestyle{empty}
\pagecolor{JungleGreen}
\definecolor{RubyPurple}{HTML}{7B287D}
\sethlcolor{RubyPurple}

\begin{document}
    \fontsize{48pt}{48pt}\selectfont
    \bfseries
""")

    for room, people in data.items():
        f.write(r"""
    \begin{center}
        \vspace*{\fill}
        \begingroup\fontsize{64pt}{64pt}\selectfont ASTRO 100 TEST\endgroup \\
        {\fontsize{36pt}{36pt}\selectfont
        \vspace{3cm}
        """ + meta['test_building'] + "-" + room.upper() + r""" \\
        \vspace{3cm}
        Students with surname beginning with
        \textcolor{white}{\hl{""" + f"{people[0]} to {people[1]}" + r"""}} (inclusive)
        \vspace*{\fill}}
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

subprocess.run(['latexmk', '-pdf', '-shell-escape', 'student_list.tex'])
subprocess.run(['latexmk', '-f', '-c', 'student_list.tex'])
subprocess.run(['latexmk', '-pdf', '-shell-escape', 'student_rooms.tex'])
subprocess.run(['latexmk', '-f', '-c', 'student_rooms.tex'])