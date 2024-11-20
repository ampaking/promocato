import sys
import json
import os
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QTextEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QFrame,
    QAbstractItemView,
    QDialog,
    QDialogButtonBox,
)
from PySide6.QtCore import QTimer, QDateTime, Qt, QRectF, QSize
from PySide6.QtGui import QFont, QPainter, QColor, QPen, QIcon, QPalette
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl
import math


class SimpleClockWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(300, 300)  # Fixed size for the clock
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)  # Update every second

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect()
        radius = min(rect.width(), rect.height()) / 2 - 15
        center = rect.center()

        # Draw clock face
        painter.setBrush(QColor("#36384a"))  # Dark background
        painter.setPen(QPen(QColor("#F9C846"), 4))  # Yellow border
        painter.drawEllipse(center, radius, radius)

        # Draw hour numerals
        painter.setPen(QPen(QColor("#F9C846"), 2))  # Yellow numerals
        font = QFont("Orbitron", 14, QFont.Bold)  # Gaming-inspired font
        painter.setFont(font)
        for hour in range(1, 13):
            angle = (hour / 12) * 360
            rad = math.radians(angle - 90)
            x = center.x() + (radius - 40) * math.cos(rad)
            y = center.y() + (radius - 40) * math.sin(rad)
            text = str(hour)
            text_rect = QRectF(x - 10, y - 10, 20, 20)
            painter.drawText(text_rect, Qt.AlignCenter, text)

        # Get current time
        current_time = QDateTime.currentDateTime()
        hour = current_time.time().hour() % 12
        minute = current_time.time().minute()
        second = current_time.time().second()

        # Calculate angles
        hour_angle = (hour + minute / 60) * 30  # 360 / 12 = 30
        minute_angle = (minute + second / 60) * 6  # 360 / 60 = 6
        second_angle = second * 6  # 360 / 60 = 6

        # Draw hour hand
        painter.save()
        painter.translate(center)
        painter.rotate(hour_angle)
        painter.setPen(QPen(QColor("#F9C846"), 6))  # Yellow hour hand
        painter.drawLine(0, 0, 0, -60)
        painter.restore()

        # Draw minute hand
        painter.save()
        painter.translate(center)
        painter.rotate(minute_angle)
        painter.setPen(QPen(QColor("#b1e7ff"), 4))  # Light blue minute hand
        painter.drawLine(0, 0, 0, -80)
        painter.restore()

        # Draw second hand
        painter.save()
        painter.translate(center)
        painter.rotate(second_angle)
        painter.setPen(QPen(QColor("#0286df"), 2))  # Bright blue second hand
        painter.drawLine(0, 0, 0, -100)
        painter.restore()

        # Draw center point
        painter.setBrush(QColor("#F9C846"))  # Yellow center
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(center, 6, 6)


