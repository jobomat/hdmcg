//Maya ASCII 2026 scene
//Name: arcArrow.ma
//Last modified: Fri, Jun 19, 2026 12:17:34 PM
//Codeset: 1252
requires maya "2026";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2026";
fileInfo "version" "2026";
fileInfo "cutIdentifier" "202507081222-4d6919b75c";
fileInfo "osv" "Windows 11 Pro v2009 (Build: 26200)";
fileInfo "UUID" "716200F1-4DD7-AA26-4BD6-268A845185AD";
fileInfo "license" "education";
createNode transform -n "arcArrow_ctrl";
	rename -uid "69BCA7C5-49D2-56BE-81D5-B6BAEAE4377A";
createNode nurbsCurve -n "arcArrow_ctrlShape" -p "arcArrow_ctrl";
	rename -uid "AD3471A7-4383-67C5-35BC-ED938212CCDE";
	setAttr -k off ".v";
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 1 0 0.018911498 ;
	setAttr ".cc" -type "nurbsCurve" 
		3 33 0 no 3
		38 0 0 0 1 2 3 4 5 6 7 8 8 8 9 9 9 10 10 10 11 11 11 12 12 12 13 14 15 16 17
		 18 19 20 20 20 21 21 21
		36
		0 0 0.24915530140818526
		-0.016241390716625309 0.0012146412121333946 0.24913136813195877
		-0.048827660390837101 0.0034112574530556538 0.24587353721352306
		-0.095791515542822628 0.0058556079393005294 0.23154578034653536
		-0.13912045341355853 0.0073619851199841768 0.20832945480348036
		-0.17711929673124219 0.0078704382425299046 0.17711929673124219
		-0.20832945480348036 0.0073619851199841768 0.13912045341355853
		-0.23154578034653536 0.0058556079393005294 0.095791515542822628
		-0.24587353721352306 0.0034112574530556538 0.048827660390837101
		-0.24913136813195877 0.0012146412121333946 0.016241390716625309
		-0.24915530140818526 0 2.1610777525832754e-19
		-0.19932424112654823 0 0
		-0.14949318084491114 0 0
		-0.099662120563274115 0 0
		-0.19932424112654823 0 -0.099662120563274115
		-0.29898636168982229 0 -0.19932424112654823
		-0.39864848225309646 0 -0.29898636168982229
		-0.49831060281637052 0 -0.19932424112654823
		-0.59797272337964458 0 -0.099662120563274115
		-0.69763484394291864 0 0
		-0.64780378366128166 0 0
		-0.59797272337964458 0 0
		-0.5481416630980076 0 0
		-0.5481132850516599 0.0026745113398070038 0.035737502184329105
		-0.5409872823524835 0.0075115101621113962 0.10744539273307303
		-0.50950389654987316 0.012894387724452172 0.21079904516542872
		-0.45844227630730999 0.016211842482007702 0.3061541413775915
		-0.38977364304122242 0.017331619794781639 0.38977364304122242
		-0.3061541413775915 0.016211842482007702 0.45844227630730999
		-0.21079904516542872 0.012894387724452172 0.50950389654987316
		-0.10744539273307303 0.0075115101621113962 0.5409872823524835
		-0.035737502184329105 0.0026745113398070038 0.5481132850516599
		1.2966466515529551e-18 2.0746346424787485e-17 0.5481416630980076
		0 0 0.44847954253473349
		0 0 0.34881742197145932
		0 0 0.24915530140818526
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
// End of arcArrow.ma
