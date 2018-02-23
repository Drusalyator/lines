"""This file implement graphical version of program"""
import sys
import logging

LOGGER = logging.getLogger("lines")
logging.basicConfig(filename="lines.log", level=logging.INFO)

try:
    from core import *
    from driver import *
except ImportError as e:
    LOGGER.error(e)
    sys.exit(f"Game modules not found: {e}")

try:
    from PyQt5 import QtWidgets, QtGui, QtCore
except ImportError as e:
    LOGGER.error(e)
    sys.exit(f"PyQt5 not found: {e}")

__version__ = '1.0'
__author__ = 'Gridin Andrey'


class StartDialog(QtWidgets.QDialog):
    """Start Dialog for setting"""

    def __init__(self):
        super().__init__()
        self.parameters = {}
        self._init_dialog()
        LOGGER.info("Start dialog was initialized")

    def _init_dialog(self):
        """Initialize dialog window"""
        self.setWindowTitle("Settings")
        layout = QtWidgets.QVBoxLayout(self)
        self.name_label = self._create_label("Enter your name:")
        self.name_line_edit = QtWidgets.QLineEdit(self)
        self.name_line_edit.textChanged[str].connect(self.set_player_name)
        self.name_line_edit.setText("Player")
        self.name_line_edit.setMaxLength(10)
        self.size_label = self._create_label("Chose size of field:")
        self.size_spin_box = QtWidgets.QSpinBox(self)
        self.size_spin_box.valueChanged[int].connect(self.set_field_size)
        self.size_spin_box.lineEdit().setReadOnly(True)
        self.size_spin_box.setRange(5, 15)
        self.size_spin_box.setValue(9)
        self.button_ok = QtWidgets.QPushButton("Ok", self)
        self.empty_label = self._create_label("")
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_line_edit)
        layout.addWidget(self.size_label)
        layout.addWidget(self.size_spin_box)
        layout.addWidget(self.button_ok)
        self.setLayout(layout)
        self.show()

    def _create_label(self, text):
        """Creating text label"""
        label = QtWidgets.QLabel(text, self)
        label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
        return label

    def set_player_name(self):
        """Set player name"""
        self.parameters["name"] = self.name_line_edit.text()

    def set_field_size(self):
        """Set field size"""
        self.parameters["size"] = self.size_spin_box.value()


