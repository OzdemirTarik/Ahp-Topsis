import sys
import numpy as np
import pandas as pd
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QLabel, QPushButton, QTableWidget,
                            QTableWidgetItem, QComboBox, QSpinBox, QMessageBox,
                            QFileDialog, QTabWidget, QGroupBox, QScrollArea,
                            QLineEdit, QCheckBox, QGridLayout, QSizePolicy,
                            QSplitter)
from PyQt6.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import seaborn as sns
from PyQt6.QtGui import QIcon

from ahp import AHP
from topsis import TOPSIS
from export_report import ReportExporter

class AHPTOPSISApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ahp = AHP()
        self.topsis = TOPSIS()
        self.criteria_weights = None
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('AHP-TOPSIS Decision Support System')
        self.setWindowIcon(QIcon('beher.svg'))

        # Ana monitörün geometrisini al ve pencereyi oraya yerleştir
        screen = QApplication.primaryScreen()
        geometry = screen.geometry()
        self.setGeometry(geometry)
        self.show()  # Pencereyi göster
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Create tab widget
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # Create AHP tab
        ahp_tab = QWidget()
        ahp_layout = QVBoxLayout(ahp_tab)
        
        # Split layout for matrix and results (QSplitter)
        split_layout = QSplitter(Qt.Orientation.Horizontal)
        
        # Left side - Matrix section (vertical splitter)
        left_widget = QWidget()
        left_splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Criteria hierarchy section
        hierarchy_group = QGroupBox("Criteria Hierarchy")
        hierarchy_layout = QVBoxLayout()
        
        # Number of criteria input
        criteria_layout = QHBoxLayout()
        criteria_layout.addWidget(QLabel("Number of Criteria:"))
        self.criteria_spin = QSpinBox()
        self.criteria_spin.setRange(2, 10)
        self.criteria_spin.valueChanged.connect(self.update_criteria_matrix)
        criteria_layout.addWidget(self.criteria_spin)
        hierarchy_layout.addLayout(criteria_layout)
        
        # Criteria names input
        self.criteria_names_layout = QHBoxLayout()
        hierarchy_layout.addLayout(self.criteria_names_layout)
        
        hierarchy_group.setLayout(hierarchy_layout)
        left_splitter.addWidget(hierarchy_group)
        
        # Pairwise comparison matrix
        matrix_group = QGroupBox("Pairwise Comparison Matrix")
        matrix_layout = QVBoxLayout()
        
        # Matrix table with size policy
        self.matrix_table = QTableWidget()
        self.matrix_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.matrix_table.setMinimumHeight(400)
        self.matrix_table.setMinimumWidth(600)
        self.matrix_table.cellChanged.connect(self.update_ahp_results)
        
        # Hücre boyutlarını ayarla
        self.matrix_table.horizontalHeader().setDefaultSectionSize(80)
        self.matrix_table.verticalHeader().setDefaultSectionSize(40)
        
        matrix_layout.addWidget(self.matrix_table)
        matrix_group.setLayout(matrix_layout)
        left_splitter.addWidget(matrix_group)
        left_splitter.setSizes([1, 3])
        left_widget_layout = QVBoxLayout(left_widget)
        left_widget_layout.addWidget(left_splitter)
        left_widget.setLayout(left_widget_layout)
        split_layout.addWidget(left_widget)
        
        # Right side - Results section (vertical splitter)
        right_widget = QWidget()
        right_splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Results section
        results_group = QGroupBox("Results")
        results_layout = QVBoxLayout()
        
        # Weights display
        self.weights_table = QTableWidget()
        self.weights_table.setColumnCount(2)
        self.weights_table.setHorizontalHeaderLabels(["Criteria", "Weight"])
        self.weights_table.horizontalHeader().setDefaultSectionSize(200)  # Genişliği artırıldı
        self.weights_table.setMinimumHeight(200)  # Yükseklik artırıldı
        results_layout.addWidget(self.weights_table)
        
        # Consistency ratio display
        self.cr_label = QLabel("Consistency Ratio: ")
        self.cr_label.setStyleSheet("font-size: 14pt; font-weight: bold;")  # Font boyutu artırıldı
        results_layout.addWidget(self.cr_label)
        
        results_group.setLayout(results_layout)
        
        # Visualization
        vis_group = QGroupBox()
        vis_layout = QVBoxLayout()
        self.figure = Figure(figsize=(10, 6))  # Grafik boyutu artırıldı
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumHeight(400)  # Canvas yüksekliği artırıldı
        vis_layout.addWidget(self.canvas)
        vis_group.setLayout(vis_layout)
        
        right_splitter.addWidget(results_group)
        right_splitter.addWidget(vis_group)
        right_splitter.setSizes([1, 2])
        right_widget_layout = QVBoxLayout(right_widget)
        right_widget_layout.addWidget(right_splitter)
        right_widget.setLayout(right_widget_layout)
        split_layout.addWidget(right_widget)
        
        split_layout.setSizes([1, 1])
        ahp_layout.addWidget(split_layout)
        tabs.addTab(ahp_tab, "AHP")
        
        # Create TOPSIS tab
        topsis_tab = QWidget()
        topsis_layout = QVBoxLayout(topsis_tab)
        
        # Matrix Creation Section
        matrix_creation_group = QGroupBox("Create Performance Matrix")
        matrix_creation_layout = QVBoxLayout()
        
        # Matrix size inputs
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("Number of Alternatives:"))
        self.alt_spin = QSpinBox()
        self.alt_spin.setRange(2, 20)
        self.alt_spin.valueChanged.connect(self.update_performance_matrix)
        size_layout.addWidget(self.alt_spin)
        
        size_layout.addWidget(QLabel("Number of Criteria:"))
        self.crit_spin = QSpinBox()
        self.crit_spin.setRange(2, 20)
        self.crit_spin.valueChanged.connect(self.update_performance_matrix)
        size_layout.addWidget(self.crit_spin)
        
        matrix_creation_layout.addLayout(size_layout)
        
        # Alternative names input
        alt_names_layout = QHBoxLayout()
        alt_names_layout.addWidget(QLabel("Alternative Names:"))
        self.alt_names_input = QLineEdit()
        self.alt_names_input.setPlaceholderText("Enter names separated by commas (e.g., Alt1, Alt2, Alt3)")
        self.alt_names_input.textChanged.connect(self.update_alternative_names)
        alt_names_layout.addWidget(self.alt_names_input)
        matrix_creation_layout.addLayout(alt_names_layout)
        
        # Criteria names input
        crit_names_layout = QHBoxLayout()
        crit_names_layout.addWidget(QLabel("Criteria Names:"))
        self.crit_names_input = QLineEdit()
        self.crit_names_input.setPlaceholderText("Enter names separated by commas (e.g., Cost, Quality, Time)")
        self.crit_names_input.textChanged.connect(self.update_criteria_names)
        crit_names_layout.addWidget(self.crit_names_input)
        matrix_creation_layout.addLayout(crit_names_layout)
        
        # Performance matrix table
        self.perf_matrix_table = QTableWidget()
        matrix_creation_layout.addWidget(self.perf_matrix_table)
        
        # Create matrix button
        create_matrix_btn = QPushButton("Create Matrix")
        create_matrix_btn.clicked.connect(self.create_performance_matrix)
        matrix_creation_layout.addWidget(create_matrix_btn)
        
        matrix_creation_group.setLayout(matrix_creation_layout)
        
        # Performance matrix section
        perf_group = QGroupBox("Performance Matrix")
        perf_layout = QVBoxLayout()
        
        # Import/Export buttons
        button_layout = QHBoxLayout()
        import_btn = QPushButton("Import CSV")
        import_btn.clicked.connect(self.import_performance_matrix)
        export_btn = QPushButton("Export Results")
        export_btn.clicked.connect(self.export_results)
        calculate_btn = QPushButton("Calculate Rankings")
        calculate_btn.clicked.connect(self.calculate_topsis)
        export_report_btn = QPushButton("Export Full Report")
        export_report_btn.clicked.connect(self.export_full_report)
        button_layout.addWidget(import_btn)
        button_layout.addWidget(export_btn)
        button_layout.addWidget(calculate_btn)
        button_layout.addWidget(export_report_btn)
        perf_layout.addLayout(button_layout)
        
        # Performance matrix table
        self.perf_table = QTableWidget()
        perf_layout.addWidget(self.perf_table)
        
        # Benefit/Cost criteria selection
        self.benefit_criteria_layout = QHBoxLayout()
        perf_layout.addLayout(self.benefit_criteria_layout)
        
        perf_group.setLayout(perf_layout)
        
        # Results section
        topsis_results_group = QGroupBox("TOPSIS Results")
        topsis_results_layout = QVBoxLayout()
        
        # Rankings table
        self.rankings_table = QTableWidget()
        self.rankings_table.setColumnCount(3)
        self.rankings_table.setHorizontalHeaderLabels(["Alternative", "Score", "Rank"])
        topsis_results_layout.addWidget(self.rankings_table)
        
        topsis_results_group.setLayout(topsis_results_layout)
        
        # TOPSIS ana bölümlerini QSplitter ile ayır
        topsis_splitter = QSplitter(Qt.Orientation.Vertical)
        topsis_splitter.addWidget(matrix_creation_group)
        topsis_splitter.addWidget(perf_group)
        topsis_splitter.addWidget(topsis_results_group)
        topsis_splitter.setSizes([1, 2, 1])
        topsis_layout.addWidget(topsis_splitter)
        
        tabs.addTab(topsis_tab, "TOPSIS")
        
    def update_criteria_matrix(self):
        n = self.criteria_spin.value()
        
        # Update criteria names input
        self.clear_layout(self.criteria_names_layout)
        self.criteria_names = []
        for i in range(n):
            label = QLabel(f"Criteria {i+1}:")
            self.criteria_names_layout.addWidget(label)
            name_input = QLineEdit(f"Criteria {i+1}")
            name_input.setMinimumWidth(150)
            self.criteria_names.append(name_input)
            self.criteria_names_layout.addWidget(name_input)
        
        # Update matrix table
        self.matrix_table.setRowCount(n)
        self.matrix_table.setColumnCount(n)
        
        # Set headers
        headers = [f"C{i+1}" for i in range(n)]
        self.matrix_table.setHorizontalHeaderLabels(headers)
        self.matrix_table.setVerticalHeaderLabels(headers)
        
        # Initialize matrix with 1s on diagonal
        for i in range(n):
            for j in range(n):
                if i == j:
                    self.matrix_table.setItem(i, j, QTableWidgetItem("1"))
                else:
                    self.matrix_table.setItem(i, j, QTableWidgetItem(""))
        
        # Hücre boyutlarını güncelle
        self.matrix_table.horizontalHeader().setDefaultSectionSize(80)
        self.matrix_table.verticalHeader().setDefaultSectionSize(40)
        
        # Matris tablosunun boyutunu güncelle
        self.matrix_table.setMinimumHeight(max(400, n * 45))
        self.matrix_table.setMinimumWidth(max(600, n * 85))
    
    def update_ahp_results(self):
        try:
            n = self.criteria_spin.value()
            matrix = np.zeros((n, n))
            
            # Get matrix values
            for i in range(n):
                for j in range(n):
                    item = self.matrix_table.item(i, j)
                    if item and item.text():
                        matrix[i, j] = float(item.text())
                    else:
                        matrix[i, j] = 1.0
            
            # Calculate weights
            weights, cr, ci = self.ahp.calculate_weights(matrix)
            
            # Update weights table
            self.weights_table.setRowCount(n)
            for i in range(n):
                self.weights_table.setItem(i, 0, QTableWidgetItem(self.criteria_names[i].text()))
                self.weights_table.setItem(i, 1, QTableWidgetItem(f"{weights[i]:.4f}"))
            
            # Update consistency ratio
            self.cr_label.setText(f"Consistency Ratio: {cr:.4f}")
            
            # Update visualization
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            sns.barplot(x=[self.criteria_names[i].text() for i in range(n)], y=weights, ax=ax)
            ax.set_title("Criteria Weights")
            ax.set_ylabel("Weight")
            plt.xticks(rotation=45)
            self.figure.tight_layout()
            self.canvas.draw()
            
            # Store weights for TOPSIS
            self.criteria_weights = weights
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Invalid matrix values: {str(e)}")
    
    def update_performance_matrix(self):
        n_alt = self.alt_spin.value()
        n_crit = self.crit_spin.value()
        
        # Update matrix table
        self.perf_matrix_table.setRowCount(n_alt)
        self.perf_matrix_table.setColumnCount(n_crit)
        
        # Set default headers
        self.perf_matrix_table.setHorizontalHeaderLabels([f"C{i+1}" for i in range(n_crit)])
        self.perf_matrix_table.setVerticalHeaderLabels([f"A{i+1}" for i in range(n_alt)])
    
    def update_alternative_names(self):
        names = self.alt_names_input.text().split(',')
        names = [name.strip() for name in names if name.strip()]
        if names:
            self.perf_matrix_table.setVerticalHeaderLabels(names[:self.alt_spin.value()])
    
    def update_criteria_names(self):
        names = self.crit_names_input.text().split(',')
        names = [name.strip() for name in names if name.strip()]
        if names:
            self.perf_matrix_table.setHorizontalHeaderLabels(names[:self.crit_spin.value()])
    
    def create_performance_matrix(self):
        try:
            # Get matrix values
            n_alt = self.alt_spin.value()
            n_crit = self.crit_spin.value()
            
            # Update main performance table
            self.perf_table.setRowCount(n_alt)
            self.perf_table.setColumnCount(n_crit + 1)  # +1 for alternative names
            
            # Set headers
            alt_names = [self.perf_matrix_table.verticalHeaderItem(i).text() for i in range(n_alt)]
            crit_names = [self.perf_matrix_table.horizontalHeaderItem(i).text() for i in range(n_crit)]
            
            self.perf_table.setHorizontalHeaderLabels(["Alternative"] + crit_names)
            
            # Copy values
            for i in range(n_alt):
                # Set alternative name
                self.perf_table.setItem(i, 0, QTableWidgetItem(alt_names[i]))
                
                # Set criteria values
                for j in range(n_crit):
                    value = self.perf_matrix_table.item(i, j)
                    if value and value.text():
                        self.perf_table.setItem(i, j + 1, QTableWidgetItem(value.text()))
                    else:
                        self.perf_table.setItem(i, j + 1, QTableWidgetItem("0"))
            
            # Update benefit/cost criteria selection
            self.clear_layout(self.benefit_criteria_layout)
            self.benefit_criteria = []
            for name in crit_names:
                label = QLabel(f"{name}:")
                self.benefit_criteria_layout.addWidget(label)
                checkbox = QCheckBox("Benefit")
                checkbox.setChecked(True)  # Default to benefit criteria
                self.benefit_criteria.append(checkbox)
                self.benefit_criteria_layout.addWidget(checkbox)
            
            QMessageBox.information(self, "Success", "Performance matrix created successfully!")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create performance matrix: {str(e)}")
    
    def import_performance_matrix(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Import CSV", "", "CSV Files (*.csv)")
        if file_name:
            try:
                df = pd.read_csv(file_name)
                self.perf_table.setRowCount(len(df))
                self.perf_table.setColumnCount(len(df.columns))
                self.perf_table.setHorizontalHeaderLabels(df.columns)
                
                for i in range(len(df)):
                    for j in range(len(df.columns)):
                        self.perf_table.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j])))
                
                # Update benefit/cost criteria selection
                self.clear_layout(self.benefit_criteria_layout)
                self.benefit_criteria = []
                for col in df.columns[1:]:  # Skip first column (alternatives)
                    label = QLabel(f"{col}:")
                    self.benefit_criteria_layout.addWidget(label)
                    checkbox = QCheckBox("Benefit")
                    checkbox.setChecked(True)  # Default to benefit criteria
                    self.benefit_criteria.append(checkbox)
                    self.benefit_criteria_layout.addWidget(checkbox)
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to import CSV: {str(e)}")
    
    def calculate_topsis(self):
        if self.criteria_weights is None:
            QMessageBox.warning(self, "Error", "Please complete AHP analysis first")
            return
        
        try:
            # Get performance matrix
            n_rows = self.perf_table.rowCount()
            n_cols = self.perf_table.columnCount()
            matrix = np.zeros((n_rows, n_cols - 1))  # Exclude alternative names column
            
            for i in range(n_rows):
                for j in range(1, n_cols):  # Skip first column
                    item = self.perf_table.item(i, j)
                    if item and item.text():
                        matrix[i, j-1] = float(item.text())
                    else:
                        raise ValueError(f"Missing value at row {i+1}, column {j+1}")
            
            # Get benefit/cost criteria
            benefit_criteria = [cb.isChecked() for cb in self.benefit_criteria]
            
            # Calculate TOPSIS scores and rankings
            scores, rankings = self.topsis.rank_alternatives(matrix, self.criteria_weights, benefit_criteria)
            
            # Update rankings table
            self.rankings_table.setRowCount(n_rows)
            for i in range(n_rows):
                alt_name = self.perf_table.item(i, 0).text()
                self.rankings_table.setItem(i, 0, QTableWidgetItem(alt_name))
                self.rankings_table.setItem(i, 1, QTableWidgetItem(f"{scores[i]:.4f}"))
                self.rankings_table.setItem(i, 2, QTableWidgetItem(str(rankings[i])))
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to calculate rankings: {str(e)}")
    
    def export_results(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Export Results", "", "CSV Files (*.csv)")
        if file_name:
            try:
                # Get data from rankings table
                data = []
                for row in range(self.rankings_table.rowCount()):
                    row_data = []
                    for col in range(self.rankings_table.columnCount()):
                        item = self.rankings_table.item(row, col)
                        row_data.append(item.text() if item else "")
                    data.append(row_data)
                
                # Create DataFrame and save to CSV
                df = pd.DataFrame(data, columns=["Alternative", "Score", "Rank"])
                df.to_csv(file_name, index=False)
                QMessageBox.information(self, "Success", "Results exported successfully!")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export results: {str(e)}")
    
    def export_full_report(self):
        """Export complete AHP-TOPSIS analysis to Excel"""
        if not self.criteria_weights is not None:
            QMessageBox.warning(self, "Error", "Please complete AHP analysis first")
            return
            
        try:
            file_name, _ = QFileDialog.getSaveFileName(
                self, "Export Report", "", "Excel Files (*.xlsx)")
            
            if file_name:
                exporter = ReportExporter()
                
                # Export AHP results
                criteria_names = [name.text() for name in self.criteria_names]
                comparison_matrix = np.zeros((len(criteria_names), len(criteria_names)))
                
                for i in range(len(criteria_names)):
                    for j in range(len(criteria_names)):
                        item = self.matrix_table.item(i, j)
                        comparison_matrix[i, j] = float(item.text()) if item and item.text() else 1.0
                
                weights, cr, ci = self.ahp.calculate_weights(comparison_matrix)
                exporter.export_ahp_results(criteria_names, comparison_matrix, weights, cr, ci)
                
                # Export TOPSIS results if available
                if self.rankings_table.rowCount() > 0:
                    alternatives = []
                    performance_matrix = np.zeros((self.rankings_table.rowCount(), len(criteria_names)))
                    
                    for i in range(self.rankings_table.rowCount()):
                        alternatives.append(self.rankings_table.item(i, 0).text())
                        for j in range(len(criteria_names)):
                            item = self.perf_table.item(i, j + 1)
                            performance_matrix[i, j] = float(item.text()) if item and item.text() else 0.0
                    
                    benefit_criteria = [cb.isChecked() for cb in self.benefit_criteria]
                    scores = np.array([float(self.rankings_table.item(i, 1).text()) 
                                     for i in range(self.rankings_table.rowCount())])
                    rankings = np.array([int(self.rankings_table.item(i, 2).text()) 
                                       for i in range(self.rankings_table.rowCount())])
                    
                    exporter.export_topsis_results(
                        alternatives, criteria_names, performance_matrix,
                        benefit_criteria, weights, scores, rankings
                    )
                
                exporter.save_report(file_name)
                QMessageBox.information(self, "Success", "Report exported successfully!")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export report: {str(e)}")
    
    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

def main():
    app = QApplication(sys.argv)
    window = AHPTOPSISApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 