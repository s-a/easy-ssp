import bpy
import json
import os

class SaveSSPDataStorageOperator(bpy.types.Operator):
	bl_idname = 'custom.ssp_save_store'
	bl_label = 'Save'
	bl_description = 'Save template.json'
	bl_options = {'INTERNAL'}
	@classmethod
	def poll(cls, context):
		return "SONIC_SOUND_PICTURE_DATA_STORAGE" in bpy.data.objects and bpy.data.is_saved
		
	def execute(self, context):
		folder = os.path.dirname(bpy.context.blend_data.filepath)
		fn = os.path.join(folder, 'template.json')
		a = {
			"version": context.scene.sonic_sound_picture_props.version,
			"minBlenderVersion": "3.4.1",
			"allowCompositionNode": context.scene.sonic_sound_picture_props.allowCompositionNode,
			"allowTransparent": context.scene.sonic_sound_picture_props.allowTransparent,
			"description": context.scene.sonic_sound_picture_props.description,
			"license": context.scene.sonic_sound_picture_props.license,
			"url": context.scene.sonic_sound_picture_props.url,
			"parms": []
		}
		if (os.path.exists(fn)):
			with open(fn,'r') as f: 
				j = json.load(f)
				a["parms"] = j["parms"] 
				f.close()

		with open(fn,"w", encoding='utf-8') as jsonfile:
			json.dump(a,jsonfile,ensure_ascii=False, indent=4)
			jsonfile.close()

		self.report({ 'INFO' }, 'Data written to "' + fn + '"')
		return {'FINISHED'}
	
def register():
   bpy.utils.register_class(SaveSSPDataStorageOperator) 

def unregister():
	bpy.utils.unregister_class(SaveSSPDataStorageOperator)