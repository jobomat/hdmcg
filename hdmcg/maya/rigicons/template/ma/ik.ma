//Maya ASCII 2026 scene
//Name: ik.ma
//Last modified: Sun, Jun 21, 2026 04:08:06 PM
//Codeset: 1252
requires maya "2026";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2026";
fileInfo "version" "2026";
fileInfo "cutIdentifier" "202510291147-60ec9eda33";
fileInfo "osv" "Windows 10 Home v2009 (Build: 19045)";
fileInfo "UUID" "EBB08CEA-4837-5ED2-94E1-DB9A1948C207";
fileInfo "license" "education";
createNode transform -n "ik_ctrl";
	rename -uid "EFCCC0A8-447D-0E9C-BEF1-37AFBDA647A5";
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0 0.48230001 1 ;
createNode nurbsCurve -n "ik_ctrlShape" -p "ik_ctrl";
	rename -uid "3C36FD33-4C90-35EC-1F47-8FB53AC316B6";
	setAttr -k off ".v";
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 1 0 0.018911498 ;
	setAttr ".tw" yes;
createNode nurbsCurve -n "ik_ctrlShape1" -p "ik_ctrl";
	rename -uid "E19400E3-4FAB-0CFA-1C5D-7BAEB75EAD22";
	setAttr -k off ".v";
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 1 0 0.018911498 ;
	setAttr ".tw" yes;
createNode nurbsCurve -n "ik_ctrlShape2" -p "ik_ctrl";
	rename -uid "639EA137-4760-A13F-A113-EFA9B52C3630";
	setAttr -k off ".v";
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 1 0 0.018911498 ;
	setAttr ".tw" yes;
createNode nurbsCurve -n "ik_ctrlShape3" -p "ik_ctrl";
	rename -uid "BCAD80EB-4FFB-30FF-E259-948ACDAF0AB0";
	setAttr -k off ".v";
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 1 0 0.018911498 ;
	setAttr ".tw" yes;
createNode nurbsCurve -n "ik_ctrlShapeOrig" -p "ik_ctrl";
	rename -uid "EFEE3B4D-4A63-6F81-C7A7-149DB513A0F1";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 2.2000000000000002 2.8999999999999999 5.0999999999999996 5.7999999999999998
		
		5
		-0.39514282677773921 -0.27736646873136306 0
		-0.39514282677773921 0.27736303694602654 0
		-0.21863798406236828 0.27736303694602654 0
		-0.21863798406236828 -0.27736646873136306 0
		-0.39514282677773921 -0.27736646873136306 0
		;
createNode nurbsCurve -n "ik_ctrlShape1Orig" -p "ik_ctrl";
	rename -uid "13D61E07-414C-F4EC-8B1F-EBAB92C74678";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".cc" -type "nurbsCurve" 
		1 11 0 no 3
		12 0 1.23627251439 2.2487727051199999 2.9487727051200001 5.1487727051199998
		 5.84877270512 6.7722090368499996 7.9151238344000001 8.6713731668200005 10.0035915986
		 11.4904891913 12.2826765721
		12
		0.23759555170727614 -0.27736646873136306 0
		0.058726768774939639 -0.022064773137589967 0
		0.058726768774939639 -0.27736646873136306 0
		-0.11777807394043133 -0.27736646873136306 0
		-0.11777807394043133 0.27736303694602654 0
		0.058726768774939639 0.27736303694602654 0
		0.058726768774939639 0.044518773389293761 0
		0.22853416564155801 0.27736303694602654 0
		0.41922226488362507 0.27736303694602654 0
		0.20607711835825629 0.017727835715711251 0
		0.43734542177311925 -0.27736646873136306 0
		0.23759555170727614 -0.27736646873136306 0
		;
createNode nurbsCurve -n "ik_ctrlShape2Orig" -p "ik_ctrl";
	rename -uid "4D2A1A61-4F6B-8167-6D97-F998967694E2";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".cc" -type "nurbsCurve" 
		1 10 0 no 3
		11 0 0.5 1.43750057221 1.83750057221 2.77500114443 3.6750011444299999 4.3750011444299997
		 6.5750011444299998 8.2515648126999999 8.6515648127000002 9.6281284809599992
		11
		0.028658463090285104 -0.27760064745178686 0
		0.028658463090285104 -0.2775182761649248 0
		0.028504016834297322 -0.2775182761649248 0
		0.028504016834297322 -0.27745237913535598 0
		0.028658463090285104 -0.27745237913535598 0
		0.028658463090285104 -0.27730411081892503 0
		0.028773782894903548 -0.27730411081892503 0
		0.028773782894903548 -0.27766654448135575 0
		0.028497581479684158 -0.27766654448135575 0
		0.028497581479684158 -0.27760064745178686 0
		0.028658463090285104 -0.27760064745178686 0
		;
createNode nurbsCurve -n "ik_ctrlShape3Orig" -p "ik_ctrl";
	rename -uid "9B6FF414-4DFA-6E92-63E2-A2B6141C58EB";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".cc" -type "nurbsCurve" 
		1 11 0 no 3
		12 0 1.23627251439 2.2487727051199999 2.9487727051200001 5.1487727051199998
		 5.84877270512 6.7722090368499996 7.9151238344000001 8.6713731668200005 10.0035915986
		 11.4904891913 12.2826765721
		12
		0.028228587915080382 -0.27730411081892503 0
		0.028345452200526363 -0.27747091270636309 0
		0.028345452200526363 -0.27730411081892503 0
		0.028460772001182192 -0.27730411081892503 0
		0.028460772001182192 -0.27766654448135575 0
		0.028345452200526363 -0.27766654448135575 0
		0.028345452200526363 -0.27751441520338677 0
		0.028234508189143654 -0.27766654448135575 0
		0.028109921729391692 -0.27766654448135575 0
		0.028249180548967929 -0.27749691128903847 0
		0.028098080927657774 -0.27730411081892503 0
		0.028228587915080382 -0.27730411081892503 0
		;
