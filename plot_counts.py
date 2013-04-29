#!python3

from tkinter import *
import subprocess
import math

def plot(cts, fname = '', threshold = False):
	root = Tk()
	cv = Canvas(width=1000, height=1000, bg='white')
	cv.pack(expand=YES, fill=BOTH)
	n = len(cts[0])
	s = int(1000//n)
	#side length of a detector on canvas

	counts = []
	for l in cts: counts.extend(l)
	min_ct = min(counts)
	max_ct = max(counts)
	ct_rg = max_ct - min_ct

	if threshold:
		anomalies = 0
		for i in range(n):
			for j in range(n):
				if math.fabs(cts[i][j]) >= 5:
					cv.create_rectangle(i*s, j*s, (i+1)*s, (j+1)*s, fill='red')
					anomalies += 1
				elif math.fabs(cts[i][j]) >= 4:
					cv.create_rectangle(i*s, j*s, (i+1)*s, (j+1)*s, fill='orange')
					anomalies += 1
				elif math.fabs(cts[i][j]) >= 3:
					cv.create_rectangle(i*s, j*s, (i+1)*s, (j+1)*s, fill='yellow')
					anomalies += 1
				else:
					cv.create_rectangle(i*s, j*s, (i+1)*s, (j+1)*s, fill='gray'+str(int(round(((cts[i][j]-min_ct)/ct_rg)*100))))
		print("anomalies: {}\ntotal:{}".format(anomalies, n**2))

	else:
		for i in range(n):
			for j in range(n):
				cv.create_rectangle(i*s, j*s, (i+1)*s, (j+1)*s, fill='gray'+str(int(round(((cts[i][j]-min_ct)/ct_rg)*100))))

	if fname:
		cv.update()
		cv.postscript(file=fname+'.ps',width=1000,height=1000,pagewidth=700,pageheight=700)
		#subprocess.check_call(['convert', fname+'.ps', fname+'.png'])

	root.mainloop()
	#root.destroy()
