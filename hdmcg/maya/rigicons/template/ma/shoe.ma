//Maya ASCII 2026 scene
//Name: shoe.ma
//Last modified: Fri, Jun 19, 2026 12:17:34 PM
//Codeset: 1252
requires maya "2026";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2026";
fileInfo "version" "2026";
fileInfo "cutIdentifier" "202507081222-4d6919b75c";
fileInfo "osv" "Windows 11 Pro v2009 (Build: 26200)";
fileInfo "UUID" "487B4A05-44B9-B6D5-15F2-4A901660B7B0";
fileInfo "license" "education";
createNode transform -n "shoe_ctrl";
	rename -uid "175EAE71-4542-57C6-1B68-74AA5E26A9CE";
createNode nurbsCurve -n "shoe_ctrlShape" -p "shoe_ctrl";
	rename -uid "535D9857-4E48-D61C-8035-A294D40B88F9";
	setAttr -k off ".v";
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 1 0 0.018911498 ;
	setAttr ".cc" -type "nurbsCurve" 
		3 16 0 no 3
		21 0 0 0 0.0625 0.125 0.1875 0.25 0.3125 0.375 0.4375 0.5 0.5625 0.625 0.6875
		 0.75 0.8125 0.875 0.9375 1 1 1
		19
		-0.12490631495017622 0 0.12490631495017622
		-0.12950051882421468 0 0.0753608038663688
		-0.14889385060344223 0 -0.017809478784451691
		-0.18253823131560365 0 -0.20668736742265156
		-0.15060589728459733 0 -0.32479044669471308
		-0.12413755113890003 0 -0.4564645883576674
		-0.051640254642412002 0 -0.55863434204279394
		0.13058361338886754 0 -0.58969625586577423
		0.1597263923519906 0 -0.49362634065748195
		0.19911483892236276 0 -0.25427613849897368
		0.17264013595100708 0 -0.10826197583080627
		0.077956163878976789 0 0.021444250581891207
		0.11383786453333654 0 0.1703984901375864
		0.13474396969846533 0 0.32006581002792001
		0.077411541530013325 0 0.45537757745676877
		-0.12467370827841438 0 0.42740287557980883
		-0.13571850266102065 0 0.26902960208139637
		-0.12559209930695456 0 0.17401317390379684
		-0.12490631495017622 0 0.12506203990766587
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
// End of shoe.ma
