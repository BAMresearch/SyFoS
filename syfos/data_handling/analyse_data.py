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

from typing import List, Tuple

import numpy as np

def extraxt_parameters(idealCurve: List) -> Tuple:
	""""""
	approachPart, contactPart = split_curve(idealCurve)

	adjustedApproachPart, adjustedContactPart = adjusted_curve_parts(
		approachPart,
		contactPart
	)

	approachParameters, contactParameters = calculate_parameters(
		adjustedApproachPart,
		adjustedContactPart
	)

	return approachParameters, contactParameters

def split_curve(idealCurve: List) -> Tuple[List, List]:
	""""""
	approachPart = get_approach_part(idealCurve)
	contactPart = get_contact_part(idealCurve)

	return approachPart, contactPart

def get_approach_part(idealCurve: List) -> List:
	""""""
	pass 

def get_contact_part(idealCurve: List) -> List:
	""""""
	pass

def adjusted_curve_parts(
	approachPart,
	contactPart
):
	""""""
	pass

def adjust_approach_part(approachPart):
	""""""
	pass


def adjust_contact_part(contactPart):
	""""""
	pass 

def calculate_adjusted_force_value():
	""""""
	pass

def calculate_adjusted_pseudo_force_value():
	""""""
	pass 

def calculate_adjusted_distance_value():
	""""""
	pass

def calculate_parameters():
	""""""
	pass 

def calculate_approach_parameters():
	""""""
	pass 

def calculate_contact_parameters():
	""""""
	pass 

def calculate_deformation():
	""""""
	pass 

def calculate_force():
	""""""
	pass 

def calculate_pseudo_force():
	""""""
	pass 

def calculate_kc_approach():
	""""""
	pass 

def calculate_kc_contact():
	""""""
	pass 

def calculate_radius_approach():
	""""""
	pass 

def calculate_radius_contact():
	""""""
	pass 

def calculate_etot():
	""""""
	pass 

def calculate_hamaker():
	""""""
	pass 