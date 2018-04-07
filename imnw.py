"""
Is My Net Working? By Dr. Fayyaz Minhas, DCIS, PIEAS
Measure time for a google search (random)
Plot the time and its average in real-time
Save it to file

Run from terminal: bokeh serve imnw.py --show
"""

from bokeh.plotting import figure, curdoc
from bokeh.driving import linear
import urllib2
from timeit import default_timer as timer
from time import gmtime, strftime
import numpy as np
import datetime
from datetime import datetime as dt
from bokeh.models import DatetimeTickFormatter
from math import pi

wait = 10 #wait between samples
max_samples = np.inf #Number of samples to show in plot
avg_samples = 180 # Number of samples to use in averaging



def randS():
    t = dt.now()
    s = 'Pakistan '+str(t)
    query = urllib2.quote(s)
    url = "http://www.google.com/search?q=%s" % query
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    try:       
        start = timer()# ...
        html = opener.open(url,timeout = wait/2).read()
        end = timer()
#        with open("temp.html",'w') as f:
#            f.write(html)
        return t,end-start
    except urllib2.URLError:
        return t,wait

p = figure(title = "Google Search Access Time -- by Dr. Fayyaz Minhas",
       x_axis_label = "Time (UTC)",
       y_axis_label = "Access Time (s)",x_axis_type='datetime')#(plot_width=400, plot_height=400)

r1 = p.line([], [], color="firebrick", line_width=2,legend="Real-Time")
r2 = p.line([], [], color="navy", line_width=2,legend="Mean (0.5h)")

ds1 = r1.data_source
ds2 = r2.data_source


@linear()
def update(step):
    tx,sx = randS()
    with open("timing.txt",'a+') as f:
        f.write(str(tx)+"\t"+str(sx)+"\n")
    ds1.data['x'].append(tx)#(wait*step)
    ds1.data['y'].append(sx)
    if len(ds1.data['x'])>max_samples:
        ds1.data['x']=ds1.data['x'][-max_samples:]
        ds1.data['y']=ds1.data['y'][-max_samples:]
    ds1.trigger('data', ds1.data, ds1.data)
    ds2.data['x'].append(tx)
    ds2.data['y'].append(np.mean(ds1.data['y'][-avg_samples:]))
    if len(ds2.data['x'])>max_samples:
        ds2.data['x']=ds2.data['x'][-max_samples:]
        ds2.data['y']=ds2.data['y'][-max_samples:]
    ds2.trigger('data', ds2.data, ds2.data)

curdoc().add_root(p)

# Add a periodic callback to be run every 500 milliseconds
curdoc().add_periodic_callback(update, wait*1e3)