class Window(QtWidgets.QWidget):
    """Main Window"""

    def __init__(self):
        super().__init__()
        LOGGER.info("Main window was initialized.")
        self.start_dialog = StartDialog()
        self.start_dialog.button_ok.clicked.connect(self._new_game)
        self.record_table = RecordTable()
        self.record_table.ok_button.clicked.connect(self.record_table.hide)
        self.record_table.hide()
        self.game_board = GameBoard(self)
        self._init_window()

    def _init_window(self):
        """Initialize application window"""
        self.setWindowTitle('Lines')
        self.setFixedSize(700, 520)
        self._center()
        self.game_board.move(0, 0)
        layout = QtWidgets.QGridLayout()
        score_lcd = QtWidgets.QLCDNumber(self)
        score_lcd.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
        self.game_board.score_changed[int].connect(score_lcd.display)
        quit_button = QtWidgets.QPushButton("Quit", self)
        quit_button.setToolTip("Quit the game")
        quit_button.setFocusPolicy(QtCore.Qt.NoFocus)
        quit_button.clicked.connect(QtCore.QCoreApplication.instance().quit)
        restart_button = QtWidgets.QPushButton("Restart", self)
        restart_button.setToolTip("Restart the game with start parameters")
        restart_button.setFocusPolicy(QtCore.Qt.NoFocus)
        restart_button.clicked.connect(self._restart_game)
        save_button = QtWidgets.QPushButton("Save game", self)
        save_button.setToolTip("Save game in file")
        save_button.setFocusPolicy(QtCore.Qt.NoFocus)
        save_button.clicked.connect(self._save_game)
        load_button = QtWidgets.QPushButton("Load game", self)
        load_button.setToolTip("Load game from file")
        load_button.setFocusPolicy(QtCore.Qt.NoFocus)
        load_button.clicked.connect(self._load_game)
        record_button = QtWidgets.QPushButton("Records", self)
        record_button.setToolTip("Show table of records")
        record_button.setFocusPolicy(QtCore.Qt.NoFocus)
        record_button.clicked.connect(self._show_record)
        layout.addWidget(self._create_label("SCORE"), 4, 51, 1, 15)
        layout.addWidget(score_lcd, 6, 51, 7, 15)
        layout.addWidget(save_button, 30, 51, 3, 15)
        layout.addWidget(load_button, 33, 51, 3, 15)
        layout.addWidget(restart_button, 44, 51, 3, 15)
        layout.addWidget(quit_button, 47, 51, 3, 15)
        layout.addWidget(record_button, 24, 51, 3, 15)
        layout.addWidget(self.game_board, 0, 0, 50, 50)
        self.setLayout(layout)

    def _create_label(self, text):
        """Create text label"""
        label = QtWidgets.QLabel(text, self)
        label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)
        return label

    def _center(self):
        """Set application on center"""
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def _new_game(self):
        """Create new game"""
        self.hide()
        self.start_dialog.show()
        self.parameters = self.start_dialog.parameters
        self.start_dialog.hide()
        size = self.parameters["size"]
        player_name = self.parameters["name"]
        if player_name is not None or player_name != "":
            self.game_board.game_field = Field(size, player_name)
        else:
            self.game_board.game_field = Field(size)
        self.game_board.new_game()
        self.update()
        self.show()
        LOGGER.info(f"Start new game. Field size: {size}. Player name: {self.game_board.game_field.player}.")

    def _restart_game(self):
        """Restart game with equals parameters"""
        self.game_board.new_game()
        self.update()
        LOGGER.info("Game was restarted with starting parameters.")

    def _save_game(self):
        """Save game"""
        filename, _ = QtWidgets.QFileDialog(self).getSaveFileName(self, "Save game", "save_name", "Data (*.lines)")
        try:
            save_in_file(self.game_board.game_field, filename)
        except Exception as exception:
            LOGGER.warning("Save error.")
            LOGGER.warning(exception)
            QtWidgets.QMessageBox.warning(self, "Error", " Save Error! ", QtWidgets.QMessageBox.Ok)

    def _load_game(self):
        """Load game"""
        filename, _ = QtWidgets.QFileDialog(self).getOpenFileName(self, "Load game", filter="Data (*.lines)")
        try:
            field = load_from_file(filename)
            self.game_board.game_field = field
            self.game_board.score_changed.emit(self.game_board.game_field.score)
            self.update()
            LOGGER.info("Game was loaded from file")
        except LoadError as exception:
            LOGGER.warning("Load error")
            LOGGER.warning(exception)
            QtWidgets.QMessageBox.warning(self, "Error", " Load error! ", QtWidgets.QMessageBox.Ok)
        except Exception as exception:
            LOGGER.warning("Load error")
            LOGGER.warning(exception)
            QtWidgets.QMessageBox.warning(self, "Error", " Load error! ", QtWidgets.QMessageBox.Ok)

    def _show_record(self):
        try:
            self.record_table.fill_record_table()
        except GetRecordsError as exception:
            LOGGER.warning(f"Can not show record table {exception}")
            QtWidgets.QMessageBox.warning(self, "Error", f" Can not show Record Table ", QtWidgets.QMessageBox.Ok)
        else:
            self.record_table.show()


