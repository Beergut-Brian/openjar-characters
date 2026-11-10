class_name JarlingHold
extends SkeletonModifier3D
## Held items on a Jarling (avatar/README.md "Holding items"): the runtime half of avatar/kit/hold.py.
##
## JarlingEquipment adds one of these under the Jarling's Skeleton3D when an item with a `hold`
## block goes into a hand slot. Every frame, after the animation: the holding arm and hand take
## the hold style's pose (with `follow` of the animation's own arm motion showing through), and
## for a two-handed item the main hand turns about its wrist and the off arm aims so the off fist
## sits on grip_l. Works on every body type: it only needs arm.L/R, hand.L/R and the hand slots.

## Animation player to read the current action from (for per-action follow). Optional.
var player: AnimationPlayer
var _holds := {}    # slot -> state


static func vec(a) -> Vector3:
	return Vector3(a[0], a[1], a[2]) if a is Array and a.size() >= 3 else Vector3.ZERO


## Item space -> slot space: turns the item's `axis` onto the fist axis (slot +Z, front) and puts
## grip_r at the slot origin.
static func item_transform(hold: Dictionary) -> Transform3D:
	var b := Basis.IDENTITY
	if hold.has("axis"):
		b = Basis(Quaternion(vec(hold["axis"]).normalized(), Vector3(0, 0, 1)))
	return Transform3D(b, -(b * vec(hold.get("grip_r", [0, 0, 0]))))


## Item space -> mouth slot space (quadruped, hold style `in_mouth`): turns the item's `axis` across
## the mouth (slot +X) and puts grip_r at the bite point. No fist, no limb pose (avatar/kit/hold.py).
static func mouth_transform(hold: Dictionary) -> Transform3D:
	var b := Basis.IDENTITY
	if hold.has("axis"):
		b = Basis(Quaternion(vec(hold["axis"]).normalized(), Vector3(1, 0, 0)))
	return Transform3D(b, -(b * vec(hold.get("grip_r", [0, 0, 0]))))


func has_hold(slot: StringName) -> bool:
	return _holds.has(slot)


func add_hold(slot: StringName, hold: Dictionary, marker: Node3D, off_marker: Node3D, holder: Node3D, piece: Node3D, body_type: String) -> bool:
	var sk := get_parent() as Skeleton3D
	if sk == null:
		return false
	var s := "L" if String(slot).ends_with("_l") else "R"
	var o := "R" if s == "L" else "L"
	var h := {"hold": hold, "holder": holder, "piece": piece, "marker": marker, "off_marker": off_marker,
			"ia": sk.find_bone("arm." + s), "ih": sk.find_bone("hand." + s), "io": sk.find_bone("arm." + o), "ioh": sk.find_bone("hand." + o),
			"local": {}, "two": hold.has("grip_l") and off_marker != null}
	if h.ia < 0 or h.ih < 0 or (h.two and (h.io < 0 or h.ioh < 0)):
		return false
	var poses: Dictionary = hold.get("poses", {})
	var st: Dictionary = poses.get(body_type, poses.get("standard", {}))
	if st.is_empty():
		return false
	var mx := Vector3(-1, 1, 1) if s == "L" else Vector3.ONE     # poses are written for a right main hand
	var ga := sk.get_bone_global_rest(h.ia)
	var gh := sk.get_bone_global_rest(h.ih)
	var gp := sk.get_bone_global_rest(sk.get_bone_parent(h.ia))
	var arm_basis := Basis(_arc(gh.origin - ga.origin, vec(st["arm"]) * mx)) * ga.basis
	h.local[h.ia] = (gp.basis.orthonormalized().inverse() * arm_basis.orthonormalized()).get_rotation_quaternion()
	var z := (vec(st["axis"]) * mx).normalized()
	var y := vec(st["up"]) * mx
	y = (y - z * y.dot(z)).normalized()
	var want := Basis(y.cross(z), y, z)                         # the slot's frame in character space
	var hand_basis := want * marker.transform.basis.orthonormalized().inverse()
	h.local[h.ih] = (arm_basis.orthonormalized().inverse() * hand_basis).get_rotation_quaternion()
	if h.two:
		var go := sk.get_bone_global_rest(h.io)
		var goh := sk.get_bone_global_rest(h.ioh)
		var off_basis := Basis(_arc(goh.origin - go.origin, vec(st["off"]) * mx)) * go.basis
		h.local[h.io] = (sk.get_bone_global_rest(sk.get_bone_parent(h.io)).basis.orthonormalized().inverse() * off_basis.orthonormalized()).get_rotation_quaternion()
		h.local[h.ioh] = sk.get_bone_rest(h.ioh).basis.get_rotation_quaternion()
	h["follow"] = float(st.get("follow", 0.2))
	_holds[slot] = h
	return true


