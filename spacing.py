# Spacing Macro beta07
# by Pablo Impallari
# modified by Daniele Capo

import fontforge
import os.path as pth
import csv

# Probably this is not the best way to find the directory where the script is
currentDir =  pth.dirname(pth.abspath(__file__))
defaultSpacing = pth.join(currentDir, "default-spacing.txt")

# here I assume that the user will put a file named spacing.txt
# in the font file directory, in this way one can separate
# the individual settings from the actual script.
# The user can copy default-spacing.txt in her font directory
# and modify the relevant part. It is not necessary
# to include all the variables: the variable unset by the user
# will take a default value from default-spacing.txt.
# If the user doesn't have a spacing.txt file in the font directory,
# default-spacing.txt will be used instead.
# The format of the file is: every line is an entry, with the name
# of parameter and the value, sperated by a space.

spacingFileName = "spacing.txt"

# -- To-Do List ------------------------------------------
# v, w: 1 for roman construction, 2 for italic construction
# y: 1 for v-like constuction, 2 for u-like construction
# option to ignore specific glyphs


# --------------------------------------------------
# --------- Do not edit bellow this line -----------
# ------ unless you know what you are doing --------
# --------------------------------------------------



# Functions

    
def getMargins (g, y):
    m = g.foreground.xBoundsAtY(y)
    if m:
        return (m[0], g.width - m[1])
    else: return (None, None)
	
def setMargins (g, y, l=None, r=None):
    margins = getMargins(g, y)
    if l is not None and margins[0] is not None:
        difference = margins[0] - g.left_side_bearing
        g.left_side_bearing = l - difference
    if r is not None and margins[1] is not None:
        difference = margins[1] - g.right_side_bearing
        g.right_side_bearing = r - difference


# The following function will take a filepath for the spacing file 
# and return a dictionary of the parameters.

def parseParams (filepath):
    reader = csv.reader(open (filepath, 'rb'),\
                            delimiter = ' ', skipinitialspace = True)
    params = dict ([[r[0], int(r[1])] for r in reader])
    return params

# The following function will supply the unset parameters with the default
# values provided by default-spacing.txt (see above).

def fillUnsetParams (params):
    defaultParams = parseParams (defaultSpacing)
    for k in defaultParams:
        if not params.has_key(k):
            params[k]=defaultParams[k]
    return params

