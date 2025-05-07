import pandas as pd
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, Reference
from openpyxl.drawing.image import Image
import matplotlib.pyplot as plt
import io

class ReportExporter:
    def __init__(self):
        self.wb = Workbook()
        
    def export_ahp_results(self, criteria_names, comparison_matrix, weights, cr, ci):
        """Export AHP results to Excel"""
        ws = self.wb.create_sheet("AHP Analysis")
        
        # Title
        ws['A1'] = "AHP Analysis Results"
        ws['A1'].font = Font(size=14, bold=True)
        
        # Criteria Names
        ws['A3'] = "Criteria Names"
        ws['A3'].font = Font(bold=True)
        for i, name in enumerate(criteria_names, 1):
            ws[f'A{i+3}'] = name
        
        # Comparison Matrix
        ws['C3'] = "Pairwise Comparison Matrix"
        ws['C3'].font = Font(bold=True)
        
        # Matrix headers
        for i, name in enumerate(criteria_names, 1):
            ws[f'{get_column_letter(i+3)}3'] = name
            ws[f'C{i+3}'] = name
        
        # Matrix values
        for i in range(len(comparison_matrix)):
            for j in range(len(comparison_matrix)):
                ws[f'{get_column_letter(j+4)}{i+4}'] = comparison_matrix[i][j]
        
        # Weights
        ws['A15'] = "Criteria Weights"
        ws['A15'].font = Font(bold=True)
        ws['A16'] = "Criteria"
        ws['B16'] = "Weight"
        ws['A16'].font = Font(bold=True)
        ws['B16'].font = Font(bold=True)
        
        for i, (name, weight) in enumerate(zip(criteria_names, weights), 1):
            ws[f'A{i+16}'] = name
            ws[f'B{i+16}'] = weight
        
        # Consistency
        ws['D15'] = "Consistency Analysis"
        ws['D15'].font = Font(bold=True)
        ws['D16'] = "Consistency Index (CI)"
        ws['E16'] = ci
        ws['D17'] = "Consistency Ratio (CR)"
        ws['E17'] = cr
        
        # Create bar chart for weights
        chart = BarChart()
        chart.title = "Criteria Weights"
        chart.y_axis.title = "Weight"
        chart.x_axis.title = "Criteria"
        
        data = Reference(ws, min_col=2, min_row=16, max_row=16+len(weights)-1)
        cats = Reference(ws, min_col=1, min_row=17, max_row=17+len(weights)-1)
        chart.add_data(data, titles_from_data=True)
        chart.set_categories(cats)
        
        ws.add_chart(chart, "G3")
        
        # Adjust column widths
        for col in range(1, 10):
            ws.column_dimensions[get_column_letter(col)].width = 15
    
    def export_topsis_results(self, alternatives, criteria_names, performance_matrix, 
                            benefit_criteria, weights, scores, rankings):
        """Export TOPSIS results to Excel"""
        ws = self.wb.create_sheet("TOPSIS Analysis")
        
        # Title
        ws['A1'] = "TOPSIS Analysis Results"
        ws['A1'].font = Font(size=14, bold=True)
        
        # Performance Matrix
        ws['A3'] = "Performance Matrix"
        ws['A3'].font = Font(bold=True)
        
        # Headers
        ws['A4'] = "Alternative"
        ws['A4'].font = Font(bold=True)
        for i, name in enumerate(criteria_names, 1):
            ws[f'{get_column_letter(i+1)}4'] = name
            ws[f'{get_column_letter(i+1)}4'].font = Font(bold=True)
        
        # Matrix values
        for i, alt in enumerate(alternatives):
            ws[f'A{i+5}'] = alt
            for j in range(len(criteria_names)):
                ws[f'{get_column_letter(j+2)}{i+5}'] = performance_matrix[i][j]
        
        # Criteria Types
        ws['A15'] = "Criteria Types"
        ws['A15'].font = Font(bold=True)
        ws['A16'] = "Criteria"
        ws['B16'] = "Type"
        ws['A16'].font = Font(bold=True)
        ws['B16'].font = Font(bold=True)
        
        for i, (name, is_benefit) in enumerate(zip(criteria_names, benefit_criteria), 1):
            ws[f'A{i+16}'] = name
            ws[f'B{i+16}'] = "Benefit" if is_benefit else "Cost"
        
        # Weights
        ws['D15'] = "Criteria Weights"
        ws['D15'].font = Font(bold=True)
        ws['D16'] = "Criteria"
        ws['E16'] = "Weight"
        ws['D16'].font = Font(bold=True)
        ws['E16'].font = Font(bold=True)
        
        for i, (name, weight) in enumerate(zip(criteria_names, weights), 1):
            ws[f'D{i+16}'] = name
            ws[f'E{i+16}'] = weight
        
        # Rankings
        ws['A25'] = "Final Rankings"
        ws['A25'].font = Font(bold=True)
        ws['A26'] = "Alternative"
        ws['B26'] = "Score"
        ws['C26'] = "Rank"
        ws['A26'].font = Font(bold=True)
        ws['B26'].font = Font(bold=True)
        ws['C26'].font = Font(bold=True)
        
        # Sort alternatives by rank
        ranked_data = sorted(zip(alternatives, scores, rankings), key=lambda x: x[2])
        for i, (alt, score, rank) in enumerate(ranked_data, 1):
            ws[f'A{i+26}'] = alt
            ws[f'B{i+26}'] = score
            ws[f'C{i+26}'] = rank
        
        # Create bar chart for rankings
        chart = BarChart()
        chart.title = "Alternative Rankings"
        chart.y_axis.title = "Score"
        chart.x_axis.title = "Alternative"
        
        data = Reference(ws, min_col=2, min_row=26, max_row=26+len(alternatives)-1)
        cats = Reference(ws, min_col=1, min_row=27, max_row=27+len(alternatives)-1)
        chart.add_data(data, titles_from_data=True)
        chart.set_categories(cats)
        
        ws.add_chart(chart, "G3")
        
        # Adjust column widths
        for col in range(1, 10):
            ws.column_dimensions[get_column_letter(col)].width = 15
    
    def save_report(self, filename):
        """Save the Excel report"""
        # Remove default sheet
        if "Sheet" in self.wb.sheetnames:
            del self.wb["Sheet"]
        
        self.wb.save(filename) 