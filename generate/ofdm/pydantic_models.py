"""
The module provides models for the request to API.
The models make parameters validation of boundary values
"""

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
