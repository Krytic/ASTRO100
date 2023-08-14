# ASTRO 100 Tools

## New Semester Setup

This toolset assumes that you have a file entitled 'Current Students.csv' in the root directory (i.e., here). To get this file, follow these steps:

1. Click "People" on the LHS menu on Canvas.
2. Click the blue "Group set" button.
3. Enter a group name (e.g., "Lab Groups"). Leave all other settings as-is. Click save.
4. Click the grey "Import" button.
5. Click "Download Course Roster CSV" button. Save this file as "Current Students.csv" in this directory.

## Routines

### Lab Group Allocation

Run `main.py` inside the Lab Group Allocation folder. Configuration takes place in `LabData.ini`. You can configure students switching to different groups in this file in the `[switches]` section. For instance, if the student with upi `jbon007` switched into the third day of labs, and the student `aein356` switched into the second day of labs, you can configure LabData to be:

```
[switches]
jbon007=B03C
aein356=B02C
```

Notice that the days are encoded using the SSO format: B (meaning Lab) and then a two-width number indicating lab day (01/02/03) and then a C (meaning City Campus).

You can also change the email generated to students by editing `email_template` (it is set up to use my plain-text signature).

This generates a bunch of files:

- `Student_List.tex`: the admin list with all the students groups on it.
- `groups/`: A list of groups formatted Tuesday1/Thursday3/etc with email addresses on the first line and the email body on subsequent lines. **LPT**: email TO: yourself and BCC: students so they don't see everyone else's emails (and heads off a reply-all chain).
- `Lab Groups -- computed.csv`: the file to UPLOAD to Canvas to assign them groups on Canvas.

After this runs, you need to run `latexmk Student_List.tex` to render the PDF to print.

### Test Group Tools

This one is easy: configure `TestData.ini` to your liking. Then just run `MakeStudentList.py`.

This generates two files:
- `student_list.tex`: a list of every student allocated to each room,
- `student_rooms.tex`: the room signs.

You again need to `latexmk` them to render the PDFs.

### Utilities

This is just a directory of the signs that we use.

### Useful knowledge:

The hex codes for the signs etc (so everything is consistent):

- Experiment 1 Cobalt Blue: `#009ffd`
- Experiment 2 Pea Green: `#7ddf64`
- Experiment 3 Fuschia: `#ff007f`
- Experiment 4 Sunset Orange: `#ffa400`
- Experiment ? Royal Purple: `#9900ff`

The final one is a dummy for if we ever go back to five experiments.