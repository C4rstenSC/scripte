"""Shared item appearance with selection and keyboard navigation preserved."""
from PySide6.QtWidgets import QStyledItemDelegate,QStyle,QStyleOptionViewItem

class CleanSelectionDelegate(QStyledItemDelegate):
    def paint(self,painter,option,index):
        clean=QStyleOptionViewItem(option)
        clean.state &= ~QStyle.State_HasFocus
        super().paint(painter,clean,index)
