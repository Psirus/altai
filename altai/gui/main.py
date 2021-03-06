#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Main file of Altai. Execute it to use the application. """
# System imports
import sys
from os.path import expanduser
import PySide2.QtGui as QtGui
import PySide2.QtCore as QtCore
import PySide2.QtWidgets as QtWidgets
# Altai imports
from . import config
from .vented_box_frame import VentedBoxFrame
from .vent_dimensions_frame import VentDimensionsFrame
from .driver_db_frame import DriverDatabaseFrame

class Gui(QtWidgets.QMainWindow):
    """ Gui class for the main window. """

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowTitle("Altai")

        self.create_menu()

        self.tab_bar = QtWidgets.QTabBar()
        self.tab_bar.addTab("Vented Box Response")
        self.tab_bar.addTab("Vent Dimensions")
        self.tab_bar.addTab("Driver Database")
        self.tab_bar.currentChanged.connect(self.change_main_tab)

        vented_box_frame = VentedBoxFrame()
        vent_dimensions_frame = VentDimensionsFrame()
        driver_database_frame = DriverDatabaseFrame()
        driver_database_frame.new_manufacturer_added.connect(
            vented_box_frame.driver_selection.update_drivers)
        driver_database_frame.new_manufacturer_added.connect(
            vent_dimensions_frame.driver_selection.update_drivers)

        self.main_frames = [vented_box_frame, vent_dimensions_frame,
                            driver_database_frame]
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.tab_bar)
        for i, frame in enumerate(self.main_frames):
            vbox.addWidget(frame)
            if i > 0:
                frame.hide()

        self.main_frame = QtWidgets.QWidget()
        self.main_frame.setLayout(vbox)
        self.setCentralWidget(self.main_frame)

    def change_main_tab(self, tab_index):
        """ Switch between main tab views. """
        for i, frame in enumerate(self.main_frames):
            if tab_index == i:
                frame.show()
            else:
                frame.hide()

    def create_menu(self):
        """ Create main menu """
        menu_file = self.menuBar().addMenu("&File")
        menu_help = self.menuBar().addMenu("&Help")

        # Save Figure
        act_save = QtWidgets.QAction(self)
        act_save.setText("Save Response as...")
        act_save.setIcon(QtGui.QIcon.fromTheme('document-save-as'))
        menu_file.addAction(act_save)
        act_save.triggered.connect(self.save_figure)

        # Exit button
        act_exit = QtWidgets.QAction(self)
        act_exit.setText("Exit")
        act_exit.setIcon(QtGui.QIcon.fromTheme('application-exit'))
        menu_file.addAction(act_exit)
        act_exit.triggered.connect(self.close)

        # About window
        act_about = QtWidgets.QAction(self)
        act_about.setText("About")
        act_about.setIcon(QtGui.QIcon.fromTheme('help-about'))
        menu_help.addAction(act_about)
        act_about.triggered.connect(self.create_about_window)

    def save_figure(self):
        """ Save figure as file; all filetypes that are supported by matplotlib"""
        home = expanduser("~")
        fname, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save Response as", home,
            "PDF, PNG and SVG (*.pdf *.png *.svg)")
        self.main_frames[0].fig.savefig(fname)

    def create_about_window(self):
        """ Creates the about window for Altai. """

        about = ("Altai is a cross-platform application for simulating audio "
                 "systems. With it, you can design speakers, find the optimum "
                 "driver, predict the frequency response, etc. It is still in "
                 "a very early stage of development. You can follow its "
                 "progress on github: <a href='http://github.com/Psirus/altai'>"
                 "Altai on GitHub</a>. Please report any issues and feature "
                 "ideas you may have.")

        reply = QtWidgets.QMessageBox(self)
        reply.setWindowTitle("About Altai")
        reply.setTextFormat(QtCore.Qt.TextFormat.RichText)
        reply.setText(about)
        reply.exec_()

def main():
    """ Main function; acts as entry point for Altai. """
    app = QtWidgets.QApplication(sys.argv)
    gui = Gui()
    gui.resize(800, 600)
    gui.show()
    sys.exit(app.exec_())
