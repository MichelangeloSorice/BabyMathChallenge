#!/usr/bin/env bash
script_dir=$(dirname $0)
ui_files=("${script_dir}\src\gui\babymath.ui")
for ui_file in "${ui_files[@]}"
do
    out_file="${ui_file%.*}_ui.py"
    echo "Generating $out_file"
    python -m PyQt5.uic.pyuic -x "$ui_file" -o "$out_file"
done

echo "All up to date!"