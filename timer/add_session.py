from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox)
from PyQt6.QtCore import Qt

class AddSessionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Session")
        self.setFixedSize(400, 320)
        self.setStyleSheet("background-color: #222222; color: #ffffff; font-size: 14px;")

        # --- The Master List of Puzzle Options ---
        self.puzzle_data = {
            "3x3x3": ["WCA", "3BLD", "Edges-only", "Corners-only", "Last Layer (LL)", "F2L", "Easy Cross", "LSLL", "ZBLL", "ZZLL", "ZBLS", "LSE", "CMLL", "CLL", "ELL", "EO Line", "2-gen RU", "2-gen LU", "2-gen MU", "3-gen FRU", "3-gen RUL", "3-gen RrU", "Half-turns"],
            "2x2x2": ["WCA", "Optimal"],
            "4x4x4": ["WCA", "4BLD", "SiGN", "Random State", "Edges"],
            "5x5x5": ["WCA", "5BLD", "SiGN", "Edges"],
            "6x6x6": ["WCA", "SiGN", "Edges"],
            "7x7x7": ["WCA", "SiGN", "Edges"],
            "Pyraminx": ["WCA", "Optimal"],
            "Megaminx": ["WCA", "Carrot", "Old Style"],
            "Square-1": ["WCA", "Face-Turn Metric", "Twist Metric"],
            "Skewb": ["WCA", "ULRB"],
            "Clock": ["WCA", "Jaap", "Concise", "Efficient Pin Order"],
            "FTO": ["Random Moves", "Random State (Slow)"],
            "Rex Cube": ["Random Moves", "Random State (Slow)"],
            "Big Cubes": ["8x8x8", "9x9x9", "10x10x10", "11x11x11"],
            "Cuboids": ["1x1x2", "1x3x3 (Floppy)", "Super Floppy", "2x2x3", "3x3x2", "3x3x4", "3x3x5", "3x3x6", "3x3x7"]
        }

        layout = QVBoxLayout(self)

        # --- Name Input ---
        name_layout = QVBoxLayout()
        name_label = QLabel("Session Name:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g., 3x3 OH Practice")
        self.name_input.setStyleSheet("background-color: #333333; padding: 5px; border-radius: 3px; border: 1px solid #555555;")
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        # --- Puzzle Category Dropdown ---
        category_layout = QVBoxLayout()
        category_label = QLabel("Puzzle Category:")
        self.category_dropdown = QComboBox()
        self.category_dropdown.addItems(list(self.puzzle_data.keys()))
        self.category_dropdown.setStyleSheet("background-color: #333333; padding: 5px; border-radius: 3px; border: 1px solid #555555;")
        self.category_dropdown.currentTextChanged.connect(self.update_variations)
        category_layout.addWidget(category_label)
        category_layout.addWidget(self.category_dropdown)
        layout.addLayout(category_layout)

        # --- Specific Variation Dropdown ---
        var_layout = QVBoxLayout()
        var_label = QLabel("Scramble Type:")
        self.var_dropdown = QComboBox()
        self.var_dropdown.setStyleSheet("background-color: #333333; padding: 5px; border-radius: 3px; border: 1px solid #555555;")
        var_layout.addWidget(var_label)
        var_layout.addWidget(self.var_dropdown)
        layout.addLayout(var_layout)
        
        # Populate the variation dropdown for the first time
        self.update_variations(self.category_dropdown.currentText())

        layout.addSpacing(10)

        # --- Save / Cancel Buttons ---
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save Session")
        self.save_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 6px; font-weight: bold; border-radius: 3px;")
        self.save_btn.clicked.connect(self.validate_and_accept)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet("background-color: #d32f2f; color: white; padding: 6px; font-weight: bold; border-radius: 3px;")
        self.cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.save_btn)
        layout.addLayout(btn_layout)

    def update_variations(self, category):
        """Updates the second dropdown based on the category chosen."""
        self.var_dropdown.clear()
        variations = self.puzzle_data.get(category, [])
        self.var_dropdown.addItems(variations)

    def validate_and_accept(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Invalid Name", "Session name cannot be empty.")
            return
        if name == "+ Add New Session...":
            QMessageBox.warning(self, "Invalid Name", "That name is reserved. Please choose another.")
            return
        self.accept()

    def get_data(self):
        """Returns the custom name and the exact concatenated puzzle type."""
        category = self.category_dropdown.currentText()
        variation = self.var_dropdown.currentText()
        combined_type = f"{category} - {variation}"
        return self.name_input.text().strip(), combined_type