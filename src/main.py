from PyQt5.QtWidgets import (
    QMainWindow, QFileDialog, QMessageBox, QTableWidget,
    QTableWidgetItem, QPushButton, QVBoxLayout, QHBoxLayout,
    QWidget, QLabel, QLineEdit, QComboBox, QCheckBox, QSpinBox
)
from PyQt5.QtCore import Qt
from pathlib import Path
import os
from core import FileRenamer
import sys



class RenamerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.renamer = FileRenamer()
        self.current_files = []
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Premium File Renamer Pro")
        self.resize(900, 700)

        # Main Widgets
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Original", "→", "New Name"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setColumnWidth(0, 300)
        self.table.setColumnWidth(1, 50)

        # File Selection
        self.btn_add = QPushButton("📁 Add Files")
        self.btn_add_folder = QPushButton("📂 Add Folder")
        self.btn_clear = QPushButton("❌ Clear List")

        # Renaming Options
        self.opt_combo = QComboBox()
        self.opt_combo.addItems([
            "Add Prefix/Suffix", 
            "Complete Name Replacement",
            "Pattern-Based Naming"
        ])
        
        # Option 1: Prefix/Suffix
        self.prefix = QLineEdit()
        self.suffix = QLineEdit()
        
        # Option 2: Complete Replacement
        self.new_name = QLineEdit()
        self.new_name.setPlaceholderText("Enter new base name")
        
        # Option 3: Pattern
        self.pattern = QLineEdit()
        self.pattern.setPlaceholderText("e.g., 'Photo_{num}_{date}'")
        
        # Numbering Options
        self.num_start = QSpinBox()
        self.num_start.setRange(1, 9999)
        self.num_start.setValue(1)
        self.num_digits = QSpinBox()
        self.num_digits.setRange(1, 5)
        self.num_digits.setValue(3)
        
        # Extension Options
        self.ext_combo = QComboBox()
        self.ext_combo.addItems([
            "Keep original",
            "Change to:",
            "Remove extension"
        ])
        self.new_ext = QLineEdit()
        self.new_ext.setPlaceholderText("Enter new extension (without dot)")
        
        # Other Options
        self.case = QComboBox()
        self.case.addItems(["Keep Case", "lowercase", "UPPERCASE", "Title Case"])
        self.chk_hash = QCheckBox("Add unique hash")
        self.hash_length = QSpinBox()
        self.hash_length.setRange(4, 32)
        self.hash_length.setValue(8)
        
        # Action Buttons
        self.btn_preview = QPushButton("🔍 Preview Changes")
        self.btn_rename = QPushButton("💾 Execute Rename")
        self.btn_undo = QPushButton("↩️ Undo Last Operation")

        # Layout
        main_layout = QVBoxLayout()
        
        # File Selection Row
        file_layout = QHBoxLayout()
        file_layout.addWidget(self.btn_add)
        file_layout.addWidget(self.btn_add_folder)
        file_layout.addWidget(self.btn_clear)
        main_layout.addLayout(file_layout)
        
        # Renaming Mode Selection
        main_layout.addWidget(QLabel("Renaming Mode:"))
        main_layout.addWidget(self.opt_combo)
        
        # Dynamic Options Stack
        self.option_stack = QHBoxLayout()
        
        # Prefix/Suffix Options
        self.prefix_group = QWidget()
        prefix_layout = QHBoxLayout()
        prefix_layout.addWidget(QLabel("Prefix:"))
        prefix_layout.addWidget(self.prefix)
        prefix_layout.addWidget(QLabel("Suffix:"))
        prefix_layout.addWidget(self.suffix)
        self.prefix_group.setLayout(prefix_layout)
        
        # Complete Replacement Options
        self.replace_group = QWidget()
        replace_layout = QHBoxLayout()
        replace_layout.addWidget(QLabel("New Name:"))
        replace_layout.addWidget(self.new_name)
        self.replace_group.setLayout(replace_layout)
        
        # Pattern Options
        self.pattern_group = QWidget()
        pattern_layout = QHBoxLayout()
        pattern_layout.addWidget(QLabel("Pattern:"))
        pattern_layout.addWidget(self.pattern)
        self.pattern_group.setLayout(pattern_layout)
        
        self.option_stack.addWidget(self.prefix_group)
        self.option_stack.addWidget(self.replace_group)
        self.option_stack.addWidget(self.pattern_group)
        main_layout.addLayout(self.option_stack)
        
        # Numbering Options
        num_layout = QHBoxLayout()
        num_layout.addWidget(QLabel("Numbering Start:"))
        num_layout.addWidget(self.num_start)
        num_layout.addWidget(QLabel("Digits:"))
        num_layout.addWidget(self.num_digits)
        main_layout.addLayout(num_layout)
        
        # Extension Options
        ext_layout = QHBoxLayout()
        ext_layout.addWidget(QLabel("Extension:"))
        ext_layout.addWidget(self.ext_combo)
        ext_layout.addWidget(self.new_ext)
        main_layout.addLayout(ext_layout)
        
        # Additional Options
        opt_layout = QHBoxLayout()
        opt_layout.addWidget(QLabel("Case:"))
        opt_layout.addWidget(self.case)
        opt_layout.addWidget(self.chk_hash)
        opt_layout.addWidget(self.hash_length)
        main_layout.addLayout(opt_layout)
        
        # Action Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_preview)
        btn_layout.addWidget(self.btn_rename)
        btn_layout.addWidget(self.btn_undo)
        main_layout.addLayout(btn_layout)
        
        # Results Table
        main_layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Connections
        self.btn_add.clicked.connect(self.add_files)
        self.btn_add_folder.clicked.connect(self.add_folder)
        self.btn_clear.clicked.connect(self.clear_list)
        self.btn_preview.clicked.connect(self.preview_changes)
        self.btn_rename.clicked.connect(self.execute_rename)
        self.btn_undo.clicked.connect(self.undo_operation)


        # Initialize
        self.update_options_view()
        self.update_ext_field()

    def update_options_view(self):
        """Show/hide appropriate options based on selected mode"""
        mode = self.opt_combo.currentIndex()
        self.prefix_group.setVisible(mode == 0)
        self.replace_group.setVisible(mode == 1)
        self.pattern_group.setVisible(mode == 2)

    def update_ext_field(self):
        """Enable/disable extension field based on selection"""
        self.new_ext.setEnabled(self.ext_combo.currentIndex() == 1)

    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files")
        if files:
            self.current_files.extend(files)
            self.update_file_list()

    def add_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.current_files.extend(
                str(f) for f in Path(folder).rglob('*') if f.is_file()
            )
            self.update_file_list()

    def clear_list(self):
        self.current_files.clear()
        self.table.setRowCount(0)

    def update_file_list(self):
        """Update the table with current file list"""
        self.table.setRowCount(len(self.current_files))
        for row, filepath in enumerate(self.current_files):
            self.table.setItem(row, 0, QTableWidgetItem(Path(filepath).name))
            self.table.setItem(row, 1, QTableWidgetItem("→"))
            self.table.setItem(row, 2, QTableWidgetItem(""))

    def get_rules(self) -> dict:
        """Get current renaming rules from UI"""
        rules = {
            'mode': self.opt_combo.currentIndex(),
            'case': self.case.currentText().lower(),
            'hash': self.hash_length.value() if self.chk_hash.isChecked() else None,
            'num_start': self.num_start.value(),
            'num_digits': self.num_digits.value(),
            'ext_mode': self.ext_combo.currentIndex(),
            'new_ext': self.new_ext.text().strip()
        }

        if rules['mode'] == 0:  # Prefix/Suffix
            rules.update({
                'prefix': self.prefix.text(),
                'suffix': self.suffix.text()
            })
        elif rules['mode'] == 1:  # Complete Replacement
            rules['new_name'] = self.new_name.text()
        else:  # Pattern
            rules['pattern'] = self.pattern.text()

        return rules

    def preview_changes(self):
        if not self.current_files:
            QMessageBox.warning(self, "Warning", "No files selected!")
            return

        rules = self.get_rules()
        preview = self.renamer.generate_preview(self.current_files, rules)
        self.table.setRowCount(len(preview))

        for row, (original, new) in enumerate(preview):
            self.table.setItem(row, 0, QTableWidgetItem(Path(original).name))
            self.table.setItem(row, 1, QTableWidgetItem("→"))
            self.table.setItem(row, 2, QTableWidgetItem(Path(new).name))

    def execute_rename(self):
        if not hasattr(self.renamer, 'preview_data') or not self.renamer.preview_data:
            QMessageBox.warning(self, "Warning", "Generate preview first!")
            return

        confirm = QMessageBox.question(
            self,
            "Confirm Rename",
            f"About to rename {len(self.renamer.preview_data)} files. Continue?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            result = self.renamer.execute_rename()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText(
                f"Renamed {result['success']} files successfully!\n"
                f"Failed: {result['failed']}"
            )
            msg.exec_()
            self.clear_list()

    def undo_operation(self):
        if not hasattr(self.renamer, 'operations') or not self.renamer.operations:
            QMessageBox.warning(self, "Warning", "Nothing to undo!")
            return

        result = self.renamer.undo_last_operation()
        QMessageBox.information(
            self, "Undo Complete", 
            f"Undone {result['undone']} renames\nFailed: {result['failed']}"
        )

def main():
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = RenamerGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py /path/to/folder")
    else:
        FileRenamer().rename(sys.argv[1])
    main()