#import the bpy module to access blender API
import bpy
import sys

bl_info = {
    "name": "easy-ssp",
    "author": "s-a",
    "version": (1, 0),
    "blender": (3, 4, 1),
    "description": "Utility addon to create Sonic Sound Picture (SSP) templates",
    "location": "View3D > Sidebar > View",
    "category": "Object",
    "support": "COMMUNITY",
    "wiki_url": "https://github.com/your-username/your-addon/wiki",
    "tracker_url": "https://github.com/your-username/your-addon/issues",
    "warning": "",
    "doc": ""
}
  
modulesNames = [
    'ssp_storage', 
    'ssp_timer_countdown', 
    'ssp_props', 
    'ssp_gui'
]
 
import sys
import importlib
 
modulesFullNames = {}
for currentModuleName in modulesNames:
    if 'DEBUG_MODE' in sys.argv:
        modulesFullNames[currentModuleName] = ('{}'.format(currentModuleName))
    else:
        modulesFullNames[currentModuleName] = ('{}.{}'.format(__name__, currentModuleName))
 
for currentModuleFullName in modulesFullNames.values():
    if currentModuleFullName in sys.modules:
        importlib.reload(sys.modules[currentModuleFullName])
    else:
        globals()[currentModuleFullName] = importlib.import_module(currentModuleFullName)
        setattr(globals()[currentModuleFullName], 'modulesNames', modulesFullNames)
 
def register():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'register'):
                sys.modules[currentModuleName].register()
 
def unregister():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'unregister'):
                sys.modules[currentModuleName].unregister()
 
if __name__ == "__main__":
    register()