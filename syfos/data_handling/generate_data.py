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
	"""Define

	Returns:
		parameterMaterial(namedtupel): Combines all parameters describing the material 
									   and geometriy of the virtuell measuring system.
		parameterMeasurement(namedtupel): Combines all parameters describing the virtuell
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
			"initialDistance",
			"distanceInterval",
			"maximumdeflection"
		]
	)
	ParameterForceVolume = namedtuple(
		"parameterForceVolume",
		[
			"numberOfCurves",
			"noise",
			"virtualDeflection",
			"topography"
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
		jtc(float): jtc value for the given probe and sample setup.
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
	"""Calculate the etot value from the poisson ration 
	   and e value of probe and sample.

	Parameters:
		poissonRatioProbe(float): Specified poisson ratio for the probe.
		eProbe(float): Specified e value for the probe.
		poissonRatioSample(float): Specified poisson ratio for the sample.
		eSample(float): Specified e value for the sample.

	Returns:
		etot(float): etot value for the given probe and sample setup.
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
	"""Calculate the hamaker value for the probe and sample

	Parameters:
		hamakerProbe(float): Specified hamaker value for the probe.
		hamakerSample(float): Specified hamaker value for the sample.

	Returns:
		hamaker(float): hamker value for the given probe and sample setup.
	"""
	return np.sqrt(hamakerProbe) * np.sqrt(hamakerSample)

def create_synthetic_force_volume(
	parameterMaterial: NamedTuple, 
	parameterMeasurement: NamedTuple, 
	parameterForceVolume: NamedTuple
) -> np.ndarray:
	"""Create a set of synthetic curves from given parameters, 
	   including a noise level, virtual deflection and topography offset.

	Parameters:
		parameterMaterial(namedtupel): Contains all parameters describing the material 
									   and geometriy of the virtuell measuring system.
		parameterMeasurement(namedtupel): Contains all parameters describing the virtuell
										  measuring system.
		parameterForceVolume(namedtupel): Contains the number of synthetic curves, the noise
										  level and the virtual deflection and topography offset.
	
	Returns:
		syntheticForceVolume(np.ndarray): Set of generated synthetic force distance curves.

	Raises:
		ValueError: If the ideal curve can not be created with the given parameters. 
		ValueError: If the given noise can not be applied to the ideal curve.
	"""
	try:
		piezo, deflection = create_ideal_curve(
			parameterMaterial, 
			parameterMeasurement
		)
	except ValueError:
		raise ValueError("") from error 
	
	shiftedPiezo, shiftedDeflection = shift_ideal_curve(
		piezo,
		deflection,
		parameterForceVolume
	)

	try:
		noisyCurves = multiply_and_apply_noise_to_ideal_curve(
			shiftedDeflection, 
			parameterForceVolume
		)
	except ValueError:
		raise ValueError("") from error
	
	syntheticForceVolume = arrange_curves_in_force_volume(
		piezo, deflection, 
		shiftedPiezo, shiftedDeflection, 
		noisyCurves
	)

	return syntheticForceVolume

def create_ideal_curve(
	parameterMaterial: NamedTuple, 
	parameterMeasurement: NamedTuple
) -> Tuple[List, List]:
	"""Create an ideal curve from the given parameters.

	Parameters:
		parameterMaterial(namedtupel): Contains all parameters describing the material 
									   and geometriy of the virtuell measuring system.
		parameterMeasurement(namedtupel): Contains all parameters describing the virtuell
										  measuring system.

	Returns:
		piezo(list): Piezo (x) values of the ideal curve.
		deflection(list): Deflection (y) values of the ideal curve. 
	"""
	piezoApproach, deflectionApproach = create_ideal_curve_approach_part(
		parameterMaterial,
		parameterMeasurement,
	)

	totalLength = len(piezoApproach)
	piezoAttraction, deflectionAttraction = create_ideal_curve_attraction_part(
		parameterMeasurement,
		totalLength
	)
	
	totalLength += len(piezoAttraction)
	piezoContact, deflectionContact = create_ideal_curve_contact_part(
		parameterMaterial,
		parameterMeasurement,
		totalLength
	)

	piezo = piezoApproach + piezoAttraction + piezoContact
	deflection = deflectionApproach + deflectionAttraction + deflectionContact

	return piezo, deflection
		
