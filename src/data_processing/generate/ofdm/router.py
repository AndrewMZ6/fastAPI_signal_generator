from fastapi import APIRouter, Path as fastApiPath
from typing_extensions import Annotated

from .pydantic_models import FftsizeMorder, RealValuedRequest
from services.operations_dispatcher import op_dispatcher as operations_dispatcher


router = APIRouter()


@router.get('/complex/fftsize/{fftsize}/morder/{modulation_order}')
async def get_ofdm_no_pilots(
								fftsize: Annotated[int, fastApiPath(ge=0, le=50000)], 
								modulation_order: Annotated[int, fastApiPath(ge=4, le=256)]
							):

	request_parameters = FftsizeMorder(fftsize=fftsize, morder=modulation_order)
	response = operations_dispatcher.generate(request_parameters)

	return response


@router.get('/real/fftsize/{fftsize}/morder/{modulation_order}/bw/{BW}/fs/{fs}/fc/{fc}')
async def get_ofdm_fft_bw_fs(
								fftsize: int,
								modulation_order: int,
								BW: float,
								fs: float,
								fc: float
							):
	request_parameters = RealValuedRequest(
		fftsize=fftsize,
		morder=modulation_order,
		bandwidth=BW,
		fs=fs,
		fc=fc
	)
	response = operations_dispatcher.generate(request_parameters)

	return response
