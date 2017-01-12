from pythonvideoannotator_models_gui.models.video.objects.object2d.datasets.contours.contours_gui import ContoursGUI
from pysettings import conf


Contours = type(
	'Contours',
	tuple(conf.MODULES.find_class('models.objects.object2d.datasets.contours.Contours') + [ContoursGUI]),
	{}
)