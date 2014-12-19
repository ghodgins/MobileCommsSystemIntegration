from libc.stdlib cimport malloc, free, calloc
from libc.string cimport strlen
from libc.stdint cimport uintptr_t

# from networks.h
cdef extern: 
	struct lookup_data:
		float amplitude
		float theta
		float omega

	struct output_data:
		int *key
		int size

	void run_tests()
	
	void build_lookup(lookup_data *lookup, int size)
	void build_gray(unsigned char *table, int num_levels, int size)

	void init_output_data(output_data *output, int key_size)

	void extract(output_data *output, unsigned char *gray_table, char *input, int num_levels)

ctypedef lookup_data* lookup_ptr
ctypedef output_data* output_ptr
ctypedef unsigned char* gray_ptr
ctypedef unsigned char gray_type

def Test():
	run_tests()

cdef class Output_Data:
	cdef output_ptr thisptr

	def __init__(self, size):
		self.thisptr = <output_data*> malloc(sizeof(output_data))
		init_output_data(self.thisptr, size)

	def __dealloc__(self):
		free(self.thisptr)

	def size(self):
		return self.thisptr.size

	def get(self, num):
		if(num < self.thisptr.size):
			return self.thisptr.key[num]

cdef class Lookup_Data:
	cdef lookup_ptr thisptr
	cdef int size

	def __init__(self, size):
		self.thisptr = <lookup_data*> malloc( sizeof(lookup_data) * size )
		self.size = size

	def __dealloc__(self):
		free(self.thisptr)

	def build(self):
		build_lookup(self.thisptr, self.size)

	def get(self, num):
		if(num < self.size):
			return self.thisptr[num]
		return 0

	def output(self):
		for i in xrange(0, self.size):
			print self.thisptr[i].theta
			print self.thisptr[i].amplitude
			print self.thisptr[i].omega

cdef class Gray_Table:
	cdef gray_ptr thisptr
	cdef int s, size, num_levels

	def __init__(self, num_levels, size):
		self.s = (size * num_levels)/8
		self.size = size
		self.num_levels = num_levels
		if(self.s > 0):
			self.thisptr = <gray_ptr> calloc( self.s, sizeof(gray_type))

	def __dealloc__(self):
		free(self.thisptr)

	def build(self):
		build_gray(self.thisptr, self.num_levels, self.size)

	def get(self, num):
		if(num < self.s):
			return self.thisptr[num]
		return 0

	def output(self):
		for i in xrange(0, self.s):
			print format(self.thisptr[i], '02x')

	def get_num_levels(self):
		return self.num_levels

cdef class Modulator:
	cdef Gray_Table gray # = Gray_Table()
	cdef Output_Data output

	def __init__(self, num_levels, size):
		self.gray = Gray_Table(num_levels, size)
		self.gray.build()

	def build(self, char *input):
		self.output = Output_Data( (strlen(input) * 8) / self.gray.get_num_levels())
		extract(self.output.thisptr, 
			self.gray.thisptr, 
			input, self.gray.num_levels)

	def size(self):
		return self.output.size()

	def get(self, s):
		return self.output.get(s)
	