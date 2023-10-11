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


# this thing is going to be exported
op_dispatcher = OperationsDispatcher()


if __name__ == '__main__':
	print(op_dispatcher)