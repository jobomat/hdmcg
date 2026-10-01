//Maya ASCII 2026 scene
//Name: slider_neg_pos.ma
//Last modified: Tue, Jul 21, 2026 12:27:06 PM
//Codeset: 1252
requires maya "2026";
currentUnit -l centimeter -a degree -t pal;
fileInfo "application" "maya";
fileInfo "product" "Maya 2026";
fileInfo "version" "2026";
fileInfo "cutIdentifier" "202507081222-4d6919b75c";
fileInfo "osv" "Windows 11 Pro v2009 (Build: 26200)";
fileInfo "UUID" "BD30C451-4799-3F7F-734F-ABB35EF698B7";
fileInfo "license" "education";
createNode transform -n "slider_frame_crv";
	rename -uid "098413AC-4340-837F-6CBE-6490F4F99A5D";
createNode nurbsCurve -n "slider_frame_crvShape" -p "slider_frame_crv";
	rename -uid "1A47A8A0-41FA-3ABB-B60C-A7AE3337D820";
	setAttr -k off ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.10000000000000001 -1 0
		0.10000000000000001 -1 0
		0.10000000000000001 1 0
		-0.10000000000000001 1 0
		-0.10000000000000001 -1 0
		;
createNode transform -n "slider_ctrl" -p "slider_frame_crv";
	rename -uid "812EF1C9-4FD0-5165-9D12-B09D3F352D64";
	addAttr -ci true -sn "val1" -ln "val1" -min 0 -max 1 -at "double";
	addAttr -ci true -sn "val2" -ln "val2" -min 0 -max 1 -at "double";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".mntl" -type "double3" 0 -1 0 ;
	setAttr ".mxtl" -type "double3" 0 1 0 ;
	setAttr ".mtxe" yes;
	setAttr ".mtye" yes;
	setAttr ".mtze" yes;
	setAttr ".xtxe" yes;
	setAttr ".xtye" yes;
	setAttr ".xtze" yes;
createNode nurbsCurve -n "slider_ctrlShape" -p "slider_ctrl";
	rename -uid "AC172999-4338-1FA1-8D19-3CBA520A1E6B";
	setAttr -k off ".v";
	setAttr ".tw" yes;
createNode expression -n "slider_ctrl_expression";
	rename -uid "4F46ABDC-4CBB-5725-EB4F-F8900C5972F9";
	setAttr -k on ".nds";
	setAttr -s 2 ".out";
	setAttr ".ixp" -type "string" ".O[0] = clamp( 0, 1, .I[0] );\n.O[1] = -1 * clamp( -1, 0, .I[0] );";
createNode makeNurbCircle -n "makeNurbCircle1";
	rename -uid "F09EF78B-40A0-2BAA-13E9-BDA11E4550B6";
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
connectAttr "slider_ctrl_expression.out[0]" "slider_ctrl.val1";
connectAttr "slider_ctrl_expression.out[1]" "slider_ctrl.val2";
connectAttr "makeNurbCircle1.oc" "slider_ctrlShape.cr";
connectAttr "slider_ctrl.ty" "slider_ctrl_expression.in[0]";
connectAttr "slider_ctrl.msg" "slider_ctrl_expression.obm";
// End of slider_neg_pos.ma