# Get the font
def spacing (registerobject, f):
    xheight = f.xHeight
    MeasurementMiddle = xheight / 2
    fileDir = pth.dirname (f.path)
    localSetting = pth.join (fileDir, spacingFileName)
    if not pth.exists (localSetting): 
        params = fillUnsetParams({})
    else:
        params = fillUnsetParams (parseParams (localSetting))

    # Calculated Variables

    nDrawWidth = (params['nStem'] * 2) + params['nCounter']
    nTotalWidth = (params['nStem'] + params['nCounter']) * 2
    straightStem = round( ((nTotalWidth - nDrawWidth) / 2) * params['globalAdjust'] / 100 )
    
    oDrawWidth = (params['oStem'] * 2) + params['oCounter']
    curvedStem = round( ((nTotalWidth - oDrawWidth) / 2) * params['globalAdjust'] / 100 )
    curvedStem = round( curvedStem * params['curvedMarginAdjust'] / 100 )

   

    # Space
    if 'space' in f:
	f['space'].width = (straightStem * 2) + params['nStem']

    # nobdhijlmpqug
    if 'n' in f:
        setMargins(f['n'], MeasurementMiddle, straightStem, straightStem)
    if 'i' in f:
        setMargins(f['i'], MeasurementMiddle, straightStem, straightStem)
    if 'm' in f:
	setMargins(f['m'], MeasurementMiddle, straightStem, straightStem)
    if 'o' in f:
	setMargins(f['o'], MeasurementMiddle, curvedStem, curvedStem)
    if 'd' in f:
	setMargins(f['d'], MeasurementMiddle, curvedStem, straightStem)
    if 'p' in f:
	setMargins(f['p'], MeasurementMiddle, straightStem, curvedStem)

    if 'b' in f:
	bMarginLeft = straightStem * params['bLeft'] / 100
	setMargins(f['b'], MeasurementMiddle, bMarginLeft, curvedStem)

    hklMarginLeft = straightStem * params['hklLeft'] / 100
    if 'l' in f:
	setMargins(f['l'], MeasurementMiddle, hklMarginLeft, straightStem)
    if 'h' in f:
	setMargins(f['h'], MeasurementMiddle, hklMarginLeft, straightStem)

    if 'u' in f:
	uMarginLeft = straightStem * params['uLeft'] / 100
	setMargins(f['u'], MeasurementMiddle, uMarginLeft, straightStem)

    if 'j' in f:
	jMarginRight = straightStem * params['jqRight'] / 100
	setMargins(f['j'], MeasurementMiddle, straightStem, jMarginRight)

    if 'q' in f:
	qMarginRight = straightStem * params['jqRight'] / 100
	setMargins(f['q'], MeasurementMiddle, curvedStem, qMarginRight)

    #nWidth
    nWidth = f['n'].width

    if params['typeStyle'] == 1: # Sans average proportions
	aProportion = 0.92
	cProportion = 0.87
	eProportion = 0.94
	fProportion = 0.58
	gProportion = 0.98
	kProportion = 0.90
	rProportion = 0.64
	sProportion = 0.79
	tProportion = 0.62
	vProportion = 0.88 # v, w, y
	xProportion = 0.87
	zProportion = 0.83

    if params['typeStyle'] == 2: # Serif average proportions
	aProportion = 0.83
	cProportion = 0.80
	eProportion = 0.83
	fProportion = 0.57
	gProportion = 0.89
	kProportion = 0.94
	rProportion = 0.69
	sProportion = 0.71
	tProportion = 0.60
	vProportion = 0.87 # v, w, y
	xProportion = 0.89
	zProportion = 0.80


    if 'a' in f:
	if params['aConstruction'] == 1:
		f['a'].left_side_bearing = 0
		setMargins(f['a'], MeasurementMiddle, None, straightStem)
		diferencia = int( ( (nWidth * aProportion ) * params['aLeft'] / 100 ) - f['a'].width )
		f['a'].left_side_bearing = diferencia
        if params['aConstruction'] == 2:
		setMargins(f['a'], MeasurementMiddle, curvedStem, straightStem)

    if 'c' in f:
	f['c'].right_side_bearing = 0
	setMargins(f['c'], MeasurementMiddle, curvedStem, None)
	diferencia = int( ( (nWidth * cProportion ) * params['cRight'] / 100 ) - f['c'].width )
	f['c'].right_side_bearing = diferencia

    if 'e' in f:
	f['e'].right_side_bearing = 0
	setMargins(f['e'], MeasurementMiddle, curvedStem, None)
	diferencia = int( ( (nWidth * eProportion ) * params['eRight'] / 100 ) - f['e'].width )
	f['e'].right_side_bearing = diferencia

    if 'f' in f:
	f['f'].right_side_bearing = 0
	setMargins(f['f'], MeasurementMiddle, straightStem, None)
	diferencia = int( ( (nWidth * fProportion ) * params['fRight'] / 100 ) - f['f'].width )
	f['f'].right_side_bearing = diferencia

    if 'g' in f:
	if params['gConstruction'] == 1:
		gMarginLeft = straightStem * params['gLeft'] / 100
		gMarginRight = straightStem * params['gRight'] / 100
		setMargins(f['g'], (MeasurementMiddle * 130 / 100), gMarginLeft, gMarginRight)
	if params['gConstruction'] == 2:
		setMargins(f['g'], MeasurementMiddle, curvedStem, straightStem)	

    if 'k' in f:
	f['k'].right_side_bearing = 0
	hklMarginLeft = straightStem * params['hklLeft'] / 100
	setMargins(f['k'], MeasurementMiddle, hklMarginLeft, None)
	diferencia = int( ( (nWidth * kProportion ) * params['kRight'] / 100 ) - f['k'].width )
	f['k'].right_side_bearing = diferencia

    if 'r' in f:
	f['r'].right_side_bearing = 0
	setMargins(f['r'], MeasurementMiddle, straightStem, None)
	diferencia = int( ( (nWidth * rProportion ) * params['rRight'] / 100 ) - f['r'].width )
	f['r'].right_side_bearing = diferencia

    if 's' in f:
	f['s'].left_side_bearing = 0
	f['s'].right_side_bearing = 0
	diferencia = int( ( (nWidth * sProportion ) * params['sBoth'] / 100 ) - f['s'].width ) / 2
	f['s'].left_side_bearing = diferencia
	f['s'].right_side_bearing = diferencia

    if 't' in f:
	f['t'].right_side_bearing = 0
	setMargins(f['t'], MeasurementMiddle, straightStem, None)
	diferencia = int( ( (nWidth * tProportion ) * params['tRight'] / 100 ) - f['t'].width )
	f['t'].right_side_bearing = diferencia

    if 'v' in f:
	f['v'].left_side_bearing = 0
	f['v'].right_side_bearing = 0
	diferencia = int( ( (nWidth * vProportion ) * params['vBoth'] / 100 ) - f['v'].width ) / 2
	f['v'].left_side_bearing = diferencia
	f['v'].right_side_bearing = diferencia

    if 'w' in f:
	f['w'].left_side_bearing = diferencia
	f['w'].right_side_bearing = diferencia

    if 'y' in f:
	f['y'].left_side_bearing = diferencia
	f['y'].right_side_bearing = diferencia

    if 'x' in f:
	f['x'].left_side_bearing = 0
	f['x'].right_side_bearing = 0
	diferencia = int( ( (nWidth * xProportion ) * params['xBoth'] / 100 ) - f['x'].width ) / 2
	f['x'].left_side_bearing = diferencia
	f['x'].right_side_bearing = diferencia

    if 'z' in f:
	f['z'].left_side_bearing = 0
	f['z'].right_side_bearing = 0
	diferencia = int( ( (nWidth * zProportion ) * params['zBoth'] / 100 ) - f['z'].width ) / 2
	f['z'].left_side_bearing = diferencia
	f['z'].right_side_bearing = diferencia

    print "done";

if fontforge.hasUserInterface():
    keyShortcut = None
    menuText = "Spacing macro"
    fontforge.registerMenuItem(spacing, None, None, "Font", keyShortcut, menuText)
