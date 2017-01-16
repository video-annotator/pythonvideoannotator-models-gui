#! /usr/bin/python2
# -*- coding: utf-8 -*-
import os
from pysettings import conf
from pyforms import BaseWidget
from PyQt4 import QtGui, QtCore
from pyforms.Controls import ControlButton
from pyforms.Controls import ControlTree
from pyforms.Controls import ControlList
from pyforms.Controls import ControlEmptyWidget
from pyforms.dialogs  import CsvParserDialog

from pythonvideoannotator_models_gui.models.imodel_gui import IModelGUI
from pythonvideoannotator_models.models import Project
from pythonvideoannotator_models_gui.models.video import Video
from pythonvideoannotator_models_gui.models.video.image import Image


class ProjectGUI(IModelGUI, Project, BaseWidget):
	"""Application form"""

	_project = None

	def __init__(self, parent=None):
		IModelGUI.__init__(self)
		Project.__init__(self)
		BaseWidget.__init__(self, 'Project window', parent_win=parent)
		
		conf.PROJECT = self
		self._parent = parent
		
		self._tree 			= ControlTree('')
		self._addvideo 		= ControlButton('Add video')
		self._removevideo 	= ControlButton('Remove video')
		self.formset 		= [
			'_tree', 
			'_addvideo',
		]
	
		## set controls ##########################################################
		self._tree.show_header  = False
		self._addvideo.value 	= self.__create_video_event

		self._addvideo.icon 	= conf.ANNOTATOR_ICON_ADD

		self.tree.item_double_clicked_event    = self.tree_item_double_clicked_event
		self.tree.item_selection_changed_event = self.tree_item_selection_changed_event
		

	######################################################################################
	#### FUNCTIONS #######################################################################
	######################################################################################

	def create_video(self): return Video(self)

	######################################################################################
	#### GUI EVENTS ######################################################################
	######################################################################################

	def tree_item_double_clicked_event(self, item):
		if isinstance(item.win, Image): item.win.double_clicked_event()

	def tree_item_selection_changed_event(self):
		print "---"
		if self.tree.selected_item is not None and hasattr(self.tree.selected_item,'win'):
			self.mainwindow.details = self.tree.selected_item.win
			print "show"
			self.mainwindow.details.show()
	

	def __create_video_event(self):
		video = self.create_video()
		video.choose_file()

	def __remove_video_event(self):
		 item = self.tree.selected_item
		 if item: self -= item.win

	######################################################################################
	#### PUBLIC FUNCTIONS ################################################################
	######################################################################################

	def __sub__(self, obj):
		super(ProjectGUI, self).__sub__(obj)
		if isinstance(obj, Video): self._tree -= obj.treenode
		return self
		
	def player_on_click(self, event, x, y):
		if self._tree.selected_row_index is not None:
			obj = self._tree.selected_item.win
			obj.on_click(event, x, y)

	def draw(self, frame, frame_index):
		if self._tree.selected_row_index is not None:
			obj = self._tree.selected_item.win
			obj.draw(frame, frame_index)

	def save(self, data, project_path=None):
		data = super(ProjectGUI, self).save(data, project_path)
		timeline_path = os.path.join(project_path, 'timeline.csv')
		self.mainwindow.timeline.export_csv_file(timeline_path)
		return data

	def load(self, data, project_path=None):
		super(ProjectGUI, self).load(data, project_path)
		timeline_path = os.path.join(project_path, 'timeline.csv')
		self.mainwindow.timeline.import_csv_file(timeline_path)
		return data
		
	######################################################################################
	#### PROPERTIES ######################################################################
	######################################################################################

	@property
	def mainwindow(self): 	return self._parent

	@property
	def tree(self): 	return self._tree

	@property
	def objects(self):  	return [item.win for item in self._tree.value]


	@property
	def name(self): return self.directory
	@name.setter
	def name(self, value): pass
		