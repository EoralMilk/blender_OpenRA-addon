import bpy
bl_info = {
    "name": "OpenRA Tools",
    "description": "Easily create OpenRA assets with Blender",
    "author": "Eoral Milk",
    "version": (0, 0, 1),
    "blender": (2, 90, 0),
    "location": "View3D",
    "warning": "This addon is still in development.插件还在开发中.",
    "wiki_url": "",
    "category": "OpenRA"}


class PanelSetting:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ORA"
    bl_context = "objectmode"


def Settings():
    bpy.types.Scene.ORA_Center = bpy.props.StringProperty(
        name="Center", default="Center")
    bpy.types.Scene.ORA_Faces = bpy.props.IntProperty(
        name="Faces", default=8, min=1, max=256)
    bpy.types.Scene.ORA_OneFrame = bpy.props.BoolProperty(
        name="One Frame", default=False, description="Whether to render only the current frame")


class ORA_PT_Render(PanelSetting, bpy.types.Panel):
    bl_idname = "ora.render"
    bl_label = "Render"

    def draw_header(self, context):
        layout = self.layout
        layout.label(icon="OUTLINER_DATA_CAMERA")

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.label(text="Center object:")
        row = layout.row()
        row.prop(scene, 'ORA_Center', text="Name", icon="EMPTY_DATA")
        row = layout.row()
        row.label(text="Render Settings:")
        row = layout.row()
        row.prop(scene, 'ORA_Faces', text="Faces", icon="SPHERE")
        row = layout.row()
        row.prop(scene, 'ORA_OneFrame', text="One Frame")
        row = layout.row()
        row.operator("ora.render", text="Start Render",
                     icon="OUTLINER_DATA_CAMERA")


class ORA_OT_Render(bpy.types.Operator):
    bl_idname = "ora.render"
    bl_label = "Render"
    bl_options = {"REGISTER"}

    def execute(self, context):
        pi2 = 6.28319
        center = context.scene.objects[context.scene.ORA_Center]
        faces = context.scene.ORA_Faces
        anim = not context.scene.ORA_OneFrame

        RGBOs = context.scene.node_tree.nodes["RGB Output"]
        ShadowOs = context.scene.node_tree.nodes["Shadow Output"]
        RGBOs_DefName = RGBOs.file_slots[0].path
        ShadowOs_DefName = ShadowOs.file_slots[0].path

        defRot = center.rotation_euler[2]

        for facing in range(faces):
            strfacing = '%03d' % facing
            RGBOs.file_slots[0].path = RGBOs_DefName + strfacing
            ShadowOs.file_slots[0].path = ShadowOs_DefName + strfacing

            # rendering
            bpy.ops.render.render(animation=anim, use_viewport=True)

            center.rotation_euler[2] += pi2/faces

        center.rotation_euler[2] = defRot
        RGBOs.file_slots[0].path = RGBOs_DefName
        ShadowOs.file_slots[0].path = ShadowOs_DefName
        self.report({"INFO"}, "Render Complete!")

        return {"FINISHED"}


classes = [
    ORA_PT_Render,
    ORA_OT_Render
]


def register():
    for c in classes:
        bpy.utils.register_class(c)
    ...
    Settings()


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    ...


if __name__ == "__main__":
    register()
