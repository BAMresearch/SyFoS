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
from typing import NamedTuple, Tuple, List

import numpy as np

def get_parameter_tuples() -> Tuple: 
	"""Combine the different components of the virtual setup
	   into named tuples.

	Returns:
		parameterMaterial(namedtupel): Combines all parameters describing the material 
									   and geometriy of the virtual measuring system.
		parameterMeasurement(namedtupel): Combines all parameters describing the virtual
										  measuring system.
		parameterForceVolume(namedtupel): Combines the number of synthetic curves, the noise
										  level and the virtual deflection and topography offset.
	"""
	ParameterMaterial = namedtuple(
		"ParameterMaterial",
		[
			"kc",
			"radius",
			"Etot",
			"Hamaker",
			"jtc"
		]
	)
	ParameterMeasurement = namedtuple(
		"ParameterMeasurement",
		[
			"startDistance",
			"stepSize",
			"maximumPiezo"
		]
	)
	ParameterForceVolume = namedtuple(
		"parameterForceVolume",
		[
			"numberOfCurves",
			"noise",
			"virtualDeflection",
			"topographyOffset"
		]
	)

	return ParameterMaterial, ParameterMeasurement, ParameterForceVolume

def calculate_jtc(
	hamaker: float, 
	radius: float, 
	kc: float
) -> float:
	"""Calculate the jtc from the probe parameters and the hamaker value.

	Parameters:
		hamaker(float): Hamker value for the specified probe and sample setup.
		radius(float): Specified value for the tip radius.
		kc(float): Specified value for the spring constant.

	Returns:
		jtc(float): Jtc value for the given probe and sample setup.
	"""
	return - np.cbrt(
		(hamaker*radius) / (3*kc)
	)

def calculate_etot(
	poissonRatioProbe: float, 
	eProbe: float, 
	poissonRatioSample: float,
	eSample: float,
) -> float:
	"""Calculate the total etot value from the poisson 
	   ration and e value of probe and sample.

	Parameters:
		poissonRatioProbe(float): Specified poisson ratio for the probe.
		eProbe(float): Specified e value for the probe.
		poissonRatioSample(float): Specified poisson ratio for the sample.
		eSample(float): Specified e value for the sample.

	Returns:
		etot(float): Etot value for the given probe and sample setup.
	"""
	return (
		4 / (3*(
			calculate_etot_inner_fraction(poissonRatioProbe, eProbe)
			+ calculate_etot_inner_fraction(poissonRatioSample, eSample)
		))
	)

def calculate_etot_inner_fraction(
	poissonRatio,
	e
) -> float: 
	"""Helper function for calculate_etot.

	Parameters:
		poissonRatio(float): Specified poisson ratio for the probe/sample.
		e(float): Specified e value for the probe/sample.

	Returns:
		innerFraction(float): Inner fraction for the probe/sample values.
	"""
	return (
		(1 - poissonRatio**2) / e
	)

def calculate_hamaker(
	hamakerProbe: float, 
	hamakerSample: float, 
) -> float:
	"""Calculate the total hamaker value for the probe and sample.

	Parameters:
		hamakerProbe(float): Specified hamaker value for the probe.
		hamakerSample(float): Specified hamaker value for the sample.

	Returns:
		hamaker(float): Hamker value for the given probe and sample setup.
	"""
	return np.sqrt(hamakerProbe) * np.sqrt(hamakerSample)

