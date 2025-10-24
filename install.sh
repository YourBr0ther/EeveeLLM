#!/bin/bash
# EeveeLLM Installation Script

echo "================================================"
echo "  EeveeLLM Installation"
echo "================================================"
echo ""

# Check Python version
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Install required packages
echo ""
echo "Installing required Python packages..."
pip install colorama pyyaml python-dateutil requests

echo ""
echo "================================================"
echo "  Installation Complete!"
echo "================================================"
echo ""
echo "To run the application:"
echo "  python main.py"
echo ""
echo "To see the brain council in action:"
echo "  python main.py"
echo "  > debug brain"
echo "  > talk Want to explore?"
echo ""
echo "For more information, see:"
echo "  - README.md (full documentation)"
echo "  - QUICKSTART.md (quick guide)"
echo "  - PROJECT_SUMMARY.md (technical details)"
echo ""
