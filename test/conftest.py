from typing import List, Tuple, NamedTuple

import pytest
from pytest_cases import fixture
import numpy as np

import syfos.data_handling.generate_data as gen_data
import syfos.data_handling.analyse_data as analyse_data


@fixture(
	unpack_into="parameterMaterial, parameterMeasurement, parameterForceVolume"
)
def get_parameters_for_synthetic_force_volume() -> Tuple:
	"""Define all parameters for a silicon probe and gold sample setup.

	Returns:
		parameterMaterial(namedtupel): Combines all parameters describing the material 
									   and geometriy of the virtual measuring system.
		parameterMeasurement(namedtupel): Combines all parameters describing the virtual
										  measuring system.
		parameterForceVolume(namedtupel): Combines the number of synthetic curves, the noise
										  level and the virtual deflection and topography offset.
	"""
	ParameterMaterial, ParameterMeasurement, ParameterForceVolume = gen_data.get_parameter_tuples()

	hamaker = gen_data.calculate_hamaker(
		hamkerProbe=66e-21,
		hamakerSample=90e-21
	)
	jtc = gen_data.calculate_jtc(
		hamaker,
		radius=25e-9,
		kc=1
	)
	etot = gen_data.calculate_etot(
		poissonRatioProbe=0.22,
		eProbe=170e9,
		poissonRatioSample=0.42,
		eSample=78e9
	)

	parameterMaterial = ParameterMaterial(
		kc=1,
		radius=25e-9,
		Hamaker=hamaker,
		Etot=etot,
		jtc=jtc,
	)
	parameterMeasurement = ParameterMeasurement(
		startDistance=-10e-9,
		stepSize=0.2e-9,
		maximumPiezo=30e-9,	
	)
	parameterForceVolume = ParameterForceVolume(
		numberOfCurves=1,
		noise=1e-10,
		virtualDeflection=3e-9,
		topography=10e-9
	)

	return parameterMaterial, parameterMeasurement, parameterForceVolume

@fixture(
	unpack_into="syntheticForcevolume"
)
def create_synthetic_test_force_volume(
	parameterMaterial: NamedTuple,
	parameterMeasurement: NamedTuple,
	parameterForceVolume: NamedTuple
) -> List:
	"""Create a synthetic force volume with parameters for
	   a silicon probe and gold sample.
	
	Parameters:
		parameterMaterial(namedtupel): Combines all parameters describing the material 
									   and geometriy of the virtual measuring system.
		parameterMeasurement(namedtupel): Combines all parameters describing the virtual
										  measuring system.
		parameterForceVolume(namedtupel): Combines the number of synthetic curves, the noise
										  level and the virtual deflection and topography offset.

	Returns:
		syntheticForcevolume(np.ndarray): Set of generated synthetic force distance curves.
	"""
	syntheticForcevolume = gen_data.create_synthetic_force_volume(
		parameterMaterial, 
		parameterMeasurement, 
		parameterForcevolume
	)

	return syntheticForcevolume

@fixture(
	unpack_into="realForcevolume"
)
def import_real_force_volume():
	"""Import real data from a from an afm measurment using glass and ... .


	Returns
		realForceVolume(np.ndarray): .
	"""
	pass

@fixture(
	unpack_into="syntheticApproachParameters, syntheticContactParameters"
)
def get_parameters_synthetic_force_volume(
	syntheticForcevolume: np.ndarray
) -> Tuple:
	"""

	Parameters:
		syntheticForcevolume(np.ndarray): Set of generated synthetic force distance curves.

	Returns: 
		approachParameters(tuple): .
		contactParameters(tuple): .
	"""
	idealCurve = syntheticForcevolume[0]

	approachParameters, contactParameters = analyse_data.calculate_ideal_curve_parameters(idealCurve)

	return approachParameters, contactParameters

@fixture(
	unpack_into="realApproachParameters, realContactParameters"
)
def get_parameters_real_force_volume(
	realForcevolume
) -> Tuple:
	"""

	Parameters:
		realForcevolume(np.ndarray): .

	Returns: 
		approachParameters(tuple): .
		contactParameters(tuple): .
	"""
	approachParameters, contactParameters = analyse_data.calculate_ideal_curve_parameters(realForcevolume)

	return approachParameters, contactParameters