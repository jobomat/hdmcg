//Maya ASCII 2026 scene
//Name: arcArrow2.ma
//Last modified: Fri, Jun 19, 2026 12:17:34 PM
//Codeset: 1252
requires maya "2026";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2026";
fileInfo "version" "2026";
fileInfo "cutIdentifier" "202507081222-4d6919b75c";
fileInfo "osv" "Windows 11 Pro v2009 (Build: 26200)";
fileInfo "UUID" "58927DAD-4912-6F57-EB5C-F787B4D4AF6C";
fileInfo "license" "education";
createNode transform -n "arcArrow2_ctrl";
	rename -uid "53FB4164-4FCB-631B-ECB7-899FC27D0D7B";
	setAttr ".s" -type "double3" 0.63750348940345347 0.63750348940345347 0.63750348940345347 ;
createNode nurbsCurve -n "arcArrow2_ctrlShape" -p "arcArrow2_ctrl";
	rename -uid "54C09FC5-448E-5E46-5B89-ACB61BC46090";
	setAttr -k off ".v";
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 1 0 0.018911498 ;
	setAttr ".cc" -type "nurbsCurve" 
		3 28 0 no 3
		33 0 0 0 1 1 1 2 2 2 3 3 3 4 4 4 5 5 5 6 6 6 7 7 7 8 8 8 9 9 9 10 10 10
		31
		-0.63663240106399999 6.0319423505800001e-17 0.92112626971099998
		-0.23556221779600001 1.2359277220200001e-17 1.1441920167299999
		0.23556221779600001 1.5353816567499999e-19 1.1441920167299999
		0.63644270064899999 4.75550328961e-17 0.92121478635800003
		0.65767353425099995 4.3775119211400001e-17 0.95700722730900001
		0.67890436785300001 3.9995205526700003e-17 0.99279966826099997
		0.70013520145499997 3.6215291841999998e-17 1.0285921092100001
		0.729258416154 6.0026840259099997e-17 0.91454556010499999
		0.75838163085300003 8.3838388676199996e-17 0.80049901099800003
		0.78750484555199995 1.0764993709300001e-16 0.68645246189099995
		0.67345829644400002 9.8958043415000003e-17 0.65732924719200003
		0.55941174733700005 9.0266149736799999e-17 0.628206032493
		0.44536519822999998 8.1574256058499995e-17 0.59908281779399997
		0.46659603183199999 7.7794342373800002e-17 0.63487525874499995
		0.487826865434 7.4014428689099997e-17 0.67066769969700002
		0.50905769903599996 7.0234515004400005e-17 0.706460140648
		0.17667166334699999 1.1665766138899999e-17 0.88387980497899998
		-0.17667166334699999 -2.2811545994999998e-18 0.88387980497899998
		-0.50885911827899999 1.1564260362700001e-17 0.70660241393900003
		-0.487563571147 3.4383998389000001e-18 0.670848437977
		-0.46626802401700002 -4.6874606849499999e-18 0.63509446201499997
		-0.44497247688500002 -1.28133212088e-17 0.59934048605199997
		-0.55907152307200003 1.0998227208300001e-17 0.62825734371499997
		-0.67317056925800001 3.4809775625399998e-17 0.657174201377
		-0.78726961544399998 5.8621324042499997e-17 0.68609105903900003
		-0.75835275778199995 6.7313217720800001e-17 0.800190105225
		-0.72943590012000004 7.6005111399200006e-17 0.91428915141099998
		-0.70051904245700003 8.4697005077399997e-17 1.0283881976
		-0.67922349532699999 7.6571144553500003e-17 0.99263422163600001
		-0.657927948195 6.8445284029699996e-17 0.95688024567399999
		-0.63663240106399999 6.0319423505800001e-17 0.92112626971099998
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
// End of arcArrow2.ma
