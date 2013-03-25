set term postscript enhanced color

set term postscript eps enhanced

set output 'sim.eps'

set xlabel "Author Name"
set ylabel "Sim Ratio"

plot "doc_sim.txt" using 3 title "Cos-word" with linespoints, \
     "intent_sim.txt" using 3 title "Cos-Intent" with linespoints