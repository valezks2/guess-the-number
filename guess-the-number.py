import sys
import random
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QDesktopWidget, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIntValidator, QIcon

class ModernGuessGame(QWidget):
    def __init__(self):
        super().__init__()
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.game_over = False  
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Guess the Number')
        self.setWindowIcon(QIcon('logo.png'))
        self.setFixedSize(500, 450) 
        self.center()
        
        self.setStyleSheet("""
            QWidget {
                background-color: #F8FAFC;
            }
            QFrame#card {
                background-color: #FFFFFF;
                border-radius: 20px;
            }
            QLabel {
                background-color: transparent;
            }
            QLabel#title {
                color: #1E293B;
                font-size: 28px;
                font-weight: 800;
                margin-top: 20px;
            }
            QLabel#subtitle {
                color: #64748B;
                font-size: 15px;
                margin-bottom: 20px;
            }
            QLineEdit {
                background-color: #F1F5F9;
                color: #1E293B;
                border: 2px solid #E2E8F0;
                border-radius: 12px;
                padding: 12px;
                font-size: 24px;
                font-weight: bold;
                margin: 10px 40px;
            }
            QLineEdit:focus {
                border: 2px solid #3B82F6;
                background-color: #FFFFFF;
            }
            QPushButton {
                background-color: #3B82F6;
                color: white;
                border-radius: 12px;
                font-size: 16px;
                font-weight: bold;
                padding: 14px;
                margin: 20px 40px;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
            QPushButton:pressed {
                background-color: #1D4ED8;
            }
            QPushButton:disabled {
                background-color: #CBD5E1;
            }
            QLabel#feedback {
                font-size: 16px;
                font-weight: 600;
                margin-top: 10px;
                padding: 10px;
            }
        """)

        main_layout = QVBoxLayout()
        
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setAlignment(Qt.AlignCenter)

        self.label_title = QLabel("Guess the Number")
        self.label_title.setObjectName("title")
        self.label_title.setAlignment(Qt.AlignCenter)

        self.label_sub = QLabel("Pick a number between 1 and 100")
        self.label_sub.setObjectName("subtitle")
        self.label_sub.setAlignment(Qt.AlignCenter)

        self.input_num = QLineEdit()
        self.input_num.setAlignment(Qt.AlignCenter)
        
        self.input_num.setMaxLength(3)
        
        only_digits = QIntValidator()
        self.input_num.setValidator(only_digits)
        
        self.input_num.returnPressed.connect(self.handle_action)

        self.btn_check = QPushButton("Try number")
        self.btn_check.setCursor(Qt.PointingHandCursor)
        self.btn_check.clicked.connect(self.handle_action)

        self.label_feedback = QLabel("")
        self.label_feedback.setObjectName("feedback")
        self.label_feedback.setAlignment(Qt.AlignCenter)

        card_layout.addWidget(self.label_title)
        card_layout.addWidget(self.label_sub)
        card_layout.addWidget(self.input_num)
        card_layout.addWidget(self.btn_check)
        card_layout.addWidget(self.label_feedback)

        main_layout.addWidget(card)
        self.setLayout(main_layout)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def handle_action(self):
        if self.game_over:
            self.reset_game()
        else:
            self.check_guess()

    def check_guess(self):
        text = self.input_num.text()
        
        if not text:
            self.label_feedback.setText("Please enter a number!")
            self.label_feedback.setStyleSheet("color: #EF4444; background-color: transparent;")
            self.input_num.setFocus()
            return

        guess = int(text)

        if guess > 100 or guess < 1:
            self.label_feedback.setText("Only numbers between 1 and 100 are allowed")
            self.label_feedback.setStyleSheet("color: #EF4444; background-color: transparent;")
            self.input_num.selectAll()
            self.input_num.setFocus()
            return

        self.attempts += 1

        if guess < self.secret_number:
            self.label_feedback.setText(f"Too low! Try higher (Attempt {self.attempts})")
            self.label_feedback.setStyleSheet("color: #EF4444; background-color: transparent;") 
            self.input_num.selectAll()  
            self.input_num.setFocus()
        elif guess > self.secret_number:
            self.label_feedback.setText(f"Too high! Try lower (Attempt {self.attempts})")
            self.label_feedback.setStyleSheet("color: #EF4444; background-color: transparent;") 
            self.input_num.selectAll()
            self.input_num.setFocus()
        else:
            self.label_feedback.setText(f"Perfect! Guessed in {self.attempts} tries.")
            self.label_feedback.setStyleSheet("color: #10B981; font-size: 18px; background-color: transparent;") 
            
            self.game_over = True
            self.btn_check.setText("Play Again")
            self.input_num.setReadOnly(True)  

    def reset_game(self):
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.game_over = False
        
        self.input_num.setReadOnly(False)
        self.input_num.clear()
        self.input_num.setFocus()
        self.btn_check.setText("Try number")
        self.label_feedback.setText("")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ModernGuessGame()
    ex.show()
    sys.exit(app.exec_())