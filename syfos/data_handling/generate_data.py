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

from sympy.solvers import solve
from sympy import Symbol

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
		raise ValueError(
			"Could not create a synthetic force volume due to negative noise value."
		) from error
	
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
	deflection = [0]
	piezo = [parameterMeasurement.initialDistance]
	index = 0
	
	index = create_ideal_curve_approach_part(
		piezo,
		deflection,
		index,
		parameterMaterial,
		parameterMeasurement
	)

	index -= 1
	piezo = piezo[:-1]
	deflection = deflection[:-1]

	index = create_ideal_curve_attraction_part(
		piezo,
		deflection,
		index,
		parameterMeasurement
	)
	
	create_ideal_curve_contact_part(
		piezo,
		deflection,
		index,
		parameterMaterial,
		parameterMeasurement
	)

	return piezo, deflection
		
def create_ideal_curve_approach_part(
	piezo: List,
	deflection: List,
	index: int,
	parameterMaterial: NamedTuple,
	parameterMeasurement: NamedTuple
)-> None: 
	""""""
	while(deflection[-1] >= parameterMaterial.jtc):
		index += 1
		piezo.append(
			calculate_piezo_value(
				parameterMeasurement.initialDistance,
				parameterMeasurement.distanceInterval,
				index
			)
		)
		deflection.append(
			calculate_deflection_approach_part(
				parameterMaterial.Hamaker,
				parameterMaterial.radius,
				parameterMaterial.kc,
				piezo[-1],
				deflection[-1]
			)
		)

	return index

def create_ideal_curve_attraction_part(
	piezo: List,
	deflection: List,
	index: int,
	parameterMeasurement: NamedTuple
)-> None: 
	""""""
	while(deflection[index] <= 0):
		index += 1
		piezo.append(
			calculate_piezo_value(
				parameterMeasurement.initialDistance,
				parameterMeasurement.distanceInterval,
				index
			)
		)
		deflection.append(
			calculate_deflection_attraction_part(
				piezo[-1]
			)
		)

	return index

def create_ideal_curve_contact_part(
	piezo: List,
	deflection: List,
	index: int,
	parameterMaterial: NamedTuple,
	parameterMeasurement: NamedTuple
)-> None: 
	""""""
	#solutions = solve_contact_equation()

	a = parameterMaterial.kc / (np.sqrt(parameterMaterial.radius) * parameterMaterial.Etot)

	while(deflection[-1] <= parameterMeasurement.maximumdeflection):
		index += 1
		piezo.append(
			calculate_piezo_value(
				parameterMeasurement.initialDistance,
				parameterMeasurement.distanceInterval,
				index
			)
		)
		x = piezo[-1]
		deflection.append(
			calculate_deflection_contact_part_slow(
				#solutions,
				a,
				x
			)
		)

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

def solve_contact_equation(): 
	""""""
	a = Symbol("argument1")
	b = Symbol("argument2")
	c = Symbol("res")

	return solve((a-c)**(3/2) / c - b,  exclude=[a, b])

def calculate_deflection_contact_part_fast(
	solutions,
	a,
	x
):
	""""""
	a = Symbol("argument1")
	b = Symbol("argument2")
	"""
	for solution in solutions:
		solution.subs([(a, x), (b, a)])
	"""
	for solution in solutions:
		result = solution.subs([(a, x), (b, a)])
		if np.isscalar(result):
			return result
		print(result)

	return 0

def calculate_deflection_contact_part_slow(
	a,
	x
):
	""""""
	y = Symbol("y")
	res = solve((x-y)**(3/2) / y - a, y)
	
	if len(res) > 0:
		return res[0]

	return 0

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