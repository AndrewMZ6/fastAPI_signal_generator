from data_processing import ofdm_fft_morder_bw_fs_fc, ofdm_fft_morder


def real_valued_handler(request_parameters: dict):
	fftsize = request_parameters['fftsize']
	morder = request_parameters['modulation_order']
	bw = request_parameters['bw']
	fs = request_parameters['fs']
	fc = request_parameters['fc']
	result = ofdm_fft_morder_bw_fs_fc(
										fftsize,
										morder,
										bw,
										fs,
										fc
									)
	return result


def complex_valued_handler(request_parameters: dict):
	fftsize = request_parameters['fftsize']
	morder = request_parameters['modulation_order']
	result = ofdm_fft_morder(fftsize, morder)
	return result


class OparationsDispatcher:

	def _decision_maker(self, request_parameters: dict):
		L = list(request_parameters.keys())
		if 'fc' in L:							# not sofisticated at all :)
			return real_valued_handler
		return complex_valued_handler

	def _apply_handler(self, request_parameters, handler):
		result = handler(request_parameters)
		return result


	def generate(self, request_parameters: dict):
		handler = self._decision_maker(request_parameters)
		result = self._apply_handler(request_parameters, handler)
		return result


# this thing is going to be exported
opertations_dispatcher = OparationsDispatcher()