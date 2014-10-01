#!/usr/bin/env python
text1 = """
#	
#
#	
#	
#
#	
#
#                           ---- GTKDynamo ----
#		                    
#		
#       Copyright 2012 Jose Fernando R Bachega  <ferbachega@gmail.com>
#
#               visit: https://sites.google.com/site/gtkdynamo/
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#	GTKDynamo team:
#	- Jose Fernando R Bachega   < Univesity of Sao Paulo - SP, Brazil                              >
#	- Troy Wymore               < Pittsburgh Super Computer Center, Pittsburgh PA - USA            >
#	- Martin Field              < Institut de Biologie Structurale, Grenoble, France               >		
#	- Osmar Norbeto de souza    < Pontifical Catholic University of Rio Grande do Sul - RS, Brazil >
#	- Luis Fernando S M Timmers < Pontifical Catholic University of Rio Grande do Sul - RS, Brazil >
#	- Walter R Paixao-Cortes    < Pontifical Catholic University of Rio Grande do Sul - RS, Brazil >
#	- Michele Silva             < Pontifical Catholic University of Rio Grande do Sul - RS, Brazil >     
#								
#	Special thanks to:          
#	- Fernando V Maluf          < Univesity of Sao Paulo - SP, Brazil                              >
#	- Lucas Assirati            < Univesity of Sao Paulo - SP, Brazil                              >
#	- Leonardo R Bachega        < University of Purdue - West Lafayette, IN - USA                  >
#	- Richard Garratt           < Univesity of Sao Paulo - SP, Brazil                              >
#
#
#		
"""


texto_d1 = "\n\n                       -- simple-distance --\n\nFor simple-distance, select two atoms in pymol using the editing mode\nfollowing the diagram:\n\n   R                    R\n    \                  /\n     A1--A2  . . . . A3\n    /                  \ \n   R                    R\n         ^            ^\n         |            |\n        pk1  . . . . pk2\n                d1\n"
texto_d2d1 = "\n                       -- multiple-distance --\n\nFor multiple-distance, select three atoms in pymol using the editing mode\nfollowing the diagram:\n\n   R                    R\n    \                  /\n     A1--A2  . . . . A3\n    /                  \ \n   R                    R\n     ^   ^            ^\n     |   |            |\n    pk1-pk2  . . . . pk3\n       d1       d2\n"


dialog_text = {
    'error_topologies/Parameters': "Error: the topology, parameters or coordinates do not match the system type: ",
    'error_coordiantes': "Error: the coordinates do not match the loaded system.",
    'error_trajectory': "Error: the trajectory does not match the loaded system.",
    'delete': "Delete memory system.",
    'prune': "Warning: this is an irreversible process. Do you want to continue?",
    'qc_region': "Warning: no quantum region has been defined. Would you like to put all atoms in the quantum region?",
    'delete2': "Warning: there is a system loaded in memory. Are you sure that you want to delete it?"
}


# System
import datetime
import time
import pygtk
pygtk.require('2.0')
import gtk
import gtk.gtkgl

#import thread
import threading
import gobject
import sys
import glob
import math
import os

# Imports
from OpenGL.GL import *
from OpenGL.GLU import *


# GUI
from MinimizationWindow import *  # window 2  - minimization
from FileChooserWindow import *
from NewProjectDialog import *

# pDynamo
from pDynamoProject import *
from WindowControl import *

#-------------------------#
#                         #
#   GTKDYNAMO TEMP DIR    #
#                         #
#-------------------------#

# get a temporary file directory
'''
GTKDYNAMO_ROOT is a system variable exported by 
"enviroment_bash.sh" file present into gtkdynamo main folder
GTKDYNAMO_TMP is a temporary folder where logs will be genareted
'''

if not sys.platform.startswith('win'):
    HOME = os.environ.get('HOME')
else:
    HOME = os.environ.get('PYMOL_PATH')


GTKDYNAMO_ROOT = os.getcwd()
GTKDYNAMO_GUI = os.path.join(GTKDYNAMO_ROOT, "gui")
print GTKDYNAMO_GUI


