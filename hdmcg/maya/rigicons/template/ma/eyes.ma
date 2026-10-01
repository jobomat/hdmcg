//Maya ASCII 2026 scene
//Name: eyes.ma
//Last modified: Thu, Jun 25, 2026 04:14:14 PM
//Codeset: 1252
requires maya "2026";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2026";
fileInfo "version" "2026";
fileInfo "cutIdentifier" "202507081222-4d6919b75c";
fileInfo "osv" "Windows 11 Pro v2009 (Build: 26200)";
fileInfo "UUID" "1F441490-4D6D-906D-7E25-E79905E59141";
fileInfo "license" "education";
createNode transform -n "eyes_ctrl";
	rename -uid "CE014491-4EBA-125B-B2D8-72910C6EC9AE";
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 1 0.71759999 0 ;
createNode nurbsCurve -n "eyes_ctrlShape" -p "eyes_ctrl";
	rename -uid "4B4C16FC-43E2-AB24-9DC6-6DB6854C5FE2";
	setAttr -k off ".v";
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 1 0 0.018911498 ;
	setAttr ".cc" -type "nurbsCurve" 
		3 16 0 no 3
		21 5.1424259980000002 5.5712129990000001 6.5712129990000001 7.5712129990000001
		 8.5712129990000001 9.5712129990000001 10.571212999 11.571212999 12 12.428787001 13.428787001
		 14.428787001 15.428787001 16.428787001 17.428787001 18.428787001 18.857574002 19.286361003
		 20.286361003 21.286361003 22.286361003
		19
		-0.091397855969000005 0.2113533878095 -3.3988217002249999e-17
		-0.25 0.27704854688750002 -4.4552804331250001e-17
		-0.44590290622250001 0.195902906223 -3.1503590063500001e-17
		-0.52704854689000002 8.0281737680999996e-17 -1.2910288071999999e-32
		-0.44590290622250001 -0.195902906223 3.1503590063500001e-17
		-0.25 -0.27704854688750002 4.4552804331250001e-17
		-0.091397855969000005 -0.2113533878095 3.3988217002249999e-17
		0 -0.10833758492700001 1.7422012413250001e-17
		0.091397855969000005 -0.2113533878095 3.3988217002249999e-17
		0.25 -0.27704854688750002 4.4552804331250001e-17
		0.44590290622250001 -0.195902906223 3.1503590063500001e-17
		0.52704854689000002 4.6353076065500002e-17 -5.3766118079499999e-33
		0.44590290622250001 0.195902906223 -3.1503590063500001e-17
		0.25 0.27704854688750002 -4.4552804331250001e-17
		0.091397855969000005 0.2113533878095 -3.3988217002249999e-17
		0 0.10833758492700001 -1.7422012413250001e-17
		-0.091397855969000005 0.2113533878095 -3.3988217002249999e-17
		-0.25 0.27704854688750002 -4.4552804331250001e-17
		-0.44590290622250001 0.195902906223 -3.1503590063500001e-17
		;
createNode transform -n "l_eye" -p "eyes_ctrl";
	rename -uid "024F28BD-4DA8-8BC5-B5C6-D5B59A4015BB";
	setAttr ".rp" -type "double3" -0.25000000000049999 0 0 ;
	setAttr ".sp" -type "double3" -0.25000000000049999 0 0 ;
createNode nurbsCurve -n "l_eyeShape" -p "l_eye";
	rename -uid "26BDAE85-4A9A-8A39-41F8-AAB2C6F045EB";
	setAttr -k off ".v";
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 1 0 0.018911498 ;
	setAttr ".cc" -type "nurbsCurve" 
		3 8 0 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		-0.191229128133 0.058770871867000002 -9.4510770189999993e-18
		-0.25 0.083114564066500002 -1.3365841299350002e-17
		-0.30877087186750002 0.058770871867000002 -9.4510770189999993e-18
		-0.33311456406750001 2.4084521304249999e-17 -3.8730864216000002e-33
		-0.30877087186750002 -0.058770871867000002 9.4510770189999993e-18
		-0.25 -0.083114564066500002 1.3365841299350002e-17
		-0.191229128133 -0.058770871867000002 9.4510770189999993e-18
		-0.1668854359335 -4.4640994494499999e-17 7.1788194350499997e-33
		-0.191229128133 0.058770871867000002 -9.4510770189999993e-18
		-0.25 0.083114564066500002 -1.3365841299350002e-17
		-0.30877087186750002 0.058770871867000002 -9.4510770189999993e-18
		;
createNode transform -n "r_eye" -p "eyes_ctrl";
	rename -uid "B6F36810-4C30-AD46-1062-1AABB0723860";
	setAttr ".rp" -type "double3" 0.25000000000049999 0 0 ;
	setAttr ".sp" -type "double3" 0.25000000000049999 0 0 ;
createNode nurbsCurve -n "r_eyeShape" -p "r_eye";
	rename -uid "EB0804E3-4E22-B0DE-875B-D5B3098E353B";
	setAttr -k off ".v";
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 1 0 0.018911498 ;
	setAttr ".cc" -type "nurbsCurve" 
		3 8 0 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.30877087186750002 0.058770871867000002 -9.4510770189999993e-18
		0.25 0.083114564066500002 -1.3365841299350002e-17
		0.191229128133 0.058770871867000002 -9.4510770189999993e-18
		0.1668854359335 2.4084521304249999e-17 -3.8730864216000002e-33
		0.191229128133 -0.058770871867000002 9.4510770189999993e-18
		0.25 -0.083114564066500002 1.3365841299350002e-17
		0.30877087186750002 -0.058770871867000002 9.4510770189999993e-18
		0.33311456406750001 -4.4640994494499999e-17 7.1788194350499997e-33
		0.30877087186750002 0.058770871867000002 -9.4510770189999993e-18
		0.25 0.083114564066500002 -1.3365841299350002e-17
		0.191229128133 0.058770871867000002 -9.4510770189999993e-18
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
// End of eyes.ma
