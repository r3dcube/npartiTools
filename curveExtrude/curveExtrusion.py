import maya.cmds as mc
import copy
import itertools
import maya.mel as mel

#-----Create the dictionary to hold all the elements

allTheCurves = []
curveBit = ''
sortedList = []
curveAttachList = []
curveItemsNew = []
SDK_Driver = ''
fldCnt = 0
amount = 0

#------------------------------------------------------------------------------------------------
# 										S O R T  C U R V E S
#------------------------------------------------------------------------------------------------
def sortedCurveList():

	global sortedList
	global curveBit

	curveDet = int(mc.textField('curveDetail', q=True, text=True)) #Query the textfield to get the users curve segments
	mc.rebuildCurve(curveBit, ch=False, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=curveDet, d=1)
	mc.select(curveBit + ".ep[0:" + str(curveDet) + "]")
	getEditPnts = mc.ls(sl=True)
	allTheCurves = mc.detachCurve(getEditPnts, ch=0, cos=1, rpo=1)
	mc.delete(allTheCurves[-2:])
	allTheCurves = allTheCurves[:-2]
	cvPosDict = {}
	for item in allTheCurves:
		cvPosDict[item] = {}
		cvPosDict[item]['cv0'] = mc.xform(item + '.cv[0]', ws=True, q=True, translation=True)
		cvPosDict[item]['cv1'] = mc.xform(item + '.cv[1]', ws=True, q=True, translation=True)

	cvPosSortedDict = copy.deepcopy(cvPosDict)
	key = allTheCurves[0]
	sortedList = [key]
	while key in cvPosSortedDict:
		cv0 = cvPosSortedDict[key]["cv0"]
		cv1 = cvPosSortedDict[key]["cv1"]
		originalKey = key
		for cv0key, cvs in cvPosSortedDict.iteritems():
			if cv1 == cvs["cv0"] or cv0 == cvs["cv1"]:
				sortedList.append(cv0key)
				key = cv0key
				break
		if originalKey == key:
			break
		del cvPosSortedDict[originalKey]
	mc.delete(sortedList, ch=True)
	mc.select(sortedList[0])
	mc.rename("curve_0")
	sortedList.pop(0)
	sortedList.insert(0, "curve_0")
	print 'made it to end'

#------------------------------------------------------------------------------------------------
# 									B U I L D  T E M P  C U R V E S
#------------------------------------------------------------------------------------------------
def bulidingCurve():

	global sortedList
	global curveAttachList
	global fldCnt
	blndShpCrvList = []
	garbageCollect = []
	curveAttachList = []
	cnt = 0
	for i, bits in enumerate(sortedList):
		blndShpCrvList.append(bits)
		cnt+= 1
		if bits == sortedList[0]:
			curveAttach = mc.duplicate(blndShpCrvList, n= str(fldCnt) + ("crvBlndShp_" + str(i+1)))
			curveAttachList.append(curveAttach)
		else:
			curveAttach = mc.attachCurve(blndShpCrvList, ch=False, rpo=False, kmk = 1, m = 0, n= str(fldCnt) + "crvBlndShp_" + str(i), bb = 0.5, bki = 0, p=0.1)
			curveAttachList.append(curveAttach)

#------------------------------------------------------------------------------------------------
# 							 	B U I L D  B L E N D S H A P E  C U R V E S
#------------------------------------------------------------------------------------------------

def buildCurveSegments():

	#global sortedList
	global curveAttachList

	#-----clean up all the curves so they have the same CV count
	cvSpans = mc.getAttr(curveAttachList[-1][0] + ".spans")
	for tmpCrvs in curveAttachList:#--rebuild the curves with the same CV count this is the only way blending curves will work
		mc.rebuildCurve(tmpCrvs, ch=False, rpo=True, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=cvSpans, d=1, tol=0.01)

#------------------------------------------------------------------------------------------------
# 							 B U I L D  F I R S T  B L E N D S H A P E  C U R V E
#------------------------------------------------------------------------------------------------

def baseCrveCreation():

	global curveAttachList
	#move all the cv's in the duplicated curve back to the first cv
	dupFirstCrv = mc.duplicate(curveAttachList[0], name='crvBlndShp_1')	#duplicate curve to make the starting curve with zero length
	getFirstCV = mc.xform(str(dupFirstCrv[0]) + '.cv[0]', q=True, ws=True, t=True) #query the first vert position to move the others to
	CrvCVSpans = mc.getAttr((str(curveAttachList[0][0]) + ".spans"))
	for i in range(CrvCVSpans+2):
		mc.xform(str(dupFirstCrv[0]) + '.cv['+ str(i) + ']', t=getFirstCV)
	curveAttachList.insert(0,dupFirstCrv)

