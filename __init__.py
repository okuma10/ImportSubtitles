bl_info = {
    "name": "Subtitle import",
    "description": "Importing subtitles",
    "version": (0, 1),
    "blender": (2, 90, 0),
    "support": "COMMUNITY",
    "category": "Sequencer"
}

import bpy
from .panel import A_OT_RunImport,B_PT_SubImportPanel,A_OT_UpdateSub



def register():
    #n1 TODO: make this a Property group
    # bpy.types.Scene.prototype_toggle = bpy.props.BoolProperty(name="Toggle", default=False)
    # bpy.types.Scene.is_over_prototype = bpy.props.BoolProperty(name="Is Over", default=False)
    # bpy.types.Scene.prototype_mX = bpy.props.IntProperty(name="MouseX", default=0)
    # bpy.types.Scene.prototype_mY = bpy.props.IntProperty(name="MouseY", default=0)
    # bpy.types.Scene.prototype_mBl = bpy.props.IntProperty(name="MouseButtonLeft", default=0)
    # bpy.types.Scene.prototype_mBm = bpy.props.IntProperty(name="MouseButtonMiddle", default=0)
    # bpy.types.Scene.prototype_mBr = bpy.props.IntProperty(name="MouseButtonRight", default=0)
    # bpy.types.Scene.prototype_draw_context = bpy.props.StringProperty()
    bpy.types.Scene.SubImportPath = bpy.props.StringProperty(name="Subtitle Path", default="")
    bpy.utils.register_class(A_OT_RunImport)
    bpy.utils.register_class(B_PT_SubImportPanel)
    bpy.utils.register_class(A_OT_UpdateSub)




def unregister():
    bpy.utils.unregister_class(A_OT_RunImport)
    bpy.utils.unregister_class(B_PT_SubImportPanel)
    bpy.utils.unregister_class(A_OT_UpdateSub)
    pass




