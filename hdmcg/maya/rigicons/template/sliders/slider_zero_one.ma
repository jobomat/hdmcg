//Maya ASCII 2026 scene
//Name: slider_zero_one.ma
//Last modified: Tue, Jul 21, 2026 12:26:25 PM
//Codeset: 1252
requires maya "2026";
currentUnit -l centimeter -a degree -t pal;
fileInfo "application" "maya";
fileInfo "product" "Maya 2026";
fileInfo "version" "2026";
fileInfo "cutIdentifier" "202507081222-4d6919b75c";
fileInfo "osv" "Windows 11 Pro v2009 (Build: 26200)";
fileInfo "UUID" "85B972FB-4498-C556-9402-04B99B2E2AB2";
fileInfo "license" "education";
createNode transform -n "slider_frame_crv";
	rename -uid "7883BFBB-4AFD-489F-3051-0B955ACC82A6";
createNode nurbsCurve -n "slider_frame_crvShape" -p "slider_frame_crv";
	rename -uid "D0820D18-4497-3332-30C3-E5922410E9B3";
	setAttr -k off ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.10000000000000001 0 0
		0.10000000000000001 0 0
		0.10000000000000001 1 0
		-0.10000000000000001 1 0
		-0.10000000000000001 0 0
		;
createNode transform -n "slider_ctrl" -p "slider_frame_crv";
	rename -uid "ED5BE6AD-4A33-67B8-FE01-1AB97DC4B636";
	addAttr -ci true -sn "val1" -ln "val1" -min 0 -max 1 -at "double";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".mntl" -type "double3" 0 0 0 ;
	setAttr ".mxtl" -type "double3" 0 1 0 ;
	setAttr ".mtxe" yes;
	setAttr ".mtye" yes;
	setAttr ".mtze" yes;
	setAttr ".xtxe" yes;
	setAttr ".xtye" yes;
	setAttr ".xtze" yes;
createNode nurbsCurve -n "slider_ctrlShape" -p "slider_ctrl";
	rename -uid "BB2B32C9-458F-C1DD-5C7D-24852AC61E07";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.11754174373368367 0.11754174373368369 0
		1.0178598484666367e-17 0.16622912813315815 0
		-0.11754174373368367 0.11754174373368365 0
		-0.16622912813315821 8.617347356287245e-18 0
		-0.11754174373368367 -0.11754174373368367 0
		-1.6651285454404835e-17 -0.16622912813315824 0
		0.11754174373368367 -0.11754174373368365 0
		0.16622912813315821 -2.2668607511699385e-17 0
		0.11754174373368367 0.11754174373368369 0
		1.0178598484666367e-17 0.16622912813315815 0
		-0.11754174373368367 0.11754174373368365 0
		;
createNode expression -n "slider_ctrl_expression";
	rename -uid "B65CFCE5-4AAC-C35F-D0AC-1D99D572EC3B";
	setAttr -k on ".nds";
	setAttr ".ixp" -type "string" ".O[0] = clamp( 0, 1, .I[0] );";
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
connectAttr "slider_ctrl.ty" "slider_ctrl_expression.in[0]";
connectAttr "slider_ctrl.msg" "slider_ctrl_expression.obm";
// End of slider_zero_one.ma