def create_synthetic_force_volume(
	parameterMaterial: NamedTuple, 
	parameterMeasurement: NamedTuple, 
	parameterForceVolume: NamedTuple
) -> List:
	"""Create a set of synthetic curves from given parameters, 
	   including a noise level, virtual deflection and topography offset.

	Parameters:
		parameterMaterial(namedtupel): Contains all parameters describing the material 
									   and geometriy of the virtual measuring system.
		parameterMeasurement(namedtupel): Contains all parameters describing the virtual
										  measuring system.
		parameterForceVolume(namedtupel): Contains the number of synthetic curves, the noise
										  level and the virtual deflection and topography offset.
	
	Returns:
		syntheticForceVolume(list): List of synthetic force distance curves and
								 	the ideal curve on which they are based.
	"""
	piezo, deflection = create_ideal_curve(
		parameterMaterial, 
		parameterMeasurement
	)
	
	shiftedPiezo, shiftedDeflection = shift_ideal_curve(
		piezo,
		deflection,
		parameterForceVolume
	)

	syntheticDeflectionValues = multiply_and_apply_noise_to_deflection(
		shiftedDeflection, 
		parameterForceVolume
	)

	syntheticCurves = create_synthetic_curves(
		shiftedPiezo,
		syntheticDeflectionValues
	)
	
	syntheticForceVolume = arrange_curves_in_force_volume(
		piezo, 
		deflection, 
		shiftedPiezo, 
		shiftedDeflection, 
		syntheticCurves
	)

	return syntheticForceVolume

def create_ideal_curve(
	parameterMaterial: NamedTuple, 
	parameterMeasurement: NamedTuple
) -> Tuple[List, List]:
	"""Create an ideal curve for the given virtual setup.

	Parameters:
		parameterMaterial(namedtupel): Contains all parameters describing the material 
									   and geometriy of the virtual measuring system.
		parameterMeasurement(namedtupel): Contains all parameters describing the virtual
										  measuring system.

	Returns:
		piezo(list): Piezo (x) values of the ideal curve.
		deflection(list): Deflection (y) values of the ideal curve. 
	"""
	piezoApproach, deflectionApproach = create_ideal_curve_approach_part(
		parameterMaterial,
		parameterMeasurement,
	)
	lengthApproach = len(piezoApproach)

	piezoAttraction, deflectionAttraction = create_ideal_curve_attraction_part(
		parameterMeasurement,
		lengthApproach
	)
	lengthUntilContact = lengthApproach + len(piezoAttraction)
	
	piezoContact, deflectionContact = create_ideal_curve_contact_part(
		parameterMaterial,
		parameterMeasurement,
		lengthUntilContact
	)

	piezo = piezoApproach + piezoAttraction + piezoContact
	deflection = deflectionApproach + deflectionAttraction + deflectionContact

	return piezo, deflection
		
def create_ideal_curve_approach_part(
	parameterMaterial: NamedTuple,
	parameterMeasurement: NamedTuple
) -> Tuple[List, List]: 
	"""Generate the approach part of the ideal curve.

	Parameters:
		parameterMaterial(namedtupel): Contains all parameters describing the material 
									   and geometriy of the virtual measuring system.
		parameterMeasurement(namedtupel): Contains all parameters describing the virtual
										  measuring system.

	Returns:
		piezoApproach(list): Piezo (x) values of the approach part of the ideal curve.
		deflectionApproach(list): Deflection (y) values of the approach part of the ideal curve. 
	
	Raises:
		ValueError: If the maximum piezo is reached before the jumpt to contact occurs.
	"""
	piezoApproach = [parameterMeasurement.startDistance]
	deflectionApproach = [0]

	while(True):
		tipSampleDistance = calculate_tip_sample_distance(
			piezoApproach[-1],
			deflectionApproach[-1]
		)
		
		piezoApproach.append(
			calculate_piezo_value(
				parameterMeasurement.startDistance,
				parameterMeasurement.stepSize,
				len(piezoApproach)
			)
		)
		deflectionApproach.append(
			calculate_deflection_approach_part(
				parameterMaterial.Hamaker,
				parameterMaterial.radius,
				parameterMaterial.kc,
				tipSampleDistance
			)
		)

		if (np.abs(tipSampleDistance) < np.abs(parameterMaterial.jtc)):
			break

		if (piezoApproach[-1] > parameterMeasurement.maximumPiezo):
			raise ValueError(
				"No ideal curve could be created. Please change the iput parameters."
			)

	return piezoApproach, deflectionApproach

