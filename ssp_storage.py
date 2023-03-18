import bpy

#in order to make a button do custom behavior we need to register and make an operator, a basic
#custom operator that does not take any property and just runs is easily made like so        
class CreateSSPDataStorageOperator(bpy.types.Operator):
    #the id variable by which we can invoke the operator in blender
    #usually its good practice to have SOMETHING.other_thing as style so we can group
    #many id's together by SOMETHING and we have less chance of overriding existing op's
    bl_idname = 'custom.ssp_create_store'
    #this is the label that essentially is the text displayed on the button
    bl_label = 'Create Storage'
    #these are the options for the operator, this one makes it not appear
    #in the search bar and only accessible by script, useful
    #NOTE: it's a list of strings in {} braces, see blender documentation on types.operator
    bl_options = {'INTERNAL'}

    #this is needed to check if the operator can be executed/invoked
    #in the current context, useful for some but not for this example    
    @classmethod
    def poll(cls, context):
        #check the context here
        return not "SONIC_SOUND_PICTURE_DATA_STORAGE" in bpy.data.objects
    
    def ssp_empty_storage_exists(self):
        return "SONIC_SOUND_PICTURE_DATA_STORAGE" in bpy.data.objects

    def ssp_empty_storage_create(self):
        # Check if the object already exists
        if self.ssp_empty_storage_exists():
            self.report({'INFO'}, "SONIC_SOUND_PICTURE_DATA_STORAGE already exist" )
        else:
            new_object = bpy.data.objects.new("SONIC_SOUND_PICTURE_DATA_STORAGE", None)
            bpy.context.scene.collection.objects.link(new_object)
            self.report({'INFO'}, "SONIC_SOUND_PICTURE_DATA_STORAGE created" )
            return new_object

    def add_custom_property(self, obj, prop_name, prop_value, min_val=None, max_val=None):
        """
        Add a new custom property to an object in Blender.
        
        Parameters:
        obj (bpy.types.Object): The object to add the custom property to.
        prop_name (str): The name of the custom property.
        data_type (str): The data type of the custom property.
        min_val (float): The minimum value for the custom property. Default is None.
        max_val (float): The maximum value for the custom property. Default is None.
        """
        
        obj[prop_name] = prop_value
        obj.id_properties_ensure()  # Make sure the manager is updated
        property_manager = obj.id_properties_ui(prop_name)
        
        if (max_val != None):
            property_manager.update(max=max_val)
        
        if (min_val != None):
            property_manager.update(min=min_val)
            
    #this is the cream of the entire operator class, this one's the function that gets
    #executed when the button is pressed
    def execute(self, context):
        store = self.ssp_empty_storage_create()
        self.add_custom_property(store, "scene_fps", 24, 0, 100)
        self.add_custom_property(store, "song_beat_id", 1, 1, 4)
        self.add_custom_property(store, "song_bpm", 95, 30, 300)
        self.add_custom_property(store, "song_impulse", 1.0, 0, 1)
        self.add_custom_property(store, "song_length_seconds", 1)
        for i in range(16):
            if i < 10:
                str_num = "0" + str(i)
            else:
                str_num = str(i)
            self.add_custom_property(store, "song_frequency_band_" + str_num, 1.0, 0.0, 1.0)

        return {'FINISHED'}
    
def register():
   bpy.utils.register_class(CreateSSPDataStorageOperator) 

def unregister():
    bpy.utils.unregister_class(CreateSSPDataStorageOperator)