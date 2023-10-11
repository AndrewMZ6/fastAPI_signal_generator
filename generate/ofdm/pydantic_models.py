from pydantic import BaseModel, Field


class FftsizeMorder(BaseModel):
	fftsize: int = Field(gt=0, lt=100000)
	morder: int = Field(ge=4, le=256)



class RealValuedRequest(BaseModel):
	fftsize: int = Field(gt=0, lt=100000)
	morder: int = Field(ge=4, le=256)
	bandwidth: int = Field(gt=0, lt = 10e7)
	fs: int = Field(gt=0)
	fc: int = Field(gt=0)



if __name__ == '__main__':
	FftsizeMorder(fftsize=1024, morder=1116)