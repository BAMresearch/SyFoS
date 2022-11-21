from typing import List, Tuple, NamedTuple

import pytest
from pytest_cases import fixture
import numpy as np

import syfos.data_handling.generate_data as gen_data
import syfos.data_handling.analyse_data as analyse_data

@pytest.fixture
def simple_ideal_curve() -> List:
	"""Define a simple ideal curve.

	Returns
		simpleIdealCurve(list): Piezo (x) and deflection (y) values
							    of a simple ideal curve.
	"""
	piezoValues = np.array([-6.0, -5.0, -4.0, -3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0])
	deflectionValues = np.array([0.0, -0.1, 0.2, -2.2, -2.5, -1.2, 0.0, 1.0, 2.5, 4.0])

	return [piezoValues, deflectionValues]

@pytest.fixture
def simple_ideal_curve_approach_part() -> List:
	"""Define the approach part of a simple ideal curve.

	Returns
		simpleIdealCurveApproach(list): Piezo (x) and deflection (y) values
									    from the approach part of a simple
									    ideal curve.
	"""
	piezoApproach = np.array([-6.0, -5.0, -4.0])
	deflectionApproach = np.array([0.0, -0.1, 0.2])

	return [piezoApproach, deflectionApproach]

@pytest.fixture
def simple_ideal_curve_contact_part() -> List:
	"""Define the contact part of a simple ideal curve.

	Returns
		simpleIdealCurveContact(list): Piezo (x) and deflection (y) values
									   from the contact part of a simple
									   ideal curve.
	"""
	piezoContact = np.array([0.0, 1.0, 2.0, 3.0])
	deflectionContact = np.array([0.0, 1.0, 2.5, 4.0])

	return [piezoContact, deflectionContact]

@fixture(
	unpack_into="trueDistance, forceApproach, forceContact, deformation"
)
def simple_ideal_curve_adjusted_values() -> Tuple: 
	"""Define simple adjusted parameters from an ideal curve.

	Returns:
		trueDistance(float): Adjusted x value of the approach part.
		forceApproach(float): Adjusted y value of the approach part.
		forceContact(float): Adjusted x value of the contact part.
		deformation(float): Adjusted y value of the contact part.
	"""
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
	"""Define parameters from a default silicon/silicon setup.

	Returns:
		radius(float): Default value for the probe's radius.
		kc(float): Default value for the probe's spring constant.
		etot(float): Reduced modulus value from a silicon/silicon setup.
		hamaker(float): Combined hamaker value from a silicon/silicon setup.
	"""
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
	unpack_into="syntheticApproachParameters, syntheticContactParameters"
)
def get_parameters_synthetic_force_volume(
	syntheticForcevolume: np.ndarray
) -> Tuple:
	"""Calculate the theoretical parameters kc, radius, 
	   hamaker and etot from the ideal curve of the 
	   synthetic force volume.

	Parameters:
		syntheticForcevolume(np.ndarray): Set of generated synthetic force distance curves
										  from a silicon/gold setup.

	Returns: 
		approachParameters(tuple): Contains the theoretical values for kc, 
								   radius and hamaker for every point of 
								   the approach part of the ideal curve.
		contactParameters(tuple): Contains the theoretical values for kc, 
								   radius and etot for every point of 
								   the contact part of the ideal curve.
	"""
	idealCurve = syntheticForcevolume[0]

	approachParameters, contactParameters = analyse_data.calculate_ideal_curve_parameters(idealCurve)

	return approachParameters, contactParameters