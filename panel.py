from .importSub import *
import bpy


#n Operator
class A_OT_RunImport(bpy.types.Operator):
    '''
    Import or update subtitle sequences.

    '''
    bl_idname = "run.subimport"
    bl_label = " runs the subtitle import script-for now "



    def execute(self,context):
        file = bpy.context.scene.SubImportPath
        fps = bpy.context.scene.render.fps
        subImport(file, fps)
        return {'FINISHED'}

class A_OT_UpdateSub(bpy.types.Operator):
    '''
    Import or update subtitle sequences.

    '''
    bl_idname = "run.subupdate"
    bl_label = " updates the subtitles imported with this script "



    def execute(self,context):
        pos = bpy.context.selected_sequences[0].location
        boxMargin = bpy.context.selected_sequences[0].box_margin
        font_size = bpy.context.selected_sequences[0].font_size
        updateSub(pos, font_size, boxMargin)
        return {'FINISHED'}




#n UI panel
class B_PT_SubImportPanel(bpy.types.Panel):
    bl_label = "SubImport"
    bl_space_type ='SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'SubImport'

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row_col = row.column(align=True)
        row_col.label(text="--Import--")
        row_col.prop(context.scene,'SubImportPath', text="")
        row_col.scale_y = 1
        row_col.scale_x = 2
        row_col.operator('run.subimport', text='Sub Import',icon='TRIA_RIGHT')

        strip = context.active_sequence_strip

        if strip != None and strip.type == 'TEXT':
            layout = self.layout

            layout.use_property_split = True
            col = layout.column()
            col.separator(factor=1.0)
            
            col.label(text="--Update--")
            col.prop(strip, "location", text="Location")
            col.prop(strip, "font_size")
            col.prop(strip, "box_margin")
            col.operator('run.subupdate', text='Sub Update', icon='TRIA_RIGHT')
        else:
            layout = self.layout
            col = layout.column()
            col.separator(factor=1.0)
            col.alignment='CENTER'
            col.label(text="--Update--")
            # col.alignment='LEFT'
            col.label(text="No 'Sub.' sequence selected")
