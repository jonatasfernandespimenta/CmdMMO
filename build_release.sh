#!/bin/bash
# Script to create standalone release of CmdMMO

set -e

echo "🎮 CmdMMO Release Builder"
echo "=========================="
echo ""

# Check if PyInstaller is installed
if ! python3 -c "import PyInstaller" 2>/dev/null; then
    echo "📦 Installing PyInstaller..."
    pip3 install pyinstaller
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build dist

# Create executable
echo "🔨 Creating executable..."
pyinstaller CmdMMO.spec

# Create release directory
echo "📦 Preparing release..."
mkdir -p release
cp dist/CmdMMO release/

# Create README for release
cat > release/README.txt << 'EOF'
CmdMMO - Standalone Release
===========================

IMPORTANT: You need the server running to play!

How to use:
-----------

1. SERVER (only one person needs to run this):
   - Download and install Node.js from: https://nodejs.org/
   - Extract the 'server' folder included in this release
   - In terminal, navigate to the server folder:
     cd server
   - Install dependencies:
     npm install
   - Run the server:
     node index.js
   
2. CLIENT (all players):
   - Run the CmdMMO file
   - On Linux/Mac: sudo ./CmdMMO
   - On Windows: Run as Administrator (CmdMMO.exe)
   
   NOTE: Administrator permissions are required for 
   keyboard input handling (keyboard library)

3. CONNECTING:
   - If the server is on another machine, update the IP in:
     client/game/server.py (line with 'http://localhost:3001')

Controls:
---------
WASD or Arrow Keys - Movement
I - Inventory

Have fun! 🎮
EOF

# Copy server folder to release
echo "📁 Copying server..."
cp -r server release/

echo ""
echo "✅ Release created successfully!"
echo "📁 Location: release/"
echo ""
echo "📤 To distribute:"
echo "   - Compress the 'release/' folder into a .zip file"
echo "   - Share the file with players"
echo "   - Instruct them to read README.txt"
echo ""
