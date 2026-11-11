extends SceneTree
## Headless tests for jarling_equipment.gd: godot --headless --path godot -s res://tests/test_equipment.gd

const Equipment := preload("res://jarling_equipment.gd")
const Gear := preload("res://jarling_gear.gd")

var fails := 0
var checks := 0


func check(cond: bool, what: String) -> void:
	checks += 1
	if not cond:
		fails += 1
	print(("  ok   " if cond else "  FAIL ") + what)


func gear(id: String) -> JarlingGear:
	return Gear.load_json("res://_lib/gear/%s.json" % id)


func make(c: String) -> Array:
	var j: Node3D = (load("res://_lib/characters/%s.glb" % c) as PackedScene).instantiate()
	root.add_child(j)
	var eq: JarlingEquipment = Equipment.new()
	j.add_child(eq)
	return [j, eq]


func _initialize() -> void:
	create_timer(120.0).timeout.connect(func(): print("RESULT: FAIL (timeout)"); quit(2))
	print("jarling_equipment.gd tests (Godot %s)" % Engine.get_version_info().string)
	var chars := ["jeff", "chuck"]
	for f in DirAccess.get_files_at("res://_lib/characters"):
		if f.begins_with("generic") and f.ends_with(".glb"):
			chars.append(f.get_basename())
	for c in chars:
		print("[%s] slots and parts" % c)
		var r := make(c)
		var j: Node3D = r[0]
		var eq: JarlingEquipment = r[1]
		for s in Equipment.SLOTS:
			var m := eq.slot_node(s)
			check(m != j and m.get_parent() is BoneAttachment3D, "slot_%s is under a BoneAttachment3D (%s)" % [s, m.get_parent().get("bone_name") if m != j else "-"])
		check(eq.body_parts().has(&"foot_l") and eq.body_parts().has(&"foot_r"), "has foot_l/foot_r parts")
		check(eq.body_parts().has(&"hand_l") and eq.body_parts().has(&"hand_r"), "has hand_l/hand_r parts")
		if c in ["jeff", "chuck", "generic4"]:   # the others wear nothing on their heads
			check(eq.body_parts().has(&"headwear"), "has headwear part")

		print("[%s] equip / replace / unequip" % c)
		var log: Array = []
		eq.item_equipped.connect(func(s, it): log.append(["eq", s, it.id]))
		eq.item_unequipped.connect(func(s, it): log.append(["un", s, it.id]))
		eq.item_leveled_up.connect(func(s, it, l): log.append(["lv", s, it.id, l]))
		var poofs := [0]
		eq.poof.connect(func(_s, _at): poofs[0] += 1)
		var sneakers := gear("sneakers")
		check(eq.equip(sneakers), "equip sneakers returns true")
		check(eq.equipped(&"foot_l") == sneakers and eq.equipped(&"foot_r") == sneakers, "sneakers fill foot_l and foot_r")
		check(eq.has_item(&"sneakers"), "has_item(sneakers)")
		check(eq.is_part_hidden(&"foot_l") and eq.is_part_hidden(&"foot_r"), "bare feet / own shoes hidden")
		check(eq.slot_node(&"foot_l").get_node_or_null("gear_sneakers/pop/foot_l") != null, "left shoe under slot_foot_l")
		check(eq.slot_node(&"foot_r").get_node_or_null("gear_sneakers/pop/foot_r") != null, "right shoe under slot_foot_r")
		check(log.count(["eq", &"foot_l", &"sneakers"]) == 1 and log.count(["eq", &"foot_r", &"sneakers"]) == 1, "item_equipped once per slot")
		var boots := gear("boots")
		log.clear()
		check(eq.equip(boots), "equip boots into filled feet swaps")
		check(eq.equipped(&"foot_l") == boots and not eq.has_item(&"sneakers"), "boots replaced sneakers")
		check(log.has(["un", &"foot_l", &"sneakers"]) and log.has(["un", &"foot_r", &"sneakers"]), "both sneakers unequipped")
		await process_frame
		check(eq.slot_node(&"foot_l").get_child_count() == 1, "one piece in slot_foot_l after swap (no stacking)")
		check(eq.is_part_hidden(&"foot_l"), "feet still hidden while boots worn")
		check(eq.unequip(&"foot_r") == boots, "unequip(foot_r) returns boots")
		check(eq.equipped(&"foot_l") == null, "unequip one side removes the pair")
		check(not eq.is_part_hidden(&"foot_l") and not eq.is_part_hidden(&"foot_r"), "feet visible again")
		check(eq.unequip(&"foot_r") == null, "unequip empty slot returns null")

		print("[%s] level_up and duplicates" % c)
		var cape := gear("cape")
		eq.equip(cape)
		var holder: Node3D = eq.slot_node(&"back").get_node("gear_cape")
		var s0 := holder.scale
		var trim := holder.find_child("trim*", true, false) as Node3D
		check(trim != null and not trim.visible, "cape trim hidden at level 1")
		log.clear()
		check(not eq.equip(gear("cape")), "equip same id again returns false (no duplicate)")
		check(eq.level(&"back") == 2, "duplicate cape -> level 2")
		check(log.has(["lv", &"back", &"cape", 2]) and not log.any(func(e): return e[0] == "eq"), "item_leveled_up, no item_equipped")
		check(eq.slot_node(&"back").get_child_count() == 1, "still one cape on the back")
		check(holder.scale.x > s0.x * 1.05, "level 2 is bigger (%.3f -> %.3f)" % [s0.x, holder.scale.x])
		check(trim.visible, "trim shown at level 2")
		check(eq.level_up(&"back") == 3 and eq.level_up(&"back") == 3, "level caps at 3")
		check(eq.level_up(&"head") == 0, "level_up empty slot -> 0")
		check(eq.is_part_hidden(&"tail") and (not eq.body_parts().has(&"tail") or not j.find_child("*_part_tail", true, false).visible), "cape hides the tail (Jeff has one, Chuck not: no-op)")
		eq.equip(gear("jetpack"))
		check(eq.equipped(&"back").id == &"jetpack" and not eq.has_item(&"cape"), "jetpack swaps out the cape")
		check(eq.level(&"back") == 1, "swapped item starts at level 1")

		print("[%s] full set" % c)
		for id in ["hat", "sunglasses", "gloves", "belt", "kneepads", "rocket_boots"]:
			check(eq.equip(gear(id)), "equip %s" % id)
		var filled := Equipment.SLOTS.filter(func(s): return eq.equipped(s) != null)
		check(filled.size() == 10, "all 10 slots filled (%d)" % filled.size())
		check(eq.is_part_hidden(&"headwear") and eq.is_part_hidden(&"hand_l"), "hat hides headwear, gloves hide hands")
		var bare := ["hand_l", "hand_r", "foot_l", "foot_r", "headwear"].filter(func(p): return eq.body_parts().has(StringName(p)))
		check(bare.all(func(p): return not j.find_child("*_part_" + p, true, false).visible if p != "headwear" or c != "chuck" else not j.find_child("chuck_hat", true, false).visible),
				"hidden part meshes are invisible (%s)" % ", ".join(bare))
		check(poofs[0] > 0, "poof emitted (%d)" % poofs[0])
		eq.unequip_all()
		check(Equipment.SLOTS.all(func(s): return eq.equipped(s) == null), "unequip_all empties every slot")
		check(eq.body_parts().all(func(p): return not eq.is_part_hidden(p)), "every body part visible again")

		print("[%s] gear follows the bone" % c)
		eq.equip(gear("sneakers"))
		var ap: AnimationPlayer = j.find_child("AnimationPlayer", true, false)
		ap.play("kick"); ap.seek(19.0 / 24.0, true); ap.pause()
		await process_frame
		var skel: Skeleton3D = j.find_child("Skeleton3D", true, false)
		var shoe: Node3D = eq.slot_node(&"foot_r").get_node("gear_sneakers")
		var bone_pos := skel.global_transform * skel.get_bone_global_pose(skel.find_bone("foot.R")).origin
		check(shoe.global_position.distance_to(bone_pos) < 0.12 and shoe.global_position.y > 0.2,
				"right shoe follows foot.R in the kick (shoe y %.2f, bone y %.2f)" % [shoe.global_position.y, bone_pos.y])
		j.queue_free()
		await process_frame

	print("[yoji] model, actions, slots, cowboy hat gear")
	var ry := make("yoji")
	var jy: Node3D = ry[0]
	var eqy: JarlingEquipment = ry[1]
	var apy: AnimationPlayer = jy.find_child("AnimationPlayer", true, false)
	for a in ["idle", "run", "kick", "cheer"]:
		check(apy != null and apy.has_animation(a), "yoji has action %s" % a)
	check(Equipment.SLOTS.all(func(s): return eqy.slot_node(s) != jy), "yoji has all %d slots" % Equipment.SLOTS.size())
	check(eqy.body_parts().has(&"headwear"), "yoji's cowboy hat is the headwear part")
	var cowboy := gear("cowboy_hat")
	check(cowboy.slots == [&"head"] and cowboy.replaces_body_part == [&"headwear"], "cowboy_hat: slot head, replaces headwear")
	check(eqy.equip(cowboy) and eqy.equipped(&"head") == cowboy, "cowboy_hat equips on yoji")
	check(eqy.slot_node(&"head").get_node_or_null("gear_cowboy_hat") != null, "cowboy_hat sits under slot_head")
	check(eqy.is_part_hidden(&"headwear") and not jy.find_child("*_part_headwear", true, false).visible, "cowboy_hat hides yoji's own hat")
	check(eqy.equip(gear("sneakers")) and eqy.is_part_hidden(&"foot_l") and eqy.is_part_hidden(&"foot_r"), "sneakers replace yoji's high-tops")
	eqy.unequip_all()
	check(eqy.body_parts().all(func(p): return not eqy.is_part_hidden(p)), "yoji's own hat and shoes back after unequip_all")
	jy.queue_free()
	await process_frame
	var rj := make("jeff")
	check(rj[1].equip(gear("cowboy_hat")) and rj[1].is_part_hidden(&"headwear"), "cowboy_hat also fits Jeff (head slot)")
	rj[0].queue_free()
	await process_frame

	print("[bobber] model, actions, slots, rain hat gear, kid rod")
	var rb := make("bobber")
	var jb: Node3D = rb[0]
	var eqb: JarlingEquipment = rb[1]
	var apb: AnimationPlayer = jb.find_child("AnimationPlayer", true, false)
	for a in ["idle", "run", "kick", "cheer"]:
		check(apb != null and apb.has_animation(a), "bobber has action %s" % a)
	check(Equipment.SLOTS.all(func(s): return eqb.slot_node(s) != jb), "bobber has all %d slots" % Equipment.SLOTS.size())
	check(eqb.body_parts().has(&"headwear"), "bobber's rain hat is the headwear part")
	var rain := gear("rain_hat")
	check(rain.slots == [&"head"] and rain.replaces_body_part == [&"headwear"], "rain_hat: slot head, replaces headwear")
	check(eqb.equip(rain) and eqb.equipped(&"head") == rain, "rain_hat equips on bobber")
	check(eqb.slot_node(&"head").get_node_or_null("gear_rain_hat") != null, "rain_hat sits under slot_head")
	check(eqb.is_part_hidden(&"headwear") and not jb.find_child("*_part_headwear", true, false).visible, "rain_hat hides bobber's own hat")
	var kid := gear("kid_rod")
	check(kid.slots == [&"hand_r"], "kid_rod: slot hand_r")
	check(eqb.equip(kid) and eqb.equipped(&"hand_r") == kid, "kid_rod equips in bobber's hand_r")
	check(eqb.hold_style(&"hand_r") == "one_hand_raised" and eqb.is_part_hidden(&"hand_r"), "kid_rod: one_hand_raised, hand closed")
	check(eqb.equip(gear("fishing_rod")) and eqb.equipped(&"hand_r").id == &"fishing_rod", "fishing_rod also equips in bobber's hand_r")
	eqb.unequip_all()
	check(eqb.body_parts().all(func(p): return not eqb.is_part_hidden(p)), "bobber's own hat and hands back after unequip_all")
	jb.queue_free()
	await process_frame
	var rj2 := make("jeff")
	check(rj2[1].equip(gear("rain_hat")) and rj2[1].is_part_hidden(&"headwear"), "rain_hat also fits Jeff (head slot)")
	check(rj2[1].equip(gear("kid_rod")) and rj2[1].hold_style(&"hand_r") == "one_hand_raised", "kid_rod also fits Jeff (hand_r)")
	rj2[0].queue_free()
	await process_frame

	print("%d checks, %d failed" % [checks, fails])
	print("RESULT: %s" % ("PASS" if fails == 0 else "FAIL"))
	quit(1 if fails else 0)
