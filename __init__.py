bl_info = {
    "name": "Classic Hide Collections Keymap",
    "author": "Dagobert",
    "version": (1, 0, 0),
    "blender": (5, 0, 0),
    "location": "3D View > Object Mode (global)",
    "description": "Adds classic-style hotkeys 1-0, Alt+1-0, Shift+1-0, Shift+Alt+1-0 to hide Collections in 3D View Object Mode, like Blender <5.0.",
    "category": "3D View",
}

import bpy

NUMBER_KEYS = [
    ('ONE', 1),
    ('TWO', 2),
    ('THREE', 3),
    ('FOUR', 4),
    ('FIVE', 5),
    ('SIX', 6),
    ('SEVEN', 7),
    ('EIGHT', 8),
    ('NINE', 9),
    ('ZERO', 10)
]

def register():
    kc = bpy.context.window_manager.keyconfigs.user
    if not kc:
        return

    km = kc.keymaps.get("Object Mode")
    if not km:
        km = kc.keymaps.new(name="Object Mode", space_type='VIEW_3D')

    # 1. Normal keys 1-0 → Collections 1-10, extend=False
    for key, index in NUMBER_KEYS:
        if not any(kmi.idname == "object.hide_collection" and kmi.type == key and not kmi.shift and not kmi.alt for kmi in km.keymap_items):
            kmi = km.keymap_items.new(idname="object.hide_collection", type=key, value='PRESS')
            kmi.properties.collection_index = index
            kmi.properties.extend = False

    # 2. Alt+1-0 → Collections 11-20, extend=False
    for key, index in NUMBER_KEYS:
        idx = index + 10
        if not any(kmi.idname == "object.hide_collection" and kmi.type == key and kmi.alt and not kmi.shift for kmi in km.keymap_items):
            kmi = km.keymap_items.new(idname="object.hide_collection", type=key, value='PRESS', alt=True)
            kmi.properties.collection_index = idx
            kmi.properties.extend = False

    # 3. Shift+1-0 → Collections 1-10, extend=True
    for key, index in NUMBER_KEYS:
        if not any(kmi.idname == "object.hide_collection" and kmi.type == key and kmi.shift and not kmi.alt for kmi in km.keymap_items):
            kmi = km.keymap_items.new(idname="object.hide_collection", type=key, value='PRESS', shift=True)
            kmi.properties.collection_index = index
            kmi.properties.extend = True

    # 4. Shift+Alt+1-0 → Collections 11-20, extend=True
    for key, index in NUMBER_KEYS:
        idx = index + 10
        if not any(kmi.idname == "object.hide_collection" and kmi.type == key and kmi.shift and kmi.alt for kmi in km.keymap_items):
            kmi = km.keymap_items.new(idname="object.hide_collection", type=key, value='PRESS', shift=True, alt=True)
            kmi.properties.collection_index = idx
            kmi.properties.extend = True


def unregister():
    kc = bpy.context.window_manager.keyconfigs.user
    if not kc:
        return

    km = kc.keymaps.get("Object Mode")
    if not km:
        return

    # Remove all four types
    for key, _ in NUMBER_KEYS:
        # Normal
        to_remove = [kmi for kmi in km.keymap_items
                     if kmi.idname == "object.hide_collection" and kmi.type == key and not kmi.shift and not kmi.alt]
        for kmi in to_remove:
            km.keymap_items.remove(kmi)

        # Alt
        to_remove = [kmi for kmi in km.keymap_items
                     if kmi.idname == "object.hide_collection" and kmi.type == key and kmi.alt and not kmi.shift]
        for kmi in to_remove:
            km.keymap_items.remove(kmi)

        # Shift
        to_remove = [kmi for kmi in km.keymap_items
                     if kmi.idname == "object.hide_collection" and kmi.type == key and kmi.shift and not kmi.alt]
        for kmi in to_remove:
            km.keymap_items.remove(kmi)

        # Shift+Alt
        to_remove = [kmi for kmi in km.keymap_items
                     if kmi.idname == "object.hide_collection" and kmi.type == key and kmi.shift and kmi.alt]
        for kmi in to_remove:
            km.keymap_items.remove(kmi)
