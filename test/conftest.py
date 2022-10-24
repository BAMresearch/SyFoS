from typing import List, Tuple, NamedTuple

import pytest
from pytest_cases import fixture
import numpy as np

import syfos.data_handling.generate_data as gen_data
import syfos.data_handling.analyse_data as analyse_data

@pytest.fixture
def simple_ideal_curve() -> List:
	""""""
	piezoValues = np.array([-6.0, -5.0, -4.0, -3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0])
	deflectionValues = np.array([0.0, -0.1, 0.2, -2.2, -2.5, -1.2, 0.0, 1.0, 2.5, 4.0])

	return [piezoValues, deflectionValues]

@pytest.fixture
def simple_ideal_curve_approach_part() -> List:
	""""""
	piezoApproach = np.array([-6.0, -5.0, -4.0])
	deflectionApproach = np.array([0.0, -0.1, 0.2])

	return [piezoApproach, deflectionApproach]

@pytest.fixture
def simple_ideal_curve_contact_part() -> List:
	""""""
	piezoContact = np.array([0.0, 1.0, 2.0, 3.0])
	deflectionContact = np.array([0.0, 1.0, 2.5, 4.0])

	return [piezoContact, deflectionContact]

@fixture(
	unpack_into="trueDistance, forceApproach, forceContact, deformation"
)
def simple_ideal_curve_values() -> Tuple: 
	""""""
	trueDistance = -4.0
	forceApproach = 0.2
	forceContact = 2.0
	deformation = 2.5

	return (
		trueDistance,
		forceApproach,
		forceContact,
		deformation
	)

@fixture(
	unpack_into="radius, kc, etot, hamaker"
)
def default_silicon_to_silicon_parameters() -> Tuple: 
	""""""
	radius = 25e-9
	kc = 1
	etot = 1.2e+11
	hamaker = 6.6e-20

	return (
		radius,
		kc,
		etot,
		hamaker
	)

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