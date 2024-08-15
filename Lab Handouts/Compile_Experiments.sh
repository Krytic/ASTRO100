# rm -rf handouts
mkdir -p handouts/solutions
mkdir -p handouts/covers

for EXPT in 1 2 3 4
do
    latexmk -shell-escape -pdf Experiment_${EXPT}.tex
    latexmk -f -c Experiment_${EXPT}.tex

    mv Experiment_${EXPT}.pdf handouts/solutions/Experiment_${EXPT}.pdf

    python GenerateSolutionFile.py --file Experiment_${EXPT}

    latexmk -shell-escape -pdf Experiment_${EXPT}.tex
    latexmk -f -c Experiment_${EXPT}.tex

    mv Experiment_${EXPT}.pdf handouts/Experiment_${EXPT}.pdf

    python GenerateSolutionFile.py --file Experiment_${EXPT}
done

pdftk handouts/Experiment_1.pdf cat 1 output handouts/covers/Experiment_1.pdf
pdftk handouts/Experiment_2.pdf cat 1 output handouts/covers/Experiment_2.pdf
pdftk handouts/Experiment_3.pdf cat 1-2 output handouts/covers/Experiment_3.pdf
pdftk handouts/Experiment_4.pdf cat 1 output handouts/covers/Experiment_4.pdf

# pdftk full-pdf.pdf cat 12-15 output outfile_p12-15.pdf