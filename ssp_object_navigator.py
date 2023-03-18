import bpy
import re

class ObjectNavigator:
	def dump(self, obj, text):
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

	def add_driver(self, target, source, prop, dataPath, driverType = 'AVERAGE', func = ''):
		d = target.driver_add( '["' + prop + '"]' ).driver
		d.type = driverType
		d.expression = func 
		v = d.variables.new()
		v.name                 = prop
		v.targets[0].id        = source
		v.targets[0].data_path = dataPath
	def get_object(self, key):
		# Use a regular expression to split the key on the period character, except when it's inside square brackets
		parts = re.split(r'(?<!\[)\.(?![^\[]*\])', key)

		# Skip the first part of the key, which represents the bpy.data object
		if len(parts) > 2:
			parts = parts[2:]
		else:
			# If the key does not contain a period character, return the bpy.data object
			return bpy.data

		# Initialize a variable to hold the current object
		obj = bpy.data

		# Iterate through the parts of the key, using getattr or __getitem__ to access the corresponding attribute of the object at each level
		for part in parts:
			if '[' in part:
				# If the part contains a square bracket, it represents an indexed element, so use __getitem__ to access it
				# First, split the part on the '[' character to separate the attribute name from the index
				attr_parts = part.split('[')
				attr_name = attr_parts[0]  # the attribute name is the part before the '[' character
				index = attr_parts[1][:-1].replace('"', '')  # the index is the part between the '[' and ']' characters

				# Check if the index is a string or an integer, and use the appropriate method to access the element
				try:
					index = int(index)
				except ValueError:
					pass

				# Finally, use __getitem__ to access the indexed element
				obj = getattr(obj, attr_name)[index]
			else:
				# Otherwise, use getattr to access the attribute
				obj =  getattr(obj, part)

		# Return the final object
		return obj

	def split_string(self, s):
		# Find the index of the last '[' or '.' character in the string
		start_index = max(s.rindex('['), s.rindex('.'))

		# Find the index of the ']' character that corresponds to the '[' character found above, if it exists
		try:
			end_index = s.index(']', start_index)
		except ValueError:
			end_index = len(s)

		# Extract the part of the string before the '[' or '.' character
		path = s[:start_index]

		# Extract the part of the string between the '[' or '.' and ']' characters, if it exists
		level = s[start_index + 1:end_index].replace('"', '')

		# Determine the type of the level based on whether it is a number or a string
		if s[start_index:start_index+1] == '.':
			level_type = 'property'
		else:
			level_type = 'array'

		return path, level, level_type

	def set_object_value(self, key, value):
		path, level, level_type = self.split_string(key)
		obj = self.get_object(path)
		if (level_type == 'array'):
			obj[level] = value
		else:
			setattr(obj, level,  value)
		return obj
