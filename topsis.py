import numpy as np
import pandas as pd
from typing import List, Tuple, Dict

class TOPSIS:
    def __init__(self):
        pass
    
    def normalize_matrix(self, matrix: np.ndarray) -> np.ndarray:
        """
        Normalize the decision matrix using vector normalization.
        
        Args:
            matrix: Decision matrix (alternatives x criteria)
            
        Returns:
            numpy.ndarray: Normalized decision matrix
        """
        squared_sum = np.sum(matrix ** 2, axis=0)
        return matrix / np.sqrt(squared_sum)
    
    def calculate_weighted_matrix(self, normalized_matrix: np.ndarray, weights: np.ndarray) -> np.ndarray:
        """
        Calculate the weighted normalized decision matrix.
        
        Args:
            normalized_matrix: Normalized decision matrix
            weights: Criteria weights
            
        Returns:
            numpy.ndarray: Weighted normalized decision matrix
        """
        return normalized_matrix * weights
    
    def find_ideal_solutions(self, weighted_matrix: np.ndarray, benefit_criteria: List[bool]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Find the ideal and negative-ideal solutions.
        
        Args:
            weighted_matrix: Weighted normalized decision matrix
            benefit_criteria: List of booleans indicating if criteria are benefit (True) or cost (False)
            
        Returns:
            Tuple containing:
            - Ideal solution
            - Negative-ideal solution
        """
        ideal = np.zeros(len(benefit_criteria))
        negative_ideal = np.zeros(len(benefit_criteria))
        
        for i, is_benefit in enumerate(benefit_criteria):
            if is_benefit:
                ideal[i] = np.max(weighted_matrix[:, i])
                negative_ideal[i] = np.min(weighted_matrix[:, i])
            else:
                ideal[i] = np.min(weighted_matrix[:, i])
                negative_ideal[i] = np.max(weighted_matrix[:, i])
                
        return ideal, negative_ideal
    
    def calculate_distances(self, weighted_matrix: np.ndarray, ideal: np.ndarray, negative_ideal: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate distances to ideal and negative-ideal solutions.
        
        Args:
            weighted_matrix: Weighted normalized decision matrix
            ideal: Ideal solution
            negative_ideal: Negative-ideal solution
            
        Returns:
            Tuple containing:
            - Distances to ideal solution
            - Distances to negative-ideal solution
        """
        d_plus = np.sqrt(np.sum((weighted_matrix - ideal) ** 2, axis=1))
        d_minus = np.sqrt(np.sum((weighted_matrix - negative_ideal) ** 2, axis=1))
        return d_plus, d_minus
    
    def calculate_scores(self, d_plus: np.ndarray, d_minus: np.ndarray) -> np.ndarray:
        """
        Calculate TOPSIS scores (closeness coefficients).
        
        Args:
            d_plus: Distances to ideal solution
            d_minus: Distances to negative-ideal solution
            
        Returns:
            numpy.ndarray: TOPSIS scores
        """
        return d_minus / (d_plus + d_minus)
    
    def rank_alternatives(self, matrix: np.ndarray, weights: np.ndarray, benefit_criteria: List[bool]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Rank alternatives using TOPSIS method.
        
        Args:
            matrix: Decision matrix (alternatives x criteria)
            weights: Criteria weights
            benefit_criteria: List of booleans indicating if criteria are benefit (True) or cost (False)
            
        Returns:
            Tuple containing:
            - TOPSIS scores
            - Rankings (1-based)
        """
        normalized_matrix = self.normalize_matrix(matrix)
        weighted_matrix = self.calculate_weighted_matrix(normalized_matrix, weights)
        ideal, negative_ideal = self.find_ideal_solutions(weighted_matrix, benefit_criteria)
        d_plus, d_minus = self.calculate_distances(weighted_matrix, ideal, negative_ideal)
        scores = self.calculate_scores(d_plus, d_minus)
        rankings = np.argsort(scores)[::-1] + 1  # 1-based rankings
        
        return scores, rankings 