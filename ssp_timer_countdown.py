import bpy
import re
 
# from .ssp_object_navigator import ObjectNavigator

#in order to make a button do custom behavior we need to register and make an operator, a basic
#custom operator that does not take any property and just runs is easily made like so        
class CreateTimerCountdownOperator(bpy.types.Operator):
    #the id variable by which we can invoke the operator in blender
    #usually its good practice to have SOMETHING.other_thing as style so we can group
    #many id's together by SOMETHING and we have less chance of overriding existing op's
    bl_idname = 'custom.ssp_create_countdown_timer'
    #this is the label that essentially is the text displayed on the button
    bl_label = 'Create Countdown Timer'
    #these are the options for the operator, this one makes it not appear
    #in the search bar and only accessible by script, useful
    #NOTE: it's a list of strings in {} braces, see blender documentation on types.operator
    bl_options = {'INTERNAL'}

    #this is needed to check if the operator can be executed/invoked
    #in the current context, useful for some but not for this example    
    @classmethod
    def poll(cls, context):
        #check the context here
        return "SONIC_SOUND_PICTURE_DATA_STORAGE" in bpy.data.objects
    
    def ssp_empty_storage_exists(self):
        return "SONIC_SOUND_PICTURE_DATA_STORAGE" in bpy.data.objects
            
    #this is the cream of the entire operator class, this one's the function that gets
    #executed when the button is pressed
    def time_countdown_node_group(self):
        time_countdown= bpy.data.node_groups.new(type = "GeometryNodeTree", name = "Time Countdown")

        #initialize time_countdown nodes
        #time_countdown outputs
        time_countdown.outputs.new("NodeSocketGeometry", "Geometry")
        time_countdown.outputs[0].attribute_domain = 'POINT'

        #node Group Output
        group_output = time_countdown.nodes.new("NodeGroupOutput")

        #node String to Curves
        string_to_curves = time_countdown.nodes.new("GeometryNodeStringToCurves")
        string_to_curves.overflow = 'OVERFLOW'
        string_to_curves.align_x = 'LEFT'
        string_to_curves.align_y = 'TOP_BASELINE'
        string_to_curves.pivot_mode = 'BOTTOM_LEFT'
        #Size
        string_to_curves.inputs[1].default_value = 1.0
        #Character Spacing
        string_to_curves.inputs[2].default_value = 1.0
        #Word Spacing
        string_to_curves.inputs[3].default_value = 1.0
        #Line Spacing
        string_to_curves.inputs[4].default_value = 1.0
        #Text Box Width
        string_to_curves.inputs[5].default_value = 0.0
        #Text Box Height
        string_to_curves.inputs[6].default_value = 0.0

        #node Set Material
        set_material = time_countdown.nodes.new("GeometryNodeSetMaterial")
        #Selection
        set_material.inputs[1].default_value = True

        #node Join Geometry
        join_geometry = time_countdown.nodes.new("GeometryNodeJoinGeometry")

        #node Fill Curve
        fill_curve = time_countdown.nodes.new("GeometryNodeFillCurve")
        fill_curve.mode = 'TRIANGLES'

        #node Value to String
        value_to_string = time_countdown.nodes.new("FunctionNodeValueToString")
        #Decimals
        value_to_string.inputs[1].default_value = 0

        #node Math
        math = time_countdown.nodes.new("ShaderNodeMath")
        math.operation = 'DIVIDE'
        #Value_001
        math.inputs[1].default_value = 60.0
        #Value_002
        math.inputs[2].default_value = 0.5

        #node Math.001
        math_001 = time_countdown.nodes.new("ShaderNodeMath")
        math_001.operation = 'TRUNC'
        #Value_001
        math_001.inputs[1].default_value = 0.5
        #Value_002
        math_001.inputs[2].default_value = 0.5

        #node Join Strings
        join_strings = time_countdown.nodes.new("GeometryNodeStringJoin")
        #Delimiter
        join_strings.inputs[0].default_value = ":"

        #node Switch
        switch = time_countdown.nodes.new("GeometryNodeSwitch")
        switch.input_type = 'STRING'
        #False
        switch.inputs[2].default_value = 0.0
        #True
        switch.inputs[3].default_value = 0.0
        #False_001
        switch.inputs[4].default_value = 0
        #True_001
        switch.inputs[5].default_value = 0
        #False_002
        switch.inputs[6].default_value = False
        #True_002
        switch.inputs[7].default_value = True
        #False_003
        switch.inputs[8].default_value = (0.0, 0.0, 0.0)
        #True_003
        switch.inputs[9].default_value = (0.0, 0.0, 0.0)
        #False_004
        switch.inputs[10].default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
        #True_004
        switch.inputs[11].default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
        #False_005
        switch.inputs[12].default_value = ""
        #True_005
        switch.inputs[13].default_value = "0"

        #node Reroute
        reroute = time_countdown.nodes.new("NodeReroute")
        #node Reroute.001
        reroute_001 = time_countdown.nodes.new("NodeReroute")
        #node Math.002
        math_002 = time_countdown.nodes.new("ShaderNodeMath")
        math_002.operation = 'LESS_THAN'
        #Value_001
        math_002.inputs[1].default_value = 10.0
        #Value_002
        math_002.inputs[2].default_value = 0.5

        #time_countdown inputs
        #input Geometry
        time_countdown.inputs.new("NodeSocketGeometry", "Geometry")

        #input TotalSeconds
        time_countdown.inputs.new("NodeSocketInt", "TotalSeconds")
        time_countdown.inputs[1].default_value = 0
        time_countdown.inputs[1].min_value = -2147483648
        time_countdown.inputs[1].max_value = 2147483647

        #input Material
        time_countdown.inputs.new("NodeSocketMaterial", "Material")


        #node Group Input
        group_input = time_countdown.nodes.new("NodeGroupInput")

        #node Scene Time
        scene_time = time_countdown.nodes.new("GeometryNodeInputSceneTime")

        #node Math.006
        math_006 = time_countdown.nodes.new("ShaderNodeMath")
        math_006.operation = 'SUBTRACT'
        #Value_002
        math_006.inputs[2].default_value = 0.5

        #node Math.005
        math_005 = time_countdown.nodes.new("ShaderNodeMath")
        math_005.operation = 'ABSOLUTE'
        #Value_001
        math_005.inputs[1].default_value = 60.0
        #Value_002
        math_005.inputs[2].default_value = 0.5

        #node Value to String.001
        value_to_string_001 = time_countdown.nodes.new("FunctionNodeValueToString")
        #Decimals
        value_to_string_001.inputs[1].default_value = 0

        #node Join Strings.001
        join_strings_001 = time_countdown.nodes.new("GeometryNodeStringJoin")
        #Delimiter
        join_strings_001.inputs[0].default_value = ""

        #node Math.004
        math_004 = time_countdown.nodes.new("ShaderNodeMath")
        math_004.operation = 'MODULO'
        #Value_001
        math_004.inputs[1].default_value = 60.0
        #Value_002
        math_004.inputs[2].default_value = 0.5

        #node Math.003
        math_003 = time_countdown.nodes.new("ShaderNodeMath")
        math_003.operation = 'TRUNC'
        #Value_001
        math_003.inputs[1].default_value = 0.5
        #Value_002
        math_003.inputs[2].default_value = 0.5

        #Set parents

        #Set locations
        group_output.location = (1063.107666015625, 0.0)
        string_to_curves.location = (271.2082824707031, 53.80760955810547)
        set_material.location = (794.931640625, -77.83922576904297)
        join_geometry.location = (861.9017944335938, 110.35808563232422)
        fill_curve.location = (575.1077880859375, -23.680580139160156)
        value_to_string.location = (-517.4986572265625, -136.13328552246094)
        math.location = (-957.2122802734375, -128.5897216796875)
        math_001.location = (-737.2122802734375, -119.74195098876953)
        join_strings.location = (50.72882080078125, -97.87395477294922)
        switch.location = (-562.0829467773438, -332.1725158691406)
        reroute.location = (-1322.0, -365.79144287109375)
        reroute_001.location = (-666.0, -646.43115234375)
        math_002.location = (-752.7150268554688, -354.92388916015625)
        group_input.location = (-2042.5443115234375, -181.13905334472656)
        scene_time.location = (-2021.193115234375, -331.2602233886719)
        math_006.location = (-1770.2362060546875, -158.28089904785156)
        math_005.location = (-1550.0, -165.69219970703125)
        value_to_string_001.location = (-547.8596801757812, -581.1226806640625)
        join_strings_001.location = (-336.318359375, -405.3781433105469)
        math_004.location = (-982.5480346679688, -573.1943359375)
        math_003.location = (-1220.3724365234375, -570.2955322265625)

        #sSet dimensions
        group_output.width, group_output.height = 140.0, 100.0
        string_to_curves.width, string_to_curves.height = 190.0, 100.0
        set_material.width, set_material.height = 140.0, 100.0
        join_geometry.width, join_geometry.height = 140.0, 100.0
        fill_curve.width, fill_curve.height = 140.0, 100.0
        value_to_string.width, value_to_string.height = 140.0, 100.0
        math.width, math.height = 140.0, 100.0
        math_001.width, math_001.height = 140.0, 100.0
        join_strings.width, join_strings.height = 140.0, 100.0
        switch.width, switch.height = 140.0, 100.0
        reroute.width, reroute.height = 16.0, 100.0
        reroute_001.width, reroute_001.height = 16.0, 100.0
        math_002.width, math_002.height = 140.0, 100.0
        group_input.width, group_input.height = 140.0, 100.0
        scene_time.width, scene_time.height = 140.0, 100.0
        math_006.width, math_006.height = 140.0, 100.0
        math_005.width, math_005.height = 140.0, 100.0
        value_to_string_001.width, value_to_string_001.height = 140.0, 100.0
        join_strings_001.width, join_strings_001.height = 140.0, 100.0
        math_004.width, math_004.height = 140.0, 100.0
        math_003.width, math_003.height = 140.0, 100.0

        #initialize time_countdown links
        #join_strings.String -> string_to_curves.String
        time_countdown.links.new(join_strings.outputs[0], string_to_curves.inputs[0])
        #fill_curve.Mesh -> set_material.Geometry
        time_countdown.links.new(fill_curve.outputs[0], set_material.inputs[0])
        #set_material.Geometry -> join_geometry.Geometry
        time_countdown.links.new(set_material.outputs[0], join_geometry.inputs[0])
        #join_geometry.Geometry -> group_output.Geometry
        time_countdown.links.new(join_geometry.outputs[0], group_output.inputs[0])
        #string_to_curves.Curve Instances -> fill_curve.Curve
        time_countdown.links.new(string_to_curves.outputs[0], fill_curve.inputs[0])
        #math_001.Value -> value_to_string.Value
        time_countdown.links.new(math_001.outputs[0], value_to_string.inputs[0])
        #reroute.Output -> math.Value
        time_countdown.links.new(reroute.outputs[0], math.inputs[0])
        #math.Value -> math_001.Value
        time_countdown.links.new(math.outputs[0], math_001.inputs[0])
        #value_to_string.String -> join_strings.Strings
        time_countdown.links.new(value_to_string.outputs[0], join_strings.inputs[1])
        #reroute_001.Output -> value_to_string_001.Value
        time_countdown.links.new(reroute_001.outputs[0], value_to_string_001.inputs[0])
        #math_003.Value -> math_004.Value
        time_countdown.links.new(math_003.outputs[0], math_004.inputs[0])
        #join_strings_001.String -> join_strings.Strings
        time_countdown.links.new(join_strings_001.outputs[0], join_strings.inputs[1])
        #math_002.Value -> switch.Switch
        time_countdown.links.new(math_002.outputs[0], switch.inputs[1])
        #math_002.Value -> switch.Switch
        time_countdown.links.new(math_002.outputs[0], switch.inputs[0])
        #switch.Output -> join_strings_001.Strings
        time_countdown.links.new(switch.outputs[5], join_strings_001.inputs[1])
        #value_to_string_001.String -> join_strings_001.Strings
        time_countdown.links.new(value_to_string_001.outputs[0], join_strings_001.inputs[1])
        #reroute.Output -> math_003.Value
        time_countdown.links.new(reroute.outputs[0], math_003.inputs[0])
        #reroute_001.Output -> math_002.Value
        time_countdown.links.new(reroute_001.outputs[0], math_002.inputs[0])
        #group_input.TotalSeconds -> math_006.Value
        time_countdown.links.new(group_input.outputs[1], math_006.inputs[0])
        #math_005.Value -> reroute.Input
        time_countdown.links.new(math_005.outputs[0], reroute.inputs[0])
        #scene_time.Seconds -> math_006.Value
        time_countdown.links.new(scene_time.outputs[0], math_006.inputs[1])
        #math_004.Value -> reroute_001.Input
        time_countdown.links.new(math_004.outputs[0], reroute_001.inputs[0])
        #math_006.Value -> math_005.Value
        time_countdown.links.new(math_006.outputs[0], math_005.inputs[0])
        #group_input.Material -> set_material.Material
        time_countdown.links.new(group_input.outputs[2], set_material.inputs[2])
        return time_countdown

    def add_driver(self, target, source, prop, dataPath, driverType = 'AVERAGE', func = ''):
        d = target.driver_add( prop ).driver
        d.type = driverType
        d.expression = func 
        v = d.variables.new()
        v.name                 = prop
        v.targets[0].id        = source
        v.targets[0].data_path = dataPath

        
    def setup_driver(self):
        target_object = bpy.data.objects["Countdown Timer"].modifiers["Time Countdown"]
        source_object = bpy.data.objects["SONIC_SOUND_PICTURE_DATA_STORAGE"]
        expr = "song_length_seconds"
        self.add_driver( target = target_object, source=source_object, prop='["Input_2"]', dataPath= '["song_length_seconds"]', func=expr )    

    def execute(self, context):
		#initialize time_countdown node group
        time_countdown = self.time_countdown_node_group()

        #name = bpy.context.object.name
        #obj = bpy.data.objects[name]
        # Create a new cube object
        bpy.ops.mesh.primitive_cube_add()

        # Get the active object (which should be the cube)
        obj = bpy.context.active_object

        # Set the name of the cube to "Countdown Timer"
        obj.name = "Countdown Timer"
        
        mod = obj.modifiers.new(name = "Time Countdown", type = 'NODES')
        mod.node_group = time_countdown

        self.setup_driver()
        
        self.report({ 'INFO' }, 'TODO: Adjust Material and Fix String join order in "Countdown Timer"s geometry node.')
        return {'FINISHED'}
    
def register():
   bpy.utils.register_class(CreateTimerCountdownOperator) 

def unregister():
    bpy.utils.unregister_class(CreateTimerCountdownOperator)