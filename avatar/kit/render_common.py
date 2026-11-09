"""Shared Cycles (CPU) render setup for Jarling sheets and scenes."""
import math
import bpy
from mathutils import Vector
import jarling_kit as kit

def setup_render(w, h, samples=48):
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = samples
    sc.cycles.use_adaptive_sampling = True
    sc.cycles.use_denoising = True
    sc.cycles.denoiser = "OPENIMAGEDENOISE"
    sc.cycles.max_bounces = 4; sc.cycles.diffuse_bounces = 2; sc.cycles.glossy_bounces = 2
    sc.cycles.transmission_bounces = 0; sc.cycles.transparent_max_bounces = 2
    sc.render.resolution_x, sc.render.resolution_y = w, h
    sc.render.resolution_percentage = 100
    sc.render.film_transparent = False
    sc.view_settings.view_transform = "Standard"   # keep the fixed colours honest (no filmic desaturation)
    sc.view_settings.look = "None"
    sc.view_settings.exposure = 0.0
    sc.render.image_settings.file_format = "PNG"
    return sc

def sky_world(zenith="#4FA6F0", horizon="#CDEBFF", strength=1.0, ground=None):
    w = bpy.data.worlds.new("sky"); bpy.context.scene.world = w
    w.use_nodes = True
    nt = w.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    bg = nt.nodes.new("ShaderNodeBackground"); out = nt.nodes.new("ShaderNodeOutputWorld")
    nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    nt.links.new(sep.outputs["Z"], ramp.inputs["Fac"])
    cr = ramp.color_ramp
    cr.elements[0].position = 0.0; cr.elements[0].color = (*kit.srgb_to_lin(kit.hex_rgb(ground or horizon)), 1)
    cr.elements[1].position = 0.55; cr.elements[1].color = (*kit.srgb_to_lin(kit.hex_rgb(zenith)), 1)
    e = cr.elements.new(0.5); e.color = (*kit.srgb_to_lin(kit.hex_rgb(horizon)), 1)
    nt.links.new(ramp.outputs["Color"], bg.inputs["Color"])
    bg.inputs["Strength"].default_value = strength
    nt.links.new(bg.outputs[0], out.inputs[0])
    return w

def sun(name, rot_deg, strength, color="#FFFFFF", angle=6.0):
    l = bpy.data.lights.new(name, "SUN"); l.energy = strength
    l.color = kit.srgb_to_lin(kit.hex_rgb(color)); l.angle = math.radians(angle)
    o = bpy.data.objects.new(name, l); bpy.context.scene.collection.objects.link(o)
    o.rotation_euler = [math.radians(a) for a in rot_deg]
    return o

def area(name, loc, target, power, size=3.0, color="#FFFFFF"):
    l = bpy.data.lights.new(name, "AREA"); l.energy = power; l.size = size
    l.color = kit.srgb_to_lin(kit.hex_rgb(color))
    o = bpy.data.objects.new(name, l); bpy.context.scene.collection.objects.link(o)
    o.location = loc
    o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    return o

def sunny_lights(key=3.2, rim=2.6):
    """Warm key from front-left-above, cool rim from behind so silhouettes pop."""
    sun("key", (50, 0, -35), key, "#FFF4E0", angle=9)
    sun("rim", (-62, 0, 160), rim, "#FFFFFF", angle=5)

def camera(loc, target, lens=50, ortho=None):
    c = bpy.data.cameras.new("cam")
    if ortho:
        c.type = "ORTHO"; c.ortho_scale = ortho
    else:
        c.lens = lens
    c.clip_end = 400
    o = bpy.data.objects.new("cam", c); bpy.context.scene.collection.objects.link(o)
    o.location = loc
    o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.camera = o
    return o

def ground(color="#EAF2F7", size=60, rough=0.9, name="ground"):
    me = bpy.data.meshes.new(name)
    s = size / 2
    me.from_pydata([(-s, -s, 0), (s, -s, 0), (s, s, 0), (-s, s, 0)], [], [(0, 1, 2, 3)])
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o)
    m = kit.Mats("").flat(name + "_mat", color, rough=rough, spec=0.1)
    me.materials.append(m)
    return o

def place(j, loc=(0, 0, 0), yaw_deg=0.0):
    j.rig.location = loc
    j.rig.rotation_euler = (0, 0, math.radians(yaw_deg))

def render(path):
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print("RENDERED", path)
