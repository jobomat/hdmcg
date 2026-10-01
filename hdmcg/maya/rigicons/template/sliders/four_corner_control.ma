//Maya ASCII 2026 scene
//Name: four_corner_control.ma
//Last modified: Tue, Jul 21, 2026 12:27:37 PM
//Codeset: 1252
requires maya "2026";
currentUnit -l centimeter -a degree -t pal;
fileInfo "application" "maya";
fileInfo "product" "Maya 2026";
fileInfo "version" "2026";
fileInfo "cutIdentifier" "202507081222-4d6919b75c";
fileInfo "osv" "Windows 11 Pro v2009 (Build: 26200)";
fileInfo "UUID" "0BB408D9-44C4-07D5-984D-4E9F410DDBB9";
fileInfo "license" "education";
createNode transform -n "fourCorner_frame_crv";
	rename -uid "F53D5D70-468D-9F44-506B-FFB548AF575C";
createNode nurbsCurve -n "fourCorner_frame_crvShape" -p "fourCorner_frame_crv";
	rename -uid "9A667850-49DD-036F-66C3-BABF449EB63F";
	setAttr -k off ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-1 -1 0
		1 -1 0
		1 1 0
		-1 1 0
		-1 -1 0
		;
createNode transform -n "fourCorner_ctrl" -p "fourCorner_frame_crv";
	rename -uid "8BBEC7CE-4F0E-DC01-E0A5-2CA0723A084D";
	addAttr -ci true -k true -sn "topLeftVal" -ln "topLeftVal" -min 0 -max 1 -at "double";
	addAttr -ci true -k true -sn "topRightVal" -ln "topRightVal" -min 0 -max 1 -at "double";
	addAttr -ci true -k true -sn "bottomLeftVal" -ln "bottomLeftVal" -min 0 -max 1 -at "double";
	addAttr -ci true -k true -sn "bottomRightVal" -ln "bottomRightVal" -min 0 -max 1 
		-at "double";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".mntl" -type "double3" -1 -1 0 ;
	setAttr ".mxtl" -type "double3" 1 1 0 ;
	setAttr ".mtxe" yes;
	setAttr ".mtye" yes;
	setAttr ".mtze" yes;
	setAttr ".xtxe" yes;
	setAttr ".xtye" yes;
	setAttr ".xtze" yes;
	setAttr -k on ".topLeftVal";
	setAttr -k on ".topRightVal";
	setAttr -k on ".bottomLeftVal";
	setAttr -k on ".bottomRightVal";
createNode nurbsCurve -n "fourCorner_ctrlShape" -p "fourCorner_ctrl";
	rename -uid "B7219EBD-4C6E-3504-3B86-4C9FE7AD5117";
	setAttr -k off ".v";
	setAttr ".tw" yes;
createNode expression -n "fourCorner_ctrl_expression";
	rename -uid "3842DF02-4CBE-BB59-1117-38859FF35227";
	setAttr -k on ".nds";
	setAttr -s 2 ".in";
	setAttr -s 2 ".in";
	setAttr -s 4 ".out";
	setAttr ".ixp" -type "string" ".O[0] = clamp( 0,1,.I[0] * (1 + clamp( -1,0,.I[1] ) ) );\n        .O[1] = clamp( 0,1,.I[0] * (1 - clamp( 0,1,.I[1] ) ) );\n        .O[2] = clamp( 0,1,-.I[0] * (1 - clamp( 0,1,.I[1] ) ) );\n        .O[3] = clamp( 0,1,-.I[0] * (1 + clamp( -1,0,.I[1] ) ) );";
createNode makeNurbCircle -n "makeNurbCircle1";
	rename -uid "E16B5383-468A-9FF6-E670-64920249B4E2";
	setAttr ".r" 0.15;
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
	setAttr ".w" 1000;
	setAttr ".h" 500;
	setAttr ".pa" 1;
select -ne :defaultColorMgtGlobals;
	setAttr ".cfe" yes;
	setAttr ".cfp" -type "string" "K:/pipeline/OCIO/cg-config-v3.0.0_aces-v2.0_ocio-v2.4.ocio";
	setAttr ".vtn" -type "string" "ACES 2.0 - SDR 100 nits (Rec.709) (sRGB - Display)";
	setAttr ".vn" -type "string" "ACES 2.0 - SDR 100 nits (Rec.709)";
	setAttr ".dn" -type "string" "sRGB - Display";
	setAttr ".wsn" -type "string" "ACEScg";
	setAttr ".otn" -type "string" "ACES 2.0 - SDR 100 nits (Rec.709) (sRGB - Display)";
	setAttr ".potn" -type "string" "ACES 2.0 - SDR 100 nits (Rec.709) (sRGB - Display)";
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
connectAttr "fourCorner_ctrl_expression.out[0]" "fourCorner_ctrl.topLeftVal";
connectAttr "fourCorner_ctrl_expression.out[1]" "fourCorner_ctrl.topRightVal";
connectAttr "fourCorner_ctrl_expression.out[2]" "fourCorner_ctrl.bottomRightVal"
		;
connectAttr "fourCorner_ctrl_expression.out[3]" "fourCorner_ctrl.bottomLeftVal";
connectAttr "makeNurbCircle1.oc" "fourCorner_ctrlShape.cr";
connectAttr "fourCorner_ctrl.ty" "fourCorner_ctrl_expression.in[0]";
connectAttr "fourCorner_ctrl.tx" "fourCorner_ctrl_expression.in[1]";
connectAttr "fourCorner_ctrl.msg" "fourCorner_ctrl_expression.obm";
// End of four_corner_control.ma
