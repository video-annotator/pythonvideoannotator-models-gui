import csv, cv2, os
from pysettings import conf
from pyforms import BaseWidget
from PyQt4 import QtCore, QtGui
from pyforms.Controls import ControlButton
from pyforms.Controls import ControlCombo
from pyforms.Controls import ControlLabel
from pyforms.Controls import ControlText
from pythonvideoannotator_models.models.video.objects.geometry import Geometry
from pythonvideoannotator_models_gui.dialogs import DatasetsDialog
from pythonvideoannotator_models_gui.models.imodel_gui import IModelGUI
from pythonvideoannotator_models_gui.models.video.objects.object2d.datasets.path import Path
from geometry_designer.modules.geometry_manual_designer.GeometryManualDesigner import GeometryManualDesigner

class GeometryGUI(IModelGUI, Geometry, BaseWidget):

	def __init__(self, video):
		IModelGUI.__init__(self)
		Geometry.__init__(self, video)
		BaseWidget.__init__(self, 'Geometry', parent_win=video)
		
		self._removeimg = ControlButton('Remove')
		self._edit  	= ControlButton('Edit')

		self._geometry_window = GeometryManualDesigner('Geometry designer', parent=self)
		self._geometry_window.apply_event = self.__geometry_end_edit_event
		
		self.formset = [
			'_name',
			'_edit',
			'_removeimg',
			' '
		]

		self._removeimg.value = self.__remove_image_event
		self._removeimg.icon = conf.ANNOTATOR_ICON_REMOVE
		self._edit.value = self.__show_geometry_window
		self._edit.icon = conf.ANNOTATOR_ICON_EDIT

		self.create_tree_nodes()


	######################################################################
	### EVENTS ###########################################################
	######################################################################

	def __show_geometry_window(self):
		self._geometry_window.video_filename = self.video.filename
		self._geometry_window.geometries = self._geometry
		self._geometry_window.show()


	def on_click(self, event, x, y):
		pass

	def __geometry_end_edit_event(self):
		self._geometry = self._geometry_window.geometries
		self._geometry_window.hide()

	######################################################################
	### OBJECT FUNCTIONS #################################################
	######################################################################

	def draw(self, frame, frame_index): pass
		
	######################################################################
	### CLASS FUNCTIONS ##################################################
	######################################################################

	def create_tree_nodes(self):
		self.treenode = self.tree.create_child(self.name, icon=conf.ANNOTATOR_ICON_PICTURE, parent=self.video.treenode)
		self.treenode.win = self

		self.tree.add_popup_menu_option(
			label='Remove', 
			function_action=self.__remove_image_event, 
			item=self.treenode, icon=conf.ANNOTATOR_ICON_DELETE
		)



	######################################################################
	### EVENTS ###########################################################
	######################################################################

	def __remove_image_event(self):
		item = self.tree.selected_item
		if item is not None: self.video -= item.win
	
	def double_clicked_event(self):
		#cv2.imshow(self.name, self.image)
		self.mainwindow.player.frame = self.image


	######################################################################
	### PROPERTIES #######################################################
	######################################################################
	
	@property
	def mainwindow(self): 	return self.video.mainwindow
	@property
	def tree(self): 		return self.video.tree
	


	@property 
	def parent_treenode(self):  return self.video.treenode

	