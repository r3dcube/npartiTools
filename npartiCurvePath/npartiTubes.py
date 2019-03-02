import maya.cmds as mc
import random
import math
import copy

def buildTubes(particleDict, tubeDiv, tubeRad, bendDet, extruOffset, folderName, animExtrusion, randOffset, aniVis, charUp, curveCNTRL, tubeDetail):
	allParticleDictionary = particleDict
	inc=0
	visibileGeo = []
	grbgCollect = []
	allTubesGrp = mc.group(em=True, n=(folderName + '_'+ str("%04d"%inc))) #Create a folder for the nParticles currently being processed
	anno = mc.annotate(str(curveCNTRL[0]), tx='CONTROL' + '_'+ str("%04d"%inc))
	mc.setAttr(anno + '.displayArrow', 0 )
	mc.setAttr(anno + '.overrideDisplayType', 2)
	annoTran = mc.listRelatives(anno,p=True)
	mc.parent(annoTran ,str(curveCNTRL[0]))
	mc.parent(str(curveCNTRL[0]), allTubesGrp)

	if randOffset >= extruOffset:
		print('You cannot have a random offset {} greater then the extrusion values {} random offset has been set to zero'.format(randOffset, extruOffset))
		randOffset = 0

	for curveParticleId in allParticleDictionary.keys():
		pointList = []
		sortedKeyFrameList = sorted(allParticleDictionary[curveParticleId].keys())
		if len(sortedKeyFrameList) > 1:

			for keyFrame in sortedKeyFrameList:
				pointList.append(allParticleDictionary[curveParticleId][keyFrame])
			#Start tube creation and attributes
			pad = str(len(str(len(pointList)))) #Adds dynamic padding by finding the total digits in a number
			tubeGrp = mc.group(em=True, n="tubeGrp_"  + charUp + '_' + str("%0" + pad + "d")%inc)
			curveObj = mc.curve(name = "npartiCurve_"  + charUp + '_' + str("%0" + pad + "d")%inc, p = pointList)
			mc.parentConstraint(str(curveCNTRL[0]), curveObj, mo=True, n="nConstraint_"  + charUp + '_' + str("%0" + pad + "d")%inc,w=1.0)#Constrain the curves to the world curve for placement
			mc.setAttr(curveObj + '.visibility',0) #Hide the curve
			rndDwnCurveLength = math.trunc(mc.arclen(curveObj))

			if rndDwnCurveLength <= 1: #check to see if the curve has at least 3 segments.
				print "This error has occured because the particle animation hasn't finished in the timeline make sure the birth of particles isn't near the end of the timeline" #This is why it's a good idea to animate the emitter to 0 several frames before the animation ends. Otherwise you emit a particle and there are less then 2 spans in the curve at the end.
			else:


				newCylinder = mc.polyCylinder(name="tubePoly_"  + charUp + '_' + str("%0" + pad + "d")%inc, ch=True, r=tubeRad, ax=[0,0,90], sh=(rndDwnCurveLength*2 + tubeDiv), h=rndDwnCurveLength, sx=tubeDetail) #original code that queries the av
				newCylBlendShp_A = mc.polyCylinder(name="tubeBlendShpA_0"  + charUp + '_' + str("%0" + pad + "d")%inc, ch=True, r=tubeRad, ax=[0,0,90], sh=(rndDwnCurveLength*2 + tubeDiv), h=rndDwnCurveLength, sx=tubeDetail)
				getBndBoxDim = mc.xform(newCylBlendShp_A[0], q=True, ws=True, bb=True)
				mc.xform(newCylBlendShp_A, p=True, sp=[0,0, getBndBoxDim[2]], rp=[0,0, getBndBoxDim[2]])
				newCylBlendShp_B = mc.polyCylinder(name="tubeBlendShpB_0"  + charUp + '_' + str("%0" + pad + "d")%inc, ch=True, r=tubeRad, ax=[0,0,90], sh=(rndDwnCurveLength*2 + tubeDiv), h=rndDwnCurveLength, sx=tubeDetail)

				mc.xform(newCylBlendShp_B, p=True, sp=[0,0, getBndBoxDim[5]], rp=[0,0, getBndBoxDim[5]])
				mc.scale(1,1,.001, newCylBlendShp_A, r=True)
				mc.makeIdentity(newCylBlendShp_A,a=True, s=True)
				mc.scale(1,1,.001, newCylBlendShp_B, r=True)
				mc.makeIdentity(newCylBlendShp_B,a=True, s=True)

				theBlndShp = mc.blendShape(newCylBlendShp_A[0], newCylBlendShp_B[0], newCylinder[0])
				moPathVar =  mc.pathAnimation(newCylinder, fa="Z", fm=True, f=True, ua="y", wut = "vector", su=0.5, eu=0.5, stu=(mc.playbackOptions(q=True, minTime=True)), etu=(mc.playbackOptions(q=True, maxTime=True)) ,c=curveObj)

				mc.cutKey(moPathVar, at="uValue", cl=True)
				mc.setAttr(moPathVar + ".uValue", 0.5)

				if 133 < rndDwnCurveLength < 400:
					#the divisions in dv can't go over 400 without an erro, force it's hand if it tries to add too many divisions.
					theFlow = mc.flow(newCylinder[0], oc =False, lc=True, dv=(2,2,rndDwnCurveLength*3 + bendDet), ld=(2,2,2))
				else:
					#Force the flow deformer divisions to 400 since this is a hard limit
					theFlow = mc.flow(newCylinder[0], oc =False, lc=True, dv=(2,2,400), ld=(2,2,2))

				mc.setAttr(theFlow[2] + ".visibility", 0)
				lattice = mc.rename(theFlow[2], 'lattice_' + charUp + '_' + str("%0" + pad + "d")%inc)
				latticebase = mc.rename(theFlow[3], 'latBase_' + charUp + '_' + str("%0" + pad + "d")%inc)

				mc.setAttr(theFlow[0] + '.latticeOnObject', 1)
				#randVal sets the random offset to the tail extrusion
				randVal = random.randint(-abs(randOffset),abs(randOffset))

				mc.setKeyframe(theBlndShp[0] + ".w[0]", v=1, t=[sortedKeyFrameList[0], sortedKeyFrameList[0]])
				mc.setKeyframe(theBlndShp[0] + ".w[0]", v=0, t=[sortedKeyFrameList[-1], sortedKeyFrameList[-1]])

				if mc.checkBox("extAnim", q=True, v=1) == True:
					mc.setKeyframe(theBlndShp[0] + ".w[1]", v=0, t=[(sortedKeyFrameList[0]+ extruOffset), (sortedKeyFrameList[0]+ extruOffset)])
					mc.setKeyframe(theBlndShp[0] + ".w[1]", v=1, t=[(sortedKeyFrameList[-1]+ (extruOffset + randVal)), (sortedKeyFrameList[-1]+ (extruOffset + randVal))])

				mc.setKeyframe(newCylinder[0] + ".v", v=0, t=[sortedKeyFrameList[0]-1, sortedKeyFrameList[0]-1])
				mc.setKeyframe(newCylinder[0] + ".v", v=1, t=[sortedKeyFrameList[0], sortedKeyFrameList[0]])

				if mc.checkBox("aniVis", q=True, v=1) == True:
					mc.setKeyframe(newCylinder[0] + ".v", v=1, t=[sortedKeyFrameList[-1]+ extruOffset, sortedKeyFrameList[-1]+ extruOffset])
					mc.setKeyframe(newCylinder[0] + ".v", v=0, t=[sortedKeyFrameList[-1]+ extruOffset +1, sortedKeyFrameList[-1]+ extruOffset + 1])

				#mc.polyNormalPerVertex(newCylinder, ufn=True) #unlock the normals to clean up the look of the geo
				inc += 1
				mc.parent(newCylinder[0], newCylBlendShp_A[0], newCylBlendShp_B[0], lattice, latticebase, curveObj, tubeGrp)
				mc.parent(tubeGrp, allTubesGrp)
				#Cleanup the mess, left over blendshapes and history
				mc.delete(newCylBlendShp_A, newCylBlendShp_B)
				getHistAttr = mc.listHistory(newCylinder,il=1, pdo=True, gl=True) #capture the pCylinder history and remove it for optimization
				mc.delete(getHistAttr[3]) #delete
				#visibileGeo.extend((newCylinder[0]))#return the visible objects to clean up the normals

	startFrame = mc.playbackOptions( q=True, min=True)
	mc.currentTime(startFrame, update=True, edit=True)
	print('There are {} particles in the dictionary'.format(len(pointList)))
	#return visibileGeo