def create_ideal_curve_approach_part(
	parameterMaterial: NamedTuple,
	parameterMeasurement: NamedTuple
) -> Tuple[List, List]: 
	"""

	Parameters:
		parameterMaterial(namedtupel): Contains all parameters describing the material 
									   and geometriy of the virtuell measuring system.
		parameterMeasurement(namedtupel): Contains all parameters describing the virtuell
										  measuring system.

	Returns:
	
	Raises:
		ValueError:
	"""
	piezoApproach = [parameterMeasurement.initialDistance]
	deflectionApproach = [0]

	while(True):
		piezoApproach.append(
			calculate_piezo_value(
				parameterMeasurement.initialDistance,
				parameterMeasurement.distanceInterval,
				len(piezoApproach)
			)
		)
		deflectionApproach.append(
			calculate_deflection_approach_part(
				parameterMaterial.Hamaker,
				parameterMaterial.radius,
				parameterMaterial.kc,
				piezoApproach[-1],
				deflectionApproach[-1]
			)
		)

		if (deflectionApproach[-1] < parameterMaterial.jtc):
			break

	return piezoApproach, deflectionApproach

def create_ideal_curve_attraction_part(
	parameterMeasurement: NamedTuple,
	totalLength: int
) -> Tuple[List, List]: 
	"""

	Parameters:
		parameterMeasurement(namedtupel): Contains all parameters describing the virtuell
										  measuring system.
		totalLength(int): .

	Returns:

	Raises:
		ValueError:
	"""
	piezoAttraction = []
	deflectionAttraction = []

	while(True):
		piezoAttraction.append(
			calculate_piezo_value(
				parameterMeasurement.initialDistance,
				parameterMeasurement.distanceInterval,
				len(piezoAttraction) + totalLength
			)
		)
		deflectionAttraction.append(
			calculate_deflection_attraction_part(
				piezoAttraction[-1]
			)
		)

		if (deflectionAttraction[-1] >= 0):
			break

	return piezoAttraction, deflectionAttraction

def create_ideal_curve_contact_part(
	parameterMaterial: NamedTuple,
	parameterMeasurement: NamedTuple,
	totalLength: int
) -> Tuple[List, List]: 
	"""

	Parameters:
		parameterMaterial(namedtupel): Contains all parameters describing the material 
									   and geometriy of the virtuell measuring system.
		parameterMeasurement(namedtupel): Contains all parameters describing the virtuell
										  measuring system.
		totalLength(int): .

	Returns:

	Raises:
		ValueError:
	"""
	parameterSubstitut = parameterMaterial.kc / (np.sqrt(parameterMaterial.radius) * parameterMaterial.Etot)

	piezoContact = []
	deflectionContact = []

	while(True):
		piezoContact.append(
			calculate_piezo_value(
				parameterMeasurement.initialDistance,
				parameterMeasurement.distanceInterval,
				len(piezoContact) + totalLength
			)
		)
		deflectionContact.append(
			calculate_deflection_contact_part(
				parameterSubstitut,
				piezoContact[-1]
			)
		)

		if (deflectionContact[-1] >= parameterMeasurement.maximumdeflection):
			break

	return piezoContact, deflectionContact

def calculate_piezo_value(
	initialDistance: float,
	distanceInterval: float,
	currentLength: int
) -> float:
	"""Calculate the current piezo value.

	Parameters:
		initialDistance(float): .
		distanceInterval(float): .
		currentLength(int): .

	Returns:
		piezoValue(float): Current piezo value of the ideal curve.
	"""
	return initialDistance + distanceInterval * currentLength

