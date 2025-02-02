#!/usr/bin/python3
import argparse
import matplotlib
import numpy
import sys
from matplotlib import pyplot
import matplotlib.dates as mdates
from dateutil.parser import parse as parse_date

CHART_HEIGHT = 32
CHART_WIDTH = 16
PHASE1_MINUTES_COL = 11
PHASE2_MINUTES_COL = 15
PHASE3_MINUTES_COL = 19
PHASE4_MINUTES_COL = 23
TOTAL_TIME_MINUTES_COL = 27
COPY_TIME_MINUTES_COL = 31
DATE_COL = 1
GRID_ALPHA = 0.5
GRID_LINE_STYLE = 'dotted'
PLOT_TITLE_FONT_SIZE = 16
DOCUMENT_TITLE_FONT_SIZE = 24

parser = argparse.ArgumentParser(description="Create a PDF report from Chia logs")
parser.add_argument("-i", dest='csv_filename', type=str, help="CSV file generated by 'plotman export'")
parser.add_argument("-o", dest='save_to', type=str, help="PDF file to save to")
parser.add_argument("-t", dest='title', type=str, default='Plotting stats', help="Title, optional")
args = parser.parse_args()

if args.csv_filename is None or args.save_to is None:
	print("Error: you must specify arguments -i and -o at least")
	sys.exit(1)

def add_phase_chart(ax, vertical, horizontal, title):
	ax.plot(horizontal, vertical)

	# https://matplotlib.org/stable/gallery/text_labels_and_annotations/date.html
	ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
	ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
	ax.xaxis.set_tick_params(rotation=30)

	ax.grid(alpha=GRID_ALPHA, linestyle=GRID_LINE_STYLE)
	ax.set_xlabel('Period')
	ax.set_ylabel('Minutes')
	ax.set_title(title, fontsize=PLOT_TITLE_FONT_SIZE)

data = numpy.genfromtxt(args.csv_filename, delimiter=',', skip_header=1, dtype=str)
period = [ parse_date(el) for el in data[:,DATE_COL] ]
phase1 = [ int(el) for el in data[:,PHASE1_MINUTES_COL] ]
phase2 = [ int(el) for el in data[:,PHASE2_MINUTES_COL] ]
phase3 = [ int(el) for el in data[:,PHASE3_MINUTES_COL] ]
phase4 = [ int(el) for el in data[:,PHASE4_MINUTES_COL] ]
total_time = [ int(el) for el in data[:,TOTAL_TIME_MINUTES_COL] ]
copy_time = [ int(el) for el in data[:,COPY_TIME_MINUTES_COL] ]

# https://matplotlib.org/devdocs/gallery/subplots_axes_and_figures/subplots_demo.html
fig, (phase1_ax, phase2_ax, phase3_ax, phase4_ax, copy_time_ax, total_time_ax) = pyplot.subplots(6)

add_phase_chart(phase1_ax, phase1, period, 'Phase 1 duration')
add_phase_chart(phase2_ax, phase2, period, 'Phase 2 duration')
add_phase_chart(phase3_ax, phase3, period, 'Phase 3 duration')
add_phase_chart(phase4_ax, phase4, period, 'Phase 4 duration')
add_phase_chart(copy_time_ax, copy_time, period, 'Copy time')
add_phase_chart(total_time_ax, total_time, period, 'Total time')

pyplot.subplots_adjust(left=0.07, right=0.95, top=0.93, hspace=0.4)

fig.suptitle(args.title, fontsize=DOCUMENT_TITLE_FONT_SIZE)
fig.set_size_inches(CHART_WIDTH, CHART_HEIGHT)
fig.savefig(args.save_to)
