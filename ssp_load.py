import os
import bpy
import json

class LoadSSPDataStorageOperator(bpy.types.Operator):
	bl_idname = 'custom.ssp_load_store'
	bl_label = 'Load'
	bl_options = {'INTERNAL'}
	@classmethod
	def poll(cls, context):
		folder = os.path.dirname(bpy.context.blend_data.filepath)
		fn = os.path.join(folder, 'template.json')
		return "SONIC_SOUND_PICTURE_DATA_STORAGE" in bpy.data.objects and bpy.data.is_saved and os.path.exists(fn)
		
	def tryLoadJsonStringValue(self, json, key):
		if (key in json):
			return json[key]
		else:
			return ""

	def tryLoadJsonBoolValue(self, json, key):
		if (key in json):
			return json[key]
		else:
			return False
		
	def execute(self, context):
		a = {
				"version": bpy.app.version_string,
				"minBlenderVersion": "3.4.1",
				"allowCompositionNode": context.scene.sonic_sound_picture_props.allowCompositionNode,
				"allowTransparent": context.scene.sonic_sound_picture_props.allowTransparent,
				"description": context.scene.sonic_sound_picture_props.description,
				"license": context.scene.sonic_sound_picture_props.license,
				"parms": [
					{
						"type": "text",
						"title": "Band Name",
						"value": "",
						"path": "bpy.data.objects[\"Band Name\"].modifiers[\"GeometryNodes\"][\"Input_2\"]"
					},
					{
						"type": "text",
						"title": "Song Name",
						"value": "",
						"path": "bpy.data.objects[\"Song Name\"].modifiers[\"GeometryNodes\"][\"Input_2\"]"
					},
					{
						"type": "color",
						"title": "Background Color",
						"value": "#F2B705",
						"path": "bpy.data.materials[\"Background\"].node_tree.nodes[\"Principled BSDF\"].inputs[0].default_value"
					},
					{
						"type": "color",
						"title": "Foreground Color",
						"value": "#0C0C0D",
						"path": "bpy.data.materials[\"Foreground\"].node_tree.nodes[\"Principled BSDF\"].inputs[0].default_value"
					}
				]
			}

		folder = os.path.dirname(bpy.context.blend_data.filepath)
		fn = os.path.join(folder, 'template.json')
		with open(fn,'r') as f: 
			j=json.load(f) 
			context.scene.sonic_sound_picture_props.version = self.tryLoadJsonStringValue(j, "version")
			context.scene.sonic_sound_picture_props.minBlenderVersion = self.tryLoadJsonStringValue(j, "minBlenderVersion")
			context.scene.sonic_sound_picture_props.allowCompositionNode = self.tryLoadJsonBoolValue(j, "allowCompositionNode")
			context.scene.sonic_sound_picture_props.allowTransparent = self.tryLoadJsonBoolValue(j, "allowTransparent")
			context.scene.sonic_sound_picture_props.description = self.tryLoadJsonStringValue(j, "description")
			context.scene.sonic_sound_picture_props.license = self.tryLoadJsonStringValue(j, "license")
			context.scene.sonic_sound_picture_props.url = self.tryLoadJsonStringValue(j, "url") 
			print (j)
        #context.scene.my_path = self.filepath
        #print (folder, file)
		return {'FINISHED'}
	
def register():
   bpy.utils.register_class(LoadSSPDataStorageOperator) 

def unregister():
	bpy.utils.unregister_class(LoadSSPDataStorageOperator)