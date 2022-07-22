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
for different probe and sample materials. 
"""

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