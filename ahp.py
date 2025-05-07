import numpy as np
from typing import List, Tuple, Dict

class AHP:
    def __init__(self):
        self.ri_dict = {
            1: 0, 2: 0, 3: 0.58, 4: 0.90, 5: 1.12,
            6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49
        }
        
    def calculate_weights(self, matrix: np.ndarray) -> Tuple[np.ndarray, float, float]:
        """
        Calculate weights using the eigenvalue method and check consistency.
        
        Args:
            matrix: Pairwise comparison matrix
            
        Returns:
            Tuple containing:
            - Priority weights
            - Consistency Ratio (CR)
            - Consistency Index (CI)
        """
        n = len(matrix)
        
        # Calculate eigenvalues and eigenvectors
        eigenvalues, eigenvectors = np.linalg.eig(matrix)
        max_eigenvalue = np.max(eigenvalues.real)
        
        # Calculate weights
        weights = eigenvectors[:, np.argmax(eigenvalues.real)].real
        weights = weights / np.sum(weights)
        
        # Calculate consistency
        ci = (max_eigenvalue - n) / (n - 1)
        cr = ci / self.ri_dict[n]
        
        return weights, cr, ci
    
    def check_consistency(self, matrix: np.ndarray) -> bool:
        """
        Check if the pairwise comparison matrix is consistent.
        
        Args:
            matrix: Pairwise comparison matrix
            
        Returns:
            bool: True if consistent (CR < 0.1), False otherwise
        """
        _, cr, _ = self.calculate_weights(matrix)
        return cr < 0.1
    
    def create_comparison_matrix(self, comparisons: List[float], n: int) -> np.ndarray:
        """
        Create a pairwise comparison matrix from a list of comparisons.
        
        Args:
            comparisons: List of comparison values
            n: Size of the matrix
            
        Returns:
            numpy.ndarray: Pairwise comparison matrix
        """
        matrix = np.ones((n, n))
        k = 0
        for i in range(n):
            for j in range(i+1, n):
                matrix[i, j] = comparisons[k]
                matrix[j, i] = 1 / comparisons[k]
                k += 1
        return matrix 