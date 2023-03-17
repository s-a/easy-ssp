import bpy


class CustomPropertyGroup(bpy.types.PropertyGroup):
    #NOTE: read documentation about 'props' to see them and their keyword arguments
    #builtin float (variable)property that blender understands
    float_slider: bpy.props.FloatProperty(name='float value', soft_min=0, soft_max=10)
    #builtin integer (variable)property
    int_slider: bpy.props.IntProperty(name='int value', soft_min=0, soft_max=10)
    #builting boolean (variable)property
    bool_toggle: bpy.props.BoolProperty(name='bool toggle')
    #builting string (variable)property
    string_field: bpy.props.StringProperty(name='start field')    

def register():
   bpy.utils.register_class(CustomPropertyGroup) 
   bpy.types.Scene.custom_props = bpy.props.PointerProperty(type=CustomPropertyGroup)

def unregister():
    bpy.utils.unregister_class(CustomPropertyGroup) 
    del bpy.types.Scene.custom_props