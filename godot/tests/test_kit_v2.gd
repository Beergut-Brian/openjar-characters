extends SceneTree
## Kit v2 in Godot: godot --headless --path godot -s res://tests/test_kit_v2.gd
## run_tests.sh builds tests/kit_v2/*.json (widest, skinniest, alien) into _lib/kit_v2/*.glb.
## Checks: fat / skinny bodies are standard Jarlings (bones, actions, slots), every starter gear
## item goes on and comes off the widest and the skinniest body and follows the bones in the kick,
## slot fit scales follow the body, head features are parts on their own bones, and gear with
## hides_features hides them.

const Equipment := preload("res://jarling_equipment.gd")
const Gear := preload("res://jarling_gear.gd")
const BONES := ["root", "spine", "head", "arm.L", "arm.R", "hand.L", "hand.R", "leg.L", "leg.R", "foot.L", "foot.R"]
const ANIMS := ["idle", "run", "kick", "cheer"]

var fails := 0
var checks := 0


func check(cond: bool, what: String) -> void:
	checks += 1
	if not cond:
		fails += 1
	print(("  ok   " if cond else "  FAIL ") + what)


func make(id: String) -> Array:
	var ps := load("res://_lib/kit_v2/%s.glb" % id) as PackedScene
	check(ps != null, "[%s] glb imports" % id)
	if ps == null:
		return []
	var j: Node3D = ps.instantiate()
	root.add_child(j)
	var eq: JarlingEquipment = Equipment.new()
	j.add_child(eq)
	return [j, eq]


func all_gear() -> Array:
	var out := []
	for f in DirAccess.get_files_at("res://_lib/gear"):
		if f.ends_with(".json"):
			out.append(Gear.load_json("res://_lib/gear/" + f))
	return out


func part_visible(j: Node, part: String) -> bool:
	var n := j.find_child("*_part_" + part, true, false) as Node3D
	return n != null and n.visible


func standard(id: String, j: Node3D, eq: JarlingEquipment) -> void:
	var skel: Skeleton3D = j.find_child("Skeleton3D", true, false)
	var missing := BONES.filter(func(b): return skel == null or skel.find_bone(b) < 0)
	check(missing.is_empty(), "[%s] standard skeleton bones %s" % [id, missing])
	var ap: AnimationPlayer = j.find_child("AnimationPlayer", true, false)
	var no_anim := ANIMS.filter(func(a): return ap == null or not ap.has_animation(a) or ap.get_animation(a).length <= 0.0)
	check(no_anim.is_empty(), "[%s] standard actions idle/run/kick/cheer %s" % [id, no_anim])
	var bad := Equipment.SLOTS.filter(func(s): return eq.slot_node(s) == j or not eq.slot_node(s).get_parent() is BoneAttachment3D)
	check(bad.is_empty() and eq.missing_slots().is_empty(), "[%s] all 10 equipment slots under BoneAttachment3D %s" % [id, bad])
	check(eq.body_type() == "standard", "[%s] body_type() is standard" % id)


func gear_round_trip(id: String, j: Node3D, eq: JarlingEquipment) -> void:
	for g: JarlingGear in all_gear():
		var ok := eq.equip(g)
		var hid: bool = g.replaces_body_part.all(func(p): return not eq.body_parts().has(p) or eq.is_part_hidden(p))
		check(ok and g.slots.all(func(s): return eq.equipped(s) == g) and hid, "[%s] %s goes on (%s)" % [id, g.id, ", ".join(g.slots)])
		check(eq.unequip(g.slots[0]) == g and g.slots.all(func(s): return eq.equipped(s) == null), "[%s] %s comes off" % [id, g.id])
		await process_frame
	check(eq.body_parts().all(func(p): return not eq.is_part_hidden(p)), "[%s] every body part visible again" % id)
	# the full set at once, then the kick: gear follows its bone
	for gid in ["sneakers", "kneepads", "cape", "hat", "sunglasses", "gloves", "belt"]:
		eq.equip(Gear.load_json("res://_lib/gear/%s.json" % gid))
	check(Equipment.SLOTS.all(func(s): return eq.equipped(s) != null), "[%s] full set: all 10 slots filled" % id)
	var ap: AnimationPlayer = j.find_child("AnimationPlayer", true, false)
	var skel: Skeleton3D = j.find_child("Skeleton3D", true, false)
	ap.play("kick"); ap.seek(19.0 / 24.0, true); ap.pause()
	await process_frame
	for pair in [["foot_r", "foot.R", "sneakers"], ["knee_r", "leg.R", "kneepads"], ["hand_l", "hand.L", "gloves"], ["head", "head", "hat"]]:
		var holder: Node3D = eq.slot_node(StringName(pair[0])).get_node("gear_" + pair[2])
		var bone_pos := skel.global_transform * skel.get_bone_global_pose(skel.find_bone(pair[1])).origin
		check(holder.global_position.distance_to(bone_pos) < 0.45, "[%s] %s follows %s in the kick (%.2f m from the bone)" % [id, pair[2], pair[1], holder.global_position.distance_to(bone_pos)])
	var shoe: Node3D = eq.slot_node(&"foot_r").get_node("gear_sneakers")
	check(shoe.global_position.y > 0.2, "[%s] the kicking shoe is off the ground (y %.2f)" % [id, shoe.global_position.y])
	eq.unequip_all()
	ap.stop()


