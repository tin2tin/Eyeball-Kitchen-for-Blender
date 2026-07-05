bl_info = {
    "name": "Procedural Eyeball Generator",
    "blender": (4, 2, 0),
    "category": "Add Mesh",
    "version": (0, 0, 1),
    "author": "Preston Chavez",
    "description": "Ready-to-Go Eyeball customizer ready for finalization",
    "location": "Add > Mesh > Prefab Meshes",
}

import bpy
from bpy.types import Operator, Menu
from bpy.props import StringProperty
from pathlib import Path
import bpy.utils.previews
from . mesh_library import create_prefab_instance

# Global icon collection
custom_icons = None

PREFABS = {
    "human_eye": {
        "blend_file": "human_eye",
        "collection": "Human_Eye",
        "description": "Realistic human eye with detailed iris and sclera",
        "icon": "human_eye_thumb_small"
    },
    "human_eye_stylized": {
        "blend_file": "human_eye_stylized",
        "collection": "Human_Eye_Stylized",
        "description": "Realistic human eye with detailed iris and sclera",
        "icon": "stylized_eye_thumb_small"
    },
    "aquatic_vertabrate_eye": {
        "blend_file": "aquatic_vertabrate_eye",
        "collection": "Aquatic_Vertabrate_Eye",
        "description": "Eye designed for aquatic creatures like fish and dolphins",
        "icon": "aquatic_vertabrate_eye_thumb_small"
    },
    "reptile_eye": {
        "blend_file": "reptile_eye",
        "collection": "Reptile_Eye",
        "description": "Reptilian eye with slit pupils and scaled texture",
        "icon": "reptile_eye_thumb_small"
    },
}

def load_custom_icons():
    """Load custom icons from the icons directory"""
    global custom_icons
    
    if custom_icons is not None:
        return custom_icons
    
    custom_icons = bpy.utils.previews.new()
    
    # Get the addon directory
    addon_dir = Path(__file__).parent
    icons_dir = addon_dir / "icons"
    
    # Load each icon
    for prefab_id, prefab_info in PREFABS.items():
        icon_name = prefab_info. get("icon", "")
        if icon_name:
            icon_path = icons_dir / f"{icon_name}.png"
            if icon_path.exists():
                custom_icons.load(icon_name, str(icon_path), 'IMAGE')
            else:
                print(f"Warning: Icon not found at {icon_path}")
    
    return custom_icons


class MESH_OT_add_prefab(Operator):
    """Add a prefabricated eyeball mesh"""
    bl_idname = "mesh.add_prefab"
    bl_label = "Add Prefab Eyeball"
    bl_options = {'REGISTER', 'UNDO'}
    
    prefab_type: StringProperty(
        name="Prefab Type",
        description="Type of prefab eyeball to add",
        default="human_eye"
    )
    
    def execute(self, context):
        try:
            if self.prefab_type not in PREFABS:
                raise ValueError(f"Unknown prefab type: {self.prefab_type}")
            
            prefab_info = PREFABS[self.prefab_type]
            create_prefab_instance(
                prefab_info["blend_file"],
                prefab_info["collection"],
                context
            )
        except Exception as e:
            self.report({'ERROR'}, f"Failed to load prefab: {str(e)}")
            return {'CANCELLED'}
        
        return {'FINISHED'}


class MESH_MT_add_prefab(Menu):
    """Menu for prefab eyeballs"""
    bl_idname = "MESH_MT_add_prefab"
    bl_label = "Prefab Eyeballs"
    
    def draw(self, context):
        layout = self.layout
        icons = load_custom_icons()

        # Dynamically create menu items from PREFABS dictionary
        #for prefab_id, prefab_info in PREFABS.items():
            # Format the display name (e.g., "human_eye" becomes "Human Eye")
            #display_name = prefab_id.replace("_", " ").title()
            #layout.operator("mesh.add_prefab", text=display_name).prefab_type = prefab_id
        # Dynamically create menu items from PREFABS dictionary

        for prefab_id, prefab_info in PREFABS.items():
            # Format the display name (e.g., "human_eye" becomes "Human Eye")
            display_name = prefab_id.replace("_", " ").title()
            # Get the description if it exists
            description = prefab_info.get("description", "")
            # Get the icon name
            icon_name = prefab_info.get("icon", "")
            
            # Determine which icon to use
            if icon_name and icon_name in icons:
                icon_id = icons[icon_name]. icon_id
            else:
                icon_id = 'NONE'
            
            # Create operator with custom icon and description
            op = layout.operator("mesh.add_prefab", text=display_name, icon_value=icon_id if icon_id != 'NONE' else 0)
            op.prefab_type = prefab_id


def menu_func_add(self, context):
    icons = load_custom_icons()
    # Use a custom icon for the main menu button, or 'PLUGIN' as fallback
    self.layout.menu("MESH_MT_add_prefab", icon='PLUGIN')


def register():
    bpy.utils.register_class(MESH_OT_add_prefab)
    bpy.utils.register_class(MESH_MT_add_prefab)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func_add)

    load_custom_icons()


def unregister():
    global custom_icons

    # Clean up custom icons
    if custom_icons is not None:
        bpy.utils.previews.remove(custom_icons)
        custom_icons = None

    bpy.utils.unregister_class(MESH_OT_add_prefab)
    bpy.utils.unregister_class(MESH_MT_add_prefab)
    bpy.types.VIEW3D_MT_mesh_add. remove(menu_func_add)


if __name__ == "__main__":
    register()
