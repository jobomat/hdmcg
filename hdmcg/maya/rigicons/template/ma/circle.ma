//Maya ASCII 2026 scene
//Name: circle.ma
//Last modified: Fri, Jun 19, 2026 12:17:33 PM
//Codeset: 1252
requires maya "2026";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2026";
fileInfo "version" "2026";
fileInfo "cutIdentifier" "202507081222-4d6919b75c";
fileInfo "osv" "Windows 11 Pro v2009 (Build: 26200)";
fileInfo "UUID" "89F0AB46-4DD4-442E-2FEC-B3B153667AC5";
fileInfo "license" "education";
createNode transform -n "circle_ctrl";
	rename -uid "27FD86C3-424B-76EC-6139-79918FDC9FA0";
createNode nurbsCurve -n "circle_ctrlShape" -p "circle_ctrl";
	rename -uid "3149F397-4E68-A6D0-E7A6-B0A917EA7319";
	setAttr -k off ".v";
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 1 0 0.018911498 ;
	setAttr ".cc" -type "nurbsCurve" 
		3 9 0 no 3
		14 3.9986081329999998 3.9986081329999998 3.9986081329999998 4 5 6 7 8 9 10
		 11 11.998608132999999 11.998608132999999 11.998608132999999
		12
		-0.000545341477605 -3.0616150729499999e-17 0.49999968563699998
		-0.00036356105383449999 -3.0616163561400003e-17 0.49999989519799998
		0.13042015695500001 -3.0620780526499999e-17 0.50007529596
		0.3918058124455 -2.3991186704949999e-17 0.3918058124455
		0.55409709377500005 -1.8223150339499999e-32 2.9760662996400002e-16
		0.3918058124455 2.3991186704949999e-17 -0.3918058124455
		-6.3215853039000001e-17 3.392866161555e-17 -0.55409709377500005
		-0.3918058124455 2.3991186704949999e-17 -0.3918058124455
		-0.55409709377500005 9.8316773081e-33 -1.6056347536199999e-16
		-0.39188110840500001 -2.3980055857899999e-17 0.39162403191849998
		-0.13096542442949999 -3.0606944345399999e-17 0.49984933397449999
		-0.000545341477605 -3.0616150729499999e-17 0.49999968563699998
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
// End of circle.ma