PDYNAMO_SCRATCH = os.environ.get('PDYNAMO_SCRATCH')
GTKDYNAMO_TMP = os.path.join(PDYNAMO_SCRATCH, '.GTKDynamo')
if not os.path.isdir(GTKDYNAMO_TMP):
    os.mkdir(GTKDYNAMO_TMP)
    print "Temporary files directory:  %s" % GTKDYNAMO_TMP


global slab
slab = 50
angle = 0.0
sprite = None
zfactor = 0.005
zoom = 1.0


def draw(glarea, event):
    # Get surface and context
    glcontext = glarea.get_gl_context()
    gldrawable = glarea.get_gl_drawable()

    # Start opengl context
    if not gldrawable.gl_begin(glcontext):
        return

    # Actual drawing
    global sprite, angle, zoom

    # Clear screen
    #rabbyt.clear((0.0, 0.0, 0.0))

    # Render sprite
    if sprite is not None:
        sprite.rot = angle
        sprite.scale = zoom
        sprite.render()

    # Flush screen
    gldrawable.swap_buffers()
    pymol.draw()
    # End opengl context
    gldrawable.gl_end()

    return True

# Resizing function


def reshape(glarea, event):

    reshape = event
    reshape_x = reshape.width
    reshape_y = reshape.height
    pymol.reshape(reshape_x, reshape_y, 0)
    pymol.idle()
    # pymol.draw()

    # Get surface and context
    glcontext = glarea.get_gl_context()
    gldrawable = glarea.get_gl_drawable()

    # Start opengl context
    if not gldrawable.gl_begin(glcontext):
        return

    # Get widget dimensions
    x, y, width, height = glarea.get_allocation()

    pymol.reshape(width, height, True)

    # Reset rabbyt viewport
    #rabbyt.set_viewport((width, height))
    # rabbyt.set_default_attribs()

    # End opengl context
    pymol.draw()
    gldrawable.swap_buffers()
    gldrawable.gl_end()
    #

    return True

# Initialization function


def init(glarea):
    print 'init'
    # Get surface and context
    glcontext = glarea.get_gl_context()
    gldrawable = glarea.get_gl_drawable()

    # Start opengl context
    if not gldrawable.gl_begin(glcontext):
        return

    # Get widget dimensions
    x, y, width, height = glarea.get_allocation()

    # Reset rabbyt viewport
    #rabbyt.set_viewport((width, height))
    # rabbyt.set_default_attribs()

    # Get sprite variable
    global sprite

    # Load sprite
    #sprite = rabbyt.Sprite('sprite.png')

    # End opengl context
    gldrawable.gl_end()

    return True

# Idle function


def idle(glarea):
    # Get vars
    global angle, zoom, zfactor

    # Update angle
    angle += 1.0
    if angle > 359:
        angle = 0.0

    # Update zoom
    if zoom > 10 or zoom < 1:
        zfactor = -zfactor
        zoom += zfactor

    # Needed for synchronous updates
    glarea.window.invalidate_rect(glarea.allocation, False)
    glarea.window.process_updates(False)

    return True

# Map events function


def map(glarea, event):
    print 'map'
    # Add idle event
    gobject.idle_add(idle, glarea)
    return True


def slabchange(button, event):
    global slab
    x, y, width, height = glarea.get_allocation()
    if event.direction == gtk.gdk.SCROLL_UP:
        step = 1.5
        slab = slab + step
        slab = slab + step
        # if  slab >=100:
        #	slab = 100
    else:
        step = -1.5

        slab = slab + step
        if slab <= -5:
            slab = -5
    pymol.cmd.clip('slab', slab)
    return step
    pymol.button(button, 0, x, y, 0)
    pymol.idle()


def show_context_menu(widget, event):
    if event.button == 3:
        widget.popup(None, None, None, event.button, event.time)


def mousepress(button, event):
    if event.button != 3:
        x, y, width, height = glarea.get_allocation()
        mousepress = event
        button = mousepress.button - 1
        pointerx = int(mousepress.x)
        pointery = int(mousepress.y)
        calc_y = height - pointery
        pymol.button(button, 0, pointerx, calc_y, 0)


