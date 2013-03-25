set term postscript enhanced color

set term postscript eps enhanced

set output 'Purity_TFIDF.eps'

set xlabel "Author Name"
set ylabel "Purity"

set key left bottom

plot "purity_TFIDF.txt" using 1 title "LapPLSA Purity" with linespoints, \
     "PLSA purity_TFIDF.txt" using 1 title "PLSA Purity" with linespoints