func _initialize() -> void:
	create_timer(240.0).timeout.connect(func(): print("RESULT: FAIL (timeout)"); quit(2))
	print("kit v2 tests (Godot %s)" % Engine.get_version_info().string)

	print("[kit v2] widest and skinniest bodies")
	var scales := {}
	for id in ["v2_widest", "v2_skinniest", "v2_alien"]:
		var r := make(id)
		if r.is_empty():
			continue
		var j: Node3D = r[0]
		var eq: JarlingEquipment = r[1]
		standard(id, j, eq)
		await gear_round_trip(id, j, eq)
		scales[id] = {"waist": eq.slot_node(&"waist").scale, "knee": eq.slot_node(&"knee_l").scale, "foot": eq.slot_node(&"foot_l").scale,
				"back": eq.slot_node(&"back").scale, "head": eq.slot_node(&"head").scale}
		j.queue_free()
		await process_frame
	if scales.has("v2_widest") and scales.has("v2_skinniest"):
		var w: Dictionary = scales.v2_widest
		var s: Dictionary = scales.v2_skinniest
		for k in ["waist", "knee", "foot", "back"]:
			check(w[k].x > 1.15 and s[k].x < 0.9, "slot_%s fit scale follows the body: widest %.2f, skinniest %.2f" % [k, w[k].x, s[k].x])
		check(absf(w.head.x - s.head.x) < 0.25, "head slot scale does not follow the belly (%.2f / %.2f)" % [w.head.x, s.head.x])

	print("[kit v2] head features are parts, hats go on top, hides_features hides them")
	var r := make("v2_alien")
	if not r.is_empty():
		var j: Node3D = r[0]
		var eq: JarlingEquipment = r[1]
		check(eq.features() == ["antennae", "fins"], "features() == [antennae, fins] (%s)" % [eq.features()])
		check(j.find_child("v2_alien_part_feature_antennae", true, false) is MeshInstance3D, "node v2_alien_part_feature_antennae is a mesh")
		check(eq.body_parts().has(&"feature_antennae") and eq.body_parts().has(&"feature_fins"), "features are body parts")
		var skel: Skeleton3D = j.find_child("Skeleton3D", true, false)
		var ai := skel.find_bone("feat_antenna.1")
		check(ai >= 0 and skel.find_bone("feat_antenna.2") >= 0 and skel.find_bone("feat_fin.1") >= 0, "feature bones exist")
		check(ai >= 0 and skel.get_bone_name(skel.get_bone_parent(ai)) == "head", "antenna bone is a child of head")
		var ap: AnimationPlayer = j.find_child("AnimationPlayer", true, false)
		var idle := ap.get_animation("idle")
		var moves := false
		for t in idle.get_track_count():
			if String(idle.track_get_path(t)).ends_with(":feat_antenna.1") and idle.track_get_type(t) == Animation.TYPE_ROTATION_3D:
				var q0: Quaternion = idle.track_get_key_value(t, 0)
				for k in idle.track_get_key_count(t):
					if q0.angle_to(idle.track_get_key_value(t, k)) > 0.02:
						moves = true
		check(moves, "antennae bob in idle (rotation track on feat_antenna.1)")
		var hat: JarlingGear = Gear.load_json("res://_lib/gear/hat.json")
		check(hat.hides_features.is_empty(), "the starter hat hides no features")
		eq.equip(hat)
		check(part_visible(j, "feature_antennae") and part_visible(j, "feature_fins"), "a hat goes on top: antennae and fins stay visible")
		eq.unequip(&"head")
		var helmet: JarlingGear = Gear.load_json("res://_lib/kit_v2/gear_closed_helmet.json")
		check(helmet != null and helmet.hides_features == [&"antennae"], "test helmet: hides_features [antennae]")
		eq.equip(helmet)
		check(not part_visible(j, "feature_antennae") and part_visible(j, "feature_fins") and eq.is_part_hidden(&"feature_antennae"),
				"closed helmet hides the antennae only")
		eq.unequip(&"head")
		check(part_visible(j, "feature_antennae") and not eq.is_part_hidden(&"feature_antennae"), "antennae back after the helmet comes off")
		var all_hide: JarlingGear = Gear.load_json("res://_lib/kit_v2/gear_hide_all.json")
		eq.equip(all_hide)
		check(not part_visible(j, "feature_antennae") and not part_visible(j, "feature_fins"), "hides_features true hides every feature")
		eq.unequip_all()
		check(part_visible(j, "feature_antennae") and part_visible(j, "feature_fins"), "all features back")
		j.queue_free()
	r = make("v2_skinniest")
	if not r.is_empty():
		check(r[1].features() == ["horns", "pointy_ears"], "skinniest test body has horns and pointy ears (%s)" % [r[1].features()])
		r[0].queue_free()

	print("[kit v2] index")
	var idx: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://_lib/characters.json"))
	var std: Dictionary = idx.body_types.standard
	check(std.params.has("width") and std.params.has("belly"), "body_types.standard params include width and belly")
	check(std.get("width", []) == [0.75, 1.5] and std.get("belly", []) == [0.0, 1.0], "limits width 0.75..1.5, belly 0..1 (%s, %s)" % [std.get("width"), std.get("belly")])
	check(float(idx.get("player_colour_min_delta_e", 0)) == 20.0, "player_colour_min_delta_e is 20")
	check(std.get("features", []).has("antennae") and std.get("features", []).has("horns") and std.get("features", []).has("pointy_ears"), "standard body lists head features")

	print("%d checks, %d failed" % [checks, fails])
	print("RESULT: %s" % ("PASS" if fails == 0 else "FAIL"))
	quit(0 if fails == 0 else 1)
