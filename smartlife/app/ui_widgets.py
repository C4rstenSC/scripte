"""Shared item appearance with selection and keyboard navigation preserved."""
from PySide6.QtWidgets import QStyledItemDelegate,QStyle,QStyleOptionViewItem,QHeaderView

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
