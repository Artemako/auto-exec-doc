import sys
import multiprocessing
import time
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtGui import QAction

def worker(identifier):
    # Имитация длительной работы
    time.sleep(2)
    return f"Работа завершена для процесса {identifier}"

def start_worker(result_queue, identifier):
    result = worker(identifier)
    result_queue.put(result)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Пример PySide6 и Multiprocessing")
        self.setGeometry(100, 100, 400, 300)

        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        action = QAction("Запустить процессы", self)
        action.triggered.connect(self.run_processes)
        file_menu.addAction(action)

    def run_processes(self):
        result_queue = multiprocessing.Queue()
        processes = []

        # Создаем несколько процессов
        for i in range(4):  # Запустим 4 процесса
            process = multiprocessing.Process(target=start_worker, args=(result_queue, i + 1))
            processes.append(process)
            process.start()

        # Ждем завершения всех процессов
        for process in processes:
            process.join()

        # Получаем результаты
        results = [result_queue.get() for _ in processes]
        self.show_message("\n".join(results))

    def show_message(self, message):
        msg = QMessageBox()
        msg.setText(message)
        msg.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
