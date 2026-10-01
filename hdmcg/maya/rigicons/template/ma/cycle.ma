//Maya ASCII 2026 scene
//Name: cycle.ma
//Last modified: Fri, Jun 19, 2026 12:17:34 PM
//Codeset: 1252
requires maya "2026";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2026";
fileInfo "version" "2026";
fileInfo "cutIdentifier" "202507081222-4d6919b75c";
fileInfo "osv" "Windows 11 Pro v2009 (Build: 26200)";
fileInfo "UUID" "0B3F9B2E-4708-E6C0-1831-9790587BD84A";
fileInfo "license" "education";
createNode transform -n "cycle_ctrl";
	rename -uid "87FA964C-4825-4CA3-3A93-B9AF52FE11CD";
createNode nurbsCurve -n "cycle_ctrlShape" -p "cycle_ctrl";
	rename -uid "83D041F7-412B-DFBD-22CE-609B74F385B1";
	setAttr -k off ".v";
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 1 0 0.018911498 ;
	setAttr ".cc" -type "nurbsCurve" 
		3 31 0 no 3
		36 0 0 0 1 2 3 4 5 6 7 8 8 8 9 9 9 10 11 12 13 14 15 16 17 17 17 18 19 20 21
		 22 23 24 25 25 25
		34
		0.30032133593499999 -6.2301024082499997e-33 1.017452936235e-16
		0.30032133593499999 -3.5587697985449998e-18 0.058119121383000003
		0.26457065616249997 -1.0847641498899999e-17 0.17715542973599999
		0.121769088064 -1.7994646640699999e-17 0.29387488136500001
		-0.062079010529999999 -1.9111192404500001e-17 0.31210945748300001
		-0.2249917627585 -1.3776772104849999e-17 0.2249917627585
		-0.31210945748300001 -3.8012430769949999e-18 0.062079010529999999
		-0.29387488136500001 7.4562061966500003e-18 -0.121769088064
		-0.17715542973599999 1.6200280360899999e-17 -0.26457065616249997
		-0.058119121383000003 1.8389378138400001e-17 -0.30032133593499999
		0 0 -0.29999999999999999
		0 0 -0.34999999999999998
		0 0 -0.45000000000000001
		3.0616169978700002e-17 3.0616169978700002e-17 -0.5
		-0.096761559085000004 3.0616169978700002e-17 -0.5
		-0.29494313013899998 2.697157747795e-17 -0.44047928752549997
		-0.48926740494549997 1.2413713753350001e-17 -0.20273133056750001
		-0.51962584761499997 -6.3286264114000001e-18 0.103354312701
		-0.37458504581149998 -2.2936718868050001e-17 0.37458504581149998
		-0.103354312701 -3.1817906551700001e-17 0.51962584761499997
		0.20273133056750001 -2.9958988069700001e-17 0.48926740494549997
		0.44047928752549997 -1.8060058012749999e-17 0.29494313013899998
		0.5 -5.9249366807000002e-18 0.096761559085000004
		0.5 -1.037239393735e-32 1.6939404805700001e-16
		0.59999999999999998 0 0
		0.59999999999999998 0 0
		0.59999999999999998 0 0
		0.40000000000000002 0 -0.20000000000000001
		0.40000000000000002 0 -0.20000000000000001
		0.40000000000000002 0 -0.20000000000000001
		0.20000000000000001 0 0
		0.20000000000000001 0 0
		0.20000000000000001 0 0
		0.29999999999999999 0 0
		;
select -ne :time1;
	setAttr ".o" 0;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr ".fprt" yes;
	setAttr ".rtfm" 1;
select -ne :renderPartition;
	setAttr -s 2 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 6 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
select -ne :standardSurface1;
	setAttr ".bc" -type "float3" 0.40000001 0.40000001 0.40000001 ;
	setAttr ".sr" 0.5;
select -ne :openPBR_shader1;
	setAttr ".bc" -type "float3" 0.40000001 0.40000001 0.40000001 ;
	setAttr ".sr" 0.5;
select -ne :initialShadingGroup;
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultResolution;
	setAttr ".pa" 1;
select -ne :defaultColorMgtGlobals;
	setAttr ".cfe" yes;
	setAttr ".cfp" -type "string" "<MAYA_RESOURCES>/OCIO-configs/Maya2022-default/config.ocio";
	setAttr ".vtn" -type "string" "ACES 1.0 SDR-video (sRGB)";
	setAttr ".vn" -type "string" "ACES 1.0 SDR-video";
	setAttr ".dn" -type "string" "sRGB";
	setAttr ".wsn" -type "string" "ACEScg";
	setAttr ".otn" -type "string" "ACES 1.0 SDR-video (sRGB)";
	setAttr ".potn" -type "string" "ACES 1.0 SDR-video (sRGB)";
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
select -ne :ikSystem;
	setAttr -s 4 ".sol";
// End of cycle.ma
