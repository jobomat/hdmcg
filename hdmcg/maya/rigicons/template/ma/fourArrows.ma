//Maya ASCII 2026 scene
//Name: fourArrows.ma
//Last modified: Fri, Jun 19, 2026 12:17:34 PM
//Codeset: 1252
requires maya "2026";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2026";
fileInfo "version" "2026";
fileInfo "cutIdentifier" "202507081222-4d6919b75c";
fileInfo "osv" "Windows 11 Pro v2009 (Build: 26200)";
fileInfo "UUID" "E7D89905-42FF-FCBB-591E-1F8EEB3FBE04";
fileInfo "license" "education";
createNode transform -n "fourArrows_ctrl";
	rename -uid "A72B11DD-41D7-4A12-6608-338987EDF099";
createNode nurbsCurve -n "fourArrows_ctrlShape" -p "fourArrows_ctrl";
	rename -uid "48C25D8A-4D1F-58D3-B7C2-119589ADC26A";
	setAttr -k off ".v";
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 1 0 0.018911498 ;
	setAttr ".cc" -type "nurbsCurve" 
		1 24 0 no 3
		25 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24
		25
		-0.057744455151983246 7.0668165980385642e-17 0.31826112597614203
		-0.057744455151983246 1.0949402431255394e-17 0.049311724709293965
		-0.31826112597614203 1.0949402431255394e-17 0.049311724709293965
		-0.31826112597614203 4.7112110653488872e-17 0.21217408398389156
		-0.53043520995820548 0 0
		-0.31826112597614203 -4.7112110653488872e-17 -0.21217408398389156
		-0.31826112597614203 -1.0949402431255394e-17 -0.049311724709293965
		-0.057744455151983246 -1.0949402431255394e-17 -0.049311724709293965
		-0.057744455151983246 -7.0668165980385642e-17 -0.31826112597614203
		-0.21217408398389156 -7.0668165980385642e-17 -0.31826112597614203
		0 -1.1778027663417919e-16 -0.53043520995820548
		0.21217408398389156 -7.0668165980385642e-17 -0.31826112597614203
		0.057744455151983246 -7.0668165980385642e-17 -0.31826112597614203
		0.057744455151983246 -1.0949402431255394e-17 -0.049311724709293965
		0.31826112597614203 -1.0949402431255394e-17 -0.049311724709293965
		0.31826112597614203 -4.7112110653488872e-17 -0.21217408398389156
		0.53043520995820548 0 0
		0.31826112597614203 4.7112110653488872e-17 0.21217408398389156
		0.31826112597614203 1.0949402431255394e-17 0.049311724709293965
		0.057744455151983246 1.0949402431255394e-17 0.049311724709293965
		0.057744455151983246 7.0668165980385642e-17 0.31826112597614203
		0.21217408398389156 7.0668165980385642e-17 0.31826112597614203
		0 1.1778027663417919e-16 0.53043520995820548
		-0.21217408398389156 7.0668165980385642e-17 0.31826112597614203
		-0.057744455151983246 7.0668165980385642e-17 0.31826112597614203
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
// End of fourArrows.ma
