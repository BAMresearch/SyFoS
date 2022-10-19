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
	approachPart, contactPart = split_ideal_curve(idealCurve)

	adjustedApproachPart, adjustedContactPart = adjusted_curve_parts(
		approachPart,
		contactPart,
		inputParameters.kc
	)

	approachParameters, contactParameters = calculate_parameters(
		adjustedApproachPart,
		adjustedContactPart,
		inputParameters
	)

	return approachParameters, contactParameters

def split_ideal_curve(idealCurve: List) -> Tuple[List, List]:
	"""Split an ideal force distance curve into its approach and contact part.

	Parameters:
		idealCurve(list): Piezo (x) and Deflection (y) values of the ideal curve.

	Returns:
		approachPart(list): Piezo (x) and Deflection (y) values 
							of the approach part of the ideal curve.
		contactPart(list): Piezo (x) and Deflection (y) values 
						   of the contact part of the ideal curve.
	"""
	approachPart = get_ideal_approach_part(idealCurve)
	contactPart = get_ideal_contact_part(idealCurve)

	return approachPart, contactPart

def get_ideal_approach_part(idealCurve: List) -> List:
	"""Extract the approach part of the ideal curve.

	Parameters:
		idealCurve(list): Piezo (x) and Deflection (y) values of the ideal curve.

	Returns:
		approachPart(list): Piezo (x) and Deflection (y) values 
							of the approach part of the ideal curve.
	"""
	indexJumpToContact = np.argmin(
		np.diff(idealCurve[1])
	)

	nonNegativeApproachValues = np.where(
		idealCurve[1][:indexJumpToContact] >= 0 
	)[0]

	try: 
		indexEndOfZeroLine = nonNegativeApproachValues[-1]
	except IndexError:
		raise ValueError("Could not locate the end of the zero line.")
	else:
		return [
			idealCurve[0][:indexEndOfZeroLine],
			idealCurve[1][:indexEndOfZeroLine],
		]

def get_ideal_contact_part(idealCurve: List) -> List:
	"""Extract the contact part of the ideal curve.

	Parameters:
		idealCurve(list): Piezo (x) and Deflection (y) values of the ideal curve.

	Returns:
		contactPart(list): Piezo (x) and Deflection (y) values 
						   of the contact part of the ideal curve.
	"""
	indexMaximumForce = np.argmax(idealCurve[1])
	
	nonPositiveApproachValues = np.where(
		idealCurve[1][:indexMaximumForce] <= 0
	)[0]

	try:
		indexPointOfContact = nonPositiveApproachValues[-1]
	except IndexError:
		raise ValueError("Could not locate the point of contact.")
	else:
		return [
			idealCurve[0][indexPointOfContact:],
			idealCurve[1][indexPointOfContact:],
		]

def adjusted_curve_parts(
	approachPart: List,
	contactPart: List,
	kc: float
) -> Tuple[List, List]:
	"""Adjust the x and y values for the approach and contact part.

	Parameters:
		approachPart(list): Piezo (x) and Deflection (y) values 
							of the approach part of the ideal curve.
		contactPart(list): Piezo (x) and Deflection (y) values 
						   of the contact part of the ideal curve.
		kc(float): .

	Returns:
		adjustedApproachPart(list): TrueDistance (x) and Force (y) values.
		adjustedContactPart(list): Force (x) and Deformation (y) values.
	"""
	adjustedApproachPart = adjust_approach_part(approachPart)
	adjustedContactPart = adjust_contact_part(contactPart)

	return adjustedApproachPart, adjustedContactPart

def adjust_approach_part(
	approachPart: List,
	kc: float
) -> List[List, List, List]:
	"""Adjust the x and y values of the approach part.

	Parameters:
		approachPart(list): Piezo (x) and Deflection (y) values 
							of the approach part of the ideal curve.
		kc(float): The spring constant used to generate the ideal curve.

	Returns:
		adjustedApproachPart(list): TrueDistance (x), Pseudo Force (y) 
									and Force (y) values.
	"""
	trueDistance = calculate_true_distance(approachPart)
	pseudoForce = calculate_adjusted_pseudo_force(approachPart)
	force = calculate_adjusted_force(approachPart, kc)

	return [trueDistance, pseudoForce, force]

def adjust_contact_part(
	contactPart: List,
	kc: float
) -> List[List, List, List]:
	"""Adjust the x and y values of the contact part.

	Parameters:
		contactPart(list): Piezo (x) and Deflection (y) values 
						   of the contact part of the ideal curve.
		kc(float): The spring constant used to generate the ideal curve.

	Returns:
		adjustedContactPart(list): Pseudo Force (x), Force (x) and 
								   Deformation (y) values.
	"""
	pseudoForce = calculate_adjusted_pseudo_force(contactPart)
	force = calculate_adjusted_force(contactPart, kc)
	deformation = calculate_deformation(contactPart)

	return [pseudoForce, force, deformation]

def calculate_true_distance(
	approachPart: List
) -> np.ndarray:
	"""
	
	Parameters:

	Returns:

	"""
	return np.asarray(approachPart[0]) - np.asarray(approachPart[1])

def calculate_adjusted_force(
	curveSection: List,
	kc: float
) -> np.ndarray:
	"""
	
	Parameters:

	Returns:
	
	"""
	return np.asarray(curveSection[1]) * kc

def calculate_adjusted_pseudo_force(
	curveSection: List
) -> np.ndarray:
	"""
	
	Parameters:

	Returns:
	
	"""
	return np.asarray(curveSection[1]) 

def calculate_deformation(
	contactPart: List
) -> np.ndarray:
	"""
	
	Parameters:

	Returns:
	
	"""
	return np.asarray(contactPart[0]) - np.asarray(contactPart[1])

def calculate_parameters(
	adjustedApproachPart,
	adjustedContactPart,
	inputParameters
):
	"""
	
	Parameters:

	Returns:
	
	"""
	pass 

def calculate_approach_parameters():
	"""
	
	Parameters:

	Returns:
	
	"""
	pass 

def calculate_contact_parameters():
	"""
	
	Parameters:

	Returns:
	
	"""
	pass 

def calculate_hamaker_approach(
	force: float,
	trueDistance: float,
	radius: float,
	kc: float
) -> float:
	"""
	
	Parameters:
		force(float): .
		trueDistance(float): .
		radius(float): .
		kc(float): .

	Returns:
		hamaker(float): .
	"""
	return - ((6*force*trueDistance**2) / (radius))

def calculate_radius_approach(
	force: float,
	trueDistance: float,
	hamaker: float,
	kc: float
) -> float:
	"""
	
	Parameters:
		force(float): .
		trueDistance(float): .
		hamaker(float): .
		kc(float): .

	Returns:
		radius(float): .
	"""
	return - ((6*force*trueDistance**2) / (hamaker)) 

def calculate_kc_approach(
	force: float,
	trueDistance: float,
	hamaker: float,
	radius: float
) -> float:
	"""
	
	Parameters:
		force(float): .
		trueDistance(float): .
		hamaker(float): .
		radius(float): .

	Returns:
		kc(float): .
	"""
	return - ((6*force*trueDistance**2) / (hamaker)) 

def calculate_etot_contact():
	"""
	
	Parameters:

	Returns:
	
	"""
	pass 

def calculate_radius_contact():
	"""
	
	Parameters:

	Returns:
	
	"""
	pass 

def calculate_kc_contact():
	"""
	
	Parameters:

	Returns:
	
	"""
	pass 