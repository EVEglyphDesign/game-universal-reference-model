extends SceneTree

# EgD-URM-001 — authored world for Chapter Three, "Four Lost Days".
# The Field of Twelve Gates: the 364-day circle, twelve solar gates, four
# intercalary marks at the season joints, and Uriel on the measuring dais.
#
# Nodes named C_* are collision proxies for the browser runtime.
# Exported to binary glTF 2.0 so the delivery lane never depends on this engine.

const TAU_ := 6.283185307179586

var wroot: Node3D


func mat(col: Color, rough := 0.85, emit := Color(0, 0, 0), emit_e := 0.0) -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.albedo_color = col
	m.roughness = rough
	m.metallic = 0.0
	if emit_e > 0.0:
		m.emission_enabled = true
		m.emission = emit
		m.emission_energy_multiplier = emit_e
	return m


func add_mesh(name_: String, mesh: Mesh, m: StandardMaterial3D, pos: Vector3,
		rot := Vector3.ZERO, scale := Vector3.ONE, parent: Node3D = null) -> MeshInstance3D:
	var mi := MeshInstance3D.new()
	mi.name = name_
	mi.mesh = mesh
	mi.material_override = m
	mi.position = pos
	mi.rotation = rot
	mi.scale = scale
	(parent if parent != null else wroot).add_child(mi)
	mi.owner = wroot
	return mi


func box(x: float, y: float, z: float) -> BoxMesh:
	var b := BoxMesh.new()
	b.size = Vector3(x, y, z)
	return b


func cyl(rt: float, rb: float, h: float, seg := 20) -> CylinderMesh:
	var c := CylinderMesh.new()
	c.top_radius = rt
	c.bottom_radius = rb
	c.height = h
	c.radial_segments = seg
	c.rings = 1
	return c


func sph(r: float, seg := 20) -> SphereMesh:
	var s := SphereMesh.new()
	s.radius = r
	s.height = r * 2.0
	s.radial_segments = seg
	s.rings = int(seg / 2)
	return s


func torus(inner: float, outer: float, seg := 40) -> TorusMesh:
	var t := TorusMesh.new()
	t.inner_radius = inner
	t.outer_radius = outer
	t.rings = seg
	t.ring_segments = 10
	return t


