import bpy
import json
import os

class DeleteSSPTemplateParameterOperator(bpy.types.Operator):
	bl_idname = 'custom.ssp_parm_delete_store'
	bl_label = 'Delete'
	bl_options = {'INTERNAL'}
	bl_description="Delete parameter from template.json"
	@classmethod
	def poll(cls, context):
		folder = os.path.dirname(bpy.context.blend_data.filepath)
		fn = os.path.join(folder, 'template.json')
		return "SONIC_SOUND_PICTURE_DATA_STORAGE" in bpy.data.objects and bpy.data.is_saved and os.path.exists(fn)
		
	def execute(self, context):
		folder = os.path.dirname(bpy.context.blend_data.filepath)
		fn = os.path.join(folder, 'template.json')
		if (os.path.exists(fn)):
			with open(fn,'r') as f: 
				j = json.load(f)
				f.close()
				for item in j["parms"]:
					if item["title"] == context.scene.sonic_sound_picture_props.current_parm_title:
						j["parms"].remove(item)

				with open(fn,"w", encoding='utf-8') as jsonfile:
					json.dump(j,jsonfile,ensure_ascii=False, indent=4)
					jsonfile.close()

				self.report({ 'INFO' }, 'Deleted "' + context.scene.sonic_sound_picture_props.current_parm_title + '" and written data to "' + fn + '"')
		
		return {'FINISHED'}
	
def register():
   bpy.utils.register_class(DeleteSSPTemplateParameterOperator) 

def unregister():
	bpy.utils.unregister_class(DeleteSSPTemplateParameterOperator)