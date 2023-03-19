import bpy
import math
import re
from .ssp_object_navigator import ObjectNavigator
 
class CopyAndSetupDriver(bpy.types.Operator):
    """Copy Driver From Automation Storage"""
    bl_idname = "object.copy_and_setup_driver"
    bl_label = "Copy and setup SSP driver"

    source: bpy.props.StringProperty()
   
    @classmethod
    def poll(cls, context):
        return "SONIC_SOUND_PICTURE_DATA_STORAGE" in bpy.data.objects

    def add_driver(self, level, target, source, prop, dataPath, driverType = 'AVERAGE', func = '', child_prop = None):
        
        if "[" in prop:
            print ("COMPLEX ADD_DRIVER", level, prop, dataPath)
            parts = prop.split('[')
            parts[1] = int(parts[1].replace("]", ""))
            print ("COMPLEX ADD_DRIVER ------------------", parts)
            print('<---------------------', prop)
            d = target.driver_add( parts[0], parts[1] ).driver
            prop = parts[0]
        else:
            print ("SIMPLE ADD_DRIVER", prop)
            d = target.driver_add( prop ).driver
        
        d.type = driverType
        d.expression = func 
        v = d.variables.new()
        v.name                 = prop
        v.targets[0].id        = source
        v.targets[0].data_path = dataPath

    def setup_driver(self, full_data_path_target, prop = None):
        nav = ObjectNavigator()

        path, level, level_type = nav.split_string(full_data_path_target)
        print ("target: ", path, level, level_type)
        print ("source: ", self.source)
        
        if (prop == None):
            prop = level

        target_object = nav.get_object(full_data_path_target)
        source_object = bpy.data.objects["SONIC_SOUND_PICTURE_DATA_STORAGE"]
        expr = self.source
        cmd = '["SONIC_SOUND_PICTURE_DATA_STORAGE"].' + str(self.source) + " -> " + full_data_path_target + '.' + prop
        print ('Try ' + cmd)
        self.add_driver(level=level, target = target_object, source=source_object, prop= prop, dataPath= '["' + self.source + '"]', func=expr )    
        self.report({"INFO"}, 'Driver added! ' + cmd)

        """     
                if hasattr(context, 'button_pointer'):
                    btn = context.button_pointer 
                    dump(btn, 'button_pointer')
                

                if hasattr(context, 'button_prop'):
                    prop = context.button_prop

                if hasattr(context, 'button_operator'):
                    op = context.button_operator
            """
    def extract_parent_child(self, path):

        parts = re.split(r'(?<!\[)\.(?![^\[]*\])', path)
        print ("FULL DATA PATH", parts)

        parent_str = ".".join(parts[:-1])
        child_str = parts[-1]

        return parent_str, child_str
    
    def execute(self, context):
        # get the data path
        bpy.ops.ui.copy_data_path_button()
        path = context.window_manager.clipboard

        # get full data path
        bpy.ops.ui.copy_data_path_button(full_path=True)
        full_path = context.window_manager.clipboard
        
        print ("__________________________________________________")
        nav = ObjectNavigator()
        obj = nav.get_object(full_path)
        if hasattr(obj, 'driver_add') and callable(getattr(obj, 'driver_add')):
            print("The '" + full_path + "' has a method called driver_add")
            self.setup_driver(full_path)
        else:
            print("The'" + full_path + "' does NOT have a method called driver_add... try parent")
            parent, child = self.extract_parent_child(full_path)
            print(parent, child)
            obj = nav.get_object(parent)
            if hasattr(obj, 'driver_add') and callable(getattr(obj, 'driver_add')):
                print("The '" + parent + "' has a method called driver_add")
                self.setup_driver(parent, child)
            else:
                print("The '" + parent + "' does NOT have a method called driver_add")
                self.report({"WARNING"}, 'Sowwy..., driver NOT added! Please do manual via "Copy As New Driver" and "Paste Driver"')
   
        return {'FINISHED'}