def mouserelease(button, event):

    x, y, width, height = glarea.get_allocation()
    mouserelease = event
    button = mouserelease.button - 1
    pointerx = int(mouserelease.x)
    pointery = int(mouserelease.y)
    calc_y = height - pointery
    pymol.button(button, 1, pointerx, calc_y, 0)


def mousemove(button, event):
    x, y, width, height = glarea.get_allocation()
    mousemove = event
    pointerx = int(mousemove.x)
    pointery = int(mousemove.y)
    calc_y = height - pointery
    pymol.drag(pointerx, calc_y, 0)
    pymol.idle()



def my_menu_func(menu):
    print "Menu clicado"

def context_menu():
    menu = gtk.Menu()
    menu_item = gtk.MenuItem("Sweet menu")
    menu_item.connect('activate', gtkdynamo.on_01_main_window_OpenNewProjectDialog_clicked)
    menu.append(menu_item)
    menu_item.show()
    menu_item = gtk.MenuItem("Salty menu")
    menu.append(menu_item)
    menu_item.show()
    return menu



# Create opengl configuration
try:
    # Try creating rgb, double buffering and depth test modes for opengl
    glconfig = gtk.gdkgl.Config(mode=(gtk.gdkgl.MODE_RGB |
                                      gtk.gdkgl.MODE_DOUBLE |
                                      gtk.gdkgl.MODE_DEPTH))
except:
    # Failed, so quit
    sys.exit(0)




