#! /usr/bin/env python
import pyqrgen

import pygtk
pygtk.require('2.0')
import gtk, gobject, cairo

class Screen(gtk.DrawingArea):

	

	__gsignals__ = { "expose-event": "override" }

	def do_expose_event(self, event):
		if self.generated:
			window = self.window
			cr = window.cairo_create()
			
			pyqrgen.setSize(event.area.width, event.area.height)
			pyqrgen.paint(cr)
	
	def redraw(self):
		self.generated = True
		self.queue_draw()
		

	def __init__(self):
		gtk.DrawingArea.__init__(self)
		self.generated = False

class ExpanderFrame(gtk.Frame):
	def activated(self, expander):
		if expander.get_expanded():
			self.w.hide()
		else:
			self.w.show_all()
			
	def getFrame(self):
		return self.frame
		
	def __init__(self, widget, label):
		gtk.Frame.__init__(self)
		self.expanderlabel = gtk.Expander(label)
		self.w = widget
		self.set_label_widget(self.expanderlabel)
		self.expanderlabel.connect("activate", self.activated)

		self.add(self.w)
		self.show_all()
		widget.hide()

class Win:
	def get_active_text(self, combobox):
		model = combobox.get_model()
		active = combobox.get_active()
		if active < 0:
			return None
		return model[active][0]
		
	def redraw_qr(self):
		self.screen.redraw()
	
	def regen_qr(self):
		print("hello")
		pyqrgen.encode()
		self.redraw_qr()
	
	
	def pcchanged(self, widget):
		if widget == self.maskspinner:
			print("hello")
			pyqrgen.setMask(self.maskspinner.props.value)
			
		elif widget == self.quietbutton:
			print("hello")
			pyqrgen.drawQuietZone(self.quietbutton.props.active)
			
		elif widget == self.forebutton:
			print("hello")
			pyqrgen.setForegroundColor(self.forebutton.props.color.red, self.forebutton.props.color.green, self.forebutton.props.color.blue, 1)
			
		elif widget == self.backbutton:
			print("hello")
			pyqrgen.setBackgroundColor(self.backbutton.props.color.red, self.backbutton.props.color.green, self.backbutton.props.color.blue, 1)
		
		
		self.redraw_qr()
		
	def sichanged(self, widget):

		if widget == self.button1:
			pyqrgen.setData(self.entry.get_text(), len(self.entry.get_text()))

			
		elif widget == self.verspinner:
			print("hello")
			pyqrgen.setVersion(self.verspinner.props.value)
			
		elif widget == self.ec:
			e = self.get_active_text(self.ec)
			ecl = 4
			if e == "L":
				ecl= 1
			elif e == "M":
				ecl = 0
			elif e == "Q":
				ecl = 3
			elif e == "H":
				ecl = 2
			pyqrgen.setEcLevel(ecl)
			
		elif widget == self.mode:
			m = self.get_active_text(self.mode)
			md = 0
			if m == "Binary":
				md = 4
			elif m == "Numeric":
				md = 1
			elif m == "Alphanumeric":
				md = 2
			pyqrgen.setMode(md)
			
		self.regen_qr()
		


	def output(self, widget):
		if widget == self.verspinner and self.verspinner.props.value == 0:
			self.verspinner.props.text = "Auto"
			return True

		if widget == self.maskspinner and self.maskspinner.props.value == 0:
			self.maskspinner.props.text = "Auto"
			return True
			
	def getAdvancedPane(self):
		detailstable = gtk.Table(4, 2, False)
		detailstable.set_row_spacings(2)
		detailstable.set_col_spacings(2)
	
		masklabel = gtk.Label("Mask")
		maskalign = gtk.Alignment(0.0, 0.5, 0.0, 0.0)
		maskalign.add(masklabel)
		maskadj = gtk.Adjustment(0, 0, 8, 1, 0 ,0)
		self.maskspinner = gtk.SpinButton(maskadj, 0.1, 0)
		self.maskspinner.set_wrap(True)
		self.maskspinner.connect("value-changed", self.pcchanged)
		self.maskspinner.connect("output", self.output)
		detailstable.attach(maskalign, 0, 1, 0, 1, gtk.FILL, gtk.FILL, 2, 0)
		detailstable.attach(self.maskspinner, 1, 2, 0, 1, gtk.EXPAND|gtk.FILL, gtk.EXPAND|gtk.FILL, 0, 0)
		
		quietlabel = gtk.Label("Quiet Zone")
		quietalign = gtk.Alignment(0.0, 0.5, 0.0, 0.0)
		quietalign.add(quietlabel)
		self.quietbutton = gtk.CheckButton(None, False)
		self.quietbutton.connect("toggled", self.pcchanged)
		detailstable.attach(quietalign, 0, 1, 1, 2, gtk.FILL, gtk.FILL, 2, 0)
		detailstable.attach(self.quietbutton, 1, 2, 1, 2, gtk.EXPAND|gtk.FILL, gtk.EXPAND|gtk.FILL, 0, 0)
		
		foregroundlabel = gtk.Label("Foreground")
		forealign = gtk.Alignment(0.0, 0.5, 0.0, 0.0)
		forealign.add(foregroundlabel)
		self.forebutton = gtk.ColorButton(gtk.gdk.Color(0,0,0))
		self.forebutton.set_use_alpha(True)
		self.forebutton.connect("color-set", self.pcchanged)
		detailstable.attach(forealign, 0, 1, 2, 3, gtk.FILL, gtk.FILL, 2, 0)
		detailstable.attach(self.forebutton, 1, 2, 2, 3, gtk.EXPAND|gtk.FILL, gtk.EXPAND|gtk.FILL, 0, 0)
		
		backgroundlabel = gtk.Label("Background")
		backalign = gtk.Alignment(0.0, 0.5, 0.0, 0.0)
		backalign.add(backgroundlabel)
		self.backbutton = gtk.ColorButton(gtk.gdk.Color(1,1,1))
		self.backbutton.set_use_alpha(True)
		self.backbutton.connect("color-set", self.pcchanged)
		detailstable.attach(backalign, 0, 1, 3, 4, gtk.FILL, gtk.FILL, 2, 0)
		detailstable.attach(self.backbutton, 1, 2, 3, 4, gtk.EXPAND|gtk.FILL, gtk.EXPAND|gtk.FILL, 0, 0)
		
		frame = ExpanderFrame(detailstable, "Advanced Settings")
		
		return frame
	
		
	def getOptionPane(self):
		detailstable = gtk.Table(3, 2, False)
		detailstable.set_row_spacings(2)
		detailstable.set_col_spacings(2)
		
		versionlabel = gtk.Label("Version")
		versalign = gtk.Alignment(0.0, 0.5, 0.0, 0.0)
		versalign.add(versionlabel)
		versadj = gtk.Adjustment(0, 0, 40, 1, 0 ,0)
		self.verspinner = gtk.SpinButton(versadj, 0.1, 0)
		self.verspinner.connect("value-changed", self.sichanged)
		#self.verspinner.connect("output", self.output)
		detailstable.attach(versalign, 0, 1, 0, 1, gtk.FILL, gtk.FILL, 2, 0)
		detailstable.attach(self.verspinner, 1, 2, 0, 1, gtk.EXPAND|gtk.FILL, gtk.EXPAND|gtk.FILL, 0, 0)
		
		modelabel = gtk.Label("Enocde Mode")
		modealig = gtk.Alignment(0.0, 0.5, 0.0, 0.0)
		modealig.add(modelabel)
		self.mode =  gtk.combo_box_new_text()
		self.mode.append_text("Binary")
		self.mode.append_text("Numeric")
		self.mode.append_text("Alphanumeric")
		self.mode.set_active(0)
		self.mode.connect("changed", self.sichanged)
		detailstable.attach(modealig, 0, 1, 1, 2, gtk.FILL, gtk.FILL, 2, 0)
		detailstable.attach(self.mode, 1, 2, 1, 2, gtk.EXPAND|gtk.FILL, gtk.EXPAND|gtk.FILL, 0, 0)
		
		eclabel = gtk.Label("Error Correction Mode")
		ecalig = gtk.Alignment(0.0, 0.5, 0.0, 0.0)
		ecalig.add(eclabel)
		self.ec = gtk.combo_box_new_text()
		self.ec.append_text("L")
		self.ec.append_text("M")
		self.ec.append_text("Q")
		self.ec.append_text("H")
		self.ec.set_active(1)
		self.ec.connect("changed", self.sichanged)
		detailstable.attach(ecalig, 0, 1, 2, 3, gtk.FILL, gtk.FILL, 2, 0)
		detailstable.attach(self.ec, 1, 2, 2, 3, gtk.EXPAND|gtk.FILL, gtk.EXPAND|gtk.FILL, 0, 0)

		frame = ExpanderFrame(detailstable, "Settings")
		
		return frame
	
	def __init__(self):

		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

		self.window.set_title("qrgen")
		self.window.connect("delete_event", gtk.main_quit)

		self.mainbox = gtk.VBox(False, 0)
		
		self.options = self.getOptionPane()
		self.advanced = self.getAdvancedPane()
		#self.debug = getDebugPane()
		
		
		self.genbox = gtk.HBox(False, 0)
		self.entry = gtk.Entry()
		self.entry.set_text("green pride")
		self.button1 = gtk.Button("Generate")
		self.button1.connect("clicked", self.sichanged)
		self.genbox.pack_start(self.button1, False, False, 0)
		self.genbox.pack_start(self.entry, True, True, 0)

		self.aframe =  gtk.AspectFrame(None, 0, 0, 1.0, False)
		self.screen = Screen()
		self.aframe.add(self.screen)

		self.mainbox.pack_start(self.genbox, False, False, 0)
		self.mainbox.pack_start(self.options, False, False, 0)
		self.mainbox.pack_start(self.advanced, False, False, 0)
		#self.mainbo0x.pack_start(self.debug, False, False, 0)
		self.mainbox.pack_start(self.aframe, True, True, 0)

		self.window.add(self.mainbox)
		
		self.window.set_default_size(215, 260)
		
		self.genbox.show_all()
		self.aframe.show_all()
		self.mainbox.show()
		self.window.show()

def run(Widget):
	widget = Widget()
	gtk.main()

if __name__ == "__main__":
	run(Win)

	
	
