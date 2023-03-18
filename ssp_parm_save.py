import bpy
import json
import os

class DeleteSSPTemplateParameterOperator(bpy.types.Operator):
	bl_idname = 'custom.ssp_parm_save_store'
	bl_label = 'Save'
	bl_description="Save parameter to template.json"
	bl_options = {'INTERNAL'}
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
				a = {
					"type": context.scene.sonic_sound_picture_props.current_parm_type,
					"title": context.scene.sonic_sound_picture_props.current_parm_title,
					"value": context.scene.sonic_sound_picture_props.current_parm_value,
					"path": context.scene.sonic_sound_picture_props.current_parm_path
				}
				if (context.scene.sonic_sound_picture_props.current_parm_accept.strip()):
					a["accept"] = context.scene.sonic_sound_picture_props.current_parm_accept

				for item in j["parms"]:
					if item["title"] == context.scene.sonic_sound_picture_props.current_parm_title:
						j["parms"].remove(item)

				j["parms"].append(a)
					
				with open(fn,"w", encoding='utf-8') as jsonfile:
					json.dump(j,jsonfile,ensure_ascii=False, indent=4)
					jsonfile.close()

				self.report({ 'INFO' }, 'Updated "' + context.scene.sonic_sound_picture_props.current_parm_title + '" and written data to "' + fn + '"')
		
		return {'FINISHED'}
	
def register():
   bpy.utils.register_class(DeleteSSPTemplateParameterOperator) 

def unregister():
	bpy.utils.unregister_class(DeleteSSPTemplateParameterOperator)