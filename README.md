# npartiTools


This tool combines several tools that exist in the ../scripts repository which will be removed soon. This update has more features and a UI bug fixes. This tool only has UI's for the tube extrusion and bubble scripts, additional tools will be added shortly.

Tube Extrusion

![](docs_images/tubeExt.gif)

To load the UI copy, paste and execute the lines below in the script editor under Python witin Maya. Otherwise copy to the script editor and drag the code to a shelf and add the snippet as python.

```
from npartiTools.npartiCurvePath import ui_tubes
ui_tubes.makeTubeExtGui()
```

nBubbles

![](docs_images/nbubbles.gif)

To load the UI copy, paste and execute the lines below in the script editor under Python witin Maya. Otherwise copy to the script editor and drag the code to a shelf and add the snippet as python.

```
from  npartiTools.npartiBubble import ui_bubble
ui_bubble.makeBubbleGui()
```
