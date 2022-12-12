"""
This file is part of SyFoS.
SyFoS is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

SyFoS is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with SyFoS.  If not, see <http://www.gnu.org/licenses/>.
"""

"""
This file contains all predefined values 
for the parameter inputs and the different 
probe and sample materials. 
"""
# Input parameters
parameterInputsProbe = {
	"e": {
		"label": "",
		"formulaCharacter": "E",
		"formulaCharacterSubscript": "tip",
		"placeholder": "1e6 - 300e9",
		"valueBoundaries": [1e6, 300e9],
		"unitLabel": "Pa"
	},
	"poissonRatio": {
		"label": "",
		"formulaCharacter": "\u03BD",
		"formulaCharacterSubscript": "tip",
		"placeholder": "0 - 0.5",
		"valueBoundaries": [0, 0.5],
		"unitLabel": ""
	},
	"hamaker": {
		"label": "",
		"formulaCharacter": "A",
		"formulaCharacterSubscript": "tip",
		"placeholder": "1 - 450",
		"valueBoundaries": [1e-21, 450e-21],
		"unitLabel": "J"
	},
	"springConstant": {
		"label": "",
		"formulaCharacter": "k",
		"formulaCharacterSubscript": "c",
		"placeholder": "0.001 - 100",
		"valueBoundaries": [0.001, 100],
		"unitLabel": "N/m"
	},
	"radius": {
		"label": "",
		"formulaCharacter": "R",
		"formulaCharacterSubscript": "",
		"placeholder": "1e-9 - 10e-6",
		"valueBoundaries": [1e-9, 10e-6],
		"unitLabel": "m"
	}
}
parameterInputsSample = {
	"e": {
		"label": "",
		"formulaCharacter": "E",
		"formulaCharacterSubscript": "sample",
		"placeholder": "1e6 - 300e9",
		"valueBoundaries": [1e6, 300e9],
		"unitLabel": "Pa"
	},
	"poissonRatio": {
		"label": "",
		"formulaCharacter": "\u03BD",
		"formulaCharacterSubscript": "sample",
		"placeholder": "0 - 0.5",
		"valueBoundaries": [0, 0.5],
		"unitLabel": ""
	},
	"hamaker": {
		"label": "",
		"formulaCharacter": "A",
		"formulaCharacterSubscript": "sample",
		"placeholder": "1 - 450",
		"valueBoundaries": [1e-21, 450e-21],
		"unitLabel": "J"
	}
}
parameterInputsExperiment = {
	"startDistance": {
		"label": "Start Distance ",
		"formulaCharacter": "Z",
		"formulaCharacterSubscript": "0",
		"placeholder": "-10e-6 - 0",
		"valueBoundaries": [-10e-6, 0],
		"unitLabel": "m"
	},
	"stepSize": {
		"label": "Step Size ",
		"formulaCharacter": "dZ",
		"formulaCharacterSubscript": "",
		"placeholder": "0.01e-9 - 1e-9",
		"valueBoundaries": [0.01e-9, 1e-9],
		"unitLabel": "m"
	},
	"maximumPiezo": {
		"label": "Maximum Piezo ",
		"formulaCharacter": "Z",
		"formulaCharacterSubscript": "max",
		"placeholder": "0 - 1e-6",
		"valueBoundaries": [0, 1e-6],
		"unitLabel": "m"
	},
	"numberOfCurves": {
		"label": "Number Of Curves",
		"formulaCharacter": "",
		"formulaCharacterSubscript": "",
		"placeholder": "1 - 1000",
		"valueBoundaries": [1, 1000],
		"unitLabel": ""
	}
}
parameterInputsArtefacts = {
	"virtualDeflection": {
		"label": "Virtual Deflection",
		"formulaCharacter": "",
		"formulaCharacterSubscript": "",
		"placeholder": "0 - 3e-6",
		"valueBoundaries": [0, 3e-6],
		"unitLabel": "m"
	},
	"topographyOffset": {
		"label": "Topography Offset",
		"formulaCharacter": "",
		"formulaCharacterSubscript": "",
		"placeholder": "0 - 10e-6",
		"valueBoundaries": [0, 10e-6],
		"unitLabel": "m"
	},
	"noise": {
		"label": "Noise",
		"formulaCharacter": "",
		"formulaCharacterSubscript": "",
		"placeholder": "0 - 1e-9",
		"valueBoundaries": [0, 1e-9],
		"unitLabel": ""
	}
}

# Default Meterial Values
defaultMaterials = {
	"silicon": {
		"e": "170e9",
		"poissonRatio": "0.22",
		"hamaker": "66e-21",
	},
	"silicon dioxide": {
		"e": "72e9",
		"poissonRatio": "0.3",
		"hamaker": "66e-21",
	},
	"gold": {
		"e": "78e9",
		"poissonRatio": "0.42",
		"hamaker": "90e-21",
	},
	"pmma": {
		"e": "2.2e9",
		"poissonRatio": "0.35",
		"hamaker": "1.47e-21",
	},
	"ps": {
		"e": "3.4e9",
		"poissonRatio": "0.35",
		"hamaker": "13e-21",
	},
	"epoxy": {
		"e": "3.5e9",
		"poissonRatio": "0.3",
		"hamaker": "25e-21",
	},
}
