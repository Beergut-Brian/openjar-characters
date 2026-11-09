"""The Spaceballs-style ball used in renders (own design)."""
import math
import bpy, bmesh

def make_ball(name, loc, r, M):
    """Six-panel ball (own design): white, sky blue and sunny yellow panels."""
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=48, v_segments=24, radius=r)
    mats = [M.flat("ball_w", "#FFFFFF", rough=0.3, spec=0.5), M.flat("ball_b", "#3E9BEA", rough=0.3, spec=0.5),
            M.flat("ball_y", "#FFD23F", rough=0.3, spec=0.5)]
    for f in bm.faces:
        c = f.calc_center_median()
        f.material_index = int(((math.atan2(c.y, c.x) + math.pi) / (2 * math.pi)) * 6) % 3 if abs(c.z) < r * 0.93 else 0
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    for m in mats: me.materials.append(m)
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o)
    o.location = loc; o.rotation_euler = (0.5, 0.3, 0.8)
    return o