def create_ideal_curve_attraction_part(
	parameterMeasurement: NamedTuple,
	lengthApproach: int
) -> Tuple[List, List]: 
	"""Generate the attraction part of the ideal curve.

	Parameters:
		parameterMeasurement(namedtupel): Contains all parameters describing the virtual
										  measuring system.
		lengthApproach(int): Length of the approach part of the ideal curve.

	Returns:
		piezoAttraction(list): Piezo (x) values of the attraction part of the ideal curve.
		deflectionAttraction(list): Deflection (y) values of the attraction part of the ideal curve. 

	Raises:
		ValueError: If the maximum piezo is reached before the point of contact occurs.
	"""
	piezoAttraction = []
	deflectionAttraction = []

	while(True):
		piezoAttraction.append(
			calculate_piezo_value(
				parameterMeasurement.startDistance,
				parameterMeasurement.stepSize,
				len(piezoAttraction) + lengthApproach
			)
		)
		deflectionAttraction.append(
			calculate_deflection_attraction_part(
				piezoAttraction[-1]
			)
		)

		if (deflectionAttraction[-1] >= 0):
			break

		if (piezoAttraction[-1] > parameterMeasurement.maximumPiezo):
			raise ValueError(
				"No ideal curve could be created. Please change the iput parameters."
			)

	return piezoAttraction, deflectionAttraction

def create_ideal_curve_contact_part(
	parameterMaterial: NamedTuple,
	parameterMeasurement: NamedTuple,
	lengthUntilContact: int
) -> Tuple[List, List]: 
	"""Generate the contact part of the ideal curve.

	Parameters:
		parameterMaterial(namedtupel): Contains all parameters describing the material 
									   and geometriy of the virtual measuring system.
		parameterMeasurement(namedtupel): Contains all parameters describing the virtual
										  measuring system.
		lengthUntilContact(int): Length of the ideal curve until the point of contact.

	Returns:
		piezoContact(list): Piezo (x) values of the contact part of the ideal curve.
		deflectionContact(list): Deflection (y) values of the contact part of the ideal curve.
	"""
	parameterSubstitut = parameterMaterial.kc / (np.sqrt(parameterMaterial.radius) * parameterMaterial.Etot)

	piezoContact = []
	deflectionContact = []

	while(True):
		piezoContact.append(
			calculate_piezo_value(
				parameterMeasurement.startDistance,
				parameterMeasurement.stepSize,
				len(piezoContact) + lengthUntilContact
			)
		)
		deflectionContact.append(
			calculate_deflection_contact_part(
				parameterSubstitut,
				piezoContact[-1]
			)
		)

		if (piezoContact[-1] >= parameterMeasurement.maximumPiezo):
			break

	return piezoContact, deflectionContact

def calculate_piezo_value(
	startDistance: float,
	stepSize: float,
	currentLength: int
) -> float:
	"""Calculate the current piezo value.

	Parameters:
		startDistance(float): Initial distance of the given virtual system.
		stepSize(float): Distance interval of the given virtual system.
		currentLength(int): Current lenght of the ideal curve.

	Returns:
		piezoValue(float): Current piezo value of the ideal curve.
	"""
	return startDistance + stepSize * currentLength

def calculate_tip_sample_distance(
	piezo: float,
	deflection: float
) -> float:
	"""Calculate the current tip-sample distance.

	Parameters:
		piezo(float): Current piezo value.
		deflection(float): Current deflection value.

	Returns:
		tipSampleDistance(float): Current tip-sample distance.
	"""
	return piezo - deflection

def calculate_deflection_approach_part(
	hamaker: float,
	radius: float, 
	kc: float, 
	tipSampleDistance: float
) -> float:
	"""Calculate the current deflection while probe and sample converge,
	   using Hooke's Law and the Hamaker constant.
	
	Parameters:
		hamaker(float): Hamaker value of the given virtual system.
		radius(float): Value for the specified tip radius.
		kc(float): Value for the specified spring constant.
		tipSampleDistance(float): Corresponding tip-sample distance.

	Returns:
		deflectionValue(float): Current deflection value while probe and
							    sample approach each other.
	"""
	return (
		- (hamaker*radius)
		/ (6*tipSampleDistance**2*kc) 
	)

def calculate_deflection_attraction_part(
	currentPiezoValue: float
) -> float:
	"""Calculate the current deflection while the probe is within the 
	   attractive regime.

	Parameters:
		currentPiezoValue(float): Corresponding piezo value.

	Returns:
		deflectionValue(float): Current deflection value while probe and
							    sample attract each other.
	"""
	return currentPiezoValue

