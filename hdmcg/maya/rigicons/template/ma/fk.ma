//Maya ASCII 2026 scene
//Name: fk.ma
//Last modified: Sun, Jun 21, 2026 04:11:45 PM
//Codeset: 1252
requires maya "2026";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2026";
fileInfo "version" "2026";
fileInfo "cutIdentifier" "202510291147-60ec9eda33";
fileInfo "osv" "Windows 10 Home v2009 (Build: 19045)";
fileInfo "UUID" "E7659AEB-404D-B107-982C-67B9FB58FD16";
fileInfo "license" "education";
createNode transform -n "fk_ctrl";
	rename -uid "980916A7-40FD-BBD2-A7B6-1D9BA7663FD5";
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0 0.48230001 1 ;
createNode nurbsCurve -n "fk_ctrlShape" -p "fk_ctrl";
	rename -uid "8B8B53F7-486E-72AF-7F23-8591A4E290EF";
	setAttr -k off ".v";
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 1 0 0.018911498 ;
	setAttr ".tw" yes;
createNode nurbsCurve -n "fk_ctrlShape1" -p "fk_ctrl";
	rename -uid "6CE5DBA3-4E35-66ED-EF1E-17BA39AAD54C";
	setAttr -k off ".v";
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 1 0 0.018911498 ;
	setAttr ".tw" yes;
createNode nurbsCurve -n "fk_ctrlShape2" -p "fk_ctrl";
	rename -uid "F86DB478-4F71-6AA1-E4A6-BAAA91E3E418";
	setAttr -k off ".v";
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 1 0 0.018911498 ;
	setAttr ".tw" yes;
createNode nurbsCurve -n "fk_ctrlShape3" -p "fk_ctrl";
	rename -uid "DA822EF9-406A-E58B-205B-94BEB879982A";
	setAttr -k off ".v";
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 1 0 0.018911498 ;
	setAttr ".tw" yes;
createNode nurbsCurve -n "fk_ctrlShapeOrig" -p "fk_ctrl";
	rename -uid "E2A497B4-441F-DDF0-9F5C-61B8C1B7D42C";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 2.2000000000000002 2.8999999999999999 5.0999999999999996 5.7999999999999998
		
		5
		0.02125766457454176 0.28013598530825762 0
		0.02125766457454176 0.27992759454363686 0
		0.0211913584219823 0.27992759454363686 0
		0.0211913584219823 0.28013598530825762 0
		0.02125766457454176 0.28013598530825762 0
		;
createNode nurbsCurve -n "fk_ctrlShape1Orig" -p "fk_ctrl";
	rename -uid "FA0D28FC-4FD7-E4FB-DC2F-02985480503A";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".cc" -type "nurbsCurve" 
		1 11 0 no 3
		12 0 1.23627251439 2.2487727051199999 2.9487727051200001 5.1487727051199998
		 5.84877270512 6.7722090368499996 7.9151238344000001 8.6713731668200005 10.0035915986
		 11.4904891913 12.2826765721
		12
		0.021019968847191744 0.28013598530825762 0
		0.021087163041653215 0.28004007817768073 0
		0.021087163041653215 0.28013598530825762 0
		0.02115346919025006 0.28013598530825762 0
		0.02115346919025006 0.27992759454363686 0
		0.021087163041653215 0.27992759454363686 0
		0.021087163041653215 0.28001506527416331 0
		0.021023372864501542 0.27992759454363686 0
		0.020951738603184149 0.27992759454363686 0
		0.021031809121897831 0.28002512960771947 0
		0.020944930421947786 0.28013598530825762 0
		0.021019968847191744 0.28013598530825762 0
		;
createNode nurbsCurve -n "fk_ctrlShape2Orig" -p "fk_ctrl";
	rename -uid "8E396066-4092-9448-A99B-93969DDB57E5";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".cc" -type "nurbsCurve" 
		1 10 0 no 3
		11 0 0.5 1.43750057221 1.83750057221 2.77500114443 3.6750011444299999 4.3750011444299997
		 6.5750011444299998 8.2515648126999999 8.6515648127000002 9.6281284809599992
		11
		-0.30995350168030622 0.17574071898556762 0
		-0.30995350168030622 0.050483786892239119 0
		-0.075096610663155414 0.050483786892239119 0
		-0.075096610663155414 -0.049721758780838621 0
		-0.30995350168030622 -0.049721758780838621 0
		-0.30995350168030622 -0.27518423654328222 0
		-0.4853132066093811 -0.27518423654328222 0
		-0.4853132066093811 0.27594626465864536 0
		-0.065310763520688986 0.27594626465864536 0
		-0.065310763520688986 0.17574071898556762 0
		-0.30995350168030622 0.17574071898556762 0
		;
createNode nurbsCurve -n "fk_ctrlShape3Orig" -p "fk_ctrl";
	rename -uid "0A4EB8FE-4FB0-12A3-FABB-62B56802621A";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".cc" -type "nurbsCurve" 
		1 11 0 no 3
		12 0 1.23627251439 2.2487727051199999 2.9487727051200001 5.1487727051199998
		 5.84877270512 6.7722090368499996 7.9151238344000001 8.6713731668200005 10.0035915986
		 11.4904891913 12.2826765721
		12
		0.34373114851015907 -0.27518423654328222 0
		0.16602284026879435 -0.0215389012743646 0
		0.16602284026879435 -0.27518423654328222 0
		-0.0093368646611126354 -0.27518423654328222 0
		-0.0093368646611126354 0.27594626465864536 0
		0.16602284026879435 0.27594626465864536 0
		0.16602284026879435 0.044612660869162026 0
		0.33472855140125496 0.27594626465864536 0
		0.52417949395315799 0.27594626465864536 0
		0.31241720218224212 0.01799553890976226 0
		0.54218507042940634 -0.27518423654328222 0
		0.34373114851015907 -0.27518423654328222 0
		;
createNode blendShape -n "fk_ik_blendShaoe";
	rename -uid "0073E0C8-4B7C-5219-8E4C-E780DF40C5A3";
	addAttr -ci true -h true -sn "aal" -ln "attributeAliasList" -dt "attributeAlias";
	setAttr -s 4 ".ip";
	setAttr -s 4 ".og";
	setAttr -s 4 ".orggeom";
	setAttr ".w[0]"  0;
	setAttr -s 4 ".it";
	setAttr ".it[0].itg[0].iti[6000].ipt" -type "pointArray" 5 -0.41640049135228097
		 -0.55750245403962073 0 1 -0.41640049135228097 -0.0025645575976103174 0 1 -0.23982934248435059
		 -0.0025645575976103174 0 1 -0.23982934248435059 -0.55750245403962073 0 1 -0.41640049135228097
		 -0.55750245403962073 0 1 ;
	setAttr ".it[0].itg[0].iti[6000].ict" -type "componentList" 1 "cv[0:4]";
	setAttr ".it[1].itg[0].iti[6000].ipt" -type "pointArray" 12 0.21657558286008441
		 -0.55750245403962073 0 1 0.037639605733286424 -0.30210485131527071 0 1 0.037639605733286424
		 -0.55750245403962073 0 1 -0.1389315431306814 -0.55750245403962073 0 1 -0.1389315431306814
		 -0.0025645575976103174 0 1 0.037639605733286424 -0.0025645575976103174 0 1 0.037639605733286424
		 -0.23549629188486954 0 1 0.20751079277705647 -0.0025645575976103174 0 1 0.39827052628044091
		 -0.0025645575976103174 0 1 0.18504530923635845 -0.26229729389200823 0 1 0.41640049135117146
		 -0.55750245403962073 0 1 0.21657558286008441 -0.55750245403962073 0 1 ;
	setAttr ".it[1].itg[0].iti[6000].ict" -type "componentList" 1 "cv[0:11]";
	setAttr ".it[2].itg[0].iti[6000].ipt" -type "pointArray" 11 0.3386119647705913
		 -0.45334136643735445 0 1 0.3386119647705913 -0.32800206305716395 0 1 0.10360062749745273
		 -0.32800206305716395 0 1 0.10360062749745273 -0.22773062035451735 0 1 0.3386119647705913
		 -0.22773062035451735 0 1 0.3386119647705913 -0.0021198742756428079 0 1 0.51408698950428466
		 -0.0021198742756428079 0 1 0.51408698950428466 -0.55361280914000111 0 1 0.093808345000373147
		 -0.55361280914000111 0 1 0.093808345000373147 -0.45334136643735445 0 1 0.3386119647705913
		 -0.45334136643735445 0 1 ;
	setAttr ".it[2].itg[0].iti[6000].ict" -type "componentList" 1 "cv[0:10]";
	setAttr ".it[3].itg[0].iti[6000].ipt" -type "pointArray" 12 -0.3155025605950787
		 -0.0021198742756428079 0 1 -0.13767738806826799 -0.25593201143199851 0 1 -0.13767738806826799
		 -0.0021198742756428079 0 1 0.037797636662294826 -0.0021198742756428079 0 1 0.037797636662294826
		 -0.55361280914000111 0 1 -0.13767738806826799 -0.55361280914000111 0 1 -0.13767738806826799
		 -0.32212707607254881 0 1 -0.30649404321211132 -0.55361280914000111 0 1 -0.4960695722237663
		 -0.55361280914000111 0 1 -0.2841680216332742 -0.29549245019880072 0 1 -0.51408698950174858
		 -0.0021198742756428079 0 1 -0.3155025605950787 -0.0021198742756428079 0 1 ;
	setAttr ".it[3].itg[0].iti[6000].ict" -type "componentList" 1 "cv[0:11]";
	setAttr ".mlid" 1;
	setAttr ".mlpr" 0;
	setAttr ".pndr[0]"  0;
	setAttr ".tgvs[0]" yes;
	setAttr ".tpvs[0]" yes;
	setAttr ".tgdt[0].cid" -type "Int32Array" 1 0 ;
	setAttr ".aal" -type "attributeAlias" 2 "ik" "weight[0]" ;
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
connectAttr "fk_ik_blendShaoe.og[0]" "fk_ctrlShape.cr";
connectAttr "fk_ik_blendShaoe.og[1]" "fk_ctrlShape1.cr";
connectAttr "fk_ik_blendShaoe.og[2]" "fk_ctrlShape2.cr";
connectAttr "fk_ik_blendShaoe.og[3]" "fk_ctrlShape3.cr";
connectAttr "fk_ctrlShapeOrig.ws" "fk_ik_blendShaoe.ip[0].ig";
connectAttr "fk_ctrlShape1Orig.ws" "fk_ik_blendShaoe.ip[1].ig";
connectAttr "fk_ctrlShape2Orig.ws" "fk_ik_blendShaoe.ip[2].ig";
connectAttr "fk_ctrlShape3Orig.ws" "fk_ik_blendShaoe.ip[3].ig";
connectAttr "fk_ctrlShapeOrig.l" "fk_ik_blendShaoe.orggeom[0]";
connectAttr "fk_ctrlShape1Orig.l" "fk_ik_blendShaoe.orggeom[1]";
connectAttr "fk_ctrlShape2Orig.l" "fk_ik_blendShaoe.orggeom[2]";
connectAttr "fk_ctrlShape3Orig.l" "fk_ik_blendShaoe.orggeom[3]";
// End of fk.ma
