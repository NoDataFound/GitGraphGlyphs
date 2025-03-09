#!/bin/bash

echo "0xDEADBEEF | Deploying cyberwarfare toolkit..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "0xC001CAFE | Install complete. Launching GitGraphGlyphs..."
python gitgraph.py
