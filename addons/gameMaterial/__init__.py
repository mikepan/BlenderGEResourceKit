from . import blenderUI
from . import easyMaterial

import imp


imp.reload(easyMaterial)
easyMaterial.refresh()


# sets up the Blender interface
imp.reload(blenderUI)
blenderUI.refresh()

