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

from collections import namedtuple

# 
ParameterBorders = namedtuple(
	"ParameterBorders",
	[
		"minValue",
		"maxValue",
	]
)

# Probe parameter borders.
kcBorders = ParameterBorders(
	minValue=0,
	maxValue=1,
)
radiusBorders = ParameterBorders(
	minValue=0,
	maxValue=1,
)
eProbeBorders = ParameterBorders(
	minValue=0,
	maxValue=1,
)
poissonRationProbeBorders = ParameterBorders(
	minValue=0,
	maxValue=1,
)
hamakerProbeBorders = ParameterBorders(
	minValue=0,
	maxValue=1,
)
# Sample parameter borders.
eSampleBorders = ParameterBorders(
	minValue=0,
	maxValue=1,
)
poissonRatioSampleBorders = ParameterBorders(
	minValue=0,
	maxValue=1,
)
hamakerSampleBorders = ParameterBorders(
	minValue=0,
	maxValue=1,
)

# 