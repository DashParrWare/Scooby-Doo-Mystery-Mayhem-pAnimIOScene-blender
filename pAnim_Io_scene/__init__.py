bl_info = {
        'name'			: 'Scooby Doo Mystery Mayhem Animation Importer',
	'author'		: 'Calum Underwood',
	'version'		: (0, 0, 2),
	'blender'		: (3, 0, 0),
	'location'		: 'File > Import-Export',
	'description'           : 'Import pAnim Still needs WIP',
	'category'		: 'Panimation'
}
import os
import bpy
import importlib
from bpy.props import CollectionProperty, StringProperty, BoolProperty, EnumProperty, FloatProperty, IntProperty
from bpy_extras.io_utils import ImportHelper


from.import pAnim

class ImportPAnim(bpy.types.Operator, ImportHelper):
        bl_idname  = 'panim_importer.panim'
        bl_label   = 'Import Panim panim'
        bl_options = {'UNDO'}
        filename_ext = '.panim'
        files: CollectionProperty(
                name	    = 'File path',
                description = 'File path used for finding the Panim file.',
                type	    = bpy.types.OperatorFileListElement
        )
        directory: StringProperty()
        filter_glob: StringProperty(default = '*.panim', options = {'HIDDEN'})
        def execute(self, context):
                paths = [os.path.join(self.directory, name.name) for name in self.files]
                if not paths: paths.append(self.filepath)
                importlib.reload(pAnim)
                for path in paths: pAnim.pAnim_importing(path)
                return {'FINISHED'}
            
def menu_func_import(self, context):
        self.layout.operator(ImportPAnim.bl_idname, text='Scooby Doo Mystery Mayhem (.panim)')

def register():
        bpy.utils.register_class(ImportPAnim)
        bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
def unregister():
        bpy.utils.unregister_class(ImportPAnim)
        bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
if __name__ == '__main__':
        register()
