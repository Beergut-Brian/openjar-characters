extends SceneTree
## Headless roster checks: godot --headless --path godot -s res://tests/test_roster.gd
## run_tests.sh copies characters.json to _lib/characters.json and every jarling.json to _lib/params/<id>.json.
## Rules: README "Playable characters" and docs/roster.md.

const Equipment := preload("res://jarling_equipment.gd")
const BONES := ["root", "spine", "head", "arm.L", "arm.R", "hand.L", "hand.R", "leg.L", "leg.R", "foot.L", "foot.R"]
const ANIMS := ["idle", "run", "kick", "cheer"]
const RESIDENTS := ["mole", "gnome_foreman", "caveman", "dragon"]
## Jeff and Chuck kept their approved green / red costume accents when they stopped being
## player-locked (2026-11-10; no look change without Kaden). Main colours are checked for everyone;
## any use at all of a player colour is refused for every other playable character.
const ACCENT_GRANDFATHERED := ["jeff", "chuck"]

var fails := 0
var checks := 0


func check(cond: bool, what: String) -> void:
	checks += 1
	if not cond:
		fails += 1
	print(("  ok   " if cond else "  FAIL ") + what)


func read_json(p: String) -> Variant:
	return JSON.parse_string(FileAccess.get_file_as_string(p)) if FileAccess.file_exists(p) else null


func colours_in(v: Variant, out: Array) -> Array:
	if v is String and v.begins_with("#"):
		out.append(v.to_lower())
	elif v is Dictionary:
		for k in v:
			colours_in(v[k], out)
	elif v is Array:
		for x in v:
			colours_in(x, out)
	return out


func main_colours(p: Dictionary) -> Dictionary:
	var o: Dictionary = p.get("outfit", {})
	var m := {"skin": p.get("skin", ""), "hair": p.get("hair", {}).get("color", ""),
			"headwear": p.get("headwear", {}).get("color", "")}
	for part in ["top", "bottoms", "shoes"]:
		m[part] = o.get(part, {}).get("color", "")
	for k in m:
		m[k] = str(m[k]).to_lower()
	return m


