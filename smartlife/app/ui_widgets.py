"""Shared item appearance with selection and keyboard navigation preserved."""
from PySide6.QtWidgets import QStyledItemDelegate,QStyle,QStyleOptionViewItem,QHeaderView,QTreeWidgetItem

class CleanSelectionDelegate(QStyledItemDelegate):
    def paint(self,painter,option,index):
        clean=QStyleOptionViewItem(option)
        clean.state &= ~QStyle.State_HasFocus
        super().paint(painter,clean,index)


def fit_columns(tree):
    """Size every column to its widest header/cell plus one logical centimetre."""
    header=tree.header();header.setStretchLastSection(False);header.setSectionResizeMode(QHeaderView.Interactive);header.setResizeContentsPrecision(-1)
    margin=max(1,round(tree.logicalDpiX()/2.54))
    for column in range(tree.columnCount()):
        tree.resizeColumnToContents(column)
        tree.setColumnWidth(column,tree.columnWidth(column)+margin)


class DeviceItem(QTreeWidgetItem):
    """Group by room, keeping names A–Z in either room sort direction."""
    def __lt__(self, other):
        from PySide6.QtCore import QCollator,QLocale,Qt
        tree=self.treeWidget()
        if tree is not None and tree.sortColumn()==1:
            collator=QCollator(QLocale(QLocale.German,QLocale.Germany))
            collator.setCaseSensitivity(Qt.CaseInsensitive)
            room=collator.compare(self.text(1),other.text(1))
            if room:return room<0
            name=collator.compare(self.text(0),other.text(0))
            return name>0 if tree.header().sortIndicatorOrder()==Qt.DescendingOrder else name<0
        column=tree.sortColumn() if tree is not None else 0
        return self.text(column)<other.text(column)