def calculate_deflection_approach_part(
	hamaker: float,
	radius: float, 
	kc: float, 
	currentPiezoValue: float,
	lastDeflectionValue: float
) -> float:
	"""Calculate the current deflection while probe and sample converge,
	   using Hooke's Law and the Hamaker constant.
	
	Parameters:
		hamaker(float): Hamaker value of the given virtual system.
		radius(float): Value for the specified tip radius.
		kc(float): Value for the specified spring constant.
		currentPiezoValue(float): Corresponding piezo value.
		lastDeflectionValue(float): Previous deflection value.

	Returns:
		deflectionValue(float): Current deflection value while probe and
							    sample approach each other.
	"""
	return (
		- (hamaker*radius)
		/ (6*(lastDeflectionValue-currentPiezoValue)**2) 
		* (1/kc)
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
		parameterSubstitut(float): .
		currentPiezoValue(float): Corresponding piezo value.

	Returns:
		deflectionValue(float): Current deflection value while the probe 
							    is in contact.
	"""
	return (
		1 / 3 
		* (
			3 * currentPiezoValue
			- parameterSubstitut**2
		)
		+ calculate_cubic_root(parameterSubstitut, currentPiezoValue)
		/ (3 * np.cbrt(2))
		- (
			np.cbrt(2)
			* (
				6 * parameterSubstitut**2
				* currentPiezoValue
				- parameterSubstitut**4
			)
		)
		/ 3 * calculate_cubic_root(parameterSubstitut, currentPiezoValue)
	)

def calculate_cubic_root(
	parameterSubstitut: float,
	currentPiezoValue: float
) -> float:
	"""Helper function for calculate_deflection_contact_part.

	Parameters:
		parameterSubstitut(float): .
		currentPiezoValue(float): .

	Returns:
		(float): .
	"""
	return np.cbrt(
		- 2 * parameterSubstitut**6
		+ 18 * parameterSubstitut**4
		* currentPiezoValue
		- 27 * parameterSubstitut**2
		* currentPiezoValue**2
		+ 3 * np.sqrt(3)
		* calculate_inner_root(parameterSubstitut, currentPiezoValue)	
	)

def calculate_inner_root(
	parameterSubstitut: float,
	currentPiezoValue: float
) -> float:
	"""Helper function for calculate_cubic_root.

	Parameters:
		parameterSubstitut(float): .
		currentPiezoValue(float): .

	Returns:
		(float): .
	"""
	return np.sqrt(
		27 * parameterSubstitut**4 
		* currentPiezoValue**4 
		- 4 * parameterSubstitut**6 
		* currentPiezoValue**3
	)	

def shift_ideal_curve(
	piezo: List,
	deflection: List,
	parameterForceVolume: NamedTuple
) -> Tuple[np.ndarray, np.ndarray]:
	"""Shift the ideal curve in the x and y direction by applying the 
	   virtual deflection and topography offset.

	Parameters:
		piezo(list): .
		deflection(list): .
		parameterForceVolume(namedtupel): .

	Returns:
		shiftedIdealCurve(tuple): .
	"""
	shiftedPiezo = np.asarray(piezo) + parameterForceVolume.topography
	shiftedDeflection = np.asarray(deflection) + parameterForceVolume.virtualDeflection

	return shiftedPiezo, shiftedDeflection

def multiply_and_apply_noise_to_ideal_curve(
	shiftedDeflection: List, 
	parameterForceVolume: NamedTuple
) -> List[np.ndarray]:
	"""Applies noise of given extent to the shifted deflection of ideal curve, 
	   shiftedDeflection shifted by virtuell shiftedDeflection, piezo is 
	   shifted by topography.

	Parameters:
		shiftedDeflection(list): shifted ideal deflection
		parameterForceVolume(namedtupel): Contains the number of synthetic curves, the noise
										  level and the virtual deflection and topography offset.

	Returns:
		noisyCurves(list): .
	"""
	return [
		apply_noise_to_curve(shiftedDeflection, parameterForceVolume)
		for index in range(parameterForceVolume.numberOfCurves)
	]

def apply_noise_to_curve(
	shiftedDeflection: List, 
	parameterForceVolume: NamedTuple
) -> np.ndarray:
	"""Apply noise to the deflection values of the shifted ideal curve.

	Parameters:
		shiftedDeflection(list): Deflection (y) values of the shifted ideal curve.
		parameterForceVolume(namedtupel): Contains the number of synthetic curves, the noise
										  level and the virtual deflection and topography offset.

	Returns:
		(np.ndarray): .

	Raises:
		ValueError: .
	"""

	try:
		noiseValues = np.random.normal(0, parameterForceVolume.noise, size=len(shiftedDeflection))
	except ValueError:
		raise ValueError("Noise value must be positive.")

	return shiftedDeflection + noiseValues


def arrange_curves_in_force_volume(
	piezo: List,
	deflection: List,  
	shiftedPiezo: np.ndarray, 
	shiftedDeflection: np.ndarray, 
	noisyCurves: List
) -> List[np.ndarray]:
	"""Arrange the ideal curve, the shifted ideal curve and the noisy curves
	   in a force volume.

	Parameters:
		piezo(list): Piezo (x) values of the ideal curve.
		deflection(list): Deflection (y) values of the ideal curve.
		shiftedPiezo(np.ndarray): Piezo (x) values of the shifted ideal curve.
		shiftedDeflection(np.ndarray): Deflection (y) values of the shifted ideal curve.
		noisyCurves(list): .

	Returns:
		forceVolume(np.ndarray): .
	"""
	forceVolume = [
		[shiftedPiezo, oneNoisyCurve]
		for oneNoisyCurve in noisyCurves
	]

	forceVolume.insert(0, [shiftedPiezo, shiftedDeflection])
	forceVolume.insert(0, [piezo, deflection])

	return np.asarray(forceVolume)