createNode blendShape -n "ik_fk_blendShape";
	rename -uid "7CA91223-44D9-C523-8AA6-31862A793758";
	addAttr -ci true -h true -sn "aal" -ln "attributeAliasList" -dt "attributeAlias";
	setAttr -s 4 ".ip";
	setAttr -s 4 ".og";
	setAttr -s 4 ".orggeom";
	setAttr ".w[0]"  0;
	setAttr -s 4 ".it";
	setAttr ".it[0].itg[0].iti[6000].ipt" -type "pointArray" 5 0.41640049135228097
		 0.55750245403962073 0 1 0.41640049135228097 0.0025645575976103174 0 1 0.23982934248435059
		 0.0025645575976103174 0 1 0.23982934248435059 0.55750245403962073 0 1 0.41640049135228097
		 0.55750245403962073 0 1 ;
	setAttr ".it[0].itg[0].iti[6000].ict" -type "componentList" 1 "cv[0:4]";
	setAttr ".it[1].itg[0].iti[6000].ipt" -type "pointArray" 12 -0.21657558286008441
		 0.55750245403962073 0 1 -0.037639605733286424 0.30210485131527071 0 1 -0.037639605733286424
		 0.55750245403962073 0 1 0.1389315431306814 0.55750245403962073 0 1 0.1389315431306814
		 0.0025645575976103174 0 1 -0.037639605733286424 0.0025645575976103174 0 1 -0.037639605733286424
		 0.23549629188486954 0 1 -0.20751079277705647 0.0025645575976103174 0 1 -0.39827052628044091
		 0.0025645575976103174 0 1 -0.18504530923635845 0.26229729389200823 0 1 -0.41640049135117146
		 0.55750245403962073 0 1 -0.21657558286008441 0.55750245403962073 0 1 ;
	setAttr ".it[1].itg[0].iti[6000].ict" -type "componentList" 1 "cv[0:11]";
	setAttr ".it[2].itg[0].iti[6000].ipt" -type "pointArray" 11 -0.3386119647705913
		 0.45334136643735445 0 1 -0.3386119647705913 0.32800206305716395 0 1 -0.10360062749745273
		 0.32800206305716395 0 1 -0.10360062749745273 0.22773062035451735 0 1 -0.3386119647705913
		 0.22773062035451735 0 1 -0.3386119647705913 0.0021198742756428079 0 1 -0.51408698950428466
		 0.0021198742756428079 0 1 -0.51408698950428466 0.55361280914000111 0 1 -0.093808345000373147
		 0.55361280914000111 0 1 -0.093808345000373147 0.45334136643735445 0 1 -0.3386119647705913
		 0.45334136643735445 0 1 ;
	setAttr ".it[2].itg[0].iti[6000].ict" -type "componentList" 1 "cv[0:10]";
	setAttr ".it[3].itg[0].iti[6000].ipt" -type "pointArray" 12 0.3155025605950787
		 0.0021198742756428079 0 1 0.13767738806826799 0.25593201143199851 0 1 0.13767738806826799
		 0.0021198742756428079 0 1 -0.037797636662294826 0.0021198742756428079 0 1 -0.037797636662294826
		 0.55361280914000111 0 1 0.13767738806826799 0.55361280914000111 0 1 0.13767738806826799
		 0.32212707607254881 0 1 0.30649404321211132 0.55361280914000111 0 1 0.4960695722237663
		 0.55361280914000111 0 1 0.2841680216332742 0.29549245019880072 0 1 0.51408698950174858
		 0.0021198742756428079 0 1 0.3155025605950787 0.0021198742756428079 0 1 ;
	setAttr ".it[3].itg[0].iti[6000].ict" -type "componentList" 1 "cv[0:11]";
	setAttr ".mlid" 0;
	setAttr ".mlpr" 0;
	setAttr ".pndr[0]"  0;
	setAttr ".tgvs[0]" yes;
	setAttr ".tpvs[0]" yes;
	setAttr ".tgdt[0].cid" -type "Int32Array" 1 0 ;
	setAttr ".aal" -type "attributeAlias" 2 "fk" "weight[0]" ;
select -ne :time1;
	setAttr ".o" 1;
	setAttr ".unw" 1;
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
connectAttr "ik_fk_blendShape.og[0]" "ik_ctrlShape.cr";
connectAttr "ik_fk_blendShape.og[1]" "ik_ctrlShape1.cr";
connectAttr "ik_fk_blendShape.og[2]" "ik_ctrlShape2.cr";
connectAttr "ik_fk_blendShape.og[3]" "ik_ctrlShape3.cr";
connectAttr "ik_ctrlShapeOrig.ws" "ik_fk_blendShape.ip[0].ig";
connectAttr "ik_ctrlShape1Orig.ws" "ik_fk_blendShape.ip[1].ig";
connectAttr "ik_ctrlShape2Orig.ws" "ik_fk_blendShape.ip[2].ig";
connectAttr "ik_ctrlShape3Orig.ws" "ik_fk_blendShape.ip[3].ig";
connectAttr "ik_ctrlShapeOrig.l" "ik_fk_blendShape.orggeom[0]";
connectAttr "ik_ctrlShape1Orig.l" "ik_fk_blendShape.orggeom[1]";
connectAttr "ik_ctrlShape2Orig.l" "ik_fk_blendShape.orggeom[2]";
connectAttr "ik_ctrlShape3Orig.l" "ik_fk_blendShape.orggeom[3]";
// End of ik.ma