func _initialize() -> void:
	create_timer(120.0).timeout.connect(func(): print("RESULT: FAIL (timeout)"); quit(2))
	print("roster tests (Godot %s)" % Engine.get_version_info().string)
	var lib: Dictionary = read_json("res://_lib/characters.json")
	var by_id := {}
	for c in lib.characters:
		by_id[c.id] = c

	print("[roster] index")
	check(lib.has("roster") and lib.roster is Array and not lib.roster.is_empty(), "characters.json has a non-empty roster")
	check(lib.roster.slice(0, 2) == ["jeff", "chuck"], "roster starts with the defaults: jeff, chuck (%s)" % [lib.roster])
	check(lib.get("defaults", {}) == {"P1": "jeff", "P2": "chuck"}, "defaults P1 jeff, P2 chuck")
	var ids: Array = []
	for c in lib.characters:
		if c.playable:
			ids.append(c.id)
	var sorted_roster: Array = lib.roster.duplicate(); sorted_roster.sort(); ids.sort()
	check(sorted_roster == ids, "roster is exactly the playable characters, once each")
	for r in RESIDENTS:
		check(by_id.has(r) and by_id[r].playable == false and not (r in lib.roster), "%s is not playable and not in the roster" % r)
	for c in lib.characters:
		check(c.has("playable") and c.has("default_for") and c.has("body_type"), "%s has playable / default_for / body_type" % c.id)
		check(c.kind != "player_locked" and c.player == null, "%s is not player-locked" % c.id)
		if not c.playable:
			check(c.default_for == null, "%s (not playable) is nobody's default" % c.id)
	var slot_seen := {}
	for c in lib.characters:
		if c.default_for != null:
			check(not slot_seen.has(c.default_for), "default_for %d is held by one character (%s)" % [c.default_for, c.id])
			slot_seen[c.default_for] = c.id
	check(by_id.jeff.default_for == 1 and by_id.chuck.default_for == 2, "Jeff default_for 1, Chuck default_for 2")

	var pc: Array = lib.player_colours.values().map(func(x): return str(x).to_lower())
	check(pc == ["#3cc24a", "#e4393c"], "player colours are P1 #3cc24a, P2 #e4393c")
	var std: Dictionary = lib.body_types.standard
	for id in lib.roster:
		var c: Dictionary = by_id[id]
		print("[%s] playable character" % id)
		check(c.body_type == "standard", "body_type is standard")
		check(c.model_3d != null and c.jarling_params != null, "has a 3D master (.glb) and jarling.json")
		check(c.pixel != null and c.pixel.source != null and c.pixel.function != null, "has a pixel form with a sprite source")
		check(str(c.voice).ends_with("/voice/"), "has a voice folder path")
		var p: Variant = read_json("res://_lib/params/%s.json" % id)
		check(p is Dictionary, "jarling.json parses")
		if not p is Dictionary:
			continue
		# colour rule
		var main := main_colours(p)
		var bad := []
		for k in main:
			if main[k] in pc:
				bad.append(k)
		check(bad.is_empty(), "no main colour is a player colour %s" % [bad])
		if not (id in ACCENT_GRANDFATHERED):
			var any_pc := colours_in(p, []).filter(func(x): return x in pc)
			check(any_pc.is_empty(), "uses no player colour anywhere %s" % [any_pc])
		# body rule
		var body: Dictionary = p.get("body", {})
		var extra := body.keys().filter(func(k): return not (k in std.params))
		check(extra.is_empty(), "body uses only %s %s" % [std.params, extra])
		check(str(body.get("build", "regular")) in std.builds, "build %s is a kit build" % body.get("build", "regular"))
		var h := float(body.get("height", 1.0))
		check(h >= std.height[0] and h <= std.height[1], "height %.2f in %s" % [h, std.height])
		var bw := float(body.get("width", 1.0))
		check(bw >= std.width[0] and bw <= std.width[1], "width %.2f in %s" % [bw, std.width])
		var bb := float(body.get("belly", 0.0))
		check(bb >= std.belly[0] and bb <= std.belly[1], "belly %.2f in %s" % [bb, std.belly])
		var ls := float(body.get("leg_scale", 1.0))
		check(ls >= std.leg_scale[0] and ls <= std.leg_scale[1], "leg_scale %.2f in %s" % [ls, std.leg_scale])
		# the glb is a standard Jarling: same skeleton, actions and slots as every other playable
		var glb := "res://_lib/characters/%s.glb" % id
		var ps := load(glb) as PackedScene
		check(ps != null, "%s.glb loads" % id)
		if ps == null:
			continue
		var j: Node3D = ps.instantiate()
		root.add_child(j)
		var skel: Skeleton3D = j.find_child("Skeleton3D", true, false)
		var missing := BONES.filter(func(b): return skel == null or skel.find_bone(b) < 0)
		check(missing.is_empty(), "standard skeleton bones %s" % [missing])
		var ap: AnimationPlayer = j.find_child("AnimationPlayer", true, false)
		var no_anim := ANIMS.filter(func(a): return ap == null or not ap.has_animation(a))
		check(no_anim.is_empty(), "standard actions idle/run/kick/cheer %s" % [no_anim])
		var eq: JarlingEquipment = Equipment.new()
		j.add_child(eq)
		var no_slot := Equipment.SLOTS.filter(func(s): return eq.slot_node(s) == j)
		check(no_slot.is_empty(), "all %d equipment slots %s" % [Equipment.SLOTS.size(), no_slot])
		j.queue_free()
		await process_frame

	print("%d checks, %d failed" % [checks, fails])
	print("RESULT: %s" % ("PASS" if fails == 0 else "FAIL"))
	quit(0 if fails == 0 else 1)
