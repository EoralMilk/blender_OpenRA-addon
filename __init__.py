import bpy
bl_info = {
    "name": "OpenRA Tools",
    "description": "Easily create OpenRA assets with Blender",
    "author": "Eoral Milk",
    "version": (0, 0, 2),
    "blender": (2, 90, 0),
    "location": "View3D",
    "warning": "This addon is still in development.插件还在开发中.",
    "wiki_url": "",
    "category": "OpenRA"}

# 面板基础设定


class PanelSetting:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ORA"
    bl_context = "objectmode"

# 全部RNA属性


def Settings():
    bpy.types.Scene.ORA_Center = bpy.props.StringProperty(
        name="Center", default="Center")
    bpy.types.Scene.ORA_Faces = bpy.props.IntProperty(
        name="Faces", default=8, min=1, max=256)

    bpy.types.Scene.ORA_OneFrame = bpy.props.BoolProperty(
        name="One Frame", default=False, description="Whether to render only the current frame")
    bpy.types.Scene.ORA_UseAlpha = bpy.props.BoolProperty(
        name="Use Alpha", default=False, description="Whether to render only with Alpha")

    bpy.types.Scene.ORA_OutPath = bpy.props.StringProperty(
        name="Output Path", description="Change the image output path", default="D: \\Blender-Desk\\OUT PUT\\")


# 渲染总面板

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
        row.operator("ora.render", text="Start Render",
                     icon="OUTLINER_DATA_CAMERA")

# 渲染设置面板


class ORA_PT_RenderSet(PanelSetting, bpy.types.Panel):
    bl_idname = "ora.renderset"
    bl_label = "Render Settings"
    bl_parent_id = "ora.render"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.prop(scene, 'ORA_Faces', text="Faces", icon="SPHERE")
        row = layout.row()
        row.prop(scene, 'ORA_OneFrame', text="One Frame")

# 输出设置面板


class ORA_PT_OutputSet(PanelSetting, bpy.types.Panel):
    bl_idname = "ora.outputset"
    bl_label = "Output Settings"
    bl_parent_id = "ora.render"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.prop(scene, 'ORA_UseAlpha', text="Use Alpha")
        row = layout.row()
        row.prop(scene, 'ORA_OutPath', text="Path")

        row = layout.row()
        row.operator("ora.setup", text="Use Output settings",
                     icon="CHECKMARK")


# 渲染器
class ORA_OT_Render(bpy.types.Operator):
    bl_idname = "ora.render"
    bl_label = "Render"
    bl_options = {"REGISTER"}

    def execute(self, context):
        # Common
        pi2 = 6.28319
        # Base Settings
        center = context.scene.objects[context.scene.ORA_Center]
        faces = context.scene.ORA_Faces
        # BoolSwitch
        anim = not context.scene.ORA_OneFrame
        # Out Put Path
        RGBOs = context.scene.node_tree.nodes["RGB Output"]
        ShadowOs = context.scene.node_tree.nodes["Shadow Output"]
        RGBOs_DefName = RGBOs.file_slots[0].path
        ShadowOs_DefName = ShadowOs.file_slots[0].path
        # Rotation
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


# 启用输出设置
class ORA_OT_SetUp(bpy.types.Operator):
    bl_idname = "ora.setup"
    bl_label = "SetUp"
    bl_options = {"REGISTER"}

    def execute(self, context):

        # BoolSwitch
        alpha = context.scene.ORA_UseAlpha

        # Out Put Path
        output = context.scene.ORA_OutPath

        # SetUp
        context.scene.node_tree.nodes["AlphaSwitch"].check = alpha
        context.scene.node_tree.nodes["AlphaSwitch-Shadow"].check = alpha

        context.scene.node_tree.nodes["RGB Output"].base_path = output
        context.scene.node_tree.nodes["Shadow Output"].base_path = output

        self.report({"INFO"}, "Settings enabled")

        return {"FINISHED"}


# 全部类注册表
classes = [
    ORA_PT_Render,
    ORA_PT_RenderSet,
    ORA_PT_OutputSet,
    ORA_OT_Render,
    ORA_OT_SetUp
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
