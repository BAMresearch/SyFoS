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

from typing import NamedTuple, Tuple, List

import numpy as np

def calculate_jtc(
	hamaker: float, 
	radius: float, 
	kc: float
) -> float:
	"""Calculate the jtc as

	Parameters:
		hamaker(float): .
		radius(float): .
		kc(float): .

	Returns:
		jtc(float): .
	"""
	return -(
		(
			(hamaker * radius) / (3 * kc)
		)**(1/3)
	)

def calculate_etot(
	poissonRatioProbe: float, 
	eProbe: float, 
	poissonRatioSample: float,
	eSample: float,
) -> float:
	"""Calculate etot as

	Parameters:
		poissonRatioProbe(float): .
		eProbe(float): .
		poissonRatioSample(float): .
		eSample(float): .

	Returns:
		etot(float): .
	"""
	return (
		4 
		/ (3 * ((1 - poissonRatioProbe**2) / eProbe + (1 - poissonRatioSample**2) / eSample))
	)

def calculate_hamaker(
	hamakerProbe: float, 
	hamakerSample: float, 
) -> float:
	"""Calculate hamaker as

	Parameters:
		hamakerProbe(float): .
		hamakerSample(float): .

	Returns:
		hamaker(float): .
	"""
	return np.sqrt(hamakerProbe) * np.sqrt(hamakerSample)

def create_synthetic_force_volume(
	parameterMaterial: NamedTuple, 
	parameterMeasurement: NamedTuple, 
	parameterForceVolume: NamedTuple
) -> np.ndarray:
	"""Create a set of synthetic curves from given parameters, 
	   including a noise level, virtuell deflection and topography offset.

	Parameters:
		parameterMaterial(nametupel): Contains all parameters describing the material 
									  and geometriy of the virtuell measuring system
		parameterMeasuerement(nametupel): 
		parameterForceVolume(nametupel):
	
	Returns:
		syntheticForceVolume(np.ndarray): Set of generated synthetic curves.

	Raises:
		ValueError: . 
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
		deflection, piezo, shiftedPiezo, 
		shiftedDeflection, noisyCurves
	)

	return syntheticForceVolume

def create_ideal_curve(
	parameterMaterial: NamedTuple, 
	parameterMeasurement: NamedTuple
) -> Tuple[List, List]:
	"""

	Parameters:
		parameterMaterial(nametupel): .
		parameterMeasurement(nametupel): .

	Returns:
		piezo(list): .
		deflection(list): . 

	Raises:
		ValueError: . 
	"""
	piezoApproach, deflectionApproach = create_ideal_curve_approach_part(
		parameterMaterial,
		parameterMeasurement
	)

	piezoAttraction, deflectionAttraction = create_ideal_curve_attraction_part(
		parameterMeasurement
	)
	
	piezoContact, deflectionContact = create_ideal_curve_contact_part(
		parameterMaterial,
		parameterMeasurement
	)

	piezo = piezoApproach + piezoAttraction + piezoContact
	deflection = deflectionApproach + deflectionAttraction + deflectionContact

	return piezo, deflection
		
def create_ideal_curve_approach_part(
	parameterMaterial: NamedTuple,
	parameterMeasurement: NamedTuple
) -> Tuple[List, List]: 
	""""""
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
	parameterMeasurement: NamedTuple
) -> Tuple[List, List]: 
	""""""
	piezoAttraction = []
	deflectionAttraction = []

	while(True):
		piezoAttraction.append(
			calculate_piezo_value(
				parameterMeasurement.initialDistance,
				parameterMeasurement.distanceInterval,
				len(piezoAttraction)
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
	parameterMeasurement: NamedTuple
) -> Tuple[List, List]: 
	""""""
	#solutions = solve_contact_equation()

	#a = parameterMaterial.kc / (np.sqrt(parameterMaterial.radius) * parameterMaterial.Etot)
	b = np.sqrt(parameterMaterial.radius) * parameterMaterial.Etot
	kc = parameterMaterial.kc

	piezoContact = []
	deflectionContact = []

	while(deflection[-1] <= parameterMeasurement.maximumdeflection):
		index += 1
		piezo.append(
			calculate_piezo_value(
				parameterMeasurement.initialDistance,
				parameterMeasurement.distanceInterval,
				index
			)
		)
		#x = piezo[-1]
		c = piezo[-1]
		deflection.append(
			calculate_deflection_contact_part(
				#solutions,
				#a,
				#x
				b,
				kc,
				c
			)
		)

	return piezoContact, deflectionContact

def calculate_piezo_value(
	initialDistance: float,
	distanceInterval: float,
	index: int
) -> float:
	""""""
	return initialDistance + distanceInterval * index

def calculate_deflection_approach_part(
	hamaker: float,
	radius: float, 
	kc: float, 
	currentPiezoValue: float,
	lastDeflectionValue: float
) -> float:
	""""""
	return (
		- (hamaker * radius)
		/ (6 * ((lastDeflectionValue - currentPiezoValue) ** 2)) * (1 / kc)
	)

def calculate_deflection_attraction_part(
	currentPiezoValue: float
) -> float:
	""""""
	return currentPiezoValue

def calculate_deflection_contact_part(
	b: float,
	kc: float,
	c: float
) -> float:
	""""""
	return (
		- (kc**2-3*b**2*c)/(3*b**2)-(2**(1/3)*(((6*kc**2*c)
		/ (b**2))-kc**4/b**4))/(3*(-((2*kc**6)/(b**6))
		+ ((18*kc**4*c)/(b**4))-((27*kc**2*c**2)*(b**2))
		+ ((3*np.sqrt(3)*np.sqrt(27*(kc**4)*(b**2)*(c**4)-4*(kc**6)
		* (c**3)))/(b**3))**(1/3)))+(((-((2*kc**6)/(b**6))+((18*(kc**4)*c)
		/ (b**4))-((27*(kc**2)*(c**2))/(b**2))+((3*np.sqrt(3)
		* np.sqrt(27*(kc**4)*(b**2)*(c**4)-4*(kc**6)*(c**3)))
		/ (b**3)))**(1/3)))/(32**(1/3))
	)

def shift_ideal_curve(
	piezo: List,
	deflection: List,
	parameterForceVolume: NamedTuple
) -> Tuple[np.ndarray, np.ndarray]:
	""""""
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
		parameterForceVolume(nametupel): contains numberOfCurves, noise, virtualDeflection and topography

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
	"""applies noise to shiftedDeflection

	Parameters:
		shiftedDeflection(list): shifted ideal deflection
		parameterForceVolume(nametupel): contains numberOfCurves, noise, virtualDeflection and topography

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
	deflection: List, 
	piezo: List, 
	shiftedPiezo: np.ndarray, 
	shiftedDeflection: np.ndarray, 
	noisyCurves: List
) -> List[np.ndarray]:
	"""

	Parameters:
		deflection(list):
		piezo(list):
		shiftedPiezo(np.ndarray):
		shiftedDeflection(np.ndarray):
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