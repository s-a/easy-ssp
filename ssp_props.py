import bpy
import json
import os
 
def loadTemplateJson():
    folder = os.path.dirname(bpy.context.blend_data.filepath)
    fn = os.path.join(folder, 'template.json')
    j = None
    if (os.path.exists(fn)):
        with open(fn,'r') as f: 
            j = json.load(f) 
    return j

def items_file(self, context):
    items = []
    j = loadTemplateJson()

    if (j != None):
        items.append(("select_a_parameter", "Select a parameter", "", -1))
        for i in range(len(j["parms"])):
            parm = j["parms"][i]            
            items.append((parm["title"], parm["title"], "", i))

    return items

def get_enum(self):
    # print("get value", bpy.context.scene.sonic_sound_picture_props.current_parm_index)
    return -1

def tryLoadJsonStringValue(json, key):
    if (key in json):
        return json[key]
    else:
        return ""
            
def set_enum(self, index):
    if (index != -1):
        j = loadTemplateJson()
        if (j != None):
            parm = j["parms"][index]
            bpy.context.scene.sonic_sound_picture_props.current_parm_title = tryLoadJsonStringValue(parm, "title")
            bpy.context.scene.sonic_sound_picture_props.current_parm_type = tryLoadJsonStringValue(parm, "type")
            bpy.context.scene.sonic_sound_picture_props.current_parm_value = tryLoadJsonStringValue(parm, "value")
            bpy.context.scene.sonic_sound_picture_props.current_parm_path = tryLoadJsonStringValue(parm, "path")
            bpy.context.scene.sonic_sound_picture_props.current_parm_accept = tryLoadJsonStringValue(parm, "accept")

parm_type = [
    "text",
    "color",
    "file",
]

class SonicSoundPictureTemplatePropertyGroup(bpy.types.PropertyGroup):
    version: bpy.props.StringProperty(name='Template Version', default="1.0.0", description= "Use carefully a valid semver version string (https://semver.org/)")
    minBlenderVersion: bpy.props.StringProperty(name='Minimum Blender Version', default=bpy.app.version_string, description= "Use carefully a valid semver version string (https://semver.org/)" )
    allowCompositionNode: bpy.props.BoolProperty(name='Allow Composition Node', default=False, description= "Will enable/disable option to render with active composition node in SSP GUI")
    allowTransparent: bpy.props.BoolProperty(name='Allow Transparent render', default=False, description= "Will enable/disable option to render transparent image or video in SSP GUI")
    description: bpy.props.StringProperty(name='Description', default="The new Sonic Sound Picture Template", description="Template description displayed in SSP GUI template overview")
    url: bpy.props.StringProperty(name='Url', default="https://github.com/s-a/sonic-sound-picture", description="A link to your social media or template website displayed in SSP GUI template overview")
    license  : bpy.props.EnumProperty(name = "License", description = "The license of your template", default="all-rights-reserved", items = (
        # value, text, tiptool
        ('public-domain', "Public Domain", "When you release your Blender files into the public domain, you are essentially giving up all of your rights to the work. This means that anyone can use, modify, or distribute the work without permission or attribution. This can be a good option if you want to encourage as much use and collaboration as possible."), 
        ('by-nc-nd-3.0', "Attribution Non-commercial No Derivatives", "This license is the most restrictive Creative Commons license, allowing redistribution. This license is often called the “free advertising” license because it allows others to download your works and share them with others as long as they mention you and link back to you, but they can’t change them in any way or use them commercially."),                  
        ('by-nc-sa-3.0', "Attribution Non-commercial Share Alike", "This license lets others remix, tweak, and build upon your work non-commercially, as long as they credit you and license their new creations under the identical terms. Others can download and redistribute your work, but they can also translate, make remixes, and produce new stories based on your work. All new work based on yours will carry the same license, so any derivatives will also be non-commercial in nature."),  
        ('by-nc-3.0', "Attribution Non-commercial", "This license lets others remix, tweak, and build upon your work non-commercially, and although their new works must also acknowledge you and be non-commercial, they don’t have to license their derivative works on the same terms."),  
        ('by-nd-3.0', "Attribution No Derivatives", "This license allows for redistribution, commercial and non-commercial, as long as it is passed along unchanged and in whole, with credit to you."),  
        ('by-sa-3.0', "Attribution Share Alike", "This license lets others remix, tweak, and build upon your work even for commercial reasons, as long as they credit you and license their new creations under the identical terms. This license is often compared to open source software licenses. All new works based on yours will carry the same license, so any derivatives will also allow commercial use."),  
        ('by-3.0', "Attribution", "This license lets others distribute, remix, tweak, and build upon your work, even commercially, as long as they credit you for the original creation. This is the most accommodating of licenses offered, in terms of what others can do with your works licensed under Attribution."),  
        ('gpl-3', "GPL (GNU General Public License)", "This license is often used for open source software, but it can also be used for other creative works. The GPL requires that any derivative works also be licensed under the GPL, which can help ensure that your work remains open and accessible to others."),  
        ('all-rights-reserved', "All rights reserved", "\"All rights reserved\" is a copyright formality indicating that the copyright holder reserves, or holds for its own use, all the rights provided by copyright law.")
    ))
    parms:  bpy.props.EnumProperty(items=items_file, get=get_enum, set=set_enum)
    current_parm_index: bpy.props.IntProperty(name='Index', default=0)
    current_parm_title: bpy.props.StringProperty(name='Title', default="", description="The Title/Name the of the use input control presented to user inside SSP GUI")
    current_parm_value: bpy.props.StringProperty(name='Default Value', default="", description="The default value a the parameter presented to user inside SSP GUI (Useful for colors)")
    current_parm_path: bpy.props.StringProperty(name='Data Path', default="", description="Use \"Copy Full Data Path\"")
    current_parm_type : bpy.props.EnumProperty(name = "Type", description = "The rendered GUI input type inside SSP GUI", default="text", items = (
        # value, text, tiptool
        ('text', "Textbox", "The use can input text via a simple textbox"), 
        ('color', "Color Picker", "The user can select and input a color via a color picker"),                  
        ('file', "File Picker", "The user can select a file via a file picker"),                  
    ))
    current_parm_accept: bpy.props.StringProperty(name='Accept', default="image/png, image/gif, image/jpeg", description="Allow to define acceptable file types for file picker control inside SSP GUI")

def register():
   bpy.utils.register_class(SonicSoundPictureTemplatePropertyGroup) 
   bpy.types.Scene.sonic_sound_picture_props = bpy.props.PointerProperty(type=SonicSoundPictureTemplatePropertyGroup)

def unregister():
    bpy.utils.unregister_class(SonicSoundPictureTemplatePropertyGroup) 
    del bpy.types.Scene.sonic_sound_picture_props