class GameBoard(QtWidgets.QWidget):
    """Game Board in application"""
    score_changed = QtCore.pyqtSignal(int)

    def __init__(self, perent, *params):
        """Initialize a Game Board object"""
        super().__init__(perent)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setFixedSize(500, 500)
        self.game_field = Field(*params)
        self.coordinates = None  # Used in Mouse Event
        LOGGER.info(f"Game Board Widget was initialized")

    def get_square_width(self):
        """Get the width of the cage of the playing field"""
        return self.width() // self.game_field.width

    def get_square_height(self):
        """Get the height of the cage of the playing field"""
        return self.height() // self.game_field.height

    def new_game(self):
        """Start new game"""
        self.game_field.refresh_field()
        self.score_changed.emit(self.game_field.score)

    def draw_blank_cell(self, painter, x, y):
        """Draw a blank cell"""
        painter.fillRect(x + 1, y + 1, self.get_square_width() - 2,
                         self.get_square_height() - 2, QtGui.QColor(0xDFDFDF))

    def draw_ball(self, painter, x, y, ball):
        """Draw a color ball"""
        color_table = [0x14D100, 0xFFFF00, 0xFFAE00, 0xFF1800, 0xD0006E,
                       0x3016B0, 0x01939A, 0xCD0074, 0x00AC6B, 0xAEF100]
        color_table_2 = [0x4AE83A, 0xFBFE72, 0xFFC340, 0xFF5240, 0xE73A95,
                         0x624AD8, 0x34C6CD, 0xE6399B, 0x35D699, 0xC4F83E]
        if not ball.selected:
            color_1 = QtGui.QColor(color_table[ball.color - 1])
            color_2 = QtGui.QColor(color_table_2[ball.color - 1])
        else:
            color_1 = QtGui.QColor(color_table_2[ball.color - 1])
            color_2 = QtGui.QColor(color_table[ball.color - 1])
        pen = QtGui.QPen()
        pen.setColor(color_1)
        pen.setWidth(3)
        painter.setPen(pen)
        painter.setBrush(color_2)
        painter.drawEllipse(x + 4, y + 4, self.get_square_width() - 8, self.get_square_height() - 8)

    def paintEvent(self, event):
        """Paint Event"""
        painter = QtGui.QPainter(self)
        rect = self.contentsRect()
        board_top = rect.bottom() - self.game_field.height * self.get_square_height()
        for x in range(self.game_field.height):
            for y in range(self.game_field.width):
                self.draw_blank_cell(painter, rect.left() + y * self.get_square_width(),
                                     board_top + x * self.get_square_height())
                ball = self.game_field.field[x][y]
                if ball is not None:
                    self.draw_ball(painter, rect.left() + y * self.get_square_width(),
                                   board_top + x * self.get_square_height(), ball)

    def mousePressEvent(self, event):
        """Mouse Press Event"""
        try:
            y = event.y() // self.get_square_width()
            x = event.x() // self.get_square_height()
            if x < 0 or x >= self.game_field.height or y < 0 or y >= self.game_field.width:
                return

            if self.game_field.get_ball(x, y) is None:
                if self.coordinates is not None:
                    if self.game_field.try_move(self.coordinates[0], self.coordinates[1], x, y):
                        self.game_field.make_step(self.coordinates[0], self.coordinates[1], x, y)
                        LOGGER.info(f"Player make step from {self.coordinates} in {(x, y)}.")
                        find_lines = self.game_field.find_full_lines(x, y)
                        if find_lines is None:
                            self.game_field.set_next_balls()
                            LOGGER.info(f"Following {self.game_field.number_of_next_ball} balls are installed.")
                            for coordinates in self.game_field.set_balls:
                                array = self.game_field.find_full_lines(coordinates[0], coordinates[1])
                                if array is not None:
                                    self.game_field.delete_full_lines(array)
                                    self.score_changed.emit(self.game_field.score)
                                    LOGGER.info(
                                        f"Found full lines: {find_lines} and deleted. Score: {self.game_field.score}.")
                        else:
                            self.game_field.delete_full_lines(find_lines)
                            self.score_changed.emit(self.game_field.score)
                            LOGGER.info(f"Found full lines: {find_lines} and deleted. Score: {self.game_field.score}.")
                        self.coordinates = None
            else:
                if self.coordinates is None:
                    self.game_field.get_ball(x, y).selected = True
                    self.coordinates = (x, y)
                else:
                    if self.coordinates == (x, y):
                        self.game_field.get_ball(x, y).selected = False
                        self.coordinates = None
                    else:
                        self.game_field.get_ball(x, y).selected = True
                        self.game_field.get_ball(self.coordinates[0], self.coordinates[1]).selected = False
                        self.coordinates = (x, y)
            self.update()
        except FieldFullException:
            LOGGER.info(f"Field full, game over. {self.game_field.score} points.")
            try:
                add_record(self.game_field.player, self.game_field.score)
                LOGGER.info(f'Record {self.game_field.player} : {self.game_field.score} was added.')
            except AddRecordError as exception:
                LOGGER.info(f"Can not add record {exception}")
            QtWidgets.QMessageBox.information(self, "Game Over",
                                              f"{self.game_field.player}, you scored: {self.game_field.score} points. "
                                              f"Game will be restart",
                                              QtWidgets.QMessageBox.Ok)
            self.coordinates = None
            self.new_game()


class RecordTable(QtWidgets.QWidget):
    """Record table class"""

    def __init__(self):
        """Initialize class"""
        super().__init__()
        self._init_table()

    def _init_table(self):
        """Initialize widgets on a record table"""
        self.setWindowTitle('Records')
        self.setFixedSize(240, 335)
        layout = QtWidgets.QVBoxLayout(self)
        self.title_label = QtWidgets.QLabel("Records Table", self)
        self.title_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)
        self.record_table = QtWidgets.QTableWidget(self)
        self.record_table.setRowCount(8)
        self.record_table.setColumnCount(2)
        item = QtWidgets.QTableWidgetItem("Player Name")
        self.record_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem("Score")
        self.record_table.setHorizontalHeaderItem(1, item)
        self.record_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.ok_button = QtWidgets.QPushButton("Ok", self)
        self.ok_button.setFocusPolicy(QtCore.Qt.StrongFocus)
        layout.addWidget(self.title_label)
        layout.addWidget(self.record_table)
        layout.addWidget(self.ok_button)
        self.setLayout(layout)
        self.show()

    def fill_record_table(self):
        """Fill record table"""
        records = get_records()
        counter = 0
        for record in records.items():
            text_item = QtWidgets.QTableWidgetItem(record[0])
            text_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.record_table.setItem(counter, 0, text_item)
            number_item = QtWidgets.QTableWidgetItem(f"{record[1]}")
            number_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.record_table.setItem(counter, 1, number_item)
            counter += 1


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    lines = Window()
    sys.exit(app.exec_())
