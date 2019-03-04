import sys
import maya.cmds as mc
from npartiTools.curveExtrude import curveExtrusion as ce

reload(sys.modules['npartiTools.curveExtrude.curveExtrusion'])
amount = 0
#------------------------------------------------------------------------------------------------
# 								G E T  S E L E C T E D  C U R V E S
#------------------------------------------------------------------------------------------------
def selectedCurves(*args):
	global curveBit

	getCurves = mc.ls(sl=True, dag=True, s=True)
	mc.textScrollList("getTheCurves", e=True, ra=True)
	if getCurves != []:
		for curveBit in getCurves:
			if len(getCurves) > 0 and mc.nodeType(curveBit) == 'nurbsCurve':
				update = mc.textScrollList("getTheCurves", e=True, a=(curveBit))
				print('Nurbs curve {} added to selection'.format(curveBit))
			else:
				mc.textScrollList("getTheCurves", e=True, ra=True)
				print('reselct only nurbsCurves')
	else:
		print('You have nothing selected')

def buildCurveExtru(*args):
	ce.CreateACurve()
	#pass

def makeCurveExtGui():

	if (mc.window("curveExtrusion", exists=True)):
		mc.deleteUI("curveExtrusion", wnd=True)
		mc.windowPref("curveExtrusion", r=True)
	# C R E A T E  U I
	mc.window("curveExtrusion", s=False, tlb=True, rtf=True, t="Curve Exxxxtrusion")
	mc.columnLayout(adj=True)
	# L I S T  S E L E C T E D  C U R V E S
	mc.frameLayout(l="Add selected curves to list", la="top", bgc=(0.329, 0.47, 0.505), cll=False, cl=False, w = 200)
	mc.columnLayout(adj=True)
	mc.textScrollList("getTheCurves", h=100, ams=False)
	mc.button(label="Add selected curves",bgc=(0.24, 0.72, 0.46), c=selectedCurves , h = 30 )
	mc.setParent('..')
	mc.setParent('..')
	# C U R V E  D E T A I L
	mc.frameLayout( l="Rebuild curve with x segments +", la="top", bgc=(0.1, 0.1, 0.1), cll=False, cl=False, w = 200)
	mc.columnLayout(adj=True)
	mc.textField('curveDetail', bgc=(0.21, 0.67, 0.72), text='200')
	# P R O G R E S S  B A R
	progressControl = mc.progressBar( 'progBar', pr=amount, width=195, st='working')
	mc.setParent('..')
	mc.setParent('..')
	# C R E A T E  C U R V E S
	mc.button(label="Create Curves", bgc=(0.24, 0.72, 0.46), c=buildCurveExtru, h = 40 )
	mc.setParent('..')
	mc.setParent('..')
	# S H O W  W I N D O W
	mc.showWindow("curveExtrusion")

if __name__ == '__main__':

    makeCurveExtGui()
