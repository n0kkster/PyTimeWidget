@echo off
python -m pip install -r requirements.txt
rm widget.pyw
cp widget.py widget.pyw
start widget.pyw
