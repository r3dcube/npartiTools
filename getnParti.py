import maya.cmds as mc
def selNParticles():
	nParticlesList = mc.ls(sl=True, dag=True, lf=True)
	selectedPartis = []
	curvePosGrp = []
	update = mc.textScrollList("getnPartiList", e=True, ra=True)
	if nParticlesList != []:

		for item in nParticlesList:

			if len(nParticlesList) > 0 and mc.nodeType(item) == 'nParticle':
				selectedPartis.append(str(item))
				update = mc.textScrollList("getnPartiList", e=True, a=(item))
				print('nParticles added to selection')
			else:
				update = mc.textScrollList("getnPartiList", e=True, ra=True)
				print 'reselct only nParticles'
	else:
		print('You have nothing selected')
	return update,selectedPartis
