from django.shortcuts import render

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import namedtuple
import os,sys
import datetime
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
from .models import Revenue 

def index(request):
	# Bar chart
	n_groups = 5

	maruti = (20, 35, 30, 35, 27)
	std_maruti = (2, 3, 4, 1, 2)

	honda = (25, 32, 34, 20, 25)
	std_honda = (3, 5, 2, 3, 3)

	fig, ax = plt.subplots()

	index = np.arange(n_groups)
	bar_width = 0.35

	opacity = 0.4
	error_config = {'ecolor': '0.3'}

	rev = Revenue.objects.all()

	rects1 = ax.bar(index, maruti, bar_width,
	                alpha=opacity, color='b',
	                yerr=std_maruti, error_kw=error_config,
	                label='Maruti')

	rects2 = ax.bar(index + bar_width, honda, bar_width,
	                alpha=opacity, color='r',
	                yerr=std_honda, error_kw=error_config,
	                label='Honda')

	ax.set_xlabel('Year')
	ax.set_ylabel('Units(in thousands)')
	ax.set_title('Yearwise sell of Maruti v/s Honda Car')
	ax.set_xticks(index + bar_width / 2)
	ax.set_xticklabels(('2013', '2014', '2015', '2016', '2017'))
	ax.legend()

	fig.tight_layout()
	if os.path.exists('dashboard/static/dashboard/images/bar.png'):
		os.remove('dashboard/static/dashboard/images/bar.png')
	plt.savefig('dashboard/static/dashboard/images/bar.png')		

	return render(request, 'dashboard/index.html')

def histogram(request):
	#Histogram
	np.random.seed(19680801)

	# example data
	mu = 100  # mean of distribution
	sigma = 15  # standard deviation of distribution
	x = mu + sigma * np.random.randn(437)

	num_bins = 50

	fig, ax = plt.subplots()

	# the histogram of the data
	n, bins, patches = ax.hist(x, num_bins, density=1)

	# add a 'best fit' line
	y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
	     np.exp(-0.5 * (1 / sigma * (bins - mu))**2))
	ax.plot(bins, y, '--')
	ax.set_xlabel('Smarts')
	ax.set_ylabel('Probability density')
	ax.set_title(r'Histogram of IQ: $\mu=100$, $\sigma=15$')

	# Tweak spacing to prevent clipping of ylabel
	fig.tight_layout()
	if os.path.exists('dashboard/static/dashboard/images/histogram.png'):
		os.remove('dashboard/static/dashboard/images/histogram.png')
	plt.savefig('dashboard/static/dashboard/images/histogram.png')

	return render(request, 'dashboard/hist.html')

def piechart(request):
	# Pie chart, where the slices will be ordered and plotted counter-clockwise:
	labels = 'Maruti', 'Honda', 'Hyundai', 'Ford'
	sizes = [45, 30, 15, 10]
	explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

	fig1, ax1 = plt.subplots()
	ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
	        shadow=True, startangle=90)
	ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

	if os.path.exists('dashboard/static/dashboard/images/pie.png'):
		os.remove('dashboard/static/dashboard/images/pie.png')
	plt.savefig('dashboard/static/dashboard/images/pie.png')

	return render(request, 'dashboard/pie.html')

def linegraph(request):	
	#Linegraph
	years = mdates.YearLocator()   # every year
	months = mdates.MonthLocator()  # every month
	yearsFmt = mdates.DateFormatter('%Y')

	# Load a numpy record array from yahoo csv data with fields date, open, close,
	# volume, adj_close from the mpl-data/example directory. The record array
	# stores the date as an np.datetime64 with a day unit ('D') in the date column.
	with cbook.get_sample_data('goog.npz') as datafile:
	    r = np.load(datafile)['price_data'].view(np.recarray)

	fig, ax = plt.subplots()
	ax.plot(r.date, r.adj_close)

	# format the ticks
	ax.xaxis.set_major_locator(years)
	ax.xaxis.set_major_formatter(yearsFmt)
	ax.xaxis.set_minor_locator(months)

	# round to nearest years...
	datemin = np.datetime64(r.date[0], 'Y')
	datemax = np.datetime64(r.date[-1], 'Y') + np.timedelta64(1, 'Y')
	ax.set_xlim(datemin, datemax)


	# format the coords message box
	def price(x):
	    return '$%1.2f' % x
	ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
	ax.format_ydata = price
	ax.grid(True)

	# rotates and right aligns the x labels, and moves the bottom of the
	# axes up to make room for them
	fig.autofmt_xdate()

	if os.path.exists('dashboard/static/dashboard/images/line.png'):
		os.remove('dashboard/static/dashboard/images/line.png')
	plt.savefig('dashboard/static/dashboard/images/line.png')

	return render(request, 'dashboard/line.html')