#import the bpy module to access blender API
import bpy
import sys

bl_info = {
    "name": "easy-ssp",
    "author": "s-a",
    "version": (1, 5),
    "blender": (3, 4, 1),
    "description": "Utility addon to create Sonic Sound Picture (SSP) templates",
    "location": "View3D > Sidebar > Tool > Sonic Sound Picture",
    "category": "Object",
    "support": "COMMUNITY",
    "wiki_url": "https://github.com/s-a/easy-ssp/blob/main/README.md",
    "tracker_url": "https://github.com/s-a/easy-ssp/issues",
    "warning": "",
    "doc": "https://github.com/s-a/easy-ssp/blob/main/README.md"
}
  
modulesNames = [
    'ssp_storage', 
    'ssp_timer_countdown', 
    'ssp_props', 
    'ssp_load', 
    'ssp_save', 
    'ssp_save_thumbnail', 
    'ssp_parm_delete', 
    'ssp_parm_save', 
    'ssp_gui',
    'ssp_context_menu',
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