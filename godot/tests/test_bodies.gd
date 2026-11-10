extends SceneTree
## Body-type contract for every character with a 3D model:
##   godot --headless --path godot -s res://tests/test_bodies.gd
## Reads res://_lib/characters.json (body_types), _lib/params/<id>.json and _lib/gear/*.json.

const Equipment := preload("res://jarling_equipment.gd")
const Gear := preload("res://jarling_gear.gd")

var fails := 0
var checks := 0


func check(cond: bool, what: String) -> void:
	checks += 1
	if not cond:
		fails += 1
	print(("  ok   " if cond else "  FAIL ") + what)


func read_json(p: String) -> Variant:
	return JSON.parse_string(FileAccess.get_file_as_string(p)) if FileAccess.file_exists(p) else null


func names_of(v: Variant) -> Array:
	if v is Array:
		return v.map(func(x): return str(x))
	if v is Dictionary:
		return v.keys()
	if v is String:
		var s: String = v.strip_edges()
		if s.begins_with("["):
			return names_of(JSON.parse_string(s))
		return Array(s.split(",", false)).map(func(x): return x.strip_edges())
	return []


func find_extras(n: Node, key: String) -> Variant:
	var stack: Array[Node] = [n]
	while not stack.is_empty():
		var c: Node = stack.pop_back()
		stack.append_array(c.get_children())
		var ex = c.get_meta("extras", null)
		if ex is Dictionary and ex.has(key):
			return ex[key]
	return null


func gear_nodes(n: Node) -> Array:
	var out := []
	for c in n.get_children():
		if String(c.name).begins_with("gear_"):
			out.append(c)
		out.append_array(gear_nodes(c))
	return out


func has_skinned_mesh(n: Node) -> bool:
	if n is MeshInstance3D and n.skin != null and n.skeleton != NodePath():
		return true
	for c in n.get_children():
		if has_skinned_mesh(c):
			return true
	return false


func load_gear() -> Array:
	var out := []
	for f in DirAccess.get_files_at("res://_lib/gear"):
		if f.ends_with(".json"):
			var g: JarlingGear = Gear.load_json("res://_lib/gear/" + f)
			if g:
				out.append(g)
	return out


func test_gear(j: Node3D, eq: JarlingEquipment, id: String, gears: Array) -> void:
	for g: JarlingGear in gears:
		var lacks: Array = g.slots.filter(func(s): return not eq.has_slot(s))
		var fired: Array = []
		var cb := func(s, it): fired.append([s, it.id])
		eq.slot_missing.connect(cb)
		if lacks.is_empty():
			var ok := eq.equip(g)
			var all_in := g.slots.all(func(s): return eq.equipped(s) == g)
			check(ok and all_in, "[%s] equip %s on %s" % [id, g.id, g.slots])
			var hid := true
			for p in g.replaces_body_part:
				if eq.body_parts().has(p):
					hid = hid and eq.is_part_hidden(p)
					for n in eq._parts[p]:
						hid = hid and not n.visible
			check(hid and fired.is_empty(), "[%s] %s hides %s, no slot_missing" % [id, g.id, g.replaces_body_part])
			check(eq.unequip(g.slots[0]) == g and g.slots.all(func(s): return eq.equipped(s) == null), "[%s] unequip %s" % [id, g.id])
			await process_frame
			var back := true
			for p in g.replaces_body_part:
				if eq.body_parts().has(p):
					back = back and not eq.is_part_hidden(p)
					for n in eq._parts[p]:
						back = back and n.visible
			check(back and gear_nodes(j).is_empty(), "[%s] %s parts visible again, no gear left" % [id, g.id])
		else:
			var ok := eq.equip(g)
			check(not ok, "[%s] equip %s refused (lacks %s)" % [id, g.id, lacks])
			var once := lacks.all(func(s): return fired.count([s, g.id]) == 1) and fired.size() == lacks.size()
			check(once, "[%s] slot_missing once per missing slot %s" % [id, lacks])
			check(gear_nodes(j).is_empty(), "[%s] no gear_* node after refusal" % id)
			check(g.slots.all(func(s): return eq.equipped(s) == null), "[%s] nothing worn after refusal" % id)
			check(g.replaces_body_part.all(func(p): return not eq.is_part_hidden(p)), "[%s] nothing hidden after refusal" % id)
			for s in lacks:
				check(eq.unequip(s) == null and eq.level_up(s) == 0 and eq.level(s) == 0 and eq.equipped(s) == null,
						"[%s] unequip/level_up/level/equipped on missing %s are no-ops" % [id, s])
		eq.slot_missing.disconnect(cb)


