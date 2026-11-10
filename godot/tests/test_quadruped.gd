extends SceneTree
## Headless tests for the quadruped body (avatar/kit/body_quadruped.py), on the cow proposal:
##   godot --headless --path godot -s res://tests/test_quadruped.gd
## Shared bones and actions, the extra tail bones, the mouth slot and the in_mouth hold, and shared code
## that expects hands (hand gear, held items, the hold modifier) refusing cleanly instead of crashing.

const Equipment := preload("res://jarling_equipment.gd")
const Gear := preload("res://jarling_gear.gd")
const SHARED := ["root", "spine", "head", "arm.L", "arm.R", "hand.L", "hand.R", "leg.L", "leg.R", "foot.L", "foot.R"]

var fails := 0


func check(cond: bool, what: String) -> void:
	if not cond:
		fails += 1
	print(("  ok   " if cond else "  FAIL ") + what)


func gear(id: String) -> JarlingGear:
	return Gear.load_json("res://_lib/gear/%s.json" % id)


func extras(n: Node, key: String) -> Variant:
	var stack: Array[Node] = [n]
	while not stack.is_empty():
		var c: Node = stack.pop_back()
		stack.append_array(c.get_children())
		var ex = c.get_meta("extras") if c.has_meta("extras") else null
		if ex is Dictionary and ex.has(key):
			return ex[key]
	return null


