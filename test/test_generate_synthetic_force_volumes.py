import pytest
import numpy as np

import synthetic_force_volumes.generate_synthetic_force_volumes as gsfv

def test_calculate_jtc():
	"""."""
	hamaker = 6
	radius = 4
	kd = 1

	result = gsfv.calculate_jtc(
		hamaker, 
		radius, 
		kd
	)
	
	assert np.isclose(result, -2.0)