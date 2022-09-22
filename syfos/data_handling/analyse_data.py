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

from typing import List, Tuple, NamedTuple

import numpy as np

def extraxt_parameters(
	idealCurve: List,
	inputParameters: NamedTuple
) -> Tuple:
	"""

	Parameters:
		idealCurve(list): Piezo (x) and Deflection (y) values of the ideal curve.
		inputParameters(namedtuple): .

	Returns:
		approachParameters(): .
		contactParameters(): .
	"""
	approachPart, contactPart = split_curve(idealCurve)

	adjustedApproachPart, adjustedContactPart = adjusted_curve_parts(
		approachPart,
		contactPart
	)

	approachParameters, contactParameters = calculate_parameters(
		adjustedApproachPart,
		adjustedContactPart,
		inputParameters
	)

	return approachParameters, contactParameters

def split_curve(idealCurve: List) -> Tuple[List, List]:
	"""Split an ideal force distance curve into its approach and contact part.

	Parameters:
		idealCurve(list): Piezo (x) and Deflection (y) values of the ideal curve.

	Returns:
		approachPart(list): Piezo (x) and Deflection (y) values 
							of the approach part of the ideal curve.
		contactPart(list): Piezo (x) and Deflection (y) values 
						   of the contact part of the ideal curve.
	"""
	approachPart = get_approach_part(idealCurve)
	contactPart = get_contact_part(idealCurve)

	return approachPart, contactPart

def get_approach_part(idealCurve: List) -> List:
	"""Extract the approach part of the ideal curve.

	Parameters:
		idealCurve(list): Piezo (x) and Deflection (y) values of the ideal curve.

	Returns:
		approachPart(list): Piezo (x) and Deflection (y) values 
							of the approach part of the ideal curve.
	"""
	pass 

def get_contact_part(idealCurve: List) -> List:
	"""Extract the contact part of the ideal curve.

	Parameters:
		idealCurve(list): Piezo (x) and Deflection (y) values of the ideal curve.

	Returns:
		contactPart(list): Piezo (x) and Deflection (y) values 
						   of the contact part of the ideal curve.
	"""
	indexContact = np.where(idealCurve >= 0)[0][-1]
	return idealCurve[indexContact:]

def adjusted_curve_parts(
	approachPart: List,
	contactPart: List
) -> Tuple[List, List]:
	"""Adjust the x and y values for the approach and contact part.

	Parameters:
		approachPart(list): Piezo (x) and Deflection (y) values 
							of the approach part of the ideal curve.
		contactPart(list): Piezo (x) and Deflection (y) values 
						   of the contact part of the ideal curve.

	Returns:
		adjustedApproachPart(list): TrueDistance (x) and Force (y) values.
		adjustedContactPart(list): Force (x) and Deformation (y) values.
	"""
	adjustedApproachPart = adjust_approach_part(approachPart)
	adjustedContactPart = adjust_contact_part(contactPart)

	return adjustedApproachPart, adjustedContactPart

def adjust_approach_part(approachPart: List):
	"""

	Parameters:
		approachPart(list): Piezo (x) and Deflection (y) values 
							of the approach part of the ideal curve.

	Returns:
		adjustedApproachPart(list): TrueDistance (x) and Force (y) values.
	"""
	trueDistance = 
	force = 

	return [trueDistance, force]

def adjust_contact_part(contactPart: List):
	"""

	Parameters:
		contactPart(list): Piezo (x) and Deflection (y) values 
						   of the contact part of the ideal curve.

	Returns:
		adjustedContactPart(list): Force (x) and Deformation (y) values.
	"""
	force = 
	deformation = 

	return [force, deformation]

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