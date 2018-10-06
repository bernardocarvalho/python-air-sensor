#set terminal wxt
set terminal aqua
set xdata time
#set timefmt "%Y-%m-%d %H:%M:%S.%*6[^\n]"
set timefmt "%Y-%m-%d %H:%M:%S"
set format x "%H:%M"
set datafile separator ";"
#set yrange [0.0:0.5] 
set title 'Air quality 06/10/2018 Av EUA 112-8'

set ylabel "Particles / ug/m^3"
#set size 1.0,0.7
#set origin 0.0,0.3
plot 'sensor.log.aveua_outdoor_06_10_fire' u 1:2 w l t '2.5' , '' u 1:3 w l t '10', \
    '' u 1:4 t 'Temperature'


