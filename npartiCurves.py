import maya.cmds as mc
def npartiDict(nParticlesList):

	allParticleDictionary = {}
	minFrames = mc.playbackOptions( q=True, min=True)
	maxFrames = mc.playbackOptions( q=True, max=True)


	print('Collecting position data from {}'.format(nParticlesList))
	for shapeSel in nParticlesList:
		if mc.objectType(shapeSel)  == "nParticle":#make sure the object passed is a nParticle
			#print('layer3 ', shapeSel)
			getTrans = mc.pickWalk(shapeSel, d="up")
			theParticle = mc.ls(getTrans, type = "transform")
			#everyThingFolder = mc.group(em=True, n="AllTheThingsAreHERE")

			for currentFrame in range(0, int(maxFrames)):
				#print('Frame=' + str(currentFrame))
				mc.currentTime(currentFrame, update=True, edit=True)

				for part in theParticle:
					for particleCount in range(0,mc.particle(part, q=True,ct=True)):

						particleName = mc.particle(part, q=True, order=particleCount, at='id')
						particlesPosition = mc.particle(part, q=True, order=particleCount, at='position')
						particleDictionary = {}

						if str(particleName[0]) in allParticleDictionary.keys():
							particleDictionary = allParticleDictionary[str(particleName[0])]

						particleDictionary[currentFrame] = particlesPosition
						allParticleDictionary[str(particleName[0])] = particleDictionary

		else:
			mc.warning('You must select an nParticle type object, your selection is {}'.format(nParticlesList))
	return allParticleDictionary
