class MyDescriptor:
	def __get__(self, instance_object, instances_class):
		print('__get__ begins --------------------------')
		print(f'{instance_object = }')
		print(f'{instance_object.z = }')
		print(f'{__class__.__name__} __get__ method')
		print('__get__ ends --------------------------')
		return instance_object._myattr

	def __set__(self, instance_object, set_value):
		print('__set__ begins --------------------------')
		print(f'{instance_object = }, {set_value = }')
		print(f'{__class__.__name__} __set__ method')
		instance_object._myattr = set_value
		print('__set__ ends --------------------------')

	def __del__(self):
		print(f'{__class__.__name__} __del__ method')

class MyClass:
	myattr = MyDescriptor()
	z = 91

	def __init__(self, myattr_value):
		self.myattr = myattr_value		# when the instance of MyClass initialized the __set__ method of the descriptor is called




if __name__ == '__main__':
	m = MyClass('ello')
	print(m.myattr)
	m.myattr = 3
	print(m)
	print(m.myattr)
	print(f'{m._myattr = }')