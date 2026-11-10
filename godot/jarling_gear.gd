class_name JarlingGear
extends Resource
## One wearable item for a Jarling (docs/equipment.md). Load the JSON next to a gear .glb with
## JarlingGear.load_json(), or make a .tres with the same fields.

@export var id: StringName
@export var display_name: String
## Slots it fills. Paired items list both sides (foot_l, foot_r) and fill them together.
@export var slots: Array[StringName] = []
## The piece, authored in slot space (see docs/equipment.md section 3).
@export var scene: PackedScene
## Body parts hidden while worn (foot_l, foot_r, hand_l, hand_r, headwear, tail).
@export var replaces_body_part: Array[StringName] = []
## Head features hidden while worn (kit v2: antennae, horns, pointy_ears, fins ...). ["*"] hides
## every feature. Features are body parts of the species, so most hats leave this empty and the
## antennae simply poke out; a closed helmet that cannot fit them lists them here.
## JSON: "hides_features": true | ["antennae", ...]
@export var hides_features: Array[StringName] = []
## Optional per-build (or per-character id) tweak: {"puffy": {"offset": [x, y, z], "scale": 1.0 or [x, y, z]}}
@export var fit: Dictionary = {}
## {"max": 3, "scale_step": 0.06}
@export var level_up: Dictionary = {}
## Optional swinging node: {"node": "cape_pivot", "stiffness", "damping", "gain", "rest_deg", "max_deg"}
@export var spring: Dictionary = {}
## Held items only (avatar/README.md "Holding items"): {"style", "grip_r", "grip_l", "axis", "poses", ...}.
## Empty for gear without grips: it sits at the slot origin as before.
@export var hold: Dictionary = {}


static func load_json(path: String) -> JarlingGear:
	var text := FileAccess.get_file_as_string(path)
	var d = JSON.parse_string(text)
	if typeof(d) != TYPE_DICTIONARY:
		push_error("JarlingGear: cannot read %s" % path)
		return null
	var g := JarlingGear.new()
	g.id = StringName(d.get("id", path.get_file().get_basename()))
	g.display_name = d.get("name", String(g.id))
	var s: Array = d.get("slots", [d["slot"]] if d.has("slot") else [])
	for x in s:
		g.slots.append(StringName(x))
	for x in d.get("replaces_body_part", []):
		g.replaces_body_part.append(StringName(x))
	var hf = d.get("hides_features", [])
	if hf is bool:
		hf = ["*"] if hf else []
	for x in hf:
		g.hides_features.append(StringName(x))
	g.fit = d.get("fit", {})
	g.level_up = d.get("level_up", {})
	g.spring = d.get("spring", {})
	g.hold = d.get("hold", {})
	if d.has("scene"):
		g.scene = load(path.get_base_dir().path_join(d["scene"])) as PackedScene
		if g.scene == null:
			push_error("JarlingGear: %s: cannot load scene %s" % [path, d["scene"]])
	return g


## Body parts this item hides on a Jarling that has `parts`: replaces_body_part plus the
## `feature_<type>` parts named by hides_features.
func hidden_parts(parts: Array) -> Array[StringName]:
	var out: Array[StringName] = replaces_body_part.duplicate()
	for p in parts:
		var n := String(p)
		if n.begins_with("feature_") and (hides_features.has(&"*") or hides_features.has(StringName(n.substr(8)))):
			if not out.has(StringName(n)):
				out.append(StringName(n))
	return out


func max_level() -> int:
	return int(level_up.get("max", 3))


func scale_step() -> float:
	return float(level_up.get("scale_step", 0.06))