func _initialize() -> void:
	create_timer(240.0).timeout.connect(func(): print("RESULT: FAIL (timeout)"); quit(2))
	print("body-type tests (Godot %s)" % Engine.get_version_info().string)
	var idx: Dictionary = read_json("res://_lib/characters.json")
	var types: Dictionary = idx.body_types
	var gears := load_gear()
	check(gears.size() > 0, "gear items found (%d)" % gears.size())
	for c: Dictionary in idx.characters:
		if c.model_3d == null:
			continue
		var id: String = c.id
		var bt: String = c.body_type
		print("[%s]" % id)
		check(types.has(bt), "[%s] body type '%s' is in body_types" % [id, bt])
		if not types.has(bt):
			continue
		var t: Dictionary = types[bt]
		if bt != "standard":
			check(c.playable == false, "[%s] non-standard body is not playable" % id)
		var params = read_json("res://_lib/params/%s.json" % id)
		var ps := load("res://_lib/characters/%s.glb" % id) as PackedScene
		check(ps != null, "[%s] glb loads" % id)
		if ps == null:
			continue
		var j: Node3D = ps.instantiate()
		check(j != null, "[%s] glb instantiates" % id)
		root.add_child(j)
		var skel: Skeleton3D = j.find_child("Skeleton3D", true, false)
		check(skel != null, "[%s] has a Skeleton3D" % id)
		var nbones: int = skel.get_bone_count() if skel else 0
		var nobone: Array = t.bones.filter(func(b): return skel == null or skel.find_bone(b) < 0)
		check(nobone.is_empty(), "[%s] bones %s missing %s" % [id, t.bones.size(), nobone])
		var ap: AnimationPlayer = j.find_child("AnimationPlayer", true, false)
		check(ap != null, "[%s] has an AnimationPlayer" % id)
		var want: Array = t.actions.duplicate()
		if params is Dictionary:
			for a in params.get("actions", []):
				if not want.has(a):
					want.append(a)
		var noact: Array = want.filter(func(a): return ap == null or not ap.has_animation(a))
		check(noact.is_empty(), "[%s] actions %s missing %s" % [id, want, noact])
		var badlen: Array = []
		if ap:
			for a in ap.get_animation_list():
				if ap.get_animation(a).length <= 0.0:
					badlen.append(a)
		check(badlen.is_empty(), "[%s] every animation has length > 0 %s" % [id, badlen])
		check(has_skinned_mesh(j), "[%s] has a skinned body mesh" % id)
		var expr = find_extras(j, "jarling_expressions")
		var en := names_of(expr)
		check(en.size() >= 4, "[%s] jarling_expressions has >= 4 entries %s" % [id, en])
		if params is Dictionary and params.get("face", {}).has("expression_list"):
			var el: Array = params.face.expression_list
			check(en == el.map(func(x): return str(x)), "[%s] expressions are exactly face.expression_list %s" % [id, el])
		var eq: JarlingEquipment = Equipment.new()
		j.add_child(eq)
		var bad: Array = []
		for s in t.slots:
			var m := eq.slot_node(StringName(s))
			if m == j or not m.get_parent() is BoneAttachment3D or String(m.name) != "slot_" + s:
				bad.append(s)
		check(bad.is_empty(), "[%s] slots under a BoneAttachment3D, missing/bad %s" % [id, bad])
		var expect_missing: Array = Equipment.SLOTS.filter(func(s): return not (String(s) in t.slots)).map(func(s): return String(s))
		var got_missing: Array = eq.missing_slots().map(func(s): return String(s))
		check(got_missing == expect_missing, "[%s] missing_slots() %s == %s" % [id, got_missing, expect_missing])
		check(eq.body_type() == bt, "[%s] body_type() '%s' == index '%s'" % [id, eq.body_type(), bt])
		await test_gear(j, eq, id, gears)
		print("[%s] body %s: %d bones, %d actions, %d slots" % [id, bt, nbones, ap.get_animation_list().size() if ap else 0, t.slots.size()])
		j.queue_free()
		await process_frame

	# Self-test of the missing-slot path on a standard body: Jeff without slot_knee_l.
	print("[self-test] Jeff without slot_knee_l")
	var jeff: Node3D = (load("res://_lib/characters/jeff.glb") as PackedScene).instantiate()
	root.add_child(jeff)
	var knee: Node = jeff.find_child("slot_knee_l", true, false)
	check(knee != null, "Jeff has slot_knee_l before removal")
	if knee:
		knee.get_parent().remove_child(knee)
		knee.free()
	var jeq: JarlingEquipment = Equipment.new()
	jeff.add_child(jeq)
	check(not jeq.has_slot(&"knee_l") and jeq.has_slot(&"knee_r"), "has_slot reflects the removed marker")
	check(jeq.missing_slots() == [&"knee_l"], "missing_slots() == [knee_l]")
	check(jeq.body_type() == "standard", "body_type() defaults to / reads standard")
	var fired: Array = []
	jeq.slot_missing.connect(func(s, it): fired.append([s, it.id]))
	var pads: JarlingGear = Gear.load_json("res://_lib/gear/kneepads.json")
	check(not jeq.equip(pads), "kneepads refused")
	check(fired == [[&"knee_l", &"kneepads"]], "slot_missing fired once for knee_l")
	check(gear_nodes(jeff).is_empty() and jeq.equipped(&"knee_r") == null, "no gear node, knee_r stays empty")
	check(jeq.unequip(&"knee_l") == null and jeq.level_up(&"knee_l") == 0 and jeq.level(&"knee_l") == 0, "other calls on the missing slot are no-ops")
	var sn: JarlingGear = Gear.load_json("res://_lib/gear/sneakers.json")
	check(jeq.equip(sn) and jeq.equipped(&"foot_l") == sn, "other gear still works")

	print("%d checks, %d failed" % [checks, fails])
	print("RESULT: %s" % ("PASS" if fails == 0 else "FAIL"))
	quit(0 if fails == 0 else 1)
