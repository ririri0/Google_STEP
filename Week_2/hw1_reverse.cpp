#include <sys/time.h>

#include <iostream>
#include <random>

using namespace std;

// Get the current time
double get_time() {
  struct timeval tv;
  gettimeofday(&tv, NULL);
  return tv.tv_sec + tv.tv_usec * 1e-6;
}

// Initialized to 0
void initialize_matrix(int N, int* matrix) {
  for (int i = 0; i < N * N; i++) {
    matrix[i] = 0;
  }
}

// Store random values less than 10 in a matrix
void random_matrix_under10(int N, int* matrix) {
  std::random_device rand_d;
  for (int i = 0; i < N; i++) {
    for (int m = 0; m < N; m++) {
      matrix[i * N + m] = rand_d() % 10;
    }
  }
}

/*
Give the size N of the matrix and two types of matrices, matrix1, matrix2
Return matrix1*matrix2
*/
void matrix_multiplication(int N, int* matrix1, int* matrix2, int* result) {
  if (matrix1 == nullptr || matrix2 == nullptr) {
    result = nullptr;
  }

  for (int k = 0; k < N; k++) {
    for (int m = 0; m < N; m++) {
      for (int i = 0; i < N; i++) {
        result[i * N + m] += matrix1[i * N + k] * matrix2[k * N + m];
      }
    }
  }
}


void print_matrix(int N, int* matrix) {
  for (int i = 0; i < N * N; i++) {
    cout << "matrix[" << i << "] = " << matrix[i] << endl;
  }
}

int main() {
  int N;
  std::cin >> N;

  if (N <= 0) {
    cout << "WE CANNOT CALCULATE!" << endl;
    return 0;
  }


  // Create matrix1
  int* matrix1 = (int*)malloc(N * N * sizeof(int));
  initialize_matrix(N, matrix1);
  random_matrix_under10(N, matrix1);

  // Create matrix2
  int* matrix2 = (int*)malloc(N * N * sizeof(int));
  initialize_matrix(N, matrix2);
  random_matrix_under10(N, matrix2);

  int* result = (int*)malloc(N * N * sizeof(int));
  initialize_matrix(N, result);

  // Get the time before calculation
  double begin_time = get_time();

  //  Calculation
  matrix_multiplication(N, matrix1, matrix2, result);
  //multiply_normal(N, matrix1, matrix2, result);

  // Get the time after calculation
  double end_time = get_time();

  // print execution time
  double execution_time = end_time - begin_time;
  std::cout << execution_time;

/* debug 
  print_matrix(N, matrix1);
  print_matrix(N, matrix2);
  print_matrix(N, result);
*/
     

  free(matrix1);
  free(matrix2);
  free(result);

  return 0;
}
