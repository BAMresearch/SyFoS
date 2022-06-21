from collections import namedtuple

import pytest
import numpy as np

import syfos.generate_synthetic_force_volumes as gsfv

def test_arrange_curves_in_forcevolume():
	""""""
	pass

def get_simple_test_parameters():
	""""""
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
			"Z0",
			"dZ",
			"maximumdeflection"
		]
	)
	ParameterForcevolume = namedtuple(
		"parameterForcevolume",
		[
			"numberOfCurves",
			"noise",
			"virtualDeflection",
			"topography"
		]
	)

	parameterMaterial = ParameterMaterial(
		kc=1,
		radius=1,
		Hamaker=1,
		Etot=1,
		jtc=1,
	)
	parameterMeasurement = ParameterMeasurement(
		Z0=1,
		dZ=1,
		maximumdeflection=1,	
	)
	parameterForcevolume = ParameterForcevolume(
		numberOfCurves=1,
		noise=1,
		virtualDeflection=1,
		topography=1
	)

	return parameterMaterial, parameterMeasurement, parameterForcevolume

def extraxt_parameters(forcevolume):
	""""""
	pass

def test_create_synthetic_force_volume():
	""""""
	pass
	"""
	parameterMaterial, parameterMeasurement, parameterForcevolume = get_simple_test_parameters()

	syntheticForcevolume = gsfv.create_synthetic_force_volume(
		parameterMaterial, 
		parameterMeasurement, 
		parameterForcevolume
	)

	extractedParameters = extraxt_parameters(syntheticForcevolume)

	np.testing.assert_allclose(
		[parameterMaterial.Hamaker, parameterMaterial.Etot, parameterMaterial.jtc], 
		[extractedParameters.Hamaker, extractedParameters.Etot, extractedParameters.jtc], 
		rtol=1e-5, 
		atol=0
	)
	"""