class EditNoteDialog(QDialog):
    def __init__(self, current_note, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Note")
        self.setFixedSize(500, 400)

        layout = QVBoxLayout()

        label = QLabel("Modify the note below:")
        label.setFont(QFont("Orbitron", 14))
        layout.addWidget(label)

        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(current_note)
        self.text_edit.setFont(QFont("Orbitron", 12))
        layout.addWidget(self.text_edit)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def get_note(self):
        return self.text_edit.toPlainText().strip()


class PromocatoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Promocato App")
        self.setMinimumSize(600, 400)  # Minimum window size
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #36384a;  /* Dark Gray/Blue */
            }
            QLabel {
                color: #F9C846;  /* Yellow */
                font-size: 18px;
                font-family: 'Orbitron', sans-serif;
            }
            QPushButton {
                font-size: 16px;
                padding: 12px 24px;
                background-color: #0286df;  /* Bright Blue */
                color: #36384a;  /* Dark text */
                border: 2px solid #F9C846;  /* Yellow border */
                border-radius: 10px;
                transition: background-color 0.3s, transform 0.2s;
            }
            QPushButton:hover {
                background-color: #b1e7ff;  /* Light Blue on hover */
                transform: scale(1.05);
            }
            QPushButton:pressed {
                background-color: #F9C846;  /* Yellow on press */
                transform: scale(0.95);
            }
            QPushButton:disabled {
                background-color: #555555;
                border: 2px solid #333333;
                color: #CCCCCC;
            }
            QComboBox {
                font-size: 16px;
                padding: 8px;
                background-color: #36384a;  /* Dark Gray/Blue */
                color: #F9C846;  /* Yellow */
                border: 2px solid #F9C846;  /* Yellow border */
                border-radius: 5px;
                font-family: 'Orbitron', sans-serif;
            }
            QComboBox::drop-down {
                border: 0;
            }
            QComboBox::drop-down::button {
                background-color: #0286df;  /* Bright Blue */
            }
            QTableWidget {
                font-size: 16px;
                background-color: #36384a;  /* Dark Gray/Blue */
                color: #F9C846;  /* Yellow */
                border: 2px solid #F9C846;  /* Yellow border */
                selection-background-color: #b1e7ff;  /* Light Blue */
                word-wrap: true;
            }
            QHeaderView::section {
                background-color: #0286df;  /* Bright Blue */
                color: white;
                font-weight: bold;
                padding: 10px;
                font-family: 'Orbitron', sans-serif;
            }
            QTextEdit {
                font-size: 16px;
                padding: 12px;
                background-color: #36384a;  /* Dark Gray/Blue */
                color: #F9C846;  /* Yellow */
                border: 2px solid #F9C846;  /* Yellow border */
                border-radius: 5px;
                font-family: 'Orbitron', sans-serif;
            }
            QFrame {
                border: none;
            }
            """
        )

        # Initialize Media Player for Alarm Sound
        self.media_player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.media_player.setAudioOutput(self.audio_output)

        if getattr(sys, "frozen", False):
            # Running as a PyInstaller bundle
            if sys.executable.startswith("/usr/bin"):
                # Installed via .deb package
                base_path = "/usr/share/promocato"
            else:
                # Running from a PyInstaller bundle
                base_path = os.path.dirname(sys.executable)
        else:
            # Running as a normal Python script during development
            base_path = os.path.dirname(os.path.abspath(__file__))

        # Example usage
        sound_path = os.path.join(base_path, "..", "sound", "data-scaner.wav")
        self.history_path = os.path.join(base_path, "..", "history.json")

        # Check if the sound file exists
        if not os.path.exists(sound_path):
            self.show_message("Error", f"Sound file not found: {sound_path}")
        else:
            self.media_player.setSource(QUrl.fromLocalFile(os.path.abspath(sound_path)))
            self.audio_output.setVolume(70)

        # Main widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main layout
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(
            20, 20, 20, 20
        )  # Reduced margins for better space usage
        self.main_layout.setSpacing(20)  # Reduced spacing

        # Current Time Display - Simple Analog Clock
        self.clock_widget = SimpleClockWidget()
        self.main_layout.addWidget(self.clock_widget, alignment=Qt.AlignCenter)

        # Countdown Timer Display
        self.countdown_label = QLabel("No Active Timer")
        self.countdown_label.setAlignment(Qt.AlignCenter)
        countdown_font = QFont("Orbitron", 36, QFont.Bold)
        self.countdown_label.setFont(countdown_font)
        self.main_layout.addWidget(self.countdown_label)

        # Timers for updating the clocks
        self.init_timers()

        # Timer Selection
        self.timer_frame = QFrame()
        self.timer_layout = QHBoxLayout(self.timer_frame)
        self.timer_label = QLabel("Select Timer Duration:")
        self.timer_combo = QComboBox()
        self.timer_options = [1, 5, 10, 20, 30, 60]
        for minutes in self.timer_options:
            self.timer_combo.addItem(f"{minutes} Minute{'s' if minutes > 1 else ''}")
        self.timer_combo.setCurrentIndex(0)
        self.timer_layout.addWidget(self.timer_label)
        self.timer_layout.addWidget(self.timer_combo)
        self.main_layout.addWidget(self.timer_frame)

        # Note Entry
        self.note_frame = QFrame()
        self.note_layout = QVBoxLayout(self.note_frame)
        self.note_label = QLabel("Note (Optional):")
        self.note_entry = QTextEdit()
        self.note_entry.setPlaceholderText(
            "Enter your note here...\nYou can add multiple lines."
        )
        self.note_entry.setFixedHeight(100)  # Fixed height for note entry
        self.note_layout.addWidget(self.note_label)
        self.note_layout.addWidget(self.note_entry)
        self.main_layout.addWidget(self.note_frame)

        # Buttons Layout
        self.buttons_frame = QFrame()
        self.buttons_layout = QHBoxLayout(self.buttons_frame)
        self.start_button = QPushButton("Start Timer")
        self.start_button.setIcon(QIcon())  # Optionally, set a gaming-themed icon here
        self.start_button.clicked.connect(self.toggle_timer)
        self.buttons_layout.addWidget(self.start_button)
        self.main_layout.addWidget(self.buttons_frame)

        # History Display - Table
        self.history_frame = QFrame()
        self.history_layout = QVBoxLayout(self.history_frame)
        self.history_label = QLabel("History:")
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(
            ["Timestamp", "Duration (min)", "Note", "Actions"]
        )
        self.history_table.horizontalHeader().setStretchLastSection(True)
        self.history_table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )  # Make table read-only
        self.history_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.history_table.setStyleSheet(
            """
            QHeaderView::section {
                background-color: #0286df;  /* Bright Blue */
                color: white;
                font-weight: bold;
                padding: 10px;
                font-family: 'Orbitron', sans-serif;
            }
            QTableWidget {
                word-wrap: true;
            }
        """
        )
        self.history_table.setColumnWidth(3, 200)  # Increased Actions column width

        self.history_layout.addWidget(self.history_label)
        self.history_layout.addWidget(self.history_table)
        self.main_layout.addWidget(self.history_frame)

        # Load history
        self.load_history()

        # Countdown Timer Variables
        self.active_timer = False
        self.remaining_seconds = 0
        self.current_notes = []
        self.current_duration = 0
        self.history_data = []  # To keep track of history entries

    def init_timers(self):
        # Timer for Countdown Display
        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self.update_countdown)

    def update_countdown_label(self):
        minutes, seconds = divmod(self.remaining_seconds, 60)
        self.countdown_label.setText(f"Time Remaining: {minutes:02d}:{seconds:02d}")

    def toggle_timer(self):
        if not self.active_timer:
            self.start_timer()
        else:
            self.stop_timer()

    def start_timer(self):
        selected_index = self.timer_combo.currentIndex()
        selected_minutes = self.timer_options[selected_index]
        notes_text = self.note_entry.toPlainText().strip()

        if selected_minutes <= 0:
            self.show_message(
                "Invalid Duration", "Please select a valid timer duration."
            )
            return

        # Notes are optional
        if notes_text:
            self.current_notes = [
                note.strip() for note in notes_text.split("\n") if note.strip()
            ]
        else:
            self.current_notes = []

        self.current_duration = selected_minutes

        # Auto-save notes and clear the notes field
        if self.current_notes:
            self.add_to_history(selected_minutes, self.current_notes)
            self.save_history()
            self.note_entry.clear()

        # Start the countdown
        self.remaining_seconds = selected_minutes * 60
        self.update_countdown_label()
        self.countdown_timer.start(1000)  # Update every second
        self.active_timer = True

        # Disable notes input and history actions during active timer
        self.note_entry.setDisabled(True)
        self.history_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # Disable action buttons in table
        for row in range(self.history_table.rowCount()):
            action_widget = self.history_table.cellWidget(row, 3)
            if action_widget:
                for i in range(action_widget.layout().count()):
                    button = action_widget.layout().itemAt(i).widget()
                    if button:
                        button.setDisabled(True)

        # Change Start Timer button to Stop Timer
        self.start_button.setText("Stop Timer")
        self.start_button.setStyleSheet(
            """
            QPushButton {
                font-size: 16px;
                padding: 12px 24px;
                background-color: #E74C3C;  /* Bright Red */
                color: white;
                border: 2px solid #C0392B;
                border-radius: 10px;
                transition: background-color 0.3s, transform 0.2s;
            }
            QPushButton:hover {
                background-color: #C0392B;
                transform: scale(1.05);
            }
            QPushButton:pressed {
                background-color: #A93226;
                transform: scale(0.95);
            }
            QPushButton:disabled {
                background-color: #555555;
                border: 2px solid #333333;
                color: #CCCCCC;
            }
        """
        )

    def stop_timer(self):
        self.countdown_timer.stop()
        self.active_timer = False
        self.countdown_label.setText("No Active Timer")

        # Re-enable notes input and history actions
        self.note_entry.setDisabled(False)
        self.history_table.setEditTriggers(
            QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked
        )
        # Re-enable action buttons in table
        for row in range(self.history_table.rowCount()):
            action_widget = self.history_table.cellWidget(row, 3)
            if action_widget:
                for i in range(action_widget.layout().count()):
                    button = action_widget.layout().itemAt(i).widget()
                    if button:
                        button.setDisabled(False)

        # Change Stop Timer button back to Start Timer
        self.start_button.setText("Start Timer")
        self.start_button.setStyleSheet(
            """
            QPushButton {
                font-size: 16px;
                padding: 12px 24px;
                background-color: #0286df;  /* Bright Blue */
                color: #36384a;  /* Dark text */
                border: 2px solid #F9C846;  /* Yellow border */
                border-radius: 10px;
                transition: background-color 0.3s, transform 0.2s;
            }
            QPushButton:hover {
                background-color: #b1e7ff;  /* Light Blue on hover */
                transform: scale(1.05);
            }
            QPushButton:pressed {
                background-color: #F9C846;  /* Yellow on press */
                transform: scale(0.95);
            }
            QPushButton:disabled {
                background-color: #555555;
                border: 2px solid #333333;
                color: #CCCCCC;
            }
        """
        )
        self.show_message("Timer Stopped", "The timer has been stopped.")

    def update_countdown(self):
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.update_countdown_label()
        else:
            self.countdown_timer.stop()
            self.timer_finished()

    def timer_finished(self):
        self.active_timer = False

        # Play the alarm sound in loop
        self.media_player.setLoops(QMediaPlayer.Loops.Infinite)
        self.media_player.play()

        # Show popup notification with notes and duration
        self.show_timer_popup()

    def show_timer_popup(self):
        if self.current_notes:
            notes_display = "\n".join(self.current_notes)
        else:
            notes_display = ""

        msg_text = f"Time's up!\nDuration: {self.current_duration} minute{'s' if self.current_duration > 1 else ''}"
        if notes_display:
            msg_text += f"\nNote:\n{notes_display}"

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Timer Alert")
        msg_box.setText(msg_text)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok)
        # Connect the OK button to stop the sound
        msg_box.button(QMessageBox.Ok).clicked.connect(self.stop_sound)
        msg_box.exec()

        # After popup is closed, reset the countdown label
        self.countdown_label.setText("No Active Timer")

        # Stop the alarm sound
        self.stop_sound()

        # Re-enable notes input and history actions
        self.note_entry.setDisabled(False)
        self.history_table.setEditTriggers(
            QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked
        )
        # Re-enable action buttons in table
        for row in range(self.history_table.rowCount()):
            action_widget = self.history_table.cellWidget(row, 3)
            if action_widget:
                for i in range(action_widget.layout().count()):
                    button = action_widget.layout().itemAt(i).widget()
                    if button:
                        button.setDisabled(False)

        # Change Stop Timer button back to Start Timer
        self.start_button.setText("Start Timer")
        self.start_button.setStyleSheet(
            """
            QPushButton {
                font-size: 16px;
                padding: 12px 24px;
                background-color: #0286df;  /* Bright Blue */
                color: #36384a;  /* Dark text */
                border: 2px solid #F9C846;  /* Yellow border */
                border-radius: 10px;
                transition: background-color 0.3s, transform 0.2s;
            }
            QPushButton:hover {
                background-color: #b1e7ff;  /* Light Blue on hover */
                transform: scale(1.05);
            }
            QPushButton:pressed {
                background-color: #F9C846;  /* Yellow on press */
                transform: scale(0.95);
            }
            QPushButton:disabled {
                background-color: #555555;
                border: 2px solid #333333;
                color: #CCCCCC;
            }
        """
        )

    def stop_sound(self):
        if self.media_player.playbackState() == QMediaPlayer.PlayingState:
            self.media_player.stop()

    def add_to_history(self, minutes, notes):
        timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        notes_combined = "\n".join(notes) if notes else ""
        row_position = self.history_table.rowCount()
        self.history_table.insertRow(row_position)
        self.history_table.setItem(row_position, 0, QTableWidgetItem(timestamp))
        self.history_table.setItem(row_position, 1, QTableWidgetItem(str(minutes)))
        self.history_table.setItem(row_position, 2, QTableWidgetItem(notes_combined))

        # Add action buttons
        action_widget = QWidget()
        action_layout = QHBoxLayout(action_widget)
        action_layout.setContentsMargins(5, 0, 5, 0)

        edit_button = QPushButton("Edit")
        delete_button = QPushButton("Delete")

        # Style the action buttons
        edit_button.setStyleSheet(
            """
            QPushButton {
                font-size: 14px;
                padding: 8px 16px;
                background-color: #0286df;  /* Bright Blue */
                color: #36384a;  /* Dark text */
                border: 2px solid #F9C846;  /* Yellow border */
                border-radius: 5px;
                transition: background-color 0.3s, transform 0.2s;
            }
            QPushButton:hover {
                background-color: #b1e7ff;  /* Light Blue on hover */
                transform: scale(1.05);
            }
            QPushButton:pressed {
                background-color: #F9C846;  /* Yellow on press */
                transform: scale(0.95);
            }
            QPushButton:disabled {
                background-color: #555555;
                border: 2px solid #333333;
                color: #CCCCCC;
            }
        """
        )
        delete_button.setStyleSheet(
            """
            QPushButton {
                font-size: 14px;
                padding: 8px 16px;
                background-color: #F9C846;  /* Yellow */
                color: #36384a;  /* Dark text */
                border: 2px solid #0286df;  /* Bright Blue border */
                border-radius: 5px;
                transition: background-color 0.3s, transform 0.2s;
            }
            QPushButton:hover {
                background-color: #FFD700;  /* Gold on hover */
                transform: scale(1.05);
            }
            QPushButton:pressed {
                background-color: #FFC300;  /* Darker Gold on press */
                transform: scale(0.95);
            }
            QPushButton:disabled {
                background-color: #555555;
                border: 2px solid #333333;
                color: #CCCCCC;
            }
        """
        )

        # Connect buttons with row-specific functions using lambda with default argument
        edit_button.clicked.connect(
            lambda checked, row=row_position: self.edit_entry(row)
        )
        delete_button.clicked.connect(
            lambda checked, row=row_position: self.delete_entry(row)
        )

        action_layout.addWidget(edit_button)
        action_layout.addWidget(delete_button)
        self.history_table.setCellWidget(row_position, 3, action_widget)

        # Adjust row height for multi-line notes
        self.history_table.resizeRowToContents(row_position)

        # Append to internal history data
        self.history_data.append(
            {"timestamp": timestamp, "duration": minutes, "notes": notes}
        )

    def edit_entry(self, row):
        if self.active_timer:
            self.show_message(
                "Timer Running", "Cannot edit entries while the timer is running."
            )
            return

        if row >= len(self.history_data):
            self.show_message("Error", "Selected entry does not exist.")
            return

        entry = self.history_data[row]
        current_notes = "\n".join(entry["notes"]) if entry["notes"] else ""

        # Open custom dialog to edit notes
        edit_dialog = EditNoteDialog(current_notes, self)
        if edit_dialog.exec() == QDialog.Accepted:
            new_notes_text = edit_dialog.get_note()
            if new_notes_text:
                new_notes = [
                    note.strip() for note in new_notes_text.split("\n") if note.strip()
                ]
            else:
                new_notes = []

            # Update internal data
            self.history_data[row]["notes"] = new_notes

            # Update table
            self.history_table.item(row, 2).setText("\n".join(new_notes))

            # Update history.json
            self.save_history()

            self.show_message("Edited", "The selected entry has been updated.")

    def delete_entry(self, row):
        if self.active_timer:
            self.show_message(
                "Timer Running", "Cannot delete entries while the timer is running."
            )
            return

        if row >= len(self.history_data):
            self.show_message("Error", "Selected entry does not exist.")
            return

        confirmation = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete this entry?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if confirmation == QMessageBox.Yes:
            # Remove from table
            self.history_table.removeRow(row)

            # Remove from internal data
            del self.history_data[row]

            # Remove from history.json
            self.save_history()

            # Remove action buttons from remaining rows to fix row indices
            for r in range(row, self.history_table.rowCount()):
                action_widget = self.history_table.cellWidget(r, 3)
                if action_widget:
                    for i in range(action_widget.layout().count()):
                        button = action_widget.layout().itemAt(i).widget()
                        if button:
                            # Reconnect buttons with updated row index
                            if button.text() == "Edit":
                                button.clicked.disconnect()
                                button.clicked.connect(
                                    lambda checked, row=r: self.edit_entry(row)
                                )
                            elif button.text() == "Delete":
                                button.clicked.disconnect()
                                button.clicked.connect(
                                    lambda checked, row=r: self.delete_entry(row)
                                )

            self.show_message("Deleted", "The selected entry has been deleted.")

    def show_message(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()

    def save_history(self):
        try:
            with open(self.history_path, "w") as f:
                json.dump(self.history_data, f, indent=4)
        except Exception as e:
            self.show_message("Error", f"Failed to save history: {e}")

    def load_history(self):
        history = self.load_history_data()
        self.history_data = history.copy()  # Keep a copy for synchronization
        for entry in history:
            timestamp = entry.get("timestamp", "")
            duration = entry.get("duration", "")
            notes = entry.get("notes", [])
            notes_combined = "\n".join(notes) if notes else ""
            row_position = self.history_table.rowCount()
            self.history_table.insertRow(row_position)
            self.history_table.setItem(row_position, 0, QTableWidgetItem(timestamp))
            self.history_table.setItem(row_position, 1, QTableWidgetItem(str(duration)))
            self.history_table.setItem(
                row_position, 2, QTableWidgetItem(notes_combined)
            )

            # Add action buttons
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(5, 0, 5, 0)

            edit_button = QPushButton("Edit")
            delete_button = QPushButton("Delete")

            # Style the action buttons
            edit_button.setStyleSheet(
                """
                QPushButton {
                    font-size: 14px;
                    padding: 8px 16px;
                    background-color: #0286df;  /* Bright Blue */
                    color: #36384a;  /* Dark text */
                    border: 2px solid #F9C846;  /* Yellow border */
                    border-radius: 5px;
                    transition: background-color 0.3s, transform 0.2s;
                }
                QPushButton:hover {
                    background-color: #b1e7ff;  /* Light Blue on hover */
                    transform: scale(1.05);
                }
                QPushButton:pressed {
                    background-color: #F9C846;  /* Yellow on press */
                    transform: scale(0.95);
                }
                QPushButton:disabled {
                    background-color: #555555;
                    border: 2px solid #333333;
                    color: #CCCCCC;
                }
            """
            )
            delete_button.setStyleSheet(
                """
                QPushButton {
                    font-size: 14px;
                    padding: 8px 16px;
                    background-color: #F9C846;  /* Yellow */
                    color: #36384a;  /* Dark text */
                    border: 2px solid #0286df;  /* Bright Blue border */
                    border-radius: 5px;
                    transition: background-color 0.3s, transform 0.2s;
                }
                QPushButton:hover {
                    background-color: #FFD700;  /* Gold on hover */
                    transform: scale(1.05);
                }
                QPushButton:pressed {
                    background-color: #FFC300;  /* Darker Gold on press */
                    transform: scale(0.95);
                }
                QPushButton:disabled {
                    background-color: #555555;
                    border: 2px solid #333333;
                    color: #CCCCCC;
                }
            """
            )

            # Connect buttons with row-specific functions using lambda with default argument
            edit_button.clicked.connect(
                lambda checked, row=row_position: self.edit_entry(row)
            )
            delete_button.clicked.connect(
                lambda checked, row=row_position: self.delete_entry(row)
            )

            action_layout.addWidget(edit_button)
            action_layout.addWidget(delete_button)
            self.history_table.setCellWidget(row_position, 3, action_widget)

            # Adjust row height for multi-line notes
            self.history_table.resizeRowToContents(row_position)

    def load_history_data(self):
        try:
            with open(self.history_path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []


def main():
    app = QApplication(sys.argv)

    # Optional: Set a gaming-inspired application icon
    # app.setWindowIcon(QIcon("path_to_icon.png"))
    print("Initializing app...")

    window = PromocatoApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    print("Running main()...")
    main()
