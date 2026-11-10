extends SceneTree
## Headless tests for held items (jarling_hold.gd): godot --headless --path godot -s res://tests/test_hold.gd
## Every held gear item has grips; on every body type each fist is within 3 mm of its grip in idle,
## run and cheer; the hold styles turn the fist the right way; gear without grips equips as before.

const Equipment := preload("res://jarling_equipment.gd")
const Gear := preload("res://jarling_gear.gd")
const HELD := ["lantern", "pennant", "shovel", "crate", "parcel"]
const STYLES := ["one_hand_low", "one_hand_raised", "two_hand_diagonal", "two_hand_front", "chest_clutch"]
const TOL := 0.003

var fails := 0


func check(cond: bool, what: String) -> void:
	if not cond:
		fails += 1
	print(("  ok   " if cond else "  FAIL ") + what)


func gear(id: String) -> JarlingGear:
	return Gear.load_json("res://_lib/gear/%s.json" % id)


func _initialize() -> void:
	create_timer(240.0).timeout.connect(func(): print("RESULT: FAIL (timeout)"); quit(2))
	print("jarling_hold.gd tests (Godot %s)" % Engine.get_version_info().string)
	var styles := {}
	for id in HELD:
		var g := gear(id)
		check(g != null and g.hold.has("grip_r") and g.hold.has("style") and g.hold.has("poses"), "%s has grip_r, a hold style (%s) and poses" % [id, g.hold.get("style", "-")])
		styles[g.hold.get("style", "")] = true
		if String(g.hold.get("style", "")).begins_with("two_hand") or g.hold.get("style", "") == "chest_clutch":
			check(g.hold.has("grip_l"), "%s is two-handed and has grip_l" % id)
	for st in STYLES:
		check(styles.has(st), "a held item uses hold style %s" % st)
	for c in ["jeff", "chuck", "mole", "gnome_foreman", "caveman", "dragon"]:
		var j: Node3D = (load("res://_lib/characters/%s.glb" % c) as PackedScene).instantiate()
		root.add_child(j)
		var eq: JarlingEquipment = Equipment.new()
		eq.pop_in = false
		j.add_child(eq)
		var ap: AnimationPlayer = j.find_child("AnimationPlayer", true, false)
		var acts := ["idle", "run", "cheer"]
		if ap.has_animation("dig"):
			acts.append("dig")
		for id in HELD:
			var g := gear(id)
			check(eq.equip(g), "[%s] equip %s" % [c, id])
			check(eq.hold_style(&"hand_r") == g.hold["style"], "[%s] %s: hold_style is %s" % [c, id, g.hold["style"]])
			check(eq.is_part_hidden(&"hand_r") and eq.slot_node(&"hand_r").get_node_or_null("fist") != null, "[%s] %s: right hand is a fist" % [c, id])
			if g.hold.has("grip_l"):
				check(eq.slot_node(&"hand_l").get_node_or_null("fist") != null, "[%s] %s: left hand is a fist too" % [c, id])
			var worst := 0.0
			var n := 0
			for a in acts:
				ap.play(a)
				for t in [0.0, 0.21, 0.4]:
					ap.seek(t, true)
					await process_frame
					await process_frame
					var e := eq.grip_error(&"hand_r")
					for k in e:
						worst = maxf(worst, e[k])
						n += 1
			# 3 mm for a standard Jarling; scaled with the hand on big bodies (the Dragon's hand slot is several times bigger)
			var tol := TOL * maxf(1.0, eq.slot_node(&"hand_r").transform.basis.get_scale().x)
			check(n > 0 and worst <= tol, "[%s] %s: fists within %.1f mm of their grips over %s (%d grips, worst %.2f mm)" % [c, id, tol * 1000.0, acts, n, worst * 1000.0])
			if c == "jeff" and id in ["lantern", "pennant"]:
				ap.play("idle")
				ap.seek(0.0, true)
				await process_frame
				await process_frame
				var b := (j.global_transform.basis.inverse() * eq.slot_node(&"hand_r").global_transform.basis).orthonormalized()
				if id == "lantern":
					check(b.y.y > 0.9 and b.z.z > 0.9, "[jeff] lantern hangs upright below the fist (slot up %.2f, front %.2f)" % [b.y.y, b.z.z])
				else:
					check(b.z.y > 0.8, "[jeff] pennant stands up out of the fist (fist axis up %.2f)" % b.z.y)
					var top: Vector3 = eq.slot_node(&"hand_r").get_node("gear_pennant/pop").get_child(0).global_transform * Vector3(0, 0.4, 0)
					check(top.y > eq.slot_node(&"hand_r").global_position.y + 0.25, "[jeff] the pennant's top is above the fist")
			check(eq.unequip(&"hand_r") == g, "[%s] unequip %s" % [c, id])
			await process_frame
			check(not eq.is_part_hidden(&"hand_r") and not eq.is_part_hidden(&"hand_l"), "[%s] hands are open again after %s" % [c, id])
		# gear without grips: as before
		var plain := Gear.load_json("res://tests/hold/gear_plain_hand.json")
		check(plain.hold.is_empty() and eq.equip(plain), "[%s] hand gear without grips still equips" % c)
		var piece := eq.slot_node(&"hand_r").get_node_or_null("gear_plain_hand/pop").get_child(0) as Node3D
		check(piece != null and piece.transform.is_equal_approx(Transform3D.IDENTITY), "[%s] gripless gear sits at the slot origin, untouched" % c)
		check(not eq.is_part_hidden(&"hand_r") and eq.hold_style(&"hand_r") == "" and eq.grip_error(&"hand_r").is_empty(), "[%s] gripless gear: open hand, no hold pose" % c)
		eq.unequip(&"hand_r")
		check(eq.equip(gear("gloves")) and eq.equip(gear("hat")), "[%s] gloves and hat still equip" % c)
		j.queue_free()
		await process_frame
	print("RESULT: %s" % ("PASS" if fails == 0 else "FAIL (%d)" % fails))
	quit(0 if fails == 0 else 1)
