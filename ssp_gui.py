import bpy

#create a panel (class) by deriving from the bpy Panel, this be the UI
class CustomToolShelf(bpy.types.Panel):
    #variable for determining which view this panel will be in
    bl_space_type = 'VIEW_3D'
    #this variable tells us where in that view it will be drawn
    bl_region_type = 'UI'
    #this variable is a label/name that is displayed to the user
    bl_label = 'Sonic Sound Picture'
    #this context variable tells when it will be displayed, edit mode, object mode etc
    bl_context = 'objectmode'
    #category is esentially the main UI element, the panels inside it are
    #collapsible dropdown menus drawn under a category
    #you can add your own name, or an existing one and it will be drawn accordingly
    bl_category = 'View'
    
    #now we define a draw method, in it we can tell what elements we want to draw
    #in this new space we created, buttons, toggles etc.
    def draw(self, context):
        #shorten the self.layout to just layout for convenience
        layout = self.layout
        #add a button to it, which is called an operator, its a little tricky to do it but...
        #first argument is a string with the operator name to be invoked
        #in example 'bpy.ops.mesh.primitive_cube_add()' is the function we want to invoke
        #so we invoke it by name 'mesh.primitive_cube_add'
        #then the rest are keyword arguments based on documentation
        #NOTE: for custom operations, you need to define and register an operator with
        #custom name, and then call it by that custom name as we did here
        #the custom operator that we just made will go here as a new button
        layout.operator('custom.ssp_create_store', text = 'Create Storage')
        layout.operator('custom.ssp_create_countdown_timer', text = 'Create Countdown Timer')
        #add multiple items on the same line, like a column layout, from left to right
        # subrow = layout.row(align=True)
        
        #the property will be drawn next to it on the right, as an adjustible slider thing
        # subrow.prop(context.scene.custom_props, 'float_slider')
        #add a label to the UI
        layout.label(text="Template Settings")
        #add a new row with multiple elements in a column
        subrow = layout.row(align=True)
        subrow.prop(context.scene.custom_props, 'bool_toggle')
        
        subrow = layout.row(align=True)
        subrow.prop(context.scene.custom_props, 'int_slider')
        #add a custom text field in the usual layout
        layout.prop(context.scene.custom_props, 'string_field')
        layout.label(text="Template Parms")
        
def register():
   bpy.utils.register_class(CustomToolShelf) 

def unregister():
    bpy.utils.unregister_class(CustomToolShelf)