func remove_hold(slot: StringName) -> void:
	_holds.erase(slot)


## Metres between each fist and its grip right now: {"main": d, "off": d} ("off" only for two-handed items).
func grip_error(slot: StringName) -> Dictionary:
	if not _holds.has(slot):
		return {}
	var h: Dictionary = _holds[slot]
	var out := {"main": h.marker.global_position.distance_to(_grip_global(h, "grip_r"))}
	if h.two:
		out["off"] = h.off_marker.global_position.distance_to(_grip_global(h, "grip_l"))
	return out


func _grip_global(h: Dictionary, key: String) -> Vector3:
	return h.marker.global_transform * (h.holder.transform * (h.piece.transform * vec(h.hold[key])))


func _action() -> String:
	return String(player.current_animation) if player else ""


func _process_modification() -> void:
	var sk := get_skeleton()
	if sk == null:
		return
	var act := _action()
	for slot in _holds:
		var h: Dictionary = _holds[slot]
		var f: float = float(h.hold.get("action_follow", {}).get(act, h.follow))
		for b in h.local:
			sk.set_bone_pose_rotation(b, (h.local[b] as Quaternion).slerp(sk.get_bone_pose_rotation(b), f))
		if h.two:
			_snap(sk, h, act in h.hold.get("rigid_actions", []))


func _snap(sk: Skeleton3D, h: Dictionary, rigid: bool) -> void:
	var grip: Vector3 = h.holder.transform * (h.piece.transform * vec(h.hold["grip_l"]))
	for i in 8:
		var th := sk.get_bone_global_pose(h.ih)
		var to := sk.get_bone_global_pose(h.io)
		var w := th.origin
		var c := to.origin
		var g: Vector3 = th * (h.marker.transform * grip)
		var t0: Vector3 = (sk.get_bone_global_pose(h.ioh) * h.off_marker.transform).origin
		var r := t0.distance_to(c)
		var rho := g.distance_to(w)
		var res := _circle_point(w, rho, c, r, t0)
		var p: Vector3 = res[0]
		var ok: bool = res[1]
		if rigid:
			p = g
			ok = absf(g.distance_to(c) - r) < 1e-5
		else:
			th.basis = Basis(_arc(g - w, p - w)) * th.basis
			sk.set_bone_global_pose(h.ih, th)
		if not ok:      # out of reach: stretch (or squash) the off arm along its length
			var yb := to.basis.y.normalized()
			var along := (t0 - c).dot(yb)
			var perp2 := maxf(r * r - along * along, 0.0)
			var d := p.distance_to(c)
			var k := sqrt(maxf(d * d - perp2, 1e-8)) / maxf(along, 1e-6)
			var sc := sk.get_bone_pose_scale(h.io)
			sc.y = clampf(sc.y * k, 0.5, 3.2)
			sk.set_bone_pose_scale(h.io, sc)
			sk.set_bone_pose_scale(h.ioh, Vector3(1.0, 1.0 / sc.y, 1.0))      # the fist keeps its shape
			to = sk.get_bone_global_pose(h.io)
			t0 = (sk.get_bone_global_pose(h.ioh) * h.off_marker.transform).origin
		to.basis = Basis(_arc(t0 - c, p - c)) * to.basis
		sk.set_bone_global_pose(h.io, to)


static func _arc(a: Vector3, b: Vector3) -> Quaternion:
	a = a.normalized()
	b = b.normalized()
	if a.dot(b) > 0.999999:
		return Quaternion.IDENTITY
	if a.dot(b) < -0.999999:
		var ax := a.cross(Vector3.UP)
		if ax.length() < 1e-4:
			ax = a.cross(Vector3.RIGHT)
		return Quaternion(ax.normalized(), PI)
	return Quaternion(a, b)


## The point at rho from w and r from c nearest t0: [point, reachable].
static func _circle_point(w: Vector3, rho: float, c: Vector3, r: float, t0: Vector3) -> Array:
	var n := c - w
	var d := n.length()
	if d < 1e-9:
		return [w + (t0 - w).normalized() * rho, false]
	n /= d
	if d >= rho + r or d <= absf(rho - r):
		return [w + n * (rho if (d >= rho + r or rho > r) else -rho), false]
	var a := (rho * rho - r * r + d * d) / (2.0 * d)
	var hh := sqrt(maxf(rho * rho - a * a, 0.0))
	var m := w + n * a
	var v := t0 - m
	v -= n * v.dot(n)
	if v.length() < 1e-9:
		v = n.cross(Vector3.UP) if absf(n.dot(Vector3.UP)) < 0.9 else n.cross(Vector3.RIGHT)
	return [m + v.normalized() * hh, true]
