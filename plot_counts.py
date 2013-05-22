#!python3

from tkinter import *
import math


def plot(cts, fname='', threshold=False):
    '''
    Plots a binned count distribution using Tkinter. Optional parameters to
        save the plot as .ps or to highlight large-sigma deviations.

    Parameters:
    cts : An NxN array representing either
        (a) the bubble counts in each of the N^2 detectors, or
        (b) the difference, in standard deviations between the counts in two
            sets of detectors
    fname : an optional filename to save the resulting plot
    threshold : optional boolean to turn on highlighting of large-sigma deviations
    '''
    root = Tk()
    cv = Canvas(width=1000, height=1000, bg='white')
    cv.pack(expand=YES, fill=BOTH)
    n = len(cts[0])     # the number of detectors on a side
    s = int(1000//n)    # the side length of a single detector on the canvas

    counts = []
    for l in cts:
        counts.extend(l)

    min_ct = min(counts)        # minimum value for color scaling
    max_ct = max(counts)        # maximum value for color scaling
    ct_rg = max_ct - min_ct     # range for color scaling

    if threshold:
        anomalies = 0           # count the number of deviations with sigma >= 2
        for i in range(n):      # for each column
            for j in range(n):  # for each row
                if math.fabs(cts[i][j]) >= 4:       # if greater than 4 sigmas
                    cv.create_rectangle(i*s, j*s, (i+1)*s, (j+1)*s, fill='red')
                    anomalies += 1
                elif math.fabs(cts[i][j]) >= 3:     # if greater than 3 sigmas
                    cv.create_rectangle(i*s, j*s, (i+1)*s, (j+1)*s, fill='orange')
                    anomalies += 1
                elif math.fabs(cts[i][j]) >= 2:     # if greater than 2 sigmas
                    cv.create_rectangle(i*s, j*s, (i+1)*s, (j+1)*s, fill='yellow')
                    anomalies += 1
                else:                               # color a square with scaled grayscale color
                    cv.create_rectangle(i*s, j*s, (i+1)*s, (j+1)*s, fill='gray'+str(int(round(((cts[i][j]-min_ct)/ct_rg)*100))))
        print("anomalies: {}\ntotal:{}".format(anomalies, n**2))

    else:
        for i in range(n):
            for j in range(n):
                cv.create_rectangle(i*s, j*s, (i+1)*s, (j+1)*s, fill='gray'+str(int(round(((cts[i][j]-min_ct)/ct_rg)*100))))

    if fname:       # write to file if desired
        cv.update()
        cv.postscript(file=fname+'.ps', width=1000, height=1000, pagewidth=700, pageheight=700)

    root.mainloop()
    #root.destroy()
