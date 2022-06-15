from collections import namedtuple

import pytest
import numpy as np

import synthetic_force_volumes.generate_synthetic_force_volumes as gsfv

def get_parameters_sampleMat_tipMat():
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

def test_arrange_curves_in_forcevolume():
	""""""
	pass

def test_create_synthetic_force_volume():
	""""""
	parameterMaterial, parameterMeasurement, parameterForcevolume = get_parameters_sampleMat_tipMat()

	syntheticForcevolume = gsfv.create_synthetic_force_volume(
		parameterMaterial, 
		parameterMeasurement, 
		parameterForcevolume
	)

	#calculatedParameters = 