def calculate_deflection_contact_part(
	parameterSubstitut: float,
	currentPiezoValue: float
) -> float:	
	"""Calculate the current deflection after probe and sample are in contact,
	   using the Hertzian contact theory.

	Parameters:
		parameterSubstitut(float): Interim result from kc, radius and etot.
		currentPiezoValue(float): Corresponding piezo value.

	Returns:
		deflectionValue(float): Current deflection value while the probe 
							    is in contact.
	"""
	return float(np.real(
		calculate_deflection_contact_first_term(
			parameterSubstitut,
			currentPiezoValue
		)
		+
		calculate_deflection_contact_second_term(
			parameterSubstitut,
			currentPiezoValue
		)
		-
		calculate_deflection_contact_third_term(
			parameterSubstitut,
			currentPiezoValue
		)
	))

def calculate_deflection_contact_first_term(
	parameterSubstitut: float,
	currentPiezoValue: float
) -> float: 
	"""Helper function for calculate_deflection_contact_part.

	Parameters:
		parameterSubstitut(float): Interim result from kc, radius and etot.
		currentPiezoValue(float): Corresponding piezo value.

	Returns:
		firstTerm(float): Interim result for calculate_deflection_contact_part.
	"""
	return (
		(1/3) * (3*currentPiezoValue - parameterSubstitut**2)
	)

def calculate_deflection_contact_second_term(
	parameterSubstitut: float,
	currentPiezoValue: float
) -> np.complex256: 
	"""Helper function for calculate_deflection_contact_part.

	Parameters:
		parameterSubstitut(float): Interim result from kc, radius and etot.
		currentPiezoValue(float): Corresponding piezo value.

	Returns:
		secondTerm(float): Interim result for calculate_deflection_contact_part.
	"""
	return (
		calculate_cubic_root(
			parameterSubstitut, 
			currentPiezoValue
		) / (3*np.cbrt(2))
	)

def calculate_deflection_contact_third_term(
	parameterSubstitut: float,
	currentPiezoValue: float
) -> np.complex256: 
	"""Helper function for calculate_deflection_contact_part.

	Parameters:
		parameterSubstitut(float): Interim result from kc, radius and etot.
		currentPiezoValue(float): Corresponding piezo value.

	Returns:
		thirdTerm(float): Interim result for calculate_deflection_contact_part.
	"""
	return (
		np.cbrt(2) * (
			6 * parameterSubstitut**2
			* currentPiezoValue
			- parameterSubstitut**4
		) / (3 * calculate_cubic_root(
			parameterSubstitut,
			currentPiezoValue
		))
	)

def calculate_cubic_root(
	parameterSubstitut: float,
	currentPiezoValue: float
) -> np.complex256:
	"""Helper function for the second and third term 
	   of calculate_deflection_contact_part.

	Parameters:
		parameterSubstitut(float): Interim result from kc, radius and etot.
		currentPiezoValue(float): Corresponding piezo value.

	Returns:
		cubicRoot(float): Interim result for the calculation of the second 
						  and third term.
	"""
	return np.clongdouble(
		- 2 * parameterSubstitut**6
		+ 18 * parameterSubstitut**4
		* currentPiezoValue
		- 27 * parameterSubstitut**2
		* currentPiezoValue**2
		+ 3 * np.sqrt(3)
		* calculate_inner_root(parameterSubstitut, currentPiezoValue)
	) ** (1/3)

def calculate_inner_root(
	parameterSubstitut: float,
	currentPiezoValue: float
) -> np.complex256:
	"""Helper function for calculate_cubic_root.

	Parameters:
		parameterSubstitut(float): .
		currentPiezoValue(float): Corresponding piezo value.

	Returns:
		innerRoot(float): Interim result for calculate_cubic_root.
	"""
	return np.clongdouble(
		27 * parameterSubstitut**4 
		* currentPiezoValue**4 
		- 4 * parameterSubstitut**6 
		* currentPiezoValue**3
	) ** (1/2)

