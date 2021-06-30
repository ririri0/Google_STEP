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

// Store random values less than 10 in a matrix
vector<vector<int> > random_matrix_under10(int N, vector<vector<int> > matrix) {
  std::random_device rand_d;
  for (int i = 0; i < N; i++) {
    for (int m = 0; m < N; m++) {
      matrix.at(i).at(m) = rand_d() % 10;
    }
  }
  return matrix;
}

/*
Give the size N of the matrix and two types of matrices, matrix1, matrix2
Return matrix1*matrix2
*/
void matrix_multiplication(int N, vector<vector<int> > matrix1,
                           vector<vector<int> > matrix2,
                           vector<vector<int> > result) {
  for (int i = 0; i < N; i++) {　
      for (int k = 0; k < N; k++) {
    for (int j = 0; j < N; j++) {
        result.at(i).at(j) += matrix1.at(i).at(k) * matrix2.at(k).at(j);
      }
    }
  }
}

void print_matrix(int N, vector<vector<int> > matrix) {
  for (int i = 0; i < N; i++) {
    for (int j = 0; j < N; j++) {
      cout << "matrix[" << i << "][" << j << "] = " << matrix.at(i).at(j)
           << endl;
    }
  }
}

int main() {
  int N = 1023;
  // std::cin >> N;

  if (N <= 0) {
    cout << "WE CANNOT CALCULATE!" << endl;
    return 0;
  }

  // Create matrix1
  vector<vector<int> > matrix1(N, vector<int>(N));
  matrix1 = random_matrix_under10(N, matrix1);

  // Create matrix2
  vector<vector<int> > matrix2(N, vector<int>(N));
  matrix2 = random_matrix_under10(N, matrix2);
  // random_matrix_under10(N, matrix2);

  // Create result
  vector<vector<int> > result(N, vector<int>(N));

  // Get the time before calculation
  double begin_time = get_time();

  //  Calculation
  matrix_multiplication(N, matrix1, matrix2, result);

  // Get the time after calculation
  double end_time = get_time();

  // print execution time
  double execution_time = end_time - begin_time;
  std::cout << execution_time;

  /*  debug
    print_matrix(N, matrix1);
    print_matrix(N, matrix2);
    print_matrix(N, result);
  */

  return 0;
}
