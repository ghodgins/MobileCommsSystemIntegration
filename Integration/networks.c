//clang -o networks.o networks.c
#include "networks.h"

#define GET_GRAY_VAL(i, num_levels) ( ( i ^ (i >> 1) ) << (i*num_levels) )
#define GET_GRAY_AT(i, j, num_levels) ( ( i ^ (i >> 1) ) << (j*num_levels) )
#define GET_AT(input, i, mask) (*input >> i) & mask
#define GET_GRAY(input, i, mask, num_levels, gray_table) ( ( gray_table >> ( ( GET_AT(input, i, mask) ) * num_levels ) ) & mask )

void build_gray_table8(char *table, int num_levels)
{
	int size = pow(2, num_levels);
	SIZE_EXCEPTION_CHECK(size*num_levels, 8);
	for(int i = 0; i < size; i++)
		*table |= GET_GRAY_VAL(i, num_levels);
}

void build_gray_table32(int32_t *table, int num_levels)
{
	int size = pow(2, num_levels);
	SIZE_EXCEPTION_CHECK(size*num_levels, 32);
	for(int i = 0; i < size; i++)
		*table |= GET_GRAY_VAL(i, num_levels);
}

// don't trust this..! Google can't print 64bit binary :P
// Alternative -> from Hacker's Delight, pg. 313
// binary abcd -> gray efgh
// e = a
// f = a ^ b
// g = b ^ c
// h = c ^ d
void build_gray_table64(int64_t *table, int num_levels)
{
	int size = pow(2, num_levels);
	SIZE_EXCEPTION_CHECK(size*num_levels, 64);
	for(int i = 0; i < size; i++)
		*table |= GET_GRAY_VAL(i, num_levels);
}

// THE ONLY ONE THAT MATTERS
void build_gray(unsigned char *table, int num_levels, int size)
{
	int num_req = (size * num_levels)/8;
	int diff = 8/num_levels;
	//printf("Size: %i Num Char: %i\n", size, num_req);
	for(int i = 0; i <= num_req; i++) {
		for(int j = 0; j < diff; j++)
			table[ i ] |= GET_GRAY_AT( (i*diff + j) , j, num_levels);	
			//printf("i: %i, ", i);		
			//PRINT_HEX(table[i]);
	}
	//for(int i = 0; i < num_req; i++)
	//	PRINT_HEX(table[i]);
}

void init_output_data(struct output_data *output, int key_size)
{
	output->size = 0; //key_size;
	output->key = (int*) malloc(sizeof(int) * key_size);
}

void init_lookup_data(struct lookup_data *val, float a, float t, float o)
{
	val->amplitude = a;
	val->theta = t;
	val->omega = o;
}

void build_qam(struct lookup_data *lookup, int size, int num_a, int max_amp)
{
	float q = 360/ (float) size; // theta

	// Don't know best way to decide on start point.
	float a_diff = 1/ (float) num_a;
	float a_min = a_diff/2; // start offset > 25% at 16 QAM
	//a_diff *= max_amp;

	float q_max = 360;
	int n = size/num_a;
	for(int i = 0; i < num_a; i++) {

		float amp = a_min + (a_diff * i); // check this.

		for(int j = 0; j < n; j++) {
			q_max -= q;
			init_lookup_data(&lookup[i*n + j], amp, q_max, 2 * PI/f);
		}
	}
}

// This isn't a nice function, but I can't see a way to correctly generate the voltages for QAM
void build_qam16(struct lookup_data *lookup, int min, int mid, int max)
{
	init_lookup_data(&lookup[0], min, -135, 2* PI/f);

	init_lookup_data(&lookup[1], mid, -165, 2* PI/f);

	init_lookup_data(&lookup[2], min, -45, 2* PI/f);

	init_lookup_data(&lookup[3], mid, -15, 2* PI/f);
	init_lookup_data(&lookup[4], mid, -105, 2* PI/f);

	init_lookup_data(&lookup[5], max, -135, 2* PI/f);

	init_lookup_data(&lookup[6], mid, -75, 2* PI/f);

	init_lookup_data(&lookup[7], max, -45, 2* PI/f);

	// Inv
	init_lookup_data(&lookup[8], min, 135, 2* PI/f);

	init_lookup_data(&lookup[9], mid, 165, 2* PI/f);

	init_lookup_data(&lookup[10], min, 45, 2* PI/f);

	init_lookup_data(&lookup[11], mid, 15, 2* PI/f);
	init_lookup_data(&lookup[12], mid, 105, 2* PI/f);

	init_lookup_data(&lookup[13], max, 135, 2* PI/f);

	init_lookup_data(&lookup[14], mid, 75, 2* PI/f);

	init_lookup_data(&lookup[15], max, 45, 2* PI/f);
}

void build_lookup(struct lookup_data *lookup, int size)
{
	float q = 360/ (float) size; // theta
	for(int i = 0; i < size; i++) {
		init_lookup_data(&lookup[i], 1.f, q - q*i, PI/2.f);//2*PI/f);
	}
	return;
}

int build_mask(int num_levels)
{
	int mask = 0;
	for(int i = 0; i < num_levels; i++) {
		mask = (mask << 1) + 1;
	}
	return mask;
}

void print_lookup_data(struct lookup_data *val)
{
	printf("Amplitude: %f\n", val->amplitude);
	printf("Theta: %f\n", val->theta);
	printf("Omega: %f\n", val->omega);
}

