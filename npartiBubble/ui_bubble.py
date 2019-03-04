import sys, importlib
import maya.cmds as mc
from npartiTools import npartiCurves as nc
from npartiTools import getnParti as gp
from npartiTools.npartiBubble import npartiBubble as nb
npartiSelection = []

reload(sys.modules['npartiTools.npartiCurves'])
reload(sys.modules['npartiTools.getnParti'])
reload(sys.modules['npartiTools.npartiBubble.npartiBubble'])

def updatePartiList(*args):
	global npartiSelection
	npartiList = []
	getit = gp.selNParticles()
	npartiSelection = getit[1]
	for nPartiSel in npartiSelection:#The scene can be heavy, after the building of bubbles this turns the nParticles back on
		if mc.getAttr(nPartiSel + '.isDynamic') != True:
			mc.setAttr(nPartiSel + '.isDynamic', 1)

def createBubbles(*args):
	inc = 0
	npartiList = []
	clothObjs = []
	char = 'A'
	#Needs a check to see if any other particle tubes have been created
	if mc.objExists('nbubbleGrp_*'):#replace this with a literal since one item would need to exist.
		getTubeNames = mc.ls('nbubbleGrp_*')
		check = []
		letterCheck = None
		for name in getTubeNames:
			breakName = name.split('_')
			letter= breakName[1]
			if letter != letterCheck:
				incLetter = ord(letter) +1
				check.append(incLetter)
		char = (chr(check[-1]))
		print(char)

	for nParti in npartiSelection:
		charUp = chr(ord(char) + inc)
		doesBubblePop = mc.checkBox("bubblePop", q=True, v=True)
		minScale = float(mc.textField('minScale', q=True, text=True))
		maxScale = float(mc.textField('maxScale', q=True, text=True))
		npartiList.append(nParti)
		particleDict = nc.npartiDict(npartiList)
		folderName = nParti
		makeBubbles = nb.buildnBubbles(particleDict, folderName, doesBubblePop, minScale, maxScale, charUp, clothObjs)
		mc.setAttr(nParti + '.isDynamic', 0)
		for objs in clothObjs:
			mc.setAttr(objs + '.isDynamic', 0)
		inc+=1
	#


def makeBubbleGui():

	if (mc.window("bubbleWin", exists=True)):
		mc.deleteUI("bubbleWin", wnd=True)
		mc.windowPref("bubbleWin", r=True)
	# C R E A T E  U I
	mc.window("bubbleWin", s=False, tlb=True, rtf=True, t="nBubbles")
	mc.columnLayout(adj=True)
	# L I S T  n P A R T I C L E S
	mc.frameLayout(l="Add selected nParticles to list", la="top", bgc=(0.329, 0.47, 0.505), cll=False, cl=False, w = 200)
	mc.columnLayout(adj=True)
	getPartiList = mc.textScrollList("getnPartiList", h=100, ams=False)
	mc.button(label="Add selected nParticles",bgc=(0.24, 0.72, 0.46), c=updatePartiList, h=30 )
	mc.setParent('..')
	mc.setParent('..')
	# B U B B L E  P O P
	mc.frameLayout(l="Does the bubble pop?", la="top", bgc=(0.1, 0.1, 0.1), cll=False, cl=False, w=200)
	mc.columnLayout(adj=True)
	mc.checkBox('bubblePop',label="Bubbles Pop On/Off", bgc=(0.21, 0.67, 0.72), v=True )
	# B U B B L E  S C A L E
	mc.frameLayout(l="Bubble Scale(Min/Max)", la="top", bgc=(0.1, 0.1, 0.1), cll=False, cl=False, w=200)
	#mc.columnLayout(adj=True,w=10)
	mc.rowColumnLayout(numberOfColumns=2, columnAttach=(1, 'left', 0), columnWidth=[(1, 100), (2, 97)] )
	mc.textField('minScale', bgc=(0.21, 0.67, 0.72), text='0.2')
	mc.textField('maxScale', bgc=(0.21, 0.67, 0.72), text='0.5')
	# E X T R U S I O N  R A N D
	mc.frameLayout(l="Execute", la="top", bgc=(0.1, 0.1, 0.1), cll=False, cl=False, w = 200)

	# C R E A T E  C U R V E S
	mc.button(label="Make Bubbles", bgc=(0.24, 0.72, 0.46), c =createBubbles , h = 40 )

	mc.setParent('..')
	mc.setParent('..')

	# S H O W  W I N D O W
	mc.showWindow("bubbleWin")

if __name__ == '__main__':

	makeBubbleGui()
