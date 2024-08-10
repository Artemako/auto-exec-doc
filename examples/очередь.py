import sys
import multiprocessing
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtGui import QAction

def worker():
    import time
    time.sleep(5)
    return "Работа завершена"

def start_worker(result_queue):
    result = worker()
    result_queue.put(result)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Пример PySide6 и Multiprocessing")
        self.setGeometry(100, 100, 300, 200)
        
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        
        action = QAction("Запустить процесс", self)
        action.triggered.connect(self.run_process)
        file_menu.addAction(action)
        
    def run_process(self):
        self.result_queue = multiprocessing.Queue()
        self.process = multiprocessing.Process(target=start_worker, args=(self.result_queue,))
        self.process.start()
        self.process.join()  # Ждать, пока процесс завершится
        # Получить результат
        result = self.result_queue.get()
        self.show_message(result)

    def show_message(self, message):
        msg = QMessageBox()
        msg.setText(message)
        msg.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
