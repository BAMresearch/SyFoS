import numpy as np

def create_synthetic_curve(
	parameterMaterial, 
	parameterMeasurement, 
	parameterForcevolume
):
	"""Creates a set of synthetic curves from given parameters, including a noise level, virtuell deflection and topography offset.

	Parameters:
		parameterMaterial(nametupel): contains all parameters describing the material and geometriy of the virtuell measuring system
		parameterMeasuerement(nametupel): 
		parameterForcevolume(nametupel):
	
	Returns:
		syntheticForcevolume(np.ndarray): set of synthetic curves from given parameters, including a noise level, virtuell deflection and topography offset
	"""
	piezo, deflection = create_ideal_curve(parameterMaterial, parameterMeasurement)
	
	shiftedPiezo = np.asarray(piezo) + parameterForcevolume.topography
	shiftedDeflection = np.asarray(deflection) + parameterForcevolume.virtualDeflection

	noisyCurves = multiply_and_apply_noise_to_ideal_curve(
		shiftedDeflection, parameterForcevolume
	)
	
	syntheticForcevolume = arrange_curves_in_forcevolume(
		deflection, piezo, shiftedPiezo, 
		shiftedDeflection, noisyCurves
	)

	return syntheticForcevolume

def create_ideal_curve(
	parameterMaterial, 
	parameterMeasurement
):
	""""""
	deflection = [0]
	piezo = [parameterMeasurement.Z0]
	index = 0
	# Create curve until the jtc.
	while(deflection[-1] >= parameterMaterial.jtc):
		index += 1
		piezo.append(parameterMeasurement.Z0 + parameterMeasurement.dZ * index)
		deflection.append(
			- (parameterMaterial.Hamaker * parameterMaterial.radius)
			/ (6 * ((deflection[-1] - piezo[-1]) ** 2)) * (1 / parameterMaterial.kc)
		)

	index -= 1
	piezo = piezo[:-1]
	deflection = deflection[:-1]

	# Create curve until the poc.
	while(deflection[index] <= 0):
		index += 1
		piezo.append(parameterMeasurement.Z0 + parameterMeasurement.dZ * index)
		deflection.append(piezo[index])
	
	b = np.sqrt(parameterMaterial.radius) * parameterMaterial.Etot
	kc = parameterMaterial.kc

	# Create contact line until trigger.
	while(deflection[-1] <= parameterMeasurement.maximumdeflection):
		index += 1
		piezo.append(parameterMeasurement.Z0 + parameterMeasurement.dZ * index)
		c = piezo[-1]
		deflection.append(
			- (kc ** 2 - 3*b**2*c)/(3*b**2)-(2**(1/3)*(((6*kc**2*c)
			/ (b**2))-kc**4/b**4))/(3*(-((2*kc**6)/(b**6))
			+ ((18*kc**4*c)/(b**4))-((27*kc**2*c**2)*(b**2))
			+ ((3*np.sqrt(3)*np.sqrt(27*(kc**4)*(b**2)*(c**4)-4*(kc**6)
			* (c**3)))/(b**3))**(1/3)))+(((-((2*kc**6)/(b**6))+((18*(kc**4)*c)
			/ (b**4))-((27*(kc**2)*(c**2))/(b**2))+((3*np.sqrt(3)
			* np.sqrt(27*(kc**4)*(b**2)*(c**4)-4*(kc**6)*(c**3)))
			/ (b**3)))**(1/3)))/(32**(1/3))	
		)
		
	return piezo, deflection

def multiply_and_apply_noise_to_ideal_curve(
	shiftedDeflection, 
	parameterForcevolume
):
	"""applies noise of given extent to shiftedDeflection of ideal curve, shiftedDeflection shifted by virtuell shiftedDeflection, piezo is shifted by topography

	Parameters:
		shiftedDeflection(list): shifted ideal deflection
		parameterForcevolume(nametupel): contains numberOfCurves, noise, virtualDeflection and topography

	Returns:
		noisyCurves
	"""
	return [
		apply_noise_to_curve(shiftedDeflection, parameterForcevolume)
		for index in range(parameterForcevolume.numberOfCurves)
	]

def apply_noise_to_curve(
	shiftedDeflection, 
	parameterForcevolume
) -> np.ndarray:
	"""applies noise to shiftedDeflection

	Parameters:
		shiftedDeflection(list): shifted ideal deflection
		parameterForcevolume(nametupel): contains numberOfCurves, noise, virtualDeflection and topography

	Returns:
		one noisy curve
	"""

	noiseValues = np.random.normal(0, parameterForcevolume.noise, size=len(shiftedDeflection))
	return shiftedDeflection + noiseValues


def arrange_curves_in_forcevolume(
	deflection, 
	piezo, 
	shiftedPiezo, 
	shiftedDeflection, 
	noisyCurves
) -> np.ndarray:
	"""

	Parameters:
		deflection
		piezo
		shiftedPiezo
		shiftedDeflection
		noisyCurves

	Returns:
		forceVolume(np.ndarray): .
	"""

	forceVolume = [
		np.column_stack((shiftedPiezo, oneNoisyCurve))
		for oneNoisyCurve in noisyCurves
	]

	forceVolume.insert(0, np.column_stack((shiftedPiezo, shiftedDeflection)))
	forceVolume.insert(0, np.column_stack((piezo, deflection)))

	return forceVolume