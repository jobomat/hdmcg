//Maya ASCII 2026 scene
//Name: fourTris.ma
//Last modified: Fri, Jun 19, 2026 12:17:34 PM
//Codeset: 1252
requires maya "2026";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2026";
fileInfo "version" "2026";
fileInfo "cutIdentifier" "202507081222-4d6919b75c";
fileInfo "osv" "Windows 11 Pro v2009 (Build: 26200)";
fileInfo "UUID" "883FAA3C-4197-C816-8701-929F33D50E13";
fileInfo "license" "education";
createNode transform -n "fourTris_ctrl";
	rename -uid "35E4EF4D-4696-8C8C-9EA9-84B11D47B82C";
createNode nurbsCurve -n "fourTris_ctrlShape" -p "fourTris_ctrl";
	rename -uid "20117402-487E-A139-9859-BE821C8B484A";
	setAttr -k off ".v";
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 1 0 0.018911498 ;
	setAttr ".cc" -type "nurbsCurve" 
		1 3 0 no 3
		4 0 1 2 3
		4
		-0.499975495933 0 0.14439929143050001
		-0.50014348008999998 0 -0.1456272316535
		-0.247538232227 0 -0.00031146189586300001
		-0.49888322218850001 0 0.1456272316535
		;
createNode nurbsCurve -n "fourTris_ctrlShape1" -p "fourTris_ctrl";
	rename -uid "19973D66-45DF-4F17-6370-899411C95E2B";
	setAttr -k off ".v";
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 1 0 0.018911498 ;
	setAttr ".cc" -type "nurbsCurve" 
		1 3 0 no 3
		4 0 1 2 3
		4
		0.499975495933 0 -0.14439929143050001
		0.50014348008999998 0 0.1456272316535
		0.247538232227 0 0.00031146189586249998
		0.49888322218850001 0 -0.1456272316535
		;
createNode nurbsCurve -n "fourTris_ctrlShape2" -p "fourTris_ctrl";
	rename -uid "79306625-49E1-335E-F3CA-AB98A8D43C7C";
	setAttr -k off ".v";
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 1 0 0.018911498 ;
	setAttr ".cc" -type "nurbsCurve" 
		1 3 0 no 3
		4 0 1 2 3
		4
		-0.14439929143050001 0 -0.499975495933
		0.1456272316535 0 -0.50014348008999998
		0.00031146189586249998 0 -0.247538232227
		-0.1456272316535 0 -0.49888322218850001
		;
createNode nurbsCurve -n "fourTris_ctrlShape3" -p "fourTris_ctrl";
	rename -uid "C7B86ADC-4DE2-DEF9-A10A-899099CB23D5";
	setAttr -k off ".v";
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 1 0 0.018911498 ;
	setAttr ".cc" -type "nurbsCurve" 
		1 3 0 no 3
		4 0 1 2 3
		4
		0.14439929143050001 0 0.499975495933
		-0.1456272316535 0 0.50014348008999998
		-0.00031146189586249998 0 0.247538232227
		0.1456272316535 0 0.49888322218850001
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
// End of fourTris.ma
