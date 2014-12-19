#!/usr/bin/python
# -*- coding: utf-8 -*-


import wx
import datetime
import numpy as np
from numpy import arange, sin, pi, cos
import matplotlib

#modulation stuff
from modulation import Signal
from demodulator import Demodulator

from BERCalculation import calculateBER

matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

import pylab

global newTransmission
global seq
global seqNoise

global pos

global const_x
const_x = 0.0,0.1,0.5,0.6,0.8,1.0,2.0
global const_y
const_y = 0.3,0.4,0.2,0.6,0.2,1.0,2.0

global ber_x
ber_x = 0.0,0.1,0.5,0.6,0.8,1.0,2.0
global ber_y
ber_y = 0.3,0.4,0.2,0.6,0.2,1.0,2.0

global con
global ber

class CS4031_GUI(wx.Frame):
           
    def __init__(self, *args, **kw):
        super(CS4031_GUI, self).__init__(*args, **kw) 
        
        self.InitUI()
                
    def InitUI(self):

        pnl = wx.Panel(self)
        pnl.SetBackgroundColour(wx.WHITE)

        pnlBER = wx.Panel(pnl, 10, (380, 400), (350, 300))
        pnlCons = wx.Panel(pnl, 10, (380, 50), (350, 300))

        global con
        global ber

        ber = self.init_plot_BER(ber_x,ber_y)
        self.canvas = FigCanvas(pnlBER, -1, self.fig)

        con = self.init_plot_Cons(const_x,const_y)
        self.canvas1 = FigCanvas(pnlCons, -1, self.fig1)

        constellation_save_BT = wx.Button(pnl, 0, "save", (700,300))
        BER_save_BT = wx.Button(pnl, 1, "save", (700,600))
        cons_clear_BT = wx.Button(pnl, 2, "clear", (700,650))
        run_BT = wx.Button(pnl, 3, "run", (50,350))
        cons_CB = wx.CheckBox(pnl, 4, 'Calculate', (700, 275))
        cons_CB.SetValue(False)
        BER_CB = wx.CheckBox(pnl, 5, 'Calculate', (700, 550))
        BER_CB.SetValue(False)
        hold_CB = wx.CheckBox(pnl, 6, 'Hold', (700, 575))
        hold_CB.SetValue(False)
		
        #Input boxes
        self.seq_length = wx.TextCtrl(pnl, value = "1011", pos = (50,100))
        self.seq_length_text = wx.StaticText(pnl, label = "Sequence Length:", pos = (50,80))

        self.mod_type = wx.TextCtrl(pnl, value = "0", pos = (50, 150))
        self.mod_type_text = wx.StaticText(pnl, label = "Mod Type:", pos = (50, 130))

        self.noise_type = wx.TextCtrl(pnl, value = "Gaussian", pos = (50, 200))
        self.noise_type_text = wx.StaticText(pnl, label = "Noise:", pos = (50, 180))

        self.speed_up = wx.TextCtrl(pnl, value = "1", pos = (175, 100))
        self.speed_up_text = wx.StaticText(pnl, label = "Speed Up:", pos = (175, 80))

        self.coding = wx.TextCtrl(pnl, value = "Gray Coding", pos = (175, 150))
        self.coding_text = wx.StaticText(pnl, label = "Coding:", pos = (175, 130))

        self.resolution = wx.TextCtrl(pnl, value = "1", pos = (50, 400))
        self.resolution_text = wx.StaticText(pnl, label = "Resolution:", pos = (50, 380))

        self.resolution_text = wx.StaticText(pnl, label = "Modulation Types", pos = (50, 460))
        self.resolution_text = wx.StaticText(pnl, label = "2PSK: 0", pos = (50, 490))
        self.resolution_text = wx.StaticText(pnl, label = "4PSK: 1", pos = (50, 510))
        self.resolution_text = wx.StaticText(pnl, label = "8PSK: 2", pos = (50, 530))
        self.resolution_text = wx.StaticText(pnl, label = "16PSK: 3", pos = (50, 550))
        self.resolution_text = wx.StaticText(pnl, label = "QAM16: 4", pos = (50, 570))

        self.Bind(wx.EVT_BUTTON, self.OnConsSave, id=0)
        self.Bind(wx.EVT_BUTTON, self.OnBERSave, id=1)
        self.Bind(wx.EVT_BUTTON, self.OnConsClear, id=2)
        self.Bind(wx.EVT_BUTTON, self.OnRun, id=3)
        self.Bind(wx.EVT_CHECKBOX, self.OnConsCalculate, id=4)
        self.Bind(wx.EVT_CHECKBOX, self.OnBERCalculate, id=5)
        self.Bind(wx.EVT_CHECKBOX, self.OnHold, id=6)
		
        self.SetSize((850, 750))
        self.SetTitle("CS4031 GUI")
        self.Centre()
        self.Show(True)

    def OnConsSave(self, event):

        # Create the PdfPages object to which we will save the graphs:
        with PdfPages('Constellation Plot.pdf') as pdf:

            plt.rc('text', usetex=True)
            plt.figure(figsize=(8, 6))
            global const_x, const_y
            plt.plot(const_x, const_y, 'b-')
            plt.title('Plot One')
            pdf.savefig()
            plt.close()

			# We can also set the file's metadata via the PdfPages object:
            d = pdf.infodict()
            d['Title'] = 'GUI Plots'
            d['Author'] = u'Button Bandits'
            d['ModDate'] = datetime.datetime.today()

    def OnBERSave(self, event):
        #Create the PdfPages object to which we will save the graphs:
        with PdfPages('BER Plot.pdf') as pdf:
            
            plt.rc('text', usetex=True)
            plt.figure(figsize=(8, 6))
            global ber_x, ber_y
            plt.scatter(ber_x, ber_y)
            plt.title('Plot One')
            pdf.savefig()
            plt.close()

            # We can also set the file's metadata via the PdfPages object:
            d = pdf.infodict()
            d['Title'] = 'GUI Plots'
            d['Author'] = u'Button Bandits'
            d['ModDate'] = datetime.datetime.today()

    def OnConsClear(self, event):
        self.plot_data.remove()
        self.canvas1.draw()

    def OnRun(self, event):
        print "Running..."
    	error = False #flag for if any invalid input is detected
    	message = "" #holds the error message if any invalid input is detected
        global pos

        # take in generated string and noise string
        global seq, seqNoise
        seq = self.seq_length.GetValue()
        seqNoise = '1001'

        mod = self.mod_type.GetValue()

        noise = self.noise_type.GetValue()

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

        levels = 2
        qam_on = False
    	if(error):
    	    wx.MessageBox(message, 'Error in input', wx.OK | wx.ICON_ERROR)
    	else:
            if int(mod) is 4:
                levels = 16
                qam_on = True
                sig = Signal((levels), True)
            if int(mod) is 3:
                levels = 16
                sig = Signal(levels)
            if int(mod) is 2:
                levels = 8
                sig = Signal(levels)
            if int(mod) is 1:
                levels = 4
                sig = Signal(levels)
            if int(mod) is 0:
                levels = 2
                sig = Signal(levels)
            else:
                levels = 2
                sig = Signal(levels)

            res, src = sig.generate(str(seq), True)

            temp = self.get_max(src)
            maxSource = res[pos]

            print "temp"
            print temp
            print "maxSource"
            print maxSource
            noise_ratio = []

            for x in range(0, 15):
                noise_ratio.append(4)

            print maxSource

            print noise_ratio

            #demodulate
            dem = Demodulator()
            if qam_on is True:
                dem.build((levels), True)
            else:
                print "check"
                dem.build(4, False)
            
            #result
            out = dem.generate(temp)

            print out

            #test stuff
            global const_x, const_y
            const_x = np.append(const_x,3.0)
            const_y = np.append(const_y,3.0)
            global con
            con.drawConsPlot(const_x,const_y)
            global ber_x, ber_y
            ber_x = np.append(ber_x,3.0)
            ber_y = np.append(ber_y,3.0)
            global ber
            ber.drawBerPlot(ber_x,ber_y)
        
        print "calculated"

    def OnConsCalculate(self, event):

        print "ConsCalc Pressed"

    def OnBERCalculate(self, event):

        print "BERCalc Pressed"

    def OnHold(self, event):

        print "Hold Pressed"

    def get_max(self, arr):
        temp = [0] * len(arr)
        global pos
        i = 0
        for r in arr:
            for s in r:
                if abs(s) > temp[i]:
                    temp[i] = s
                    pos = i
            i += 1
        return temp

    def drawBerPlot(self, t, c):
        self.plot_data = self.axes.plot(
            t,c, 
            linewidth=1,
            color=(1, 0.5, 0),
            )[0]
        self.canvas.draw()

    def drawConsPlot(self, t, c):

        self.plot_data = self.axes1.scatter(
            t,c, 
            linewidth=1,
            color=(1, 0.5, 0),
            )
        self.canvas1.draw()

    def init_plot_BER(self, t, s):
        self.dpi = 95
        self.fig = Figure((3.3, 3), dpi=self.dpi, facecolor='white')

        self.axes = self.fig.add_subplot(111)
        self.axes.set_axis_bgcolor('white')
        self.axes.set_title('BER curves', size=12)
        pylab.setp(self.axes.get_xticklabels(), fontsize=8)
        pylab.setp(self.axes.get_yticklabels(), fontsize=8)

        self.plot_data = self.axes.plot(
            t,s, 
            linewidth=1,
            color=(1, 0.5, 0),
            )[0]
        return self
	
    def init_plot_Cons(self, t, s):
        self.dpi = 95
        self.fig1 = Figure((3.3, 3), dpi=self.dpi, facecolor='white')

        self.axes1 = self.fig1.add_subplot(111)
        self.axes1.set_axis_bgcolor('white')
        self.axes1.set_title('Constellation Diagram', size=12)
        self.axes1.spines['left'].set_position('center')
        self.axes1.spines['right'].set_color('none')
        self.axes1.spines['bottom'].set_position('center')
        self.axes1.spines['top'].set_color('none')
        self.axes1.spines['left'].set_smart_bounds(True)
        self.axes1.spines['bottom'].set_smart_bounds(True)
        self.axes1.xaxis.set_ticks_position('bottom')
        self.axes1.yaxis.set_ticks_position('left')
        pylab.setp(self.axes1.get_xticklabels(), fontsize=8)
        pylab.setp(self.axes1.get_yticklabels(), fontsize=8)

        self.plot_data = self.axes1.scatter(
            t,s, 
            linewidth=1,
            color=(1, 0.5, 0),
            )
        return self

def set_ber_y(charOriginal, charNoise):
    global ber_y
    global newTransmission

    if newTransmission == True:
        ber_y.clear()
        newTransmission = False
    #TODO: charOriginal, charNoise should preferably be passed in here as bit arrays
    newValue = calculateBER(charOriginal, charNoise)
    const_x = np.append(const_x, newValue)
		  
def main():
    
    ex = wx.App()
    CS4031_GUI(None)
    ex.MainLoop()

if __name__ == '__main__':
    main()