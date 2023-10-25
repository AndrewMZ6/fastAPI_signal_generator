"""
The module provides controller of MVC model. 
Instance of OperationsDispatcher class makes processing of a request
based on request model attributes.

The dispatcher is able to generate complex or real valued
of signal, depending of the request attrs. The functions for 
signal generation are imported from 'data_processing' module.
"""

from pathlib import Path
import sys
path = Path().cwd().parent
sys.path.append(str(path))

from data_processing.process_data import ofdm_fft_morder_bw_fs_fc, ofdm_fft_morder, np_complex_arr_to_json


def real_valued_handler(request_parameters: dict):
	fftsize = request_parameters.fftsize
	morder = request_parameters.morder
	bw = request_parameters.bandwidth
	fs = request_parameters.fs
	fc = request_parameters.fc
	result = ofdm_fft_morder_bw_fs_fc(
										fftsize,
										morder,
										bw,
										fs,
										fc
									)
	
	return result


def complex_valued_handler(request_parameters: dict):
	fftsize = request_parameters.fftsize
	morder = request_parameters.morder
	result = ofdm_fft_morder(fftsize, morder)

	return np_complex_arr_to_json(result)


class OperationsDispatcher:
	def _decision_maker(self, request_parameters: dict):
		if hasattr(request_parameters, 'fc'):							# not sofisticated at all :)
			return real_valued_handler
		return complex_valued_handler

	def _apply_handler(self, request_parameters, handler):
		result = handler(request_parameters)
		return result

	def generate(self, request_parameters: dict):
		handler = self._decision_maker(request_parameters)
		result = self._apply_handler(request_parameters, handler)
		return result


# the instance is going to be exported
op_dispatcher = OperationsDispatcher()
