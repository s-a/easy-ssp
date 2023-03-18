import bpy
from bpy.types import Header, Menu, Panel
from .ssp_object_navigator import ObjectNavigator

def dump(obj, text):
    print('-'*40, text, '-'*40)
    for attr in dir(obj):
        if hasattr(obj, attr):
            value = getattr(obj, attr)
            if isinstance(value, bpy.types.Property):
                print("obj.%s = %s" % (attr, value))
                # print("  Data path: %s" % value.path())
            else:
                print("obj.%s = %s" % (attr, value))
    # print("Full path: ", bpy.path.abspath(obj.bl_rna.filepath))
 
class CopyAndSetupDriver(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.copy_and_setup_driver"
    bl_label = "Create SSP GUI User Input Parameter"

    source: bpy.props.StringProperty()
    @classmethod
    def poll(cls, context):
        return "SONIC_SOUND_PICTURE_DATA_STORAGE" in bpy.data.objects

    def setup_driver(self, full_data_path_target):
        nav = ObjectNavigator()

        path, level, level_type = nav.split_string(full_data_path_target)
        print ("target: ", path, level, level_type)
        print ("source: ", self.source)
        #nav.get_object()
        target_object = nav.get_object(path)
        source_object = bpy.data.objects["SONIC_SOUND_PICTURE_DATA_STORAGE"]
        expr = self.source
        nav.add_driver( target = target_object, source=source_object, prop= level, dataPath= '["' + self.source + '"]', func=expr )    

    def execute(self, context):
        # get the data path
        bpy.ops.ui.copy_data_path_button()
        path = context.window_manager.clipboard

        # get full data path
        bpy.ops.ui.copy_data_path_button(full_path=True)
        full_path = context.window_manager.clipboard
        
        """     
            if hasattr(context, 'button_pointer'):
                btn = context.button_pointer 
                dump(btn, 'button_pointer')
            

            if hasattr(context, 'button_prop'):
                prop = context.button_prop

            if hasattr(context, 'button_operator'):
                op = context.button_operator
        """
        # print (path)
        self.setup_driver(full_path)
        self.report({"INFO"}, "Driver added! " + str(self.source) + " - " + full_path)
   
        return {'FINISHED'}

# This class has to be exactly named like that to insert an entry in the right click menu
class WM_MT_button_context(Menu):
    bl_label = "Add Viddyoze Tag"

    def draw(self, context):
        pass

class SSP_CUSTOM_MT_Menu(bpy.types.Menu):
    bl_label = "First Menu"
    bl_idname = "SSP_CUSTOM_MT_Menu"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Connect SSP Automation Driver", icon='SOUND')
      
        op1 = layout.operator(operator = CopyAndSetupDriver.bl_idname, text="song_beat_id")
        op1.source = "song_beat_id"
        op1 = layout.operator(operator = CopyAndSetupDriver.bl_idname, text="song_bpm")
        op1.source = "song_bpm"
        op1 = layout.operator(operator = CopyAndSetupDriver.bl_idname, text="song_impulse")
        op1.source = "song_impulse"
        op1 = layout.operator(operator = CopyAndSetupDriver.bl_idname, text="song_length_seconds")
        op1.source = "song_length_seconds"
        for i in range(16):
            if i < 10:
                str_num = "0" + str(i)
            else:
                str_num = str(i)
            op1 = layout.operator(operator = CopyAndSetupDriver.bl_idname, text="song_frequency_band_" + str_num)
            op1.source = "song_frequency_band_" + str_num
      
        # call the second custom menu using bl_idname attribute
        """ layout.menu(SSP_CUSTOM_MT_SubMenu.bl_idname, icon="COLLAPSEMENU")
        
         OR use the name of the class
        layout.menu(CUSTOM_MT_SubMenu.__name__, icon="COLLAPSEMENU")
        
         OR just pass the class name as string
        layout.menu("CUSTOM_MT_SubMenu", icon="COLLAPSEMENU")
        
         use an operator enum property to populate a sub-menu
        layout.operator_menu_enum("object.select_by_type",
                                  property="type",
                                  text="Select All Objects by Type...",
                                  ) """
        
class SSP_CUSTOM_MT_SubMenu(bpy.types.Menu):
    bl_label = "Sub Menu"
    bl_idname = "SSP_CUSTOM_MT_SubMenu" # Optional

    def draw(self, context):
        layout = self.layout
        layout.label(text="Hello Second Menu!", icon='WORLD_DATA')

        # call another menu
        layout.operator("wm.call_menu", text="Unwrap").name = "VIEW3D_MT_uv_map"

        # just for fun call the first one again
        layout.menu(SSP_CUSTOM_MT_SubSubMenu.__name__, icon="COLLAPSEMENU")


class SSP_CUSTOM_MT_SubSubMenu(bpy.types.Menu):
    bl_label = "Sub Sub Menu"
    bl_idname = "SSP_CUSTOM_MT_SubSubMenu" # Optional
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="Hello Third Menu!", icon='WORLD_DATA')  

def menu_func(self, context):
    layout = self.layout
    layout.separator()
    layout.label(text="Sonic Sound Picture", icon='SOUND')
    layout.operator(CopyAndSetupDriver.bl_idname)
    layout.operator("wm.call_menu", text="Connect SSP Automation Driver").name = SSP_CUSTOM_MT_Menu.__name__
 
 

classes = (
    SSP_CUSTOM_MT_Menu,
    SSP_CUSTOM_MT_SubMenu,
    SSP_CUSTOM_MT_SubSubMenu,
    CopyAndSetupDriver,
    WM_MT_button_context,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.WM_MT_button_context.append(menu_func)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.types.WM_MT_button_context.remove(menu_func)
