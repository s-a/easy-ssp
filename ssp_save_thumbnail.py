import bpy
import os

class SaveSSPThumbnailStorageOperator(bpy.types.Operator):
	bl_idname = 'custom.ssp_save_thumbnail'
	bl_label = 'Write Thumbnail'
	bl_description = 'Render and save image as template.png'
	bl_options = {'INTERNAL'}
	@classmethod
	def poll(cls, context):
		return "SONIC_SOUND_PICTURE_DATA_STORAGE" in bpy.data.objects and bpy.data.is_saved
		
	def load_resize_save_png(self, filename, width):
		# Load the PNG file as an Image object
		img = bpy.data.images.load(filename)

		# Calculate the new height while preserving aspect ratio
		ratio = width / img.size[0]
		height = round(img.size[1] * ratio)

		# Resize the image
		img.scale(width, height)

		# Save the image to a new file
		# new_filename = f"{filename.split('.')[0]}_{width}x{height}.png"
		img.save_render(filepath=filename)

		# Unload the image from memory
		bpy.data.images.remove(img)

	def execute(self, context):
		folder = os.path.dirname(bpy.context.blend_data.filepath)
		fn = os.path.join(folder, 'template.png')
		
		context.scene.render.image_settings.file_format = 'PNG'
		context.scene.render.filepath = fn
		bpy.ops.render.render(write_still = 1)
		self.load_resize_save_png(fn, 480)
		self.report({ 'INFO' }, 'Data written to "' + fn + '"')
		return {'FINISHED'}
	
def register():
   bpy.utils.register_class(SaveSSPThumbnailStorageOperator) 

def unregister():
	bpy.utils.unregister_class(SaveSSPThumbnailStorageOperator)