func _init() -> void:
	wroot = Node3D.new()
	wroot.name = "ChapterThree"

	# ---- palette -----------------------------------------------------------
	var STONE      := mat(Color(0.796, 0.765, 0.698), 0.92)        # pale limestone
	var STONE_DARK := mat(Color(0.643, 0.612, 0.549), 0.95)
	var GROUND     := mat(Color(0.858, 0.831, 0.769), 0.98)
	var INLAY      := mat(Color(0.741, 0.702, 0.612), 0.80)
	var INLAY_LOST := mat(Color(0.910, 0.467, 0.133), 0.55, Color(0.910, 0.467, 0.133), 0.35)
	var GATE_LIVE  := mat(Color(0.910, 0.467, 0.133), 0.45, Color(0.965, 0.596, 0.259), 1.25)
	var ROBE       := mat(Color(0.976, 0.945, 0.882), 0.88)        # cream
	var ROBE_DEEP  := mat(Color(0.420, 0.400, 0.361), 0.90)       # mute, for the mantle
	var ROBE_MID   := mat(Color(0.639, 0.612, 0.561), 0.88)       # half-tone, for sleeves
	var ROBE_TRIM  := mat(Color(0.910, 0.467, 0.133), 0.60)
	var LIGHT_CORE := mat(Color(1.0, 0.882, 0.706), 0.30, Color(1.0, 0.816, 0.549), 2.4)
	var ROD        := mat(Color(0.784, 0.667, 0.478), 0.55, Color(0.910, 0.573, 0.239), 0.30)
	var CHILD      := mat(Color(0.949, 0.906, 0.827), 0.90)
	var CHILD_DEEP := mat(Color(0.435, 0.416, 0.376), 0.90)
	var CHILD_MID  := mat(Color(0.663, 0.635, 0.584), 0.88)
	var CHILD_TRIM := mat(Color(0.910, 0.467, 0.133), 0.65)

	# ---- ground ------------------------------------------------------------
	# Wide plain, so the horizon is not a visible edge.
	add_mesh("Ground", cyl(74.0, 74.0, 1.0, 64), GROUND, Vector3(0, -0.5, 0))

	var COURT := mat(Color(0.894, 0.867, 0.800), 0.96)
	add_mesh("InnerCourt", cyl(17.4, 17.4, 0.10, 64), COURT, Vector3(0, 0.03, 0))

	# ---- the 364-day circle ------------------------------------------------
	# Four concentric inlaid rings. Flattened tori read as engraved lines.
	for spec in [[17.6, 17.9], [18.6, 18.8], [23.2, 23.4], [24.4, 24.7]]:
		var idx := [[17.6, 17.9], [18.6, 18.8], [23.2, 23.4], [24.4, 24.7]].find(spec)
		add_mesh("Ring_%d" % idx, torus(spec[0], spec[1], 96), INLAY,
			Vector3(0, 0.02, 0), Vector3.ZERO, Vector3(1, 0.10, 1))

	# 364 day-ticks would be 364 nodes. Twelve months of thirty, drawn as
	# grouped tick blocks, keeps the count honest and the node budget sane.
	for month in range(12):
		var a0: float = float(month) / 12.0 * TAU_
		for day in range(30):
			var a: float = a0 + (float(day) + 0.5) / 30.0 * (TAU_ / 12.0)
			var r := 21.0
			var long_tick := (day % 10 == 0)
			var ln := 1.30 if long_tick else 0.62
			add_mesh("Tick_%d_%d" % [month, day], box(0.095, 0.030, ln), INLAY,
				Vector3(sin(a) * r, 0.03, cos(a) * r),
				Vector3(0, a, 0))

	# The four lost days — the intercalary marks at the season joints.
	for q in range(4):
		var a: float = float(q) / 4.0 * TAU_
		add_mesh("LostDay_%d" % q, box(0.62, 0.10, 8.0), INLAY_LOST,
			Vector3(sin(a) * 21.0, 0.05, cos(a) * 21.0), Vector3(0, a, 0))
		add_mesh("LostDayCap_%d" % q, cyl(0.85, 0.85, 0.18, 24), INLAY_LOST,
			Vector3(sin(a) * 25.6, 0.06, cos(a) * 25.6))

	# ---- twelve solar gates ------------------------------------------------
	# Trilithons on the ring at thirty-degree spacing. Gate 0 is the live gate.
	var GR := 30.0
	for i in range(12):
		var a: float = float(i) / 12.0 * TAU_
		var c := Vector3(sin(a) * GR, 0.0, cos(a) * GR)
		var live := (i == 0)
		var post_m: StandardMaterial3D = STONE if not live else STONE
		var lint_m: StandardMaterial3D = GATE_LIVE if live else STONE_DARK
		var h := 8.2 if not live else 9.0
		var half := 3.1

		# Posts carry collision. Lintels deliberately do not, so the player
		# can walk through a gate rather than into it.
		for s in [-1.0, 1.0]:
			var off := Vector3(cos(a) * half * s, 0, -sin(a) * half * s)
			add_mesh("C_GatePost_%02d_%s" % [i, "L" if s < 0 else "R"],
				box(1.5, h, 1.5), post_m, c + off + Vector3(0, h * 0.5, 0),
				Vector3(0, a, 0))
			add_mesh("GatePostCap_%02d_%s" % [i, "L" if s < 0 else "R"],
				box(1.9, 0.5, 1.9), STONE_DARK, c + off + Vector3(0, h + 0.1, 0),
				Vector3(0, a, 0))

		add_mesh("GateLintel_%02d" % i, box(8.4, 1.5, 2.0), lint_m,
			c + Vector3(0, h + 1.05, 0), Vector3(0, a, 0))

		# Base plinth reads as built, not dropped on the ground.
		add_mesh("GatePlinth_%02d" % i, box(9.6, 0.5, 3.4), STONE_DARK,
			c + Vector3(0, 0.25, 0), Vector3(0, a, 0))

		# Gate number stone, set in front of each gate on the inner side.
		var inner := c - Vector3(sin(a), 0, cos(a)) * 3.6
		add_mesh("GateMark_%02d" % i, cyl(0.9, 1.15, 0.7 + 0.09 * float(i), 6),
			INLAY_LOST if live else INLAY,
			inner + Vector3(0, (0.7 + 0.09 * float(i)) * 0.5, 0), Vector3(0, a, 0))

	# ---- the sun in the live gate ------------------------------------------
	var sa := 0.0
	add_mesh("Sun", sph(1.55, 28), LIGHT_CORE,
		Vector3(sin(sa) * (GR - 0.4), 5.6, cos(sa) * (GR - 0.4)))
	add_mesh("SunHalo", torus(2.15, 2.45, 48), LIGHT_CORE,
		Vector3(sin(sa) * (GR - 0.4), 5.6, cos(sa) * (GR - 0.4)),
		Vector3(PI * 0.5, sa, 0), Vector3(1, 1, 0.10))

	# ---- the measuring dais ------------------------------------------------
	add_mesh("Dais", cyl(4.4, 5.0, 0.55, 48), STONE, Vector3(0, 0.275, 0))
	add_mesh("DaisInlay", torus(3.5, 3.8, 64), INLAY_LOST,
		Vector3(0, 0.56, 0), Vector3.ZERO, Vector3(1, 0.14, 1))
	add_mesh("DaisStep", cyl(5.6, 6.0, 0.28, 48), STONE_DARK, Vector3(0, 0.14, 0))

	# ---- Uriel -------------------------------------------------------------
	# Stylised and faceless by intention: a guide over the luminaries, carrying
	# a measure. No wings, no face, no Watcher iconography. Labelled as fiction
	# at the point of display, per URM 2.4.
	var U := Node3D.new()
	U.name = "Uriel"
	U.position = Vector3(0, 0.55, 0)
	U.rotation = Vector3(0, PI, 0)
	wroot.add_child(U)
	U.owner = wroot

	# Uriel, built to human proportion on a 6.6 m frame: skirt, torso, mantle,
	# shoulders, hanging arms, cowl. Faceless by intention \u2014 no features are
	# modelled, and the cowl keeps the face in shadow.
	add_mesh("UrielSkirt", cyl(0.58, 1.10, 4.00, 30), ROBE, Vector3(0, 2.00, 0),
		Vector3.ZERO, Vector3.ONE, U)
	add_mesh("UrielHem", torus(1.00, 1.13, 44), ROBE_TRIM, Vector3(0, 0.07, 0),
		Vector3.ZERO, Vector3(1, 0.40, 1), U)

	# Eight shallow folds break the lathe so the robe does not read as a cone.
	for f in range(8):
		var fa: float = float(f) / 8.0 * TAU_
		add_mesh("UrielFold_%d" % f, cyl(0.055, 0.135, 3.85, 6), ROBE,
			Vector3(sin(fa) * 0.86, 1.95, cos(fa) * 0.86), Vector3(0, fa, 0),
			Vector3.ONE, U)

	add_mesh("UrielTorso", cyl(0.48, 0.58, 1.40, 26), ROBE, Vector3(0, 4.60, 0),
		Vector3.ZERO, Vector3.ONE, U)
	add_mesh("UrielSash", torus(0.52, 0.60, 34), ROBE_TRIM, Vector3(0, 4.00, 0),
		Vector3.ZERO, Vector3(1, 0.34, 1), U)

	# Mantle across the shoulders, falling just past the sash.
	add_mesh("UrielMantle", cyl(0.50, 1.02, 0.98, 28), ROBE_DEEP, Vector3(0, 4.96, -0.02),
		Vector3.ZERO, Vector3(1.04, 1.0, 1.12), U)
	add_mesh("UrielMantleEdge", torus(0.97, 1.05, 36), ROBE_TRIM, Vector3(0, 4.50, -0.02),
		Vector3.ZERO, Vector3(1.04, 0.26, 1.12), U)

	add_mesh("UrielShoulders", sph(0.62, 26), ROBE_DEEP, Vector3(0, 5.18, 0),
		Vector3.ZERO, Vector3(1.42, 0.52, 0.94), U)
	add_mesh("UrielNeck", cyl(0.17, 0.20, 0.26, 14), ROBE, Vector3(0, 5.48, 0),
		Vector3.ZERO, Vector3.ONE, U)
	add_mesh("UrielHead", sph(0.315, 22), ROBE_DEEP, Vector3(0, 5.86, 0.05),
		Vector3.ZERO, Vector3(1, 1.08, 1), U)
	add_mesh("UrielCowl", sph(0.415, 24), ROBE, Vector3(0, 5.94, -0.36),
		Vector3.ZERO, Vector3(1.10, 1.12, 1.22), U)
	add_mesh("UrielCowlBrow", torus(0.295, 0.410, 30), ROBE, Vector3(0, 6.04, -0.02),
		Vector3(1.24, 0, 0), Vector3(1.05, 0.46, 1.05), U)
	add_mesh("UrielCowlDrape", cyl(0.34, 0.62, 0.66, 22), ROBE, Vector3(0, 5.44, -0.20),
		Vector3.ZERO, Vector3(1.02, 1.0, 1.20), U)

	# Arms hang from the shoulders: upper arm out, forearm down.
	for sgn in [-1.0, 1.0]:
		var sn := "L" if sgn < 0 else "R"
		add_mesh("UrielUpperArm_%s" % sn, cyl(0.150, 0.185, 1.24, 16), ROBE_MID,
			Vector3(sgn * 0.80, 4.62, 0.03), Vector3(0, 0, -sgn * 0.07), Vector3.ONE, U)
		add_mesh("UrielForearm_%s" % sn, cyl(0.118, 0.155, 1.14, 16), ROBE_MID,
			Vector3(sgn * 0.87, 3.44, 0.07), Vector3(0, 0, -sgn * 0.05), Vector3.ONE, U)
		add_mesh("UrielCuff_%s" % sn, torus(0.11, 0.155, 18), ROBE_TRIM,
			Vector3(sgn * 0.90, 2.90, 0.08), Vector3.ZERO, Vector3(1, 0.44, 1), U)
		add_mesh("UrielHand_%s" % sn, sph(0.125, 14), ROBE,
			Vector3(sgn * 0.91, 2.76, 0.09), Vector3.ZERO, Vector3.ONE, U)

	# The measure, planted in the ground and held in the right hand.
	add_mesh("UrielRod", cyl(0.058, 0.058, 6.05, 12), ROD,
		Vector3(1.16, 2.95, 0.34), Vector3(0.022, 0, -0.030), Vector3.ONE, U)
	add_mesh("UrielRodRing", torus(0.24, 0.32, 24), ROD,
		Vector3(1.02, 5.42, 0.42), Vector3(0, 0, 0.06), Vector3(1, 0.28, 1), U)
	add_mesh("UrielRodTip", sph(0.175, 16), LIGHT_CORE,
		Vector3(1.00, 5.80, 0.43), Vector3.ZERO, Vector3.ONE, U)

	for sg3 in [-1.0, 1.0]:
		var tn := "L" if sg3 < 0 else "R"
		add_mesh("UrielStole_%s" % tn, box(0.155, 2.00, 0.055), ROBE_TRIM,
			Vector3(sg3 * 0.25, 4.15, 0.72), Vector3(0.075, sg3 * 0.02, 0),
			Vector3.ONE, U)
	add_mesh("UrielCollar", torus(0.28, 0.40, 28), ROBE_TRIM, Vector3(0, 5.30, 0.12),
		Vector3(0.22, 0, 0), Vector3(1.24, 0.26, 1.0), U)

	add_mesh("UrielHeartLight", sph(0.14, 14), LIGHT_CORE, Vector3(0, 4.30, 0.50),
		Vector3.ZERO, Vector3(1, 1, 0.5), U)
	add_mesh("UrielHalo", torus(0.66, 0.76, 48), LIGHT_CORE, Vector3(0, 6.44, -0.06),
		Vector3.ZERO, Vector3(1, 0.14, 1), U)

	# Collision proxy: a plain column, so the player cannot walk through him.
	add_mesh("CX_Uriel", cyl(1.15, 1.15, 6.0, 12), ROBE, Vector3(0, 2.6, 0),
		Vector3.ZERO, Vector3.ONE, U)

	# ---- the player avatar -------------------------------------------------
	# A child of the cohort, not a capsule. The runtime clones this node and
	# hides the original.
	var P := Node3D.new()
	P.name = "PlayerAvatar"
	P.position = Vector3(0, -40.0, 0)   # parked; the runtime repositions it
	wroot.add_child(P)
	P.owner = wroot

	# The child of the cohort, 1.55 m, same construction at a smaller scale.
	add_mesh("AvatarSkirt", cyl(0.215, 0.335, 0.82, 22), CHILD, Vector3(0, 0.41, 0),
		Vector3.ZERO, Vector3.ONE, P)
	add_mesh("AvatarHem", torus(0.305, 0.345, 24), CHILD_TRIM, Vector3(0, 0.045, 0),
		Vector3.ZERO, Vector3(1, 0.38, 1), P)
	add_mesh("AvatarTorso", cyl(0.195, 0.220, 0.36, 20), CHILD, Vector3(0, 0.99, 0),
		Vector3.ZERO, Vector3.ONE, P)
	add_mesh("AvatarSash", torus(0.205, 0.245, 24), CHILD_TRIM, Vector3(0, 0.82, 0),
		Vector3.ZERO, Vector3(1, 0.36, 1), P)
	# A small hooded cape in the same construction as Uriel's, so the two
	# figures read as the same world.
	add_mesh("AvatarCape", cyl(0.135, 0.290, 0.30, 22), CHILD_DEEP, Vector3(0, 1.13, -0.01),
		Vector3.ZERO, Vector3(1.04, 1.0, 1.14), P)
	add_mesh("AvatarCapeEdge", torus(0.275, 0.305, 24), CHILD_TRIM, Vector3(0, 0.99, -0.01),
		Vector3.ZERO, Vector3(1.04, 0.26, 1.14), P)
	add_mesh("AvatarHead", sph(0.140, 18), CHILD_DEEP, Vector3(0, 1.37, 0.02),
		Vector3.ZERO, Vector3(1, 1.08, 1), P)
	add_mesh("AvatarHood", sph(0.168, 18), CHILD, Vector3(0, 1.395, -0.055),
		Vector3.ZERO, Vector3(1.08, 1.10, 1.14), P)
	add_mesh("AvatarHoodBrow", torus(0.120, 0.168, 22), CHILD, Vector3(0, 1.455, 0.02),
		Vector3(1.24, 0, 0), Vector3(1.05, 0.46, 1.05), P)
	add_mesh("AvatarPack", box(0.24, 0.26, 0.13), CHILD_DEEP,
		Vector3(0, 0.86, -0.26), Vector3.ZERO, Vector3.ONE, P)
	for sgn2 in [-1.0, 1.0]:
		var an := "L" if sgn2 < 0 else "R"
		add_mesh("AvatarArm_%s" % an, cyl(0.052, 0.066, 0.60, 12), CHILD_MID,
			Vector3(sgn2 * 0.235, 0.86, 0.02), Vector3(0, 0, -sgn2 * 0.10), Vector3.ONE, P)
		add_mesh("AvatarHand_%s" % an, sph(0.058, 12), CHILD_MID,
			Vector3(sgn2 * 0.268, 0.54, 0.03), Vector3.ZERO, Vector3.ONE, P)

	# ---- scattered field stones, for depth cues ----------------------------
	var rng := RandomNumberGenerator.new()
	rng.seed = 3641982
	for i in range(22):
		var a := rng.randf() * TAU_
		var r := rng.randf_range(34.0, 62.0)
		var hh := rng.randf_range(0.9, 3.4)
		add_mesh("C_FieldStone_%02d" % i,
			box(rng.randf_range(0.8, 2.2), hh, rng.randf_range(0.8, 2.2)),
			STONE_DARK if (i % 3 == 0) else STONE,
			Vector3(sin(a) * r, hh * 0.5, cos(a) * r),
			Vector3(0, rng.randf() * TAU_, 0))

	# ---- export ------------------------------------------------------------
	var doc := GLTFDocument.new()
	var state := GLTFState.new()
	var err := doc.append_from_scene(wroot, state)
	if err != OK:
		printerr("append_from_scene failed: %d" % err)
		quit(1)
		return
	var out := "/home/user/workspace/urm/docs/play/world.glb"
	err = doc.write_to_filesystem(state, out)
	if err != OK:
		printerr("write_to_filesystem failed: %d" % err)
		quit(1)
		return
	print("wrote %s  nodes=%d" % [out, wroot.get_child_count()])
	quit(0)
