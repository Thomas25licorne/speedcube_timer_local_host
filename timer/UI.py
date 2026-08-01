import time
import math
from PyQt6.QtWidgets import (QMainWindow, QLabel, QVBoxLayout, 
                             QWidget, QHBoxLayout, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QGridLayout, QFrame, QPushButton, QComboBox,
                             QLineEdit, QMessageBox)
from PyQt6.QtCore import Qt, QTimer

# Import ALL twisty scramblers
from pyTwistyScrambler import (scrambler222, scrambler333, scrambler444, scrambler555, 
                               scrambler666, scrambler777, pyraminxScrambler, megaminxScrambler, 
                               squareOneScrambler, skewbScrambler, clockScrambler, ftoScrambler, 
                               rexScrambler, bigCubesScrambler, cuboidsScrambler)

# Import custom files
from database import DatabaseManager
from add_session import AddSessionDialog

class SpeedcubeTimer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Speedcube Timer")
        self.setFixedSize(1100, 650)
        self.setStyleSheet("background-color: #222222; color: #ffffff;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        self.db = DatabaseManager()
        self.session_dict = {}
        self.current_session = "3x3"
        
        # --- The Master Scrambler Router ---
        self.scramble_routers = {
            # 3x3x3
            "3x3x3 - WCA": scrambler333.get_WCA_scramble,
            "3x3x3 - 3BLD": scrambler333.get_3BLD_scramble,
            "3x3x3 - Edges-only": scrambler333.get_edges_scramble,
            "3x3x3 - Corners-only": scrambler333.get_corners_scramble,
            "3x3x3 - Last Layer (LL)": scrambler333.get_LL_scramble,
            "3x3x3 - F2L": scrambler333.get_F2L_scramble,
            "3x3x3 - Easy Cross": scrambler333.get_easy_cross_scramble,
            "3x3x3 - LSLL": scrambler333.get_LSLL_scramble,
            "3x3x3 - ZBLL": scrambler333.get_ZBLL_scramble,
            "3x3x3 - ZZLL": scrambler333.get_ZZLL_scramble,
            "3x3x3 - ZBLS": scrambler333.get_ZBLS_scramble,
            "3x3x3 - LSE": scrambler333.get_LSE_scramble,
            "3x3x3 - CMLL": scrambler333.get_CMLL_scramble,
            "3x3x3 - CLL": scrambler333.get_CLL_scramble,
            "3x3x3 - ELL": scrambler333.get_ELL_scramble,
            "3x3x3 - EO Line": scrambler333.get_EOLine_scramble,
            "3x3x3 - 2-gen RU": scrambler333.get_2genRU_scramble,
            "3x3x3 - 2-gen LU": scrambler333.get_2genLU_scramble,
            "3x3x3 - 2-gen MU": scrambler333.get_2genMU_scramble,
            "3x3x3 - 3-gen FRU": scrambler333.get_3genFRU_scramble,
            "3x3x3 - 3-gen RUL": scrambler333.get_3genRUL_scramble,
            "3x3x3 - 3-gen RrU": scrambler333.get_3genRrU_scramble,
            "3x3x3 - Half-turns": scrambler333.get_half_turns_scramble,
            
            # 2x2x2
            "2x2x2 - WCA": scrambler222.get_WCA_scramble,
            "2x2x2 - Optimal": scrambler222.get_optimal_scramble,
            
            # 4x4x4
            "4x4x4 - WCA": scrambler444.get_WCA_scramble,
            "4x4x4 - 4BLD": scrambler444.get_4BLD_scramble,
            "4x4x4 - SiGN": scrambler444.get_SiGN_scramble,
            "4x4x4 - Random State": scrambler444.get_random_state_scramble,
            "4x4x4 - Edges": scrambler444.get_edges_scramble,
            
            # 5x5x5
            "5x5x5 - WCA": scrambler555.get_WCA_scramble,
            "5x5x5 - 5BLD": scrambler555.get_5BLD_scramble,
            "5x5x5 - SiGN": scrambler555.get_SiGN_scramble,
            "5x5x5 - Edges": scrambler555.get_edges_scramble,
            
            # 6x6x6
            "6x6x6 - WCA": scrambler666.get_WCA_scramble,
            "6x6x6 - SiGN": scrambler666.get_SiGN_scramble,
            "6x6x6 - Edges": scrambler666.get_edges_scramble,
            
            # 7x7x7
            "7x7x7 - WCA": scrambler777.get_WCA_scramble,
            "7x7x7 - SiGN": scrambler777.get_SiGN_scramble,
            "7x7x7 - Edges": scrambler777.get_edges_scramble,
            
            # Pyraminx & Megaminx
            "Pyraminx - WCA": pyraminxScrambler.get_WCA_scramble,
            "Pyraminx - Optimal": pyraminxScrambler.get_optimal_scramble,
            "Megaminx - WCA": megaminxScrambler.get_WCA_scramble,
            "Megaminx - Carrot": megaminxScrambler.get_Carrot_scramble,
            "Megaminx - Old Style": megaminxScrambler.get_old_style_scramble,
            
            # Square-1 & Skewb
            "Square-1 - WCA": squareOneScrambler.get_WCA_scramble,
            "Square-1 - Face-Turn Metric": squareOneScrambler.get_face_turn_metric_scramble,
            "Square-1 - Twist Metric": squareOneScrambler.get_twist_metric_scramble,
            "Skewb - WCA": skewbScrambler.get_WCA_scramble,
            "Skewb - ULRB": skewbScrambler.get_ULRB_scramble,
            
            # Clock
            "Clock - WCA": clockScrambler.get_WCA_scramble,
            "Clock - Jaap": clockScrambler.get_Jaap_scramble,
            "Clock - Concise": clockScrambler.get_concise_scramble,
            "Clock - Efficient Pin Order": clockScrambler.get_efficient_pin_order_scramble,
            
            # FTO & Rex Cube (Using Random Moves default for safety)
            "FTO - Random Moves": ftoScrambler.get_random_moves_scramble,
            "FTO - Random State (Slow)": ftoScrambler.get_random_state_scramble,
            "Rex Cube - Random Moves": rexScrambler.get_random_moves_scramble,
            "Rex Cube - Random State (Slow)": rexScrambler.get_random_state_scramble,
            
            # Big Cubes
            "Big Cubes - 8x8x8": bigCubesScrambler.get_8x8x8_scramble,
            "Big Cubes - 9x9x9": bigCubesScrambler.get_9x9x9_scramble,
            "Big Cubes - 10x10x10": bigCubesScrambler.get_10x10x10_scramble,
            "Big Cubes - 11x11x11": bigCubesScrambler.get_11x11x11_scramble,
            
            # Cuboids
            "Cuboids - 1x1x2": cuboidsScrambler.get_1x1x2_scramble,
            "Cuboids - 1x3x3 (Floppy)": cuboidsScrambler.get_1x3x3_scramble,
            "Cuboids - Super Floppy": cuboidsScrambler.get_super_floppy_cube_scramble,
            "Cuboids - 2x2x3": cuboidsScrambler.get_2x2x3_scramble,
            "Cuboids - 3x3x2": cuboidsScrambler.get_3x3x2_scramble,
            "Cuboids - 3x3x4": cuboidsScrambler.get_3x3x4_scramble,
            "Cuboids - 3x3x5": cuboidsScrambler.get_3x3x5_scramble,
            "Cuboids - 3x3x6": cuboidsScrambler.get_3x3x6_scramble,
            "Cuboids - 3x3x7": cuboidsScrambler.get_3x3x7_scramble
        }

        # ==================== LEFT SIDE (Timer) ====================
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.scramble_label = QLabel()
        self.scramble_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scramble_label.setStyleSheet("color: #cccccc; font-size: 24px; font-weight: bold; letter-spacing: 2px;")
        self.scramble_label.setWordWrap(True)
        left_layout.addWidget(self.scramble_label)

        left_layout.addSpacing(30)

        self.timer_label = QLabel("0.000")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setStyleSheet("color: #ffffff; font-size: 140px; font-weight: bold;")
        left_layout.addWidget(self.timer_label)

        self.hint_label = QLabel("Hold SPACE to start, press SPACE to stop.")
        self.hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hint_label.setStyleSheet("color: #666666; font-size: 16px; margin-top: 20px;")
        left_layout.addWidget(self.hint_label)

        main_layout.addWidget(left_widget, stretch=2)

        # ==================== RIGHT SIDE (Stats & History) ====================
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        # --- Session Selector Dropdown ---
        self.session_selector = QComboBox()
        self.session_selector.setStyleSheet("""
            QComboBox { background-color: #333333; color: #ffffff; font-size: 16px; padding: 5px; border-radius: 3px; }
            QComboBox::drop-down { border: 0px; }
        """)
        self.session_selector.currentTextChanged.connect(self.change_session)
        right_layout.addWidget(self.session_selector)
        
        self.load_sessions_into_dropdown()
        
        # --- Summary Stats ---
        summary_frame = QFrame()
        summary_frame.setStyleSheet("background-color: #333333; border-radius: 5px;")
        summary_layout = QGridLayout(summary_frame)
        
        headers = ["", "current", "best"]
        for col, text in enumerate(headers):
            lbl = QLabel(text)
            lbl.setStyleSheet("font-weight: bold; font-size: 16px;")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            summary_layout.addWidget(lbl, 0, col)

        rows = ["time", "mo3", "ao5", "ao12", "ao100"]
        self.stat_labels = {}
        
        for row, text in enumerate(rows, start=1):
            lbl = QLabel(text)
            lbl.setStyleSheet("font-weight: bold; font-size: 14px;")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            summary_layout.addWidget(lbl, row, 0)
            
            cur_lbl = QLabel("-")
            cur_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            cur_lbl.setStyleSheet("color: #5ea8ff; font-size: 14px;")
            summary_layout.addWidget(cur_lbl, row, 1)
            
            best_lbl = QLabel("-")
            best_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            best_lbl.setStyleSheet("color: #5ea8ff; font-size: 14px;")
            summary_layout.addWidget(best_lbl, row, 2)
            
            self.stat_labels[text] = {"current": cur_lbl, "best": best_lbl}
            
        right_layout.addWidget(summary_frame)
        
        self.mean_label = QLabel("solve: 0/0\nmean: -")
        self.mean_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mean_label.setStyleSheet("font-weight: bold; font-size: 16px; margin: 10px 0;")
        right_layout.addWidget(self.mean_label)

        # --- History Table ---
        self.history_table = QTableWidget(0, 5)
        self.history_table.setHorizontalHeaderLabels(["id", "time", "ao5", "ao12", "ao100"])
        self.history_table.setStyleSheet("""
            QTableWidget { background-color: #333333; color: #ffffff; gridline-color: #555555; font-size: 14px; }
            QHeaderView::section { background-color: #444444; color: #ffffff; font-weight: bold; font-size: 14px; }
        """)
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.history_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        right_layout.addWidget(self.history_table)

        # --- Delete Solve UI ---
        delete_layout = QHBoxLayout()
        delete_label = QLabel("Delete Solve ID:")
        delete_label.setStyleSheet("font-size: 14px;")
        self.delete_input = QLineEdit()
        self.delete_input.setPlaceholderText("ID #")
        self.delete_input.setFixedWidth(60)
        self.delete_input.setStyleSheet("background-color: #444444; color: #ffffff; font-size: 14px; padding: 4px; border: 1px solid #555555; border-radius: 3px;")
        self.delete_input.returnPressed.connect(self.handle_delete_solve)
        
        self.delete_btn = QPushButton("Delete")
        self.delete_btn.setStyleSheet("""
            QPushButton { background-color: #d32f2f; color: white; font-size: 14px; font-weight: bold; padding: 4px 12px; border-radius: 3px; }
            QPushButton:hover { background-color: #f44336; }
        """)
        self.delete_btn.clicked.connect(self.handle_delete_solve)
        
        delete_layout.addWidget(delete_label)
        delete_layout.addWidget(self.delete_input)
        delete_layout.addWidget(self.delete_btn)
        delete_layout.addStretch()
        right_layout.addLayout(delete_layout)

        main_layout.addWidget(right_widget, stretch=1)

        # ==================== LOGIC SETUP ====================
        self.q_timer = QTimer()
        self.q_timer.timeout.connect(self.update_timer_display)
        self.is_running = False
        self.is_ready = False
        self.start_time = 0
        
        self.refresh_data()
        self.generate_new_scramble()

    def load_sessions_into_dropdown(self):
        self.session_selector.blockSignals(True)
        self.session_selector.clear()
        
        db_sessions = self.db.get_all_sessions()
        self.session_dict = {} 
        
        for name, puzzle in db_sessions:
            self.session_selector.addItem(name)
            self.session_dict[name] = puzzle
            
        self.session_selector.addItem("+ Add New Session...")
        self.session_selector.setCurrentText(self.current_session)
        self.session_selector.blockSignals(False)

    def change_session(self, new_session):
        if new_session == "+ Add New Session...":
            dialog = AddSessionDialog(self)
            if dialog.exec():
                new_name, new_puzzle = dialog.get_data()
                self.db.add_session(new_name, new_puzzle)
                self.current_session = new_name
                self.load_sessions_into_dropdown()
                self.refresh_data()
                self.generate_new_scramble()
            else:
                self.session_selector.blockSignals(True)
                self.session_selector.setCurrentText(self.current_session)
                self.session_selector.blockSignals(False)
        else:
            self.current_session = new_session
            self.refresh_data()
            self.generate_new_scramble()

    def handle_delete_solve(self):
        id_text = self.delete_input.text().strip()
        if not id_text: return
        try:
            solve_id = int(id_text)
            self.db.delete_solve_by_id(solve_id)
            self.delete_input.clear()
            self.refresh_data()
            self.delete_input.clearFocus() 
        except ValueError:
            QMessageBox.warning(self, "Invalid ID", "Please enter a valid numeric ID.")

    def calc_raw_ao(self, times, n):
        if len(times) < n: return None
        last_n = sorted(times[-n:])
        trim = math.ceil(n * 0.05)
        trimmed = last_n[trim:-trim] if trim > 0 else last_n
        return sum(trimmed) / len(trimmed)

    def calc_mo3(self, times):
        if len(times) < 3: return None
        return sum(times[-3:]) / 3.0

    def refresh_data(self):
        rows = self.db.get_all_solves(self.current_session)
        all_times = [r[1] for r in rows]
        solve_count = len(all_times)
        
        if solve_count > 0:
            overall_mean = sum(all_times) / solve_count
            self.mean_label.setText(f"solve: {solve_count}/{solve_count}\nmean: {overall_mean:.2f}")
        else:
            self.mean_label.setText("solve: 0/0\nmean: -")
            
        self.update_summary_block(all_times)
        self.update_history_table(rows, all_times)

    def update_summary_block(self, times):
        if not times:
            def fmt_dash(): return "-"
            self.stat_labels["time"]["current"].setText(fmt_dash())
            self.stat_labels["time"]["best"].setText(fmt_dash())
            self.stat_labels["mo3"]["current"].setText(fmt_dash())
            self.stat_labels["mo3"]["best"].setText(fmt_dash())
            self.stat_labels["ao5"]["current"].setText(fmt_dash())
            self.stat_labels["ao5"]["best"].setText(fmt_dash())
            self.stat_labels["ao12"]["current"].setText(fmt_dash())
            self.stat_labels["ao12"]["best"].setText(fmt_dash())
            self.stat_labels["ao100"]["current"].setText(fmt_dash())
            self.stat_labels["ao100"]["best"].setText(fmt_dash())
            return
            
        cur_time = times[-1]
        cur_mo3 = self.calc_mo3(times)
        cur_ao5 = self.calc_raw_ao(times, 5)
        cur_ao12 = self.calc_raw_ao(times, 12)
        cur_ao100 = self.calc_raw_ao(times, 100)
        
        best_time = min(times)
        best_mo3 = min([self.calc_mo3(times[i:i+3]) for i in range(len(times)-2)]) if len(times) >= 3 else None
        best_ao5 = min([self.calc_raw_ao(times[i:i+5], 5) for i in range(len(times)-4)]) if len(times) >= 5 else None
        best_ao12 = min([self.calc_raw_ao(times[i:i+12], 12) for i in range(len(times)-11)]) if len(times) >= 12 else None
        best_ao100 = min([self.calc_raw_ao(times[i:i+100], 100) for i in range(len(times)-99)]) if len(times) >= 100 else None

        def fmt(val): return f"{val:.2f}" if val is not None else "-"
        
        self.stat_labels["time"]["current"].setText(fmt(cur_time))
        self.stat_labels["time"]["best"].setText(fmt(best_time))
        self.stat_labels["mo3"]["current"].setText(fmt(cur_mo3))
        self.stat_labels["mo3"]["best"].setText(fmt(best_mo3))
        self.stat_labels["ao5"]["current"].setText(fmt(cur_ao5))
        self.stat_labels["ao5"]["best"].setText(fmt(best_ao5))
        self.stat_labels["ao12"]["current"].setText(fmt(cur_ao12))
        self.stat_labels["ao12"]["best"].setText(fmt(best_ao12))
        self.stat_labels["ao100"]["current"].setText(fmt(cur_ao100))
        self.stat_labels["ao100"]["best"].setText(fmt(best_ao100))

    def update_history_table(self, rows, all_times):
        self.history_table.setRowCount(0)
        start_index = max(0, len(rows) - 10)
        display_rows = rows[start_index:]
        
        for i, row_data in enumerate(display_rows):
            actual_index = start_index + i
            solve_id = row_data[0]
            solve_time = row_data[1]
            times_up_to_this = all_times[:actual_index+1]
            
            ao5 = self.calc_raw_ao(times_up_to_this, 5)
            ao12 = self.calc_raw_ao(times_up_to_this, 12)
            ao100 = self.calc_raw_ao(times_up_to_this, 100)
            
            def fmt(val): return f"{val:.2f}" if val is not None else "-"
            
            row_position = self.history_table.rowCount()
            self.history_table.insertRow(row_position)
            self.history_table.setItem(row_position, 0, QTableWidgetItem(str(solve_id)))
            self.history_table.setItem(row_position, 1, QTableWidgetItem(fmt(solve_time)))
            self.history_table.setItem(row_position, 2, QTableWidgetItem(fmt(ao5)))
            self.history_table.setItem(row_position, 3, QTableWidgetItem(fmt(ao12)))
            self.history_table.setItem(row_position, 4, QTableWidgetItem(fmt(ao100)))
            
            for col in range(5):
                self.history_table.item(row_position, col).setTextAlignment(Qt.AlignmentFlag.AlignCenter)

    def generate_new_scramble(self):
        # Look up the puzzle type string from the database (e.g. "3x3x3 - ZBLL")
        puzzle_type = self.session_dict.get(self.current_session, "3x3x3 - WCA")
        
        # Route it to the correct function in the dictionary. 
        # Fall back to standard 3x3 WCA if something is missing.
        scramble_func = self.scramble_routers.get(puzzle_type, scrambler333.get_WCA_scramble)
        
        try:
            scramble = scramble_func()
        except Exception as e:
            scramble = f"Failed to generate scramble for {puzzle_type}. Error: {e}"
            
        self.scramble_label.setText(scramble)

    def update_timer_display(self):
        elapsed = time.time() - self.start_time
        self.timer_label.setText(f"{elapsed:.3f}")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            if self.delete_input.hasFocus():
                self.delete_input.clearFocus()
            return
        if self.delete_input.hasFocus():
            return
            
        if event.key() == Qt.Key.Key_Space:
            if event.isAutoRepeat():
                return
            if self.is_running:
                self.q_timer.stop()
                self.is_running = False
                final_time = time.time() - self.start_time
                self.timer_label.setText(f"{final_time:.3f}")
                solved_scramble = self.scramble_label.text()
                
                self.db.save_solve(self.current_session, solved_scramble, final_time)
                self.refresh_data()
                self.generate_new_scramble()
            else:
                self.is_ready = True
                self.timer_label.setStyleSheet("color: #00ff00; font-size: 140px; font-weight: bold;")
                self.timer_label.setText("0.000")

    def keyReleaseEvent(self, event):
        if self.delete_input.hasFocus():
            return
        if event.key() == Qt.Key.Key_Space:
            if event.isAutoRepeat():
                return
            if self.is_ready and not self.is_running:
                self.is_ready = False
                self.is_running = True
                self.timer_label.setStyleSheet("color: #ffffff; font-size: 140px; font-weight: bold;")
                self.start_time = time.time()
                self.q_timer.start(10)