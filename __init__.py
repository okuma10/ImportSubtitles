bl_info = {
    "name": "Subtitle import",
    "description": "Importing subtitles",
    "version": (0, 1),
    "blender": (2, 90, 0),
    "support": "COMMUNITY",
    "category": "Sequencer"
}

import bpy
from .add_external_modules import add_external_modules,remove_external_modules




def register():
    try:
        import pysubs2
    except:
        add_external_modules()
    from .panel import A_OT_RunImport, B_PT_SubImportPanel, A_OT_UpdateSub, GetFileOperator
    bpy.types.Scene.SubImportPath = bpy.props.StringProperty(name="Subtitle Path", default="")
    bpy.utils.register_class(A_OT_RunImport)
    bpy.utils.register_class(B_PT_SubImportPanel)
    bpy.utils.register_class(A_OT_UpdateSub)
    bpy.utils.register_class(GetFileOperator)


def unregister():

    from .panel import A_OT_RunImport, B_PT_SubImportPanel, A_OT_UpdateSub, GetFileOperator
    bpy.utils.unregister_class(A_OT_RunImport)
    bpy.utils.unregister_class(B_PT_SubImportPanel)
    bpy.utils.unregister_class(A_OT_UpdateSub)
    bpy.utils.unregister_class(GetFileOperator)

    pass