func _initialize() -> void:
	create_timer(240.0).timeout.connect(func(): print("RESULT: FAIL (timeout)"); quit(2))
	print("quadruped body tests (Godot %s)" % Engine.get_version_info().string)
	var idx: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://_lib/characters.json"))
	var t: Dictionary = idx.body_types.get("quadruped", {})
	check(not t.is_empty() and t.playable == false, "characters.json lists body type quadruped (not playable)")
	var cow_e: Array = idx.get("proposed", []).filter(func(c): return c.id == "cow")
	check(cow_e.size() == 1 and cow_e[0].body_type == "quadruped" and cow_e[0].playable == false and cow_e[0].model_3d != null,
			"the cow is a proposal with a quadruped 3D master, not playable")
	check(not idx.roster.has("cow"), "the cow is not in the playable roster")
	var ps := load("res://_lib/characters/cow.glb") as PackedScene
	check(ps != null, "cow.glb loads")
	if ps == null:
		print("RESULT: FAIL (%d)" % fails); quit(1); return
	var j: Node3D = ps.instantiate()
	root.add_child(j)
	var sk: Skeleton3D = j.find_child("Skeleton3D", true, false)
	check(sk != null and SHARED.all(func(b): return sk.find_bone(b) >= 0), "the shared eleven bones are there")
	check(sk.find_bone("tail.1") >= 0 and sk.get_bone_parent(sk.find_bone("tail.2")) == sk.find_bone("tail.1"), "tail.1 > tail.2")
	# front legs hang from the spine, hind legs from root, hooves below them: game code that swings arm/leg still works
	check(sk.get_bone_parent(sk.find_bone("arm.L")) == sk.find_bone("spine") and sk.get_bone_parent(sk.find_bone("leg.R")) == sk.find_bone("root"),
			"arm.L/R (front legs) on spine, leg.L/R (hind legs) on root")
	var front := sk.get_bone_global_rest(sk.find_bone("hand.L")).origin
	var hind := sk.get_bone_global_rest(sk.find_bone("foot.L")).origin
	check(front.z > hind.z + 0.3 and front.y < 0.15 and hind.y < 0.15, "hand.L is a front hoof (front %.2f, hind %.2f, both near the ground)" % [front.z, hind.z])
	var ap: AnimationPlayer = j.find_child("AnimationPlayer", true, false)
	var want := ["idle", "run", "cheer", "tipped", "stiff", "graze", "sit"]
	check(want.all(func(a): return ap.has_animation(a)), "actions %s" % [want])
	check(str(extras(j, "jarling_body_type")) == "quadruped", "rig extras: jarling_body_type quadruped")
	var ex = extras(j, "jarling_expressions")
	var names: Array = ex.keys() if ex is Dictionary else []
	check(names.size() == 6 and ["neutral", "happy", "wide_eyed", "dizzy", "smug", "panicked"].all(func(n): return names.has(n)),
			"six expressions: the yard's reaction list %s" % [names])
	# a tipped cow lies low; a hopping cow leaves the ground
	var face: Node3D = j.find_child("slot_face", true, false)
	ap.play("tipped"); ap.seek(0.2, true)
	await process_frame
	await process_frame
	var head_y := face.global_position.y
	ap.play("idle"); ap.seek(0.2, true)
	await process_frame
	await process_frame
	var head_idle := face.global_position.y
	check(head_y < head_idle - 0.2, "tipped: she is on her side (face %.2f m vs %.2f m standing)" % [head_y, head_idle])

	var eq: JarlingEquipment = Equipment.new()
	eq.pop_in = false
	j.add_child(eq)
	check(eq.body_type() == "quadruped", "JarlingEquipment.body_type() is quadruped")
	for s in ["head", "face", "back", "waist", "mouth"]:
		check(eq.has_slot(StringName(s)), "has slot %s" % s)
	check(eq.missing_slots() == [&"hand_l", &"hand_r", &"knee_l", &"knee_r", &"foot_l", &"foot_r"], "hands, knees and feet are reported missing %s" % [eq.missing_slots()])
	# shared code that expects hands: refused with slot_missing, nothing changes, no crash
	var fired := []
	eq.slot_missing.connect(func(s, it): fired.append(String(s)))
	for id in ["lantern", "shovel", "gloves", "sneakers"]:
		fired.clear()
		check(not eq.equip(gear(id)) and not fired.is_empty() and eq.hold_style(&"hand_r") == "" and eq.grip_error(&"hand_r").is_empty(),
				"%s refused (slot_missing %s), no hold, no crash" % [id, fired])
	check(sk.find_child("JarlingHold", false, false) == null, "no hold modifier was added")
	# the mouth: a pail hangs from the bite point
	var pail := gear("pail")
	check(pail != null and pail.slots == [&"mouth"] and pail.hold.get("style", "") == "in_mouth", "pail.json: slot mouth, hold style in_mouth")
	check(eq.equip(pail), "equip pail in the mouth")
	check(eq.hold_style(&"mouth") == "in_mouth", "hold_style(mouth) is in_mouth")
	var piece := eq.slot_node(&"mouth").get_node("gear_pail/pop").get_child(0) as Node3D
	check(piece.transform.is_equal_approx(JarlingHold.mouth_transform(pail.hold)), "the pail's grip sits on the bite point")
	check(not eq.is_part_hidden(&"hand_r") and sk.find_child("JarlingHold", false, false) == null, "mouth carry: no fist, no limb pose")
	var bite_idle := eq.slot_node(&"mouth").global_position.y
	ap.play("graze"); ap.seek(0.3, true)
	await process_frame
	await process_frame
	var bite := eq.slot_node(&"mouth").global_position
	check(bite.y < bite_idle - 0.2, "the pail follows the head down when grazing (bite %.2f m, standing %.2f m)" % [bite.y, bite_idle])
	check(eq.unequip(&"mouth") == pail and eq.equipped(&"mouth") == null, "unequip the pail")
	# gear on the other slots: hat on the head, belt as a girth strap, back items on top of the barrel
	for id in ["hat", "sunglasses", "belt", "jetpack"]:
		var g := gear(id)
		check(eq.equip(g), "equip %s" % id)
	var back := eq.slot_node(&"back").global_transform
	check(-back.basis.z.normalized().y > 0.9, "back slot faces up: gear's back (-Z) points at the sky, on top of the barrel")
	check(eq.features() == ["horns"], "horns are a body feature %s" % [eq.features()])
	j.queue_free()
	await process_frame
	# the pail on a body without a mouth: refused, no crash
	var jeff: Node3D = (load("res://_lib/characters/jeff.glb") as PackedScene).instantiate()
	root.add_child(jeff)
	var jeq: JarlingEquipment = Equipment.new()
	jeff.add_child(jeq)
	check(not jeq.has_slot(&"mouth") and not jeq.equip(pail), "Jeff has no mouth slot: the pail is refused")
	jeff.queue_free()
	print("RESULT: %s" % ("PASS" if fails == 0 else "FAIL (%d)" % fails))
	quit(0 if fails == 0 else 1)
