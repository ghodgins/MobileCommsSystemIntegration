#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

#include <inttypes.h>
#include <stdint.h>

#include <assert.h>

typedef enum boolean { FALSE, TRUE} bool;
typedef enum TYPES { CHAR, INT, SHORT } TYPE; // Don't think this is used.

#define SIZE_EXCEPTION_CHECK(size, limit) if(size > limit) { \
		printf("Size exceeds function limits in %s: %i\n", __func__, __LINE__); \
		return;\
	}

// Will auto convert to int, hence the output padding.
#define PRINT_HEX(val) printf("0x%x\n", val);
// Var + Data types

// Asin(wt + theta)
float f = 10240;
float PI = 3.14;
int num_levels = 2; // Default value

// Our output data structure.
struct lookup_data {
	float amplitude;
	float theta, omega;
};

struct output_data {
	//struct lookup_data *lookup;
	int *key;
	int size;
} output;

// Functions :)

// Constructors.
// output->size inits to 0, so we can use it as a setter.
void init_output_data(struct output_data *output, int key_size);
void init_lookup_data(struct lookup_data *val, float a, float t, float o);
// Generate a lookup table of size 2^num_levels.
// Only modulating theta just now.
void build_lookup(struct lookup_data *lookup, int size);
void build_qam(struct lookup_data *lookup, int size, int num_a, int max_amp);
void build_qam16(struct lookup_data *lookup, int min, int mid, int max);
// Generate our mask. 2 -> 11, 4 -> 1111, etc.
int build_mask(int num_levels);

void print_lookup_data(struct lookup_data *val);

void build_gray_table32(int32_t *table, int num_levels);
void build_gray_table64(int64_t *table, int num_levels);
void build_gray_table8(char *table, int num_levels);