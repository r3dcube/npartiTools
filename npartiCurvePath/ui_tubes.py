import sys, importlib
import maya.cmds as mc
from npartiTools import npartiCurves as nc
from npartiTools import getnParti as gp
from npartiTools.npartiCurvePath import npartiTubes as nt

npartiSelection = []

def updatePartiList(*args):
    global npartiSelection
    npartiList = []
    getit = gp.selNParticles()
    npartiSelection = getit[1]

def createCurves(*args):
    global npartiSelection
    npartiList = []
    inc = 0
    char = 'A'
    #Needs a check to see if any other particle tubes have been created
    if mc.objExists('tubeGrp_*'):#replace this with a literal since one item would need to exist.
        getTubeNames = mc.ls('tubeGrp_*')
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
        #build a world controller for the particle curves
        partiTrans = mc.listRelatives(nParti, p=True)
        getPartiPos = mc.xform(partiTrans[0] , ws=True, q=True, t=True)
        curveCNTRL = mc.circle(c=getPartiPos, nr=(0,1,0), r=10,n=partiTrans[0] + '_' + char + '_CNTRL')
        mc.xform(curveCNTRL, cpc=True)
        charUp = chr(ord(char) + inc) #increment the letters in the major version. This has a limit of 26 and should be fixed in future verwsions.
        tubeDiv = int(mc.textField('tubeDiv', q=True, text=True)) #Query user poly divisions in tube length
        tubeDetail = int(mc.textField('tubeDet', q=True, text=True)) #Query user poly divisions in tube radius.
        tubeRad = float(mc.textField('tubeRadius', q=True, text=True)) #Query user tube radius in maya units
        bendDet = int(mc.textField('bendDetail', q=True, text=True))
        extruOffset = int(mc.textField('extOffSet', q=True, text=True))
        animExtrusion, aniVis = mc.checkBox("extAnim", q=True, v=True), mc.checkBox("aniVis", q=True, v=True)
        randOffset = int(mc.textField('randOffSet', q=True, text=True))
        npartiList.append(nParti)
        particleDict = nc.npartiDict(npartiList)
        folderName = nParti
        #querie the ui for the values below here
        tubes = nt.buildTubes(particleDict, tubeDiv, tubeRad, bendDet, extruOffset, folderName, animExtrusion, randOffset, aniVis, charUp, curveCNTRL,tubeDetail)
        inc+=1

#--------------------------------------------------------------------------------------------------------

def makeTubeExtGui():

	if (mc.window("partiCurveExtrusion", exists=True)):
		mc.deleteUI("partiCurveExtrusion", wnd=True)
		mc.windowPref("partiCurveExtrusion", r=True)

	# C R E A T E  U I
	mc.window("partiCurveExtrusion", s=False, tlb=True, rtf=True, t="Tube Exxxxtrusion")
	mc.columnLayout(adj=True)
	# L I S T  n P A R T I C L E S
	mc.frameLayout(l="Add selected nParticles to list", la="top", bgc=(0.329, 0.47, 0.505), cll=False, cl=False, w = 200)
	mc.columnLayout(adj=True)
	getPartiList = mc.textScrollList("getnPartiList", h=100, ams=False)
	mc.button(label="Add selected nParticles",bgc=(0.24, 0.72, 0.46), c=updatePartiList ,h = 30 )
	mc.setParent('..')
	mc.setParent('..')

	# A N I M A T I O N  V I S I B I L I T Y
	mc.frameLayout(l="End of tube animation on/off", la="top", bgc=(0.1, 0.1, 0.1), cll=False, cl=False, w = 200)
	mc.columnLayout(adj=True)
	mc.checkBox('extAnim',label="Animatie Extrusion", bgc=(0.21, 0.67, 0.72), v=True )

	# E X T R U S I O N   A N I M A T I O N
	mc.frameLayout(l="Tube visibility on/off", la="top", bgc=(0.1, 0.1, 0.1), cll=False, cl=False, w = 200)
	mc.columnLayout(adj=True)
	mc.checkBox('aniVis', label="Animate Visibility", bgc=(0.21, 0.67, 0.72), v=True )

	# E X T R U S I O N  O F F S E T - animates the tail of the tube based off keyframes default is a hold for 20 keyframes
	mc.frameLayout(l="Animate Extrusion Tail Offset", la="top", bgc=(0.1, 0.1, 0.1), cll=False, cl=False, w = 200)
	mc.columnLayout(adj=True)
	mc.textField('extOffSet', bgc=(0.21, 0.67, 0.72), text='20')

	# E X T R U S I O N  R A N D
	mc.frameLayout(l="Add an random offset", la="top", bgc=(0.1, 0.1, 0.1), cll=False, cl=False, w = 200)
	mc.columnLayout(adj=True)
	mc.textField('randOffSet', bgc=(0.21, 0.67, 0.72), text='0')

	# T U B E  D E T A I L
	mc.frameLayout(l="Tube Divisions +", la="top", bgc=(0.1, 0.1, 0.1), cll=False, cl=False, w = 200)
	#mc.columnLayout(adj=True)
	mc.rowColumnLayout(numberOfColumns=2, columnAttach=(1, 'left', 0), columnWidth=[(1, 100), (2, 97)] )
	mc.textField('tubeDiv', bgc=(0.21, 0.67, 0.72), text='0')
	mc.textField('tubeDet', bgc=(0.21, 0.67, 0.72), text='20')

	# T U B E  R A D I U S
	mc.frameLayout(l="Tube Radius", la="top", bgc=(0.1, 0.1, 0.1), cll=False, cl=False, w = 200)
	mc.columnLayout(adj=True)
	mc.textField('tubeRadius', bgc=(0.21, 0.67, 0.72), text='.25')

	# B E N D  D E T A I L
	mc.frameLayout(l="Lattice Detail +", la="top", bgc=(0.1, 0.1, 0.1), cll=False, cl=False, w = 200)
	mc.columnLayout(adj=True)
	mc.textField('bendDetail', bgc=(0.21, 0.67, 0.72), text='0')

	# C R E A T E  C U R V E S
	mc.button(label="Create Curves", bgc=(0.24, 0.72, 0.46), c =createCurves , h = 40 )
	mc.setParent('..')
	mc.setParent('..')

	# S H O W  W I N D O W
	mc.showWindow("partiCurveExtrusion")

if __name__ == '__main__':

    makeTubeExtGui()
