extends SceneTree
## Real Forward+ frames of Jarlings wearing gear (needs a GPU or godot-render):
##   godot/run_tests.sh   # once, to sync + import the glbs
##   godot-render --path godot --resolution 900x900 -s res://tools/shots.gd -- ../handoff/shots [shot,shot]
## Writes one PNG per shot plus contact.png (2x2 of the first four).

const Equipment := preload("res://jarling_equipment.gd")
const Gear := preload("res://jarling_gear.gd")

const JEFF_SET := ["sunglasses", "cape", "gloves", "belt", "kneepads", "sneakers"]
const CHUCK_SET := ["hat", "sunglasses", "jetpack", "gloves", "belt", "kneepads", "rocket_boots"]
# name, character, gear, animation, frame (24 fps), run speed (m/s), camera yaw (deg, 0 = front), distance, height
var SHOTS := [
	["jeff_stand", "jeff", JEFF_SET, "idle", 1, 0.0, 30.0, 2.4, 0.9],
	["jeff_run", "jeff", JEFF_SET, "run", 3, 3.0, 125.0, 2.5, 0.95],
	["chuck_stand", "chuck", CHUCK_SET, "idle", 1, 0.0, -35.0, 2.4, 0.9],
	["chuck_kick", "chuck", CHUCK_SET, "kick", 18, 0.0, -110.0, 2.6, 0.95],
	["jeff_back", "jeff", JEFF_SET, "idle", 1, 0.0, 160.0, 2.4, 0.9],
	["chuck_back", "chuck", CHUCK_SET, "idle", 1, 0.0, 200.0, 2.4, 0.9],
	["jeff_kick", "jeff", JEFF_SET, "kick", 18, 0.0, -70.0, 2.6, 0.95],
	["chuck_run", "chuck", CHUCK_SET, "run", 3, 3.0, 70.0, 2.6, 0.95],
	["jeff_boots_lv3", "jeff", ["boots", "boots", "boots", "hat"], "idle", 1, 0.0, 25.0, 2.2, 0.85],
	["chuck_plain", "chuck", [], "idle", 1, 0.0, -35.0, 2.4, 0.9],
	["generic4_set", "generic4", CHUCK_SET, "idle", 1, 0.0, 30.0, 2.4, 0.9],
	["generic10_set", "generic10", JEFF_SET + ["hat"], "kick", 18, 0.0, -100.0, 2.5, 0.9],
	["generic11_set", "generic11", ["hat", "sunglasses", "cape", "boots", "belt", "kneepads", "gloves"], "run", 3, 3.0, 140.0, 2.5, 0.95],
]


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	var out := ProjectSettings.globalize_path("res://").path_join(args[0] if args.size() > 0 else "../handoff/shots")
	var only: Array = Array(args[1].split(",")) if args.size() > 1 else []
	DirAccess.make_dir_recursive_absolute(out)
	var world := _world()
	root.add_child(world)
	var cam := Camera3D.new()
	cam.fov = 32.0
	world.add_child(cam)
	cam.make_current()
	var imgs := []
	for sh in SHOTS:
		if not only.is_empty() and not only.has(sh[0]):
			continue
		if not ResourceLoader.exists("res://_lib/characters/%s.glb" % sh[1]):
			continue
		var j: Node3D = (load("res://_lib/characters/%s.glb" % sh[1]) as PackedScene).instantiate()
		world.add_child(j)
		_rim(j)
		var eq: JarlingEquipment = Equipment.new()
		eq.pop_in = false
		j.add_child(eq)
		for id in sh[2]:
			eq.equip(Gear.load_json("res://_lib/gear/%s.json" % id))
		var ap: AnimationPlayer = j.find_child("AnimationPlayer", true, false)
		var speed: float = sh[5]
		ap.play(sh[3])
		ap.seek((sh[4] - 1) / 24.0, true)
		ap.pause()
		# run forward (+Z) with physics ticks so the cape spring sees real motion
		for i in (60 if speed > 0.0 else 3):
			j.position.z += speed / 60.0
			_aim(cam, j.position, sh)
			await physics_frame
		await process_frame
		await process_frame
		var img := root.get_texture().get_image()
		img.save_png(out.path_join("%s.png" % sh[0]))
		print("SHOT ", sh[0])
		imgs.append(img)
		j.queue_free()
		await process_frame
	if imgs.size() >= 4 and only.is_empty():
		var w: int = imgs[0].get_width()
		var h: int = imgs[0].get_height()
		var sheet := Image.create(w * 2, h * 2, false, imgs[0].get_format())
		for k in 4:
			sheet.blit_rect(imgs[k], Rect2i(0, 0, w, h), Vector2i((k % 2) * w, (k / 2) * h))
		sheet.save_png(out.path_join("contact.png"))
		print("SHOT contact")
	quit()


func _aim(cam: Camera3D, at: Vector3, sh: Array) -> void:
	var yaw := deg_to_rad(sh[6])
	var tgt := at + Vector3(0, 0.5, 0)
	cam.look_at_from_position(tgt + Vector3(sin(yaw) * sh[7], sh[8] - 0.5, cos(yaw) * sh[7]), tgt, Vector3.UP)


func _rim(n: Node) -> void:
	if n is MeshInstance3D and n.mesh:
		for s in n.mesh.get_surface_count():
			var m := n.mesh.surface_get_material(s) as StandardMaterial3D
			if m:
				m.rim_enabled = true
				m.rim = 0.4
				m.rim_tint = 0.3
	for c in n.get_children():
		_rim(c)


func _world() -> Node3D:
	var w := Node3D.new()
	var env := Environment.new()
	var sky := Sky.new()
	var mat := ProceduralSkyMaterial.new()
	mat.sky_top_color = Color("#5FB0F0")
	mat.sky_horizon_color = Color("#EAF6FF")
	mat.ground_horizon_color = Color("#EAF6FF")
	mat.ground_bottom_color = Color("#9FD3F7")
	sky.sky_material = mat
	env.background_mode = Environment.BG_SKY
	env.sky = sky
	env.ambient_light_source = Environment.AMBIENT_SOURCE_SKY
	env.ambient_light_energy = 0.55
	env.tonemap_mode = Environment.TONE_MAPPER_FILMIC
	var we := WorldEnvironment.new()
	we.environment = env
	w.add_child(we)
	var sun := DirectionalLight3D.new()
	sun.light_color = Color("#FFF1D6")
	sun.light_energy = 1.15
	sun.shadow_enabled = true
	sun.directional_shadow_max_distance = 12.0
	sun.rotation_degrees = Vector3(-50, 35, 0)
	w.add_child(sun)
	var rim := DirectionalLight3D.new()
	rim.light_color = Color("#CFE6FF")
	rim.light_energy = 0.5
	rim.rotation_degrees = Vector3(-20, 200, 0)
	w.add_child(rim)
	var g := MeshInstance3D.new()
	var pm := PlaneMesh.new()
	pm.size = Vector2(60, 60)
	var gm := StandardMaterial3D.new()
	gm.albedo_color = Color("#8FC46E")
	gm.roughness = 0.9
	pm.material = gm
	g.mesh = pm
	w.add_child(g)
	return w
