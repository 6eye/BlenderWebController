bl_info = {
    "name": "Blender Web Conttroller",
    "category": "Game Engine",
}

import bpy
import math

class BlenderWebController_pl(bpy.types.Panel):
    bl_idname = "game.panel.webcontroller"
    bl_label = "Web Controller"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    def draw(self, context):
        layout = self.layout

        obj = context.object
        row = layout.row()
        row.operator('game.webcontroller')



class BlenderWebController_op(bpy.types.Operator):
    """Launches a website to contoller a new BGE camera"""      # blender will use this as a tooltip for menu items and buttons.
    bl_idname = "game.webcontroller"        # unique identifier for buttons and menu items to reference.
    bl_label = "Setup Web Controller"         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO' }
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"

    #when to show this add on
    @classmethod
    def poll(self, context):
        return True
    
    
    def execute(self, context):
        bpy.context.scene.render.engine = 'BLENDER_GAME'
        #-------------- Create Text Files --------------------------
        bpy.ops.text.new()
        bpy.data.texts[-1].name = "StartServer"

        #-------------- Add empty Controller ------------------------
        bpy.ops.object.add(type='EMPTY')
        bpy.context.active_object.name = "Controller"
        bpy.data.objects["Controller"].location = (0.0, 0.0, 0.0)

        bpy.ops.logic.sensor_add(       type="DELAY",  name="StartServer")
        bpy.ops.logic.controller_add(   type="PYTHON", name="Sever")
        bpy.ops.logic.actuator_add(     type="MOTION", name="RotateRight")
        bpy.ops.logic.actuator_add(     type="MOTION", name="RotateLeft")
        bpy.ops.logic.actuator_add(     type="MOTION", name="RotateUp")
        bpy.ops.logic.actuator_add(     type="MOTION", name="RotateDown")
        bpy.ops.logic.actuator_add(     type="MOTION", name="ZRotateLeft")
        bpy.ops.logic.actuator_add(     type="MOTION", name="ZRotateRight")

        #------------- Add Camera ----------------
        bpy.ops.object.add(type='CAMERA')
        bpy.context.active_object.name = "ControllerView"
        bpy.data.objects["ControllerView"].location = (0.0, -5.0, 0.0)
        bpy.data.objects["ControllerView"].rotation_euler = (math.radians(90),0.0,0.0)
        bpy.data.objects["ControllerView"].parent = bpy.data.objects["Controller"]
        bpy.ops.logic.actuator_add(type="MOTION", name="ZoomOut")
        bpy.ops.logic.actuator_add(type="MOTION", name="ZoomIn")
        con = bpy.data.objects["ControllerView"].constraints.new('DAMPED_TRACK')
        con.name = "ViewLock"
        con.target = bpy.data.objects["Controller"]
        con.track_axis = 'TRACK_NEGATIVE_Z'
        bpy.context.scene.camera = bpy.data.objects["ControllerView"]

        #------------------ Add Logic Block Info -----------------------
        bpy.data.objects["Controller"].game.sensors["StartServer"].use_repeat           = True
        bpy.data.objects['Controller'].game.controllers['Sever'].use_priority           = True
        bpy.data.objects['Controller'].game.controllers['Sever'].text                   = bpy.data.texts['StartServer']
        bpy.data.objects["Controller"].game.actuators["RotateRight"].offset_rotation    = (0.0,     0.0,   math.radians(-1))
        bpy.data.objects["Controller"].game.actuators["RotateLeft"].offset_rotation     = (0.0,     0.0,    math.radians(1))
        bpy.data.objects["Controller"].game.actuators["RotateUp"].offset_rotation       = (math.radians(1),     0.0,    0.0)
        bpy.data.objects["Controller"].game.actuators["RotateDown"].offset_rotation     = (math.radians(-1),    0.0,    0.0)
        bpy.data.objects["Controller"].game.actuators["ZRotateLeft"].offset_rotation    = (0.0,     math.radians(1),    0.0)
        bpy.data.objects["Controller"].game.actuators["ZRotateRight"].offset_rotation   = (0.0,     math.radians(-1),   0.0)
        bpy.data.objects["ControllerView"].game.actuators["ZoomIn"].offset_location     = (0.0,     0.0,                0.01)
        bpy.data.objects["ControllerView"].game.actuators["ZoomOut"].offset_location    = (0.0,     0.0,                -0.01)

        c = bpy.data.objects['Controller'].game.controllers['Sever']
        bpy.data.objects['Controller'].game.sensors['StartServer'].link(c)
        bpy.data.objects['Controller'].game.actuators['RotateRight'].link(c)
        bpy.data.objects['Controller'].game.actuators['RotateLeft'].link(c)
        bpy.data.objects['Controller'].game.actuators['RotateUp'].link(c)
        bpy.data.objects['Controller'].game.actuators['RotateDown'].link(c)
        bpy.data.objects['Controller'].game.actuators['ZRotateLeft'].link(c)
        bpy.data.objects['Controller'].game.actuators['ZRotateRight'].link(c)
        bpy.data.objects["ControllerView"].game.actuators["ZoomIn"].link(c)
        bpy.data.objects["ControllerView"].game.actuators["ZoomOut"].link(c)

        return {'FINISHED'}  

def register():
    bpy.utils.register_class(BlenderWebController_op)
    bpy.utils.register_class(BlenderWebController_pl)


def unregister():
    bpy.utils.unregister_class(BlenderWebController_op)
    bpy.utils.unregister_class(BlenderWebController_pl)


# This allows you to run the script directly from blenders text editor
# to test the addon without having to install it.
if __name__ == "__main__":
    register()