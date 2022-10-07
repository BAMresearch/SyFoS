import pytest
from pytest_cases import fixture
import numpy as np

import syfos.data_handling.generate_data as gen_data
#import syfos.data_handling.analyse_data as analyse_data

'''
@fixture(
	unpack_into="parameterMaterial, parameterMeasurement, parameterForceVolume"
)
def get_parameters_for_synthetic_force_volume():
	""""""
	ParameterMaterial, ParameterMeasurement, ParameterForceVolume = gen_data.get_parameter_tuples()

	hamaker = gen_data.calculate_hamaker(
		hamkerProbe=0,
		hamakerSample=0
	)
	jtc = gen_data.calculate_jtc(
		hamaker,
		radius=0,
		kc=0
	)
	etot = gen_data.calculate_etot(
		poissonRatioProbe=0,
		eProbe=0,
		poissonRatioSample=0,
		eSample=0
	)

	parameterMaterial = ParameterMaterial(
		kc=0,
		radius=0,
		Hamaker=hamaker,
		Etot=etot,
		jtc=jtc,
	)
	parameterMeasurement = ParameterMeasurement(
		initialDistance=0,
		distanceInterval=0,
		maximumdeflection=0,	
	)
	parameterForceVolume = ParameterForceVolume(
		numberOfCurves=4,
		noise=0,
		virtualDeflection=0,
		topography=0
	)

	return parameterMaterial, parameterMeasurement, parameterForceVolume

@fixture(
	unpack_into="syntheticForcevolume"
)
def create_synthetic_test_force_volume(
	parameterMaterial,
	parameterMeasurement,
	parameterForceVolume
):
	""""""
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
	"""Import real data from a from a measurment using glass and ... ."""
	pass
	realForceVolume = 0

	return realForceVolume

@fixture(
	unpack_into="syntheticApproachParameters, syntheticContactParameters"
)
def get_parameters_synthetic_force_volume(
	syntheticForcevolume
):
	""""""
	approachParameters, contactParameters = analyse_data.extraxt_parameters(syntheticForcevolume)

	return approachParameters, contactParameters

@fixture(
	unpack_into="realApproachParameters, realContactParameters"
)
def get_parameters_real_force_volume(
	realForcevolume
):
	""""""
	approachParameters, contactParameters = analyse_data.extraxt_parameters(realForcevolume)

	return approachParameters, contactParameters
'''