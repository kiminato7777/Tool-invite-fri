from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex
from PySide6.QtGui import QColor, QBrush, QIcon, QPalette
from PySide6.QtWidgets import QApplication

class AccountTableModel(QAbstractTableModel):
    def __init__(self, accounts, parent=None):
        super().__init__(parent)
        self.accounts = accounts
        self.headers = ["No.", "Category", "Username", "Profile Name", "Friend Count", "Password", "Cookies", "Status", "Sent", "Failed"]

    def rowCount(self, parent=QModelIndex()):
        return len(self.accounts)

    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()
        acc = self.accounts[row]

        if role == Qt.DisplayRole:
            if col == 0: return str(row + 1)
            if col == 1: return acc.category
            if col == 2: return acc.username
            if col == 3: return acc.profile_name
            if col == 4: return str(acc.friend_count)
            if col == 5: return acc.password if acc.password else "None"
            if col == 6: return "✅ Yes" if acc.cookies else "❌ No"
            if col == 7: return acc.status
            if col == 8: return str(acc.invites_sent)
            if col == 9: return str(acc.invites_failed)

        # Detect active background light/dark theme dynamically
        is_dark = False
        app = QApplication.instance()
        if app:
            is_dark = app.palette().color(QPalette.Window).lightness() < 128

        if role == Qt.ForegroundRole:
            # Special row coloring for status flags to guarantee high contrast
            if acc.status in ("Check Point", "Chapracters dynamic function"):
                return QBrush(QColor("#fecaca" if is_dark else "#991b1b"))
            elif acc.status in ("Dead", "Error", "Login Failed", "Failed", "Error Verify Google", "Error Login Google"):
                return QBrush(QColor("#fef08a" if is_dark else "#854d0e"))
            
            # Default coloring for normal rows
            if col == 7: # Status column
                if acc.status == "Active":
                    return QBrush(QColor("#34d399" if is_dark else "#059669"))
                elif acc.status in ("Idle", "Pending"):
                    return QBrush(QColor("#94a3b8"))
                else:
                    return QBrush(QColor("#60a5fa" if is_dark else "#2563eb"))
            elif col == 6: # Cookies column
                if acc.cookies:
                    return QBrush(QColor("#34d399" if is_dark else "#059669"))
                else:
                    return QBrush(QColor("#f87171" if is_dark else "#dc2626"))
            
            # Normal text fallback based on active theme
            return QBrush(QColor("#e2e8f0" if is_dark else "#0f172a"))

        if role == Qt.BackgroundRole:
            if acc.status in ("Check Point", "Chapracters dynamic function"):
                return QBrush(QColor("#450a0a" if is_dark else "#fee2e2"))
            elif acc.status in ("Dead", "Error", "Login Failed", "Failed", "Error Verify Google", "Error Login Google"):
                return QBrush(QColor("#422006" if is_dark else "#fef9c3"))

        if role == Qt.TextAlignmentRole:
            if col in (0, 4, 8, 9):
                return Qt.AlignCenter
            return Qt.AlignLeft | Qt.AlignVCenter

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[section]
        return None

    def update_data(self):
        self.layoutAboutToBeChanged.emit()
        self.layoutChanged.emit()

    def update_row(self, row):
        start = self.index(row, 0)
        end = self.index(row, self.columnCount() - 1)
        self.dataChanged.emit(start, end, [Qt.DisplayRole, Qt.ForegroundRole, Qt.BackgroundRole])
