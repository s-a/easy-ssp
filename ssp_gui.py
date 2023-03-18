import bpy
import os
from bpy_extras.io_utils import ImportHelper
  
class TemplateSettings(bpy.types.Panel):
    bl_parent_id = "CustomToolShelf"
    bl_label = "template.json"
    bl_category = "Example tab"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        #layout.label(text="template.json")
        subrow = layout.row(align=True)
        layout.operator('custom.ssp_load_store', text = 'Load')
        layout.separator()

        subrow = layout.row(align=True)
        subrow.prop(context.scene.sonic_sound_picture_props, 'version')
        subrow = layout.row(align=True)
        subrow.prop(context.scene.sonic_sound_picture_props, 'minBlenderVersion')
        subrow = layout.row(align=True)
        subrow.prop(context.scene.sonic_sound_picture_props, 'allowCompositionNode')
        subrow = layout.row(align=True)
        subrow.prop(context.scene.sonic_sound_picture_props, 'allowTransparent')
        subrow = layout.row(align=True)
        # 
        subrow.prop(context.scene.sonic_sound_picture_props, 'description')
        subrow = layout.row(align=True)
        layout.prop(context.scene.sonic_sound_picture_props, "license") 
        subrow = layout.row(align=True)
        layout.prop(context.scene.sonic_sound_picture_props, "url") 
        layout.separator()
        layout.operator('custom.ssp_save_store', text = 'Save')

        
        layout.separator()
        layout.label(text="Template Parameters")
        layout.prop(context.scene.sonic_sound_picture_props, "parms") 
        row1 = layout.row(align=True)
        box1 = row1.box()
        # box1.label(text="parms 1")
        box1.prop(context.scene.sonic_sound_picture_props, "current_parm_title") 
        box1.prop(context.scene.sonic_sound_picture_props, "current_parm_type") 
        box1.prop(context.scene.sonic_sound_picture_props, "current_parm_value") 
        box1.prop(context.scene.sonic_sound_picture_props, "current_parm_path") 
        box1.prop(context.scene.sonic_sound_picture_props, "current_parm_accept") 
        box1.operator('custom.ssp_parm_save_store', text = 'Save')
        box1.operator('custom.ssp_parm_delete_store', text = 'Delete')

        
#create a panel (class) by deriving from the bpy Panel, this be the UI
class CustomToolShelf(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = 'Sonic Sound Picture'
    bl_context = 'objectmode'
    bl_category = 'Tool'
    
    def draw(self, context):
        layout = self.layout
        
        layout.operator('custom.ssp_create_store', text = 'Create Storage')
        layout.operator('custom.ssp_create_countdown_timer', text = 'Create Countdown Timer')
        
        
classes = (CustomToolShelf, TemplateSettings)


def register():
   for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)