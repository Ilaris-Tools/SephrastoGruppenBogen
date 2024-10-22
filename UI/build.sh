#!/bin/bash
for ui_file in $(find . -name "*.ui"); do
    py_file="${ui_file%.ui}.py"
    echo "pyside6-uic $ui_file -o $py_file"
    pyside6-uic "$ui_file" -o "$py_file"
done