// Testing

void mask_test(int size, int lookup[])
{
	for(int i = 0; i < size; i++)
	{
		//int res = build_mask(i+1);
		//PRINT_HEX(res);
		assert(build_mask(i+1) == lookup[i]);
	}
	return;
}

void run_tests()
{
	printf("Testing mask.\n");
	int lookup[] = { 0x1, 0x3, 0x7, 0xf, 0x1f, 0x3f, 0x7f, 0xff};
	mask_test(8, lookup);

	// 2 bit gray encoding.
	printf("Testing 2 bit Gray Code.\n");
	char gray[1]; 
	gray[0] = 0x0;
	build_gray(gray, 2, 4);

	assert( (gray[0] & 0x03) == 0x00);
	assert( (gray[0] & 0x0c) == 0x04);
	assert( (gray[0] & 0x30) == 0x30);
	assert( (gray[0] & 0xc0) == 0x80);

	// 4 bit gray encoding
	printf("Testing 4 bit Gray Code.\n");
	char gray4[8];
	for(int i = 0; i < 8; i++)
		gray4[i] = 0x0;

	build_gray(gray4, 4, 16);

	assert( (gray4[0] & 0xff) == 0x10 ); // 0b 0001 0000
	assert( (gray4[1] & 0xff) == 0x23 ); // 0b 0010 0011	
	assert( (gray4[2] & 0xff) == 0x76 ); // 0b 0111 0110
	assert( (gray4[3] & 0xff) == 0x45 ); // 0b 0100 0101
	assert( (gray4[4] & 0xff) == 0xdc ); // 0b 1101 1100
	assert( (gray4[5] & 0xff) == 0xef ); // 0b 1110 1111	
	assert( (gray4[6] & 0xff) == 0xba ); // 0b 1011 1010	
	assert( (gray4[7] & 0xff) == 0x89 ); // 0b 1000 1001	

	// TO DO QAM tests.
}

int main(int argc, char **argv)
{
	run_tests();

	/*
	// 32 QAM
	struct lookup_data *lookup = (struct lookup_data*) malloc(16 * sizeof(struct lookup_data));
	build_qam(lookup, 16, 2, 2);

	printf("Loopup:\n");
	for(int i = 0; i < 16; i++)
	{
		printf("%f, %f\n", lookup[i].amplitude, lookup[ i ].theta);
	}
	return 0;
	*/
	/*
	if(argc != 3) {
		printf("No arguments found!\n"
			"Expected: \n\t(int)  num_levels"
			"\n\t(char *) buffer \n");
		return -1;
	}

	num_levels = atoi( argv[1] );
	if(num_levels%2 != 0)
		printf("Warning: Number of levels used is not divisible by 2.\n");
	int size = pow(2, num_levels);
	
	char *input = argv[2];

	char *gray_table = (char *) calloc( (size * num_levels)/8, sizeof(char) );
	build_gray(gray_table, num_levels, size);

	printf("Comp:\n");

	struct lookup_data *lookup = (struct lookup_data*) malloc(size * sizeof(struct lookup_data));
	printf("Size: %i\n", size);
	build_lookup(lookup, size);

	init_output_data(&output, (strlen(input) * 8)/num_levels);

	int mask = build_mask(num_levels);

	printf("Input: %s\n", input);
	int num_in_char = 8/num_levels;
	for(; *input; input++)
	{
		for(int i = 0; i < 8; i += num_levels) {
			//printf("%i, %i\n", (*input >> i) & mask, ( *gray_table >> ( ( (*input >> i) & mask ) * num_levels ) ) & mask);
			//output.key[output.size++] = GET_GRAY(*input, i, mask, num_levels, gray_table);//(*input >> i) & mask;
			//( ( gray_table >> ( ( (input >> i) & mask ) * num_levels ) ) & mask )

			int in = (*input >> i) & mask;
			int access = in/num_in_char;
			int diff = in - access ;

			output.key[output.size++] = ( gray_table[access] >> (diff * num_levels) ) & mask;
			printf("%i, %i, %i, %i\n", access, diff, ((*input >> i) & mask), output.key[output.size-1]);
		}
	}

	//printf("Loopup:\n");
	//for(int i = 0; i < size; i++)
	//{
	//	printf("%f\n", lookup[ i ].theta);
	//}

	printf("Output:\n");
	for(int i = 0; i < output.size; i++)
	{
		printf("%i, %f\n", output.key[i], lookup[ output.key[i] ].theta);
	}
	return 0;
	*/
}

void extract(struct output_data *output, unsigned char *gray_table, char *input, int num_levels)
{
	int mask = build_mask(num_levels);
	int num_in_char = 8/num_levels;

	for(; *input; input++)
	{
		//printf("%c\n", input[0]);
		//PRINT_HEX(input[0])
		//printf("%i %i %i %i\n", input[0] & 0x3, input[0] & 0xc, input[0] & 0x30, input[0] & 0xc0);
		for(int i = 0; i < 8; i += num_levels) {
			int in = (*input >> i) & mask;
			int access = in/num_in_char;
			int diff = in - access ;

			output->key[output->size++] = ( gray_table[access] >> (diff * num_levels) ) & mask;
			//printf("%i %i %i\n", i, in, output->key[output->size - 1]);
			//printf("%i, %i, %i, %i\n", access, diff, ((*input >> i) & mask), output->key[output->size-1]);
		}
	}
}