from abc import ABC, abstractmethod
from enum import Enum


class Signal(ABC):
	@abstractmethod
	def generate(self):
		"""generate data"""



class Ofdm(Signal):
	def generate(self):
		return 'ofdm generated'


class Sine(Signal):
	def generate(self):
		return 'sine generated'


class Qam(Signal):
	def generate(self):
		return 'qam generated'


# some sort of controller or DATABASE
class VariantDB(Enum):
	ofdm = Ofdm
	qam = Qam
	sine = Sine
	metadata = 4


user_input = 'qam'

output = VariantDB[user_input].value()
# print(output.generate())

# print(VariantDB(4))


class Abstractfromatter(ABC):
	def format(self):
		"""This is what formatter does, duh..."""


class Mailformatter(Abstractfromatter):
	def format(self, something: str) -> str:
		return f'{something}@mailaddress.com'


class Bingoformatter(Abstractfromatter):
	def format(self, something: str) -> str:
		return f'{something} just got bingo!'


def format_applyer(something: str, formatter: Abstractfromatter) -> str:
	_formatter = formatter()
	result = _formatter.format(something)
	return result



something = 'Jane'
print(format_applyer(something, Mailformatter))



from pydantic import BaseModel, Field


class User(BaseModel):
	name: str = Field(default='Jane')
	age: int = Field(ge=0, le=60, default=25)

user = User(name='Andrew', age=51)
print(user.name)
print(user.age)

from typing import Callable


class superdecorator:
	def __init__(self, limit: int = 50) -> None:
		self.limit = limit

	def __call__(self, func: Callable) -> Callable:
		def wrapper(*args, **kwargs):
			print(f'some operation with {self.limit}')
			func(*args, **kwargs)

		return wrapper


@superdecorator(limit=13)
def show_something(a):
	print(f'something with {a}')

show_something('ffffffffffffff')