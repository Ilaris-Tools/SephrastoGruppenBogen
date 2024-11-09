from PySide6 import QtWidgets, QtCore

class CustomTreeWidgetItem(QtWidgets.QWidget):
    def __init__(self, text, cat):
        super().__init__()
        self.cat = cat
        layout = QtWidgets.QHBoxLayout(self)
        self.label = QtWidgets.QLabel(text)
        self.toggle = QtWidgets.QCheckBox()
        self.toggle.setTristate(True)
        self.toggle.setCheckState(QtCore.Qt.Unchecked)  # todo get from cat
        self.toggle.stateChanged.connect(self.onCheckChanged)
        layout.addWidget(self.label)
        layout.addStretch()
        layout.addWidget(self.toggle)
        layout.setContentsMargins(0, 0, 0, 0)
        self.memory = []
        # flags to avoid recursion
        self.categoryChanged = False
        self.singleItemChanged = False

    def onCheckChanged(self, state):
        if self.singleItemChanged:
            return
        if not len(self.memory) == self.cat.childCount():
            self.memory = []
            for i in range(self.cat.childCount()):
                self.memory.append(self.cat.child(i).isSelected())

        self.categoryChanged = True
        for i in range(self.cat.childCount()):
            child = self.cat.child(i)
            if state == 0:
                child.setSelected(False)
            elif state == 2:
                self.memory[i] = child.isSelected()
                self.parent().blockSignals(True)
                child.setSelected(True)
                self.parent().blockSignals(False)
            elif state == 1:
                child.setSelected(self.memory[i])
        self.categoryChanged = False

    def handle_child_selection_changed(self):
        # Custom logic when child selection changes
        print("Child selection changed")

class FilterableTreeWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Create the main layout
        layout = QtWidgets.QVBoxLayout(self)

        # Create the search bar
        self.search_bar = QtWidgets.QLineEdit(self)
        self.search_bar.setPlaceholderText("Search...")
        layout.addWidget(self.search_bar)

        # Create the tree widget
        self.tree_widget = QtWidgets.QTreeWidget(self)
        self.tree_widget.setHeaderHidden(True)
        self.tree_widget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        layout.addWidget(self.tree_widget)

        # Populate the tree widget with example data
        self.populate_tree()

        # Connect the search bar to the filter
        self.search_bar.textChanged.connect(self.filter_tree)

        # Connect the itemSelectionChanged signal to a custom slot
        self.tree_widget.itemSelectionChanged.connect(self.handle_item_selection_changed)

        # Store the previous selection
        self.previous_selection = set()

    def populate_tree(self):
        categories = {
            "Fruits": ["Apple", "Banana", "Cherry"],
            "Vegetables": ["Carrot", "Lettuce", "Tomato"],
            "Dairy": ["Milk", "Cheese", "Yogurt"]
        }

        for category, items in categories.items():
            category_item = QtWidgets.QTreeWidgetItem(self.tree_widget)
            category_item.setFlags(category_item.flags() | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsAutoTristate)
            category_item.setCheckState(0, QtCore.Qt.Unchecked)
            category_item.setExpanded(True)
            custom_widget = CustomTreeWidgetItem(category, category_item)
            self.tree_widget.setItemWidget(category_item, 0, custom_widget)
            for item in items:
                item_widget = QtWidgets.QTreeWidgetItem(category_item, [item])
                item_widget.setFlags(item_widget.flags() | QtCore.Qt.ItemIsUserCheckable)
                # item_widget.setCheckState(0, QtCore.Qt.Unchecked)

    def filter_tree(self, text):
        for i in range(self.tree_widget.topLevelItemCount()):
            top_item = self.tree_widget.topLevelItem(i)
            self.filter_item(top_item, text)

    def filter_item(self, item, text):
        match = text.lower() in item.text(0).lower()
        for i in range(item.childCount()):
            child = item.child(i)
            match = self.filter_item(child, text) or match
        item.setHidden(not match)
        return match

    def handle_item_selection_changed(self):
        current_selection = set(self.tree_widget.selectedItems())
        added_items = current_selection - self.previous_selection
        removed_items = self.previous_selection - current_selection
        for item in added_items | removed_items:
            print(f"Item changed: {item.text(0)}")
            parent = item.parent()
            if parent:
                custom_widget = self.tree_widget.itemWidget(parent, 0)
                if custom_widget:
                    print("parents check_state")
                    if custom_widget.categoryChanged:
                        return
                    if custom_widget.toggle.checkState() != QtCore.Qt.PartiallyChecked:
                        # Temporarily disconnect the itemChanged signal to not restore
                        custom_widget.singleItemChanged = True
                        custom_widget.toggle.setCheckState(QtCore.Qt.PartiallyChecked)
                        custom_widget.singleItemChanged = False
                        # item.setCheckState(0, state)
                    # custom_widget.toggle.setCheckState(QtCore.Qt.PartiallyChecked)
                    # custom_widget.handle_child_selection_changed()
        self.previous_selection = current_selection

# Example usage
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = FilterableTreeWidget()
    widget.show()
    app.exec()