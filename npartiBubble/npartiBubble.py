
import maya.cmds as mc
import random
import maya.mel as mel

def buildnBubbles(particleDict, folderName, doesBubblePop, minScale, maxScale, charUp, clothObjs):
	print(doesBubblePop)
	allParticleDictionary = particleDict
	inc=0
	minFrames = mc.playbackOptions( q=True, min=True)
	maxFrames = mc.playbackOptions( q=True, max=True)
	allBubblesGrp = mc.group(em=True, n=(folderName + '_'+ str("%04d"%inc)))

	for curveParticleId in allParticleDictionary.keys():
		allParticleDictionary = particleDict
		pointList = []

		sortedKeyFrameList = sorted(allParticleDictionary[curveParticleId].keys())
		if len(sortedKeyFrameList) > 1:

			for keyFrame in sortedKeyFrameList:
				pointList.append(allParticleDictionary[curveParticleId][keyFrame])
			pad = str(len(str(len(pointList))))
			grpFolder = mc.group(em=True, n="nbubbleGrp_" + charUp + '_' + str("%0" + pad + "d")%inc)
			#curveName = "partiCurve" + charUp + '_' + str(curveParticleId)
			curveObj = mc.curve(name = 'curveName_' + charUp + '_' + str("%0" + pad + "d")%inc, p = pointList)
			locObj = mc.spaceLocator(name="bubLocator_" + charUp + '_' + str("%0" + pad + "d")%inc)
			mc.pathAnimation(locObj, stu=sortedKeyFrameList[0], etu=sortedKeyFrameList[-1] ,c=curveObj,n=("moPath_" + charUp + '_' + str("%0" + pad + "d")%inc))
			#For every locator created, make a bubble and attach that to the locator in worldspace and parent in underneath
			makeBubble = mc.polyCube(name="bubble_" + charUp + '_' + str("%0" + pad + "d")%inc, w=.1, h=.1, d=.1, sx=8, sy=8, sz=8)
			mc.sculpt(makeBubble, maxDisplacement=.1)
			mc.delete(makeBubble, ch=True)
			getPos = mc.xform(locObj, ws=True, q=True, translation=True)
			mc.xform(makeBubble[0], t=(getPos[0], getPos[1], getPos[2]))
			mc.parent(makeBubble[0], locObj)
			randBubbleSize = random.uniform(minScale, maxScale)#This is what will give our bubbles the random size
			mc.scale(randBubbleSize, randBubbleSize, randBubbleSize, makeBubble[0])
			#Create nCloth for each bubble and set the collide strength to turn on when the bubble moves, never before.
			mc.select(makeBubble[0])
			mc.nClothCreate()
			bubbleNClothName = mc.rename("nCloth1", "nClothBub_" + charUp + '_' + str("%0" + pad + "d")%inc)
			#
			mc.setKeyframe(bubbleNClothName, attribute='collideStrength', t=[sortedKeyFrameList[0], sortedKeyFrameList[-1]])
			mc.setAttr(bubbleNClothName + ".collideStrength", 0)
			mc.setKeyframe(bubbleNClothName, attribute='collideStrength', t=[sortedKeyFrameList[0]-1, sortedKeyFrameList[-1]+1])
			#Rigidity helps to matain some of the bubble volume
			mc.setKeyframe(bubbleNClothName, attribute='rigidity', t=[sortedKeyFrameList[0], sortedKeyFrameList[-1]+10])
			mc.setAttr(bubbleNClothName + ".rigidity", .1)
			mc.setKeyframe(bubbleNClothName, attribute='rigidity', t=[sortedKeyFrameList[0]+10, sortedKeyFrameList[-1]])
			#70% strength to follow the locator and then reduced to 30% after 10 frames
			mc.setAttr(bubbleNClothName + ".inputMeshAttract", .7)
			mc.setKeyframe(bubbleNClothName, attribute='inputMeshAttract', t=[sortedKeyFrameList[0], sortedKeyFrameList[-1]+10])
			mc.setAttr(bubbleNClothName + ".inputMeshAttract", .3)
			mc.setKeyframe(bubbleNClothName, attribute='inputMeshAttract', t=[sortedKeyFrameList[0]+10, sortedKeyFrameList[-1]])
			#For performance this sets the nCLoth on/off during it's lifespan
			mc.setAttr(bubbleNClothName + ".isDynamic", 0)
			mc.setKeyframe(bubbleNClothName, attribute='isDynamic', t=[sortedKeyFrameList[0]-1])
			mc.setAttr(bubbleNClothName + ".isDynamic", 1)
			mc.setKeyframe(bubbleNClothName, attribute='isDynamic', t=[sortedKeyFrameList[0], sortedKeyFrameList[-1]])
			mc.setAttr(bubbleNClothName + ".isDynamic", 0)
			mc.setKeyframe(bubbleNClothName, attribute='isDynamic', t=[sortedKeyFrameList[-1]+1])

			mc.setAttr(bubbleNClothName + ".stretchResistance", 20)
			mc.setAttr(bubbleNClothName + ".compressionResistance", 80)
			mc.setAttr(bubbleNClothName + ".selfCollisionFlag", 4)
			mc.setAttr(bubbleNClothName + ".trappedCheck", 1)
			mc.setAttr(bubbleNClothName + ".pressure", 3)
			mc.setAttr(bubbleNClothName + ".pointMass", .4)
			mc.setAttr(bubbleNClothName + ".isDynamic", 0)#This is turned on later but if left on causes the setup time to run slow.

			exprShpName = mc.pickWalk(bubbleNClothName, d="down")
			#set the visibiliy of the LOCATORS on when it's moving and off when it has stopped
			setOn = mc.setKeyframe(locObj[0], attribute='visibility', t=[sortedKeyFrameList[0], sortedKeyFrameList[-1]])
			mc.setAttr(locObj[0] + ".visibility", 0)
			setOff = mc.setKeyframe( locObj[0], attribute='visibility', t=[sortedKeyFrameList[0]-1, sortedKeyFrameList[-1]+1])

			######################### BUBBLE POP TIME #############################################
			if mc.checkBox("bubblePop", q=True, v=1) == True:
				#pop the bubble - there are 152 verts in the bubble. Pick a random number in that and go up and down from that number by 35 to get random selections
				getRandNum = random.randint(34,300) #this is 35 above 0 and 35 below 151 so that we don't reach higher
				randVertValHi = getRandNum + 35
				randVertValLo = getRandNum - 35
				mc.select(makeBubble[0] + ".vtx[" + str(randVertValLo) + ":" + str(randVertValHi) + "]")
				makeTearableCon = mel.eval('createNConstraint tearableSurface false;')
				#changes the transform and shape names, the order is specific
				consTransform = mc.listRelatives(str(makeTearableCon[0]),p=True)
				makeTearable = mc.rename(makeTearableCon, 'dynConsShape_'+ str("%0" + pad + "d")%inc)
				makeTearable = mc.rename(consTransform, 'dynConstrain_'+ charUp + '_' + str("%0" + pad + "d")%inc)
				#Increase pressure before the tear happens
				mc.setKeyframe(bubbleNClothName, attribute='pres', t=[sortedKeyFrameList[-1]-3])
				mc.setAttr(bubbleNClothName + ".pres", 10)
				mc.setKeyframe(bubbleNClothName, attribute='pres', t=[sortedKeyFrameList[-1]-2])
				#Tear it apart 10frames before it ends its run
				mc.setKeyframe(makeTearable, attribute='gls', t=[sortedKeyFrameList[-1]-2])
				mc.setAttr(makeTearable + ".glueStrength", 0)
				mc.setKeyframe(makeTearable, attribute='gls', t=[sortedKeyFrameList[-1]-1])
				#Turn off the constratint when the bubble disappears
				mc.setAttr(makeTearable + ".enable", 0)
				mc.setKeyframe(makeTearable, attribute='enable', t=[sortedKeyFrameList[0]-1])
				mc.setAttr(makeTearable + ".enable", 1)
				mc.setKeyframe(makeTearable, attribute='enable', t=[sortedKeyFrameList[0], sortedKeyFrameList[-1]])
				mc.setAttr(makeTearable + ".enable", 0)
				mc.setKeyframe(makeTearable, attribute='enable', t=[sortedKeyFrameList[-1]+1])
				mc.setAttr(makeTearable + '.visibility', 0)
				mc.parent(makeTearable, grpFolder)
			elif mc.checkBox("bubblePop", q=True, v=1) == False:
				print('bubble popping disabled')
			#######################################################################
			#place the newly created objects into nCloth_Objs folder
			inc += 1
			#Collect all the dynamics
			clothObjs.append(mc.listRelatives(bubbleNClothName, s=True)[0])
			mc.parent(locObj,curveObj, bubbleNClothName, grpFolder)
			mc.parent(grpFolder, allBubblesGrp)
			mc.setAttr(curveObj + '.visibility', 0)


	mc.currentTime(1)
	print('cloth objs variable {}'.format(clothObjs))
	return clothObjs