def shift_ideal_curve(
	piezo: List,
	deflection: List,
	parameterForceVolume: NamedTuple
) -> Tuple[np.ndarray, np.ndarray]:
	"""Shift the ideal curve in the x and y direction by applying the 
	   virtual deflection and topography offset.

	Parameters:
		piezo(list): Piezo (x) values of the ideal curve.
		deflection(list): Deflection (y) values of the ideal curve. 
		parameterForceVolume(namedtupel): Contains the number of synthetic curves, the noise
										  level and the virtual deflection and topography offset.

	Returns:
		shiftedPiezo(np.ndarray): Piezo (x) values shifted by the topography offset.
		shiftedDeflection(np.ndarray): Deflection (y) values shifted by the virtual deflection.
	"""
	shiftedPiezo = np.asarray(piezo) + parameterForceVolume.topographyOffset
	shiftedDeflection = np.asarray(deflection) + parameterForceVolume.virtualDeflection

	return shiftedPiezo, shiftedDeflection

def multiply_and_apply_noise_to_deflection(
	shiftedDeflection: np.ndarray, 
	parameterForceVolume: NamedTuple
) -> List[np.ndarray]:
	"""Multiplies the deflection (y) values of the shifted 
	   ideal curve and applies noise to each copy.

	Parameters:
		shiftedDeflection(np.ndarray): Shifted deflection (y) values of the ideal curve.
		parameterForceVolume(namedtupel): Contains the number of synthetic curves, the noise
										  level and the virtual deflection and topography offset.

	Returns:
		syntheticDeflectionValues(list): List of synthetic deflection values.
	"""
	return [
		apply_noise_to_deflection(shiftedDeflection, parameterForceVolume)
		for _ in range(parameterForceVolume.numberOfCurves)
	]

def apply_noise_to_deflection(
	shiftedDeflection: List, 
	parameterForceVolume: NamedTuple
) -> np.ndarray:
	"""Apply noise to the deflection (y) values of the shifted ideal curve.

	Parameters:
		shiftedDeflection(list): Shifted deflection (y) values of the ideal curve.
		parameterForceVolume(namedtupel): Contains the number of synthetic curves, the noise
										  level and the virtual deflection and topography offset.

	Returns:
		(np.ndarray): Shifted deflection (y) values of the ideal curve with added noise.

	Raises:
		ValueError: If the noise value is negative.
	"""

	try:
		noiseValues = np.random.normal(0, parameterForceVolume.noise, size=len(shiftedDeflection))
	except ValueError:
		raise ValueError("Noise value must be positive.")

	return shiftedDeflection + noiseValues

def create_synthetic_curves(
	shiftedPiezo: np.ndarray,
	syntheticDeflectionValues: List
) -> List:
	"""Combines the shifted piezo (x) values with the 
	   corresponding synthetic deflection (y) values.
	
	Parameters:
		shiftedPiezo(np.ndarray): Shifted piezo (x) values of the ideal curve.
		syntheticDeflectionValues(list): List of synthetic deflection values.

	Returns:
		syntheticCurves(list): List of synthetic force distance curves.
	"""
	return [
		[shiftedPiezo, syntheticDeflection]
		for syntheticDeflection in syntheticDeflectionValues
	]

def arrange_curves_in_force_volume(
	piezo: List,
	deflection: List,  
	shiftedPiezo: np.ndarray, 
	shiftedDeflection: np.ndarray, 
	syntheticCurves: List
) -> List:
	"""Arrange the ideal curve, the shifted ideal curve 
	   and the synthetic curves in a force volume.

	Parameters:
		piezo(list): Piezo (x) values of the ideal curve.
		deflection(list): Deflection (y) values of the ideal curve.
		shiftedPiezo(np.ndarray): Piezo (x) values of the shifted ideal curve.
		shiftedDeflection(np.ndarray): Deflection (y) values of the shifted ideal curve.
		syntheticCurves(list): List of synthetic force distance curves based on the 
							   shifted ideal curve.

	Returns:
		forceVolume(list): List of synthetic force distance curves and
						   the ideal curve on which they are based.
	"""
	return [
		[piezo, deflection],
		[shiftedPiezo, shiftedDeflection],
	] + syntheticCurves