class AddGUIParameter(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.add_ssp_gui_user_input_parameter"
    bl_label = "Create SSP GUI User Input Parameter"
 
    @classmethod
    def poll(cls, context):
        return "SONIC_SOUND_PICTURE_DATA_STORAGE" in bpy.data.objects


    def srgb_to_linearrgb(self, c):
        if c < 0:
            return 0
        elif c < 0.04045:
            return c / 12.92
        else:
            return ((c + 0.055) / 1.055) ** 2.4

    def linearrgb_to_srgb(self, c):
        if c < 0:
            return 0
        elif c > 1:
            return 1
        elif c < 0.0031308:
            return 12.92 * c
        else:
            return 1.055 * c ** (1/2.4) - 0.055

    def node_socket_color_to_hex_string(self, color):
        """
        Converts a NodeSocketColor object to a hexadecimal color string.

        Parameters:
            color (bpy.types.NodeSocketColor): The color to convert.

        Returns:
            A string representing the color in hexadecimal format with a leading hash tag.
        """
        # Convert the color components from sRGB to linear RGB
        r_lin = self.srgb_to_linearrgb(color[0])
        g_lin = self.srgb_to_linearrgb(color[1])
        b_lin = self.srgb_to_linearrgb(color[2])

        # Convert the linear RGB components to sRGB
        r_srgb = self.linearrgb_to_srgb(r_lin)
        g_srgb = self.linearrgb_to_srgb(g_lin)
        b_srgb = self.linearrgb_to_srgb(b_lin)

        # Convert the sRGB components from float to integer values
        r = int(r_srgb * 255)
        g = int(g_srgb * 255)
        b = int(b_srgb * 255)

        # Format the color components as a hexadecimal string
        hex_string = '{:02X}{:02X}{:02X}'.format(r, g, b)

        # Ensure the hex string has a length of 6 with a leading hash tag
        hex_string = '#' + hex_string.zfill(6)

        return hex_string

         
    
    def execute(self, context):
        # get the data path
        bpy.ops.ui.copy_data_path_button()
        path = context.window_manager.clipboard

        # get full data path
        bpy.ops.ui.copy_data_path_button(full_path=True)
        full_path = context.window_manager.clipboard
         
        nav = ObjectNavigator()
        # print (path)
        value = nav.get_object(full_path)

        context.scene.sonic_sound_picture_props.current_parm_title = ""
        context.scene.sonic_sound_picture_props.current_parm_accept = ""
        if isinstance(value, bpy.types.bpy_prop_array) and len(value) == 4:
            context.scene.sonic_sound_picture_props.current_parm_type = 'color'
            value = self.node_socket_color_to_hex_string(value)
        else:
            value = str(value)
            context.scene.sonic_sound_picture_props.current_parm_type = 'text'

        context.scene.sonic_sound_picture_props.current_parm_value = value
        context.scene.sonic_sound_picture_props.current_parm_path = full_path
        # if hasattr(context, 'button_pointer'):
        #    path, level, level_type = nav.split_string(full_path)
        #    btn = context.button_pointer 
        #    nav.dump(btn, '________________________________________')
        #    context.scene.sonic_sound_picture_props.current_parm_title = btn.name + ' ' + path + level
        
        self.report({"INFO"}, "Parameter prepared. Adjust and save! " + full_path)
   
        return {'FINISHED'}

# This class has to be exactly named like that to insert an entry in the right click menu
class WM_MT_button_context(bpy.types.Menu):
    bl_label = "SSP"

    def draw(self, context):
        pass

class SSP_CUSTOM_MT_Menu(bpy.types.Menu):
    bl_label = "Sonic Sound Picture"
    bl_idname = "SSP_CUSTOM_MT_Menu"

    @classmethod
    def poll(cls, context):
        return "SONIC_SOUND_PICTURE_DATA_STORAGE" in bpy.data.objects

    def draw(self, context):
        layout = self.layout
        layout.label(text="Connect SSP Automation Driver", icon='SOUND')
      
        op = layout.operator(operator = CopyAndSetupDriver.bl_idname, text="song_beat_id")
        op.source = "song_beat_id"
        op = layout.operator(operator = CopyAndSetupDriver.bl_idname, text="song_bpm")
        op.source = "song_bpm"
        op = layout.operator(operator = CopyAndSetupDriver.bl_idname, text="song_impulse")
        op.source = "song_impulse"
        op = layout.operator(operator = CopyAndSetupDriver.bl_idname, text="song_length_seconds")
        op.source = "song_length_seconds"
        for i in range(16):
            if i < 10:
                str_num = "0" + str(i)
            else:
                str_num = str(i)
            op = layout.operator(operator = CopyAndSetupDriver.bl_idname, text="song_frequency_band_" + str_num)
            op.source = "song_frequency_band_" + str_num
      
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
    layout.operator(AddGUIParameter.bl_idname)
    layout.operator("wm.call_menu", text="Connect SSP Automation Driver").name = SSP_CUSTOM_MT_Menu.__name__
 
 

classes = (
    SSP_CUSTOM_MT_Menu,
    SSP_CUSTOM_MT_SubMenu,
    SSP_CUSTOM_MT_SubSubMenu,
    CopyAndSetupDriver,
    AddGUIParameter,
    WM_MT_button_context,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.WM_MT_button_context.append(menu_func)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
