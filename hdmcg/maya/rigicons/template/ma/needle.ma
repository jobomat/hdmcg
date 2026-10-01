//Maya ASCII 2026 scene
//Name: needle.ma
//Last modified: Fri, Jun 19, 2026 12:17:34 PM
//Codeset: 1252
requires maya "2026";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2026";
fileInfo "version" "2026";
fileInfo "cutIdentifier" "202507081222-4d6919b75c";
fileInfo "osv" "Windows 11 Pro v2009 (Build: 26200)";
fileInfo "UUID" "440F0163-47A1-0A78-3C1A-E5BE7921AB5B";
fileInfo "license" "education";
createNode transform -n "needle_ctrl";
	rename -uid "7B65FE29-4D7D-19BD-1674-E0A613486B57";
createNode nurbsCurve -n "needle_ctrlShape" -p "needle_ctrl";
	rename -uid "C84D6501-4D99-2BC4-85F4-1E862D24180E";
	setAttr -k off ".v";
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 1 0 0.018911498 ;
	setAttr ".cc" -type "nurbsCurve" 
		3 14 0 no 3
		19 0 0 0 1 2 3 4 5 6 7 8 8 8 9 10 11 12 12 12
		17
		-5.906749519568157e-18 0.30877873043976795 -0.017825926526720555
		-5.3872837499085627e-18 0.31308592633483057 -0.042253248293577073
		-3.1758781043142215e-18 0.34142682404094998 -0.089501997038473127
		1.7816549927523427e-18 0.41966876788830049 -0.11201525776080015
		5.8106156442762653e-18 0.49282766123101079 -0.076025679835991261
		6.7843817660592004e-18 0.5223811738637264 2.8440762485977311e-17
		4.1938711371497869e-18 0.49282766123101079 0.076025679835991261
		-6.0043554678290092e-19 0.41966876788830049 0.11201525776080015
		-5.0792068532493255e-18 0.34142682404094998 0.089501997038473127
		-6.2858315463201529e-18 0.31308592633483057 0.042253248293577073
		-6.2858315463201529e-18 0.30877873043976795 0.017825926526720555
		0 0.20493729173458181 5.6881524971954619e-18
		0 4.5505219977604679e-17 1.1376304994411416e-17
		0 4.5505219977604679e-17 1.1376304994411416e-17
		0 4.5505219977604679e-17 1.1376304994411416e-17
		0 0.20493729173458181 5.6881524971954619e-18
		0 0.30903511841493253 -0.019218525183097891
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
// End of needle.ma