class gtkdynamo_main():

    def testGTKMatplotLib(self, button):
        """ Function doc """
        import gtk

        from matplotlib.figure import Figure
        from numpy import arange, sin, pi

        # uncomment to select /GTK/GTKAgg/GTKCairo
        #from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
        from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
        #from matplotlib.backends.backend_gtkcairo import FigureCanvasGTKCairo as FigureCanvas
        from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar

        #win = gtk.Window()
        #win.connect("destroy", lambda x: gtk.main_quit())
        # win.set_default_size(400,300)
        #win.set_title("Embedding in GTK")
        box = self.builder.get_object('vbox4')
        self.graph = box

        f = Figure(figsize=(5, 4), dpi=100)
        a = f.add_subplot(111)
        #t = arange(0.0,3.0,0.01)
        #s = sin(2*pi*t)
        t = range(0, 10)
        s = range(0, 10)

        t = [0,
             5,
             10,
             15,
             20,
             25,
             30,
             35,
             40,
             45,
             50,
             55,
             60,
             65,
             70,
             75,
             80,
             85,
             90,
             95,
             100,
             105,
             110,
             115,
             120,
             125,
             130,
             135,
             140,
             145,
             150,
             155,
             160,
             165,
             170,
             175,
             180,
             185,
             190,
             195,
             200]

        s = [-913.53086808,
             -1978.05074306,
             -2218.21815405,
             -2333.01919415,
             -2391.82858579,
             -2435.17776079,
             -2486.44564867,
             -2543.07423428,
             -2571.71716511,
             -2598.62940311,
             -2616.98004127,
             -2631.60794731,
             -2648.00535887,
             -2661.72725012,
             -2675.65233140,
             -2686.34375946,
             -2696.94907090,
             -2708.65130605,
             -2718.73853503,
             -2726.36193409,
             -2732.59504750,
             -2737.83623730,
             -2742.33435229,
             -2745.28712806,
             -2748.82036113,
             -2752.12502818,
             -2754.57566090,
             -2756.97531091,
             -2758.83136980,
             -2760.53521449,
             -2762.79017667,
             -2764.47319544,
             -2765.99011566,
             -2767.77186148,
             -2770.20329165,
             -2772.66204338,
             -2775.05818125,
             -2776.97966619,
             -2779.02106271,
             -2781.43441141,
             -2783.70324049]

        a.plot(t, s, 'ko', t, s, 'k')
        #a.plot(x, y, 'ko',x, y,'k')
        canvas = FigureCanvas(f)  # a gtk.DrawingArea
        self.graph.pack_start(canvas)
        toolbar = NavigationToolbar(canvas, self.graph)
        self.graph.pack_end(toolbar, False, False)
        self.graph.show_all()
        # gtk.main()

    '''
	#--------------------------------------------#
	#               01_main_window               #
	#--------------------------------------------#
	'''

    def on_01_main_window_ShowValences_toggled(self, button):
        print """ Function doc """
        if self.builder.get_object('ShowValences').get_active() == True:
            #cmd.set('valence', 0.1)
            cmd.do('set valence, 0.1')
        else:
            #cmd.set('valence', 0.0)
            cmd.do('set valence, 0.0')

    def on_01_main_window_PyMOLCommandLine_entry1_activate(self, button):
        """ Function doc """
        command = self.builder.get_object('entry1').get_text()
        print command
        cmd.do(command)

    def on_01_main_window_OpenNewProjectDialog_clicked(self, button):
        """ Function doc """
        self._NewProjectDialog.dialog.run()
        self._NewProjectDialog.dialog.hide()

    def on_01_main_window_OpenFileChooserWindow_clicked(self, button):
        """ Function doc """

        FileChooser = FileChooserWindow()
        FileName = FileChooser.GetFileName(self.builder)
        try:
            _FileType = GetFileType(FileName)

            if _FileType in ['pkl', 'yaml']:
                self.project.load_coordinate_file_as_new_system(FileName)
                self.project.From_PDYNAMO_to_GTKDYNAMO(type_='new')
        except:
            pass

    def on_01_main_window_OpenMinimizationWindow_clicked(self, button):
        """ Function doc """
        self._02MinimizationWindow.dialog.run()
        self._02MinimizationWindow.dialog.hide()

    def on_01_main_window_ChangeSelectionMode_togglebutton1_toggled(self, button):
        if self.builder.get_object('togglebutton1').get_active():
            # print '# If control reaches here, the toggle button is down'
            self.builder.get_object('togglebutton1').set_label('Editing')
            self.builder.get_object('label_viewing').set_label('Picking')
            self.builder.get_object('combobox1').set_sensitive(False)
            cmd.edit_mode(1)
        else:
            # print '# If control reaches here, the toggle button is up'
            self.builder.get_object('togglebutton1').set_label('Viewing')
            self.builder.get_object('label_viewing').set_label('Selecting')
            self.builder.get_object('combobox1').set_sensitive(True)
            cmd.edit_mode(0)

    def on_01_main_window_ChangeSelection_combobox1_changed(self, button):
        """ Function doc """
        mode = self.builder.get_object('combobox1').get_active_text()
        if mode == "Atom":
            cmd.set("mouse_selection_mode", 0)
        if mode == "Residue":
            cmd.set("mouse_selection_mode", 1)
        if mode == "Chain":
            cmd.set("mouse_selection_mode", 2)
        if mode == "Molecule":
            cmd.set("mouse_selection_mode", 5)

    def row_activated(self, tree, path, column):

        model = tree.get_model()  # @+
        iter = model.get_iter(path)  # @+
        pymol_object = model.get_value(iter, 0)  # @+
        # atomtype = model.get_value( iter, 2) #@+
        cmd.enable(pymol_object)

    # def on_treeview1_select_cursor_row (self, tree, path, column):
    #	print "button"
    #
    # def on_cellrenderertoggle1_toggled (self, widget, event):
    #	""" Function doc """
    # print "button"
    #	if widget.get_active():
    #		print True
    #		widget.set_active(False)
    #	else:
    #		print False
    #		widget.set_active(True)
    #
    def row_activated2(self, tree, path, column):

        model = tree.get_model()  # @+
        iter = model.get_iter(path)  # @+
        pymol_object = model.get_value(iter, 1)  # @+
        true_or_false = model.get_value(iter, 0)
        # atomtype = model.get_value( iter, 2) #@+
        # print true_or_false

        if true_or_false == False:
            cmd.enable(pymol_object)
            true_or_false = True
            model.set(iter, 0, true_or_false)
            # print true_or_false

        else:
            cmd.disable(pymol_object)
            true_or_false = False
            model.set(iter, 0, true_or_false)
            # print true_or_false

    def __init__(self):

        print '           Intializing GTKdynamo GUI object          '
        self.home = os.environ.get('HOME')
        self.scratch = os.environ.get('PDYNAMO_SCRATCH')

        #---------------------------------- GTKDYNAMO ------------------------------------#
        #
        #
        self.builder = gtk.Builder()
        self.builder.add_from_file(
            os.path.join(GTKDYNAMO_GUI, "01_GTKDynamo_main.glade"))
        #
        self.win = self.builder.get_object("win")
        #
        self.win.show()
        #
        self.builder.connect_signals(self)
        #
        #---------------------------------------------------------------------------------#

        container = self.builder.get_object("container")
        #container = self.builder.get_object("hpaned1")
        pymol.start()
        cmd = pymol.cmd
        # container.pack2(glarea)
        container.pack_end(glarea)
        glarea.show()

        #-------------------- config PyMOL ---------------------#
        #
        pymol.cmd.set("internal_gui", 0)                         #
        pymol.cmd.set("internal_gui_mode", 0)                    #
        pymol.cmd.set("internal_feedback", 0)                   #
        pymol.cmd.set("internal_gui_width", 220)		        #
        sphere_scale = 0.25                            #
        stick_radius = 0.15                            #
        label_distance_digits = 4                               #
        mesh_width = 0.3                             #
        cmd.set('sphere_scale', sphere_scale)          #
        cmd.set('stick_radius', stick_radius)          #
        cmd.set('label_distance_digits', label_distance_digits)
        cmd.set('mesh_width', mesh_width)           #
        cmd.set("retain_order")        # keep atom ordering    #
        cmd.bg_color("grey")            # background color      #
        cmd.do("set field_of_view, 70")                         #
        #-------------------------------------------------------#
        print text1

        '''
		-------------------------------------------------
		-                                               -
		-	              WindowControl                 -
		-                                               -
		-------------------------------------------------
		'''
        self.window_control = WindowControl(self.builder)

        #----------------- Setup ComboBoxes -------------------------#
        #
        combobox = 'combobox1'                                      #
        combolist = ["Atom", "Residue", "Chain", "Molecule"]            #
        self.window_control.SETUP_COMBOBOXES(combobox, combolist, 1)
        #
        #------------------------------------------------------------#

        #--------------------------------------------------GTKDynamo project---------------------------------------------------------#
        #
        self.project = pDynamoProject(
            data_path=GTKDYNAMO_TMP, builder=self.builder, window_control=self.window_control)
        #
        self.project.PyMOL = True
        #
        #----------------------------------------------------------------------------------------------------------------------------#

        self.project.data_path = GTKDYNAMO_TMP
        # self.project.load_coordinate_file_as_new_system("/home/fernando/Dropbox/GTKPyMOL/test/test.pkl")

        #------------------------------ GTKDynamo Dialogs ------------------------------------------------#
        #                                                                                                 #
        '''os dialogs precisam ser criados aqui para que nao percam as alteracoes                         #
		# que o usuario farah nas 'entries' '''                                                           #
        #
        self._02MinimizationWindow = MinimizationWindow(
            self.project, self.window_control, self.builder)
        self._NewProjectDialog = NewProjectDialog(
            self.project, self.window_control, self.builder)
        #-------------------------------------------------------------------------------------------------#
        self.graph = None

        # print GTKDYNAMO_TMP
        # print self.project.data_path

    def run(self):
        gtk.main()

print "Creating object"
# Create our glarea widget
glarea = gtk.gtkgl.DrawingArea(glconfig)
#glarea.set_size_request(400, 400)
glarea.connect_after('realize', init)
glarea.connect('configure_event', reshape)
glarea.connect('expose_event', draw)
glarea.connect('map_event', map)
glarea.set_events(glarea.get_events() | gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_RELEASE_MASK |
                  gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.POINTER_MOTION_HINT_MASK | gtk.gdk.KEY_PRESS_MASK)
glarea.connect("button_press_event", mousepress)
glarea.connect("button_release_event", mouserelease)
glarea.connect("motion_notify_event", mousemove)
glarea.connect("scroll_event", slabchange)
glarea.set_can_focus(True)

import pymol2
pymol = pymol2.PyMOL(glarea)
gtkdynamo = gtkdynamo_main()
glarea.connect_object("button_press_event", show_context_menu, context_menu())


gtkdynamo.run()
