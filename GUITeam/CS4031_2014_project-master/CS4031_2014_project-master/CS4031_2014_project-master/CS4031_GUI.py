#!/usr/bin/python
# -*- coding: utf-8 -*-


import wx
import matplotlib
import datetime
import numpy as np
from numpy import arange, sin, pi, cos

matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

import pylab

class CS4031_GUI(wx.Frame):
           
    def __init__(self, *args, **kw):
        super(CS4031_GUI, self).__init__(*args, **kw) 
        
        self.InitUI()
                
    def InitUI(self):

        pnl = wx.Panel(self)
        pnl.SetBackgroundColour(wx.WHITE)
        pnlBER = wx.Panel(pnl, 10, (630, 400), (350, 300))
        pnlCons = wx.Panel(pnl, 10, (630, 50), (350, 300))
        
        c = self.init_plot_BER() 
        self.canvas = FigCanvas(pnlBER, -1, self.fig)
        self.init_plot_Cons()
        self.canvas1 = FigCanvas(pnlCons, -1, self.fig)
        constellation_save_BT = wx.Button(pnl, 0, "save", (1000,300))
        BER_save_BT = wx.Button(pnl, 1, "save", (1000,600))
        cons_clear_BT = wx.Button(pnl, 2, "clear", (1000,650))
        run_BT = wx.Button(pnl, 3, "run", (200,550))
        cons_CB = wx.CheckBox(pnl, 4, 'Calculate', (1000, 275))
        cons_CB.SetValue(False)
        BER_CB = wx.CheckBox(pnl, 5, 'Calculate', (1000, 550))
        BER_CB.SetValue(False)
        hold_CB = wx.CheckBox(pnl, 6, 'Hold', (1000, 575))
        hold_CB.SetValue(False)
		
        #Input boxes
        self.seq_length = wx.TextCtrl(pnl, value = "Seq length: ", pos = (50,100))
        self.mod_type = wx.TextCtrl(pnl, value = "Mod type: ", pos = (50, 150))
        self.noise_type = wx.TextCtrl(pnl, value = "Noise type: ", pos = (50, 200))
        self.speed_up = wx.TextCtrl(pnl, value = "Speed up: ", pos = (175, 100))
        self.coding = wx.TextCtrl(pnl, value = "Coding: ", pos = (175, 150))
        self.resolution = wx.TextCtrl(pnl, value = "Resolution: ", pos = (200, 600))

        self.Bind(wx.EVT_BUTTON, self.OnConsSave, id=0)
        self.Bind(wx.EVT_BUTTON, self.OnBERSave, id=1)
        self.Bind(wx.EVT_BUTTON, self.OnConsClear, id=2)
        self.Bind(wx.EVT_BUTTON, self.OnRun, id=3)
        self.Bind(wx.EVT_CHECKBOX, self.OnConsCalculate, id=4)
        self.Bind(wx.EVT_CHECKBOX, self.OnBERCalculate, id=5)
        self.Bind(wx.EVT_CHECKBOX, self.OnHold, id=6)
		
        self.SetSize((1200, 800))
        self.SetTitle("CS4031 GUI")
        self.Centre()
        self.Show(True)

    def OnConsSave(self, event):
	
		# Create the PdfPages object to which we will save the graphs:
				
		with PdfPages('Plots.pdf') as pdf:
			
			plt.rc('text', usetex=True)
			plt.figure(figsize=(8, 6))
			x = np.arange(0, 5, 0.1)
			plt.plot(x, np.sin(x), 'b-')
			plt.title('Plot One')
			pdf.savefig()
			plt.close()

			plt.rc('text', usetex=False)
			fig = plt.figure(figsize=(4, 5))
			plt.plot(x, x*x, 'ko')
			plt.title('Plot Two')
			pdf.savefig(fig)  # or you can pass a Figure object to pdf.savefig
			plt.close()

			# We can also set the file's metadata via the PdfPages object:
			d = pdf.infodict()
			d['Title'] = 'GUI Plots'
			d['Author'] = u'Button Bandits'
			d['ModDate'] = datetime.datetime.today()
        

    def OnBERSave(self, event):

        print "BERSave Pressed"

    def OnConsClear(self, event):

		self.plot_data.remove()
		self.axes.figure.canvas.draw()
		
    def OnRun(self, event):

	error = False #flag for if any invalid input is detected
	message = "" #holds the error message if any invalid input is detected

        # read data from input fields
        seq = self.seq_length.GetValue()
        try: 
            int(seq)
            print seq
        except ValueError:
	    message = message + 'Invalid input on sequence length\r\n'
            print "invalid input on sequence_length"
	    error = True

        mod = self.mod_type.GetValue()
        print mod

        noise = self.noise_type.GetValue()
        print noise

        speed = self.speed_up.GetValue()
        try: 
            int(speed)
            print speed
        except ValueError:
	    message = message + 'Invalid input on speed up\r\n'
            print "invalid input on speed_up"
	    error = True

        code = self.coding.GetValue()
        print noise

        res = self.resolution.GetValue()
        try: 
            int(res)
            print res
        except ValueError:
	    message = message + 'Invalid input on resolution\r\n'
            print "invalid input on resolution"
	    error = True

	if(error):
	    wx.MessageBox(message, 'Error in input', wx.OK | wx.ICON_ERROR)
	else:
            c = self.init_plot_BER()
	    print "Run"

    def OnConsCalculate(self, event):

        print "ConsCalc Pressed"

    def OnBERCalculate(self, event):

        print "BERCalc Pressed"

    def OnHold(self, event):

        print "Hold Pressed"

    def drawBerPlot(self, t, c):
        self.plot_data = self.axes.plot(
            t,c, 
            linewidth=1,
            color=(1, 0.8, 0),
            )[0]

    def drawConsPlot(self, t, c):
        self.plot_data = self.axes.scatter(
            t,c, 
            linewidth=1,
            color=(1, 0.8, 0),
            )

    def init_plot_BER(self):
        self.dpi = 95
        self.fig = Figure((3.3, 3), dpi=self.dpi, facecolor='white')

        self.axes = self.fig.add_subplot(111)
        self.axes.set_axis_bgcolor('white')
        self.axes.set_title('BER curves', size=12)
        pylab.setp(self.axes.get_xticklabels(), fontsize=8)
        pylab.setp(self.axes.get_yticklabels(), fontsize=8)

        # plot the data as a line series, and save the reference 
        # to the plotted line series
        #
        t = arange(0.0, 6.0, 0.05)
        s = sin(2 * pi * t)
        #self.axes.plot(t, s)
        c = cos(2 * pi * t)
        self.plot_data = self.axes.plot(
            t,s, 
            linewidth=1,
            color=(1, 0.5, 0),
            )[0]
        return self
	
    def init_plot_Cons(self):
        self.dpi = 95
        self.fig = Figure((3.3, 3), dpi=self.dpi, facecolor='white')

        self.axes = self.fig.add_subplot(111)
        self.axes.set_axis_bgcolor('white')
        self.axes.set_title('Constellation Diagram', size=12)
        self.axes.spines['left'].set_position('center')
        self.axes.spines['right'].set_color('none')
        self.axes.spines['bottom'].set_position('center')
        self.axes.spines['top'].set_color('none')
        self.axes.spines['left'].set_smart_bounds(True)
        self.axes.spines['bottom'].set_smart_bounds(True)
        self.axes.xaxis.set_ticks_position('bottom')
        self.axes.yaxis.set_ticks_position('left')
        pylab.setp(self.axes.get_xticklabels(), fontsize=8)
        pylab.setp(self.axes.get_yticklabels(), fontsize=8)

        # plot the data as a line series, and save the reference 
        # to the plotted line series
        #
        t = arange(0.0, 3.0, 0.01)
        s = sin(2 * pi * t)
        #self.axes.plot(t, s)
        c = cos(2 * pi * t)
        self.plot_data = self.axes.plot(
            t,s, 
            linewidth=1,
            color=(1, 0.5, 0),
            )[0]
        return self
		  
def main():
    
    ex = wx.App()
    CS4031_GUI(None)
    ex.MainLoop()   

if __name__ == '__main__':
    main() 

