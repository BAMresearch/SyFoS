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

def calculate_ideal_curve_parameters(
	idealCurve: List,
	inputParameters: NamedTuple
) -> Tuple:
	"""Calculate the theoretical parameters kc, radius, 
	   hamaker and etot from the ideal curve. These can 
	   be compared with the actual parameter values used 
	   to create the ideal curve.

	Parameters:
		idealCurve(list): Piezo (x) and Deflection (y) values of the ideal curve.
		inputParameters(namedtuple): Contains the material parameters used to 
									 create the ideal curve

	Returns:
		approachParameters(tuple): Contains the theoretical values for kc, 
								   radius and hamaker for every point of 
								   the approach part of the ideal curve.
		contactParameters(tuple): Contains the theoretical values for kc, 
								   radius and etot for every point of 
								   the contact part of the ideal curve.
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
		idealCurve[1][:indexJumpToContact+1] >= 0 
	)[0]

	try: 
		indexEndOfZeroLine = nonNegativeApproachValues[-1]
	except IndexError:
		raise ValueError("Could not locate the end of the zero line.")
	else:
		return [
			idealCurve[0][:indexEndOfZeroLine+1],
			idealCurve[1][:indexEndOfZeroLine+1],
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
) -> Tuple[List, List, List]:
	"""Adjust the x and y values of the approach part.

	Parameters:
		approachPart(list): Piezo (x) and Deflection (y) values 
							of the approach part of the ideal curve.
		kc(float): Spring constant used to generate the ideal curve.

	Returns:
		adjustedApproachPart(list): TrueDistance (x), Pseudo Force (y) 
									and Force (y) values.
	"""
	trueDistance = calculate_true_distance(approachPart)
	pseudoForce = calculate_adjusted_pseudo_force(approachPart)
	force = calculate_adjusted_force(approachPart, kc)

	return trueDistance, pseudoForce, force

def adjust_contact_part(
	contactPart: List,
	kc: float
) -> Tuple[List, List, List]:
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

	return pseudoForce, force, deformation

def calculate_true_distance(
	approachPart: List
) -> np.ndarray:
	"""Adjust the x values of the approach part.
	
	Parameters:
		approachPart(list): Piezo (x) and Deflection (y) values 
							of the approach part of the ideal curve.

	Returns:
		trueDistance(np.ndarray): New x values for the approach part.
	"""
	return np.asarray(approachPart[0]) - np.asarray(approachPart[1])

def calculate_adjusted_force(
	curveSection: List,
	kc: float
) -> np.ndarray:
	"""Adjust the y values of the approach part
	   or the x values of the contact part.
	
	Parameters:
		curveSection(list): Piezo (x) and Deflection (y) values 
							of the approach or contact part of 
							the ideal curve.
		kc(float): Spring constant used to generate the ideal curve.

	Returns:
		force(np.ndarray): New y/x values for the approach/contact part.
	"""
	return np.asarray(curveSection[1]) * kc

def calculate_adjusted_pseudo_force(
	curveSection: List
) -> np.ndarray:
	"""Alternative adjustment for the y values 
	   of the approach part or the x values 
	   of the contact part.
	
	Parameters:
		curveSection(list): Piezo (x) and Deflection (y) values 
							of the approach or contact part of 
							the ideal curve.

	Returns:
		pseudoForce(np.ndarray): New y/x values for the approach/contact part.
	"""
	return np.asarray(curveSection[1]) 

def calculate_deformation(
	contactPart: List
) -> np.ndarray:
	"""Adjust the y values of the contact part.
	
	Parameters:
		contactPart(list): Piezo (x) and Deflection (y) values 
						   of the contact part of the ideal curve.

	Returns:
		deformation(np.ndarray): New y values for the contact part.
	"""
	return np.asarray(contactPart[0]) - np.asarray(contactPart[1])

def calculate_parameters(
	adjustedApproachPart: List,
	adjustedContactPart: List,
	inputParameters: NamedTuple
) -> Tuple[List, List]:
	"""Calculate the theoretical parameters from the approach 
	   and contact part from which the ideal curve is based.
	
	Parameters:
		adjustedApproachPart(list): True Distance (x) and Force (y) values 
						   			of the approach part of the ideal curve.
		adjustedContactPart(list): Force (x) and Deformation (y) values 
						   		   of the contact part of the ideal curve.
		inputParameters(namedtuple): Parameters used to create the ideal curve.

	Returns:
		approachParameters(tuple): Contains the theoretical values for kc, 
								   radius and hamaker for every point of 
								   the approach part of the ideal curve.
		contactParameters(tuple): Contains the theoretical values for kc, 
								   radius and etot for every point of 
								   the contact part of the ideal curve.
	"""
	approachParameters = calculate_approach_parameters(
		adjustedApproachPart,
		inputParameters
	)
	contactParameters = calculate_contact_parameters(
		adjustedContactPart,
		inputParameters
	)

	return approachParameters, contactParameters

def calculate_approach_parameters(
	adjustedApproachPart: List,
	inputParameters: NamedTuple
) -> Tuple[List, List, List]:
	"""Calculate the theoretical kc, raidus and hamaker values 
	   for every point of the approach part of the ideal curve
	   using the actual parameter values.
	
	Parameters:
		adjustedApproachPart(list): True Distance (x) and Force (y) values 
						   			of the approach part of the ideal curve.
		inputParameters(namedtuple): Parameters used to create the ideal curve.

	Returns:
		springConstant(list): Theoretical kc values.
		radius(list): Theoretical radius values.
		hamaker(list): Theoretical hamaker values.
	"""
	springConstant = [
		calculate_kc_approach(
			trueDistance,
			force,
			inputParameters.hamaker,
			inputParameters.radius
		)
		for trueDistance, force in zip(
			adjustedApproachPart[0],
			adjustedApproachPart[2],
		)
	]

	radius = [
		calculate_kc_approach(
			trueDistance,
			force,
			inputParameters.hamaker,
			inputParameters.kc
		)
		for trueDistance, force in zip(
			adjustedApproachPart[0],
			adjustedApproachPart[2],
		)
	]

	hamaker = [
		calculate_kc_approach(
			trueDistance,
			force,
			inputParameters.radius,
			inputParameters.kc
		)
		for trueDistance, force in zip(
			adjustedApproachPart[0],
			adjustedApproachPart[2],
		)
	]

	return (
		springConstant,
		radius,
		hamaker
	)

def calculate_contact_parameters(
	adjustedContactPart: List,
	inputParameters: NamedTuple
) -> Tuple[List, List, List]:
	"""Calculate the theoretical kc, raidus and etot values 
	   for every point of the contact part of the ideal curve
	   using the actual parameter values.
	
	Parameters:
		adjustedContactPart(list): Force (x) and Deformation (y) values 
						   		   of the contact part of the ideal curve.
		inputParameters(namedtuple): Parameters used to create the ideal curve.

	Returns:
		springConstant(list): Theoretical kc values.
		radius(list): Theoretical radius values.
		etot(list): Theoretical etot values.
	"""
	springConstant = [
		calculate_kc_contact(
			force,
			deformation,
			inputParameters.etot,
			inputParameters.radius
		)
		for force, deformation in zip(
			adjustedApproachPart[1],
			adjustedApproachPart[2],
		)
	]

	radius = [
		calculate_kc_contact(
			force,
			deformation,
			inputParameters.etot,
			inputParameters.kc
		)
		for force, deformation in zip(
			adjustedApproachPart[1],
			adjustedApproachPart[2],
		)
	]

	etot = [
		calculate_etot_contact(
			force,
			deformation,
			inputParameters.radius,
			inputParameters.kc
		)
		for force, deformation in zip(
			adjustedApproachPart[1],
			adjustedApproachPart[2],
		)
	]

	return (
		springConstant,
		radius,
		etot
	)

def wrapper_calculate_parameter(
	calculateParameterFunction,
	xValues,
	yValues,
	firstParameter,
	secondParameter
) -> List:
	"""Calculates a parameter for each point of a part of the ideal curve.

	Parameters:
		calculateParameterFunction(function): Function to calculate a certain parameter.
		xValues(): X values of a part of the ideal curve.
		yValues(): Y values of a part of the ideal curve.
		firstParameter(): First acutal parameter used to create the ideal curve.
		secondParameter(): Second acutal parameter used to create the ideal curve.

	Returns:
		parameterValues(list): Parameter values for each point 
							   of the part of the ideal curve.
	"""
	return [
		calculateParameterFunction(
			xValue,
			yValue,
			firstParameter,
			secondParameter
		)
		for xValue, yValue in zip(
			xValues,
			yValues
		)
	]

def calculate_kc_approach(
	trueDistance: float,
	force: float,
	hamaker: float,
	radius: float
) -> float:
	"""Calculate the theoretical kc value for the approach 
	   part using the actual hamaker and radius values.
	
	Parameters:
		trueDistance(float): Adjusted x value for the approach part.
		force(float): Adjusted y value for the approach part.
		hamaker(float): Hamaker value used to create the ideal curve.
		radius(float): Radius value used to create the ideal curve.

	Returns:
		kc(float): Theoretical kc value.
	"""
	return - ((hamaker*radius) / (6*trueDistance**2*force)) 

def calculate_radius_approach(
	trueDistance: float,
	force: float,
	hamaker: float,
	kc: float
) -> float:
	"""Calculate the theoretical radius value for the 
	   approach part using the actual hamaker and kc values.
	
	Parameters:
		trueDistance(float): Adjusted x value for the approach part.
		force(float): Adjusted y value for the approach part.
		hamaker(float): Hamaker value used to create the ideal curve.
		kc(float): Kc value used to create the ideal curve.

	Returns:
		radius(float): Theoretical radius value.
	"""
	return - ((kc*6*force*trueDistance**2) / (hamaker)) 

def calculate_hamaker_approach(
	trueDistance: float,
	force: float,
	radius: float,
	kc: float
) -> float:
	"""Calculate the theoretical hamaker value for the 
	   approach part using the actual radius and kc values.
	
	Parameters:
		trueDistance(float): Adjusted x value for the approach part.
		force(float): Adjusted y value for the approach part.
		radius(float): Radius value used to create the ideal curve.
		kc(float): Kc value used to create the ideal curve.

	Returns:
		hamaker(float): Theoretical hamaker value.
	"""
	return - ((kc*6*force*trueDistance**2) / (radius))

def calculate_kc_contact(
	force: float,
	deformation: float,
	etot: float, 
	radius: float
) -> float:
	"""Calculate the theoretical kc value for the contact part
	   using the actual etot and radius values.
	
	Parameters:
		force(float): Adjusted x value for the contact part.
		deformation(float): Adjusted y value for the contact part.
		etot(float): Etot value used to create the ideal curve.
		radius(float): Radius value used to create the ideal curve.

	Returns:
		kc(float): Theoretical kc value.
	"""
	return (etot * np.sqrt(radius) * deformation**(2/3)) / force 

def calculate_radius_contact(
	force: float,
	deformation: float,
	etot: float, 
	kc: float
) -> float:
	"""Calculate the theoretical raidus value for the contact part
	   using the actual etot and kc values.
	
	Parameters:
		force(float): Adjusted x value for the contact part.
		deformation(float): Adjusted y value for the contact part.
		etot(float): Etot value used to create the ideal curve.
		kc(float): Kc value used to create the ideal curve.

	Returns:
		radius(float): Theoretical radius value.
	"""
	return (kc**2 * force**2) / (etot**2 * deformation**3) 

def calculate_etot_contact(
	force: float,
	deformation: float,
	radius: float, 
	kc: float
) -> float:
	"""Calculate the theoretical etot value for the contact part
	   using the actual raidus and kc values.
	
	Parameters:
		force(float): Adjusted x value for the contact part.
		deformation(float): Adjusted y value for the contact part.
		radius(float): Radius value used to create the ideal curve.
		kc(float): Kc value used to create the ideal curve.

	Returns:
		etot(float): Theoretical etot value.
	"""
	return (kc * force) / (np.sqrt(radius) * deformation**(3/2))