def blndShpSetup():

	global curveAttachList
	global curveItemsNew
	curveAttachItems = list(itertools.chain.from_iterable(curveAttachList))
	aCnt = 1
	curveItemsNew = curveAttachItems
	for crvBlnd in curveItemsNew:
		if crvBlnd == curveItemsNew[-1]:
			break
		else:
			mc.blendShape(curveItemsNew[aCnt],crvBlnd)
			aCnt+=1

def curveAttrSetup():

	global allBlndShpList
	global SDK_Driver
	#----Create an attribute for the first curve DRIVE to hold the slider for the set driven key
	mc.addAttr(curveItemsNew[0], ln="DRIVE", at="double", min=0, max=10, dv=0)
	mc.setAttr(curveItemsNew[0] + ".DRIVE", e=True, k=True)
	#-----get all the blendshapes
	allBlndShpList = []
	for crvBlndShp in curveItemsNew:
		getBlndShpObj = mc.ls(crvBlndShp, dag=True, s=True)
		findBlndShp = mc.listConnections(getBlndShpObj, t='blendShape')
		allBlndShpList.append(findBlndShp[0])
	SDK_Driver = (curveItemsNew[0] + ".DRIVE")


def assignBlndShpToCurveAttr():

	global SDK_Driver
	cntDwn = 0
	for val in range(len(curveItemsNew)): #val prints 0-199
		if curveItemsNew[1 + val] == curveItemsNew[-1]:
			mc.setAttr(allBlndShpList[val] + "." + curveItemsNew[1 + val], 0)
			mc.setDrivenKeyframe(allBlndShpList[val] + "." + curveItemsNew[1 + val], cd = SDK_Driver)
			mc.setAttr(SDK_Driver, cntDwn)
			mc.setAttr(allBlndShpList[val] + "." + curveItemsNew[1 + val], 1)
			mc.setDrivenKeyframe(allBlndShpList[val] + "." + curveItemsNew[1 + val], cd = SDK_Driver)
			cntDwn += (float(10)/float(len(curveItemsNew)))
			break
		else:
			mc.setAttr(allBlndShpList[val] + "." + curveItemsNew[1 + val], 0)
			mc.setDrivenKeyframe(allBlndShpList[val] + "." + curveItemsNew[1 + val], cd = SDK_Driver)
			mc.setAttr(SDK_Driver, cntDwn)
			cntDwn += (float(10)/float(len(curveItemsNew)))
			mc.setAttr(SDK_Driver, cntDwn)
			mc.setAttr(allBlndShpList[val] + "." + curveItemsNew[1 + val], 1)
			mc.setDrivenKeyframe(allBlndShpList[val] + "." + curveItemsNew[1 + val], cd = SDK_Driver)

def cleanupDeleteGarbage():
	global fldCnt
	grpFolder = mc.group(em=True, n="blendShapeCurves_" + str(fldCnt))
	mc.setAttr(grpFolder + ".visibility", 0)
	curveFolder = mc.group(em=True, n="curveFolder_" + str(fldCnt))
	mc.delete(sortedList)
	mc.parent(curveItemsNew[1::], grpFolder)
	mc.parent(grpFolder, curveAttachList[0], curveFolder)
	for crv in curveAttachList:
		mc.rename(crv, "crvChild_" + str(fldCnt))
	fldCnt = fldCnt+1

def CreateACurve():
	global curveBit
	global amount

	getCurves = mc.ls(sl=True, tr=True)#progress bar updates too much and is slowing everything down
	for curveBit in getCurves:
		mc.progressBar('progBar', e=True, pr=amount, st='working')
		sortedCurveList()
		amount+=12.5
		mc.progressBar('progBar', e=True, pr=amount, st='working')
		bulidingCurve()
		amount+=12.5
		mc.progressBar('progBar', e=True, pr=amount, st='working')
		buildCurveSegments()
		amount+=12.5
		mc.progressBar('progBar', e=True, pr=amount, st='working')
		baseCrveCreation()
		amount+=12.5
		mc.progressBar('progBar', e=True, pr=amount, st='working')
		blndShpSetup()
		amount+=12.5
		mc.progressBar('progBar', e=True, pr=amount, st='working')
		curveAttrSetup()
		amount+=12.5
		mc.progressBar('progBar', e=True, pr=amount, st='working')
		assignBlndShpToCurveAttr()
		amount+=12.5
		mc.progressBar('progBar', e=True, pr=amount, st='working')
		cleanupDeleteGarbage()
		amount+=12.5
		mc.progressBar('progBar', e=True, pr=amount, st='working')
		amount =  0
		mc.progressBar('progBar', e=True, pr=amount, st='working')
