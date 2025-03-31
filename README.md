🛠 Float32, SignedInt16 Trainer

A powerful visual tool for inspecting and decoding binary data at the byte level.
Built with Python and Tkinter, this interactive application allows users to:
✨ Features

    View raw hexadecimal data with visual byte highlighting

    Decode 4-byte blocks as Float32 (little-endian) and 2-byte blocks as Signed Int16

    Save decoded values to a structured log with options:

        Clean output or Create table formatting

        Byte or Hex offset display

    Navigate data using arrow keys with adjustable step size (1, 2, or 4 bytes)

    Smart auto-detection of valid Float32 blocks (Magic Float32 mode)

    Integrated sound feedback for clicks, saves, and invalid data

    Works as a .exe (Windows) or .app (macOS) – all sounds embedded

🧩 Ideal for:

    Reverse engineering

    Firmware/data analysis

    Sensor and float pattern discovery

    Binary inspection and training


==============================================================================================================

Hex Data Converter & Visualizer

A Python GUI application built with Tkinter that provides tools for working with hexadecimal data:

    Conversions:

        Hex ↔ Float32 (little-endian)

        Hex ↔ Signed Int16 (little-endian)

        Hex ↔ Little-endian byte order conversion

    Features:

        Visualize numeric data as grayscale images

        "Float32 Magic" function to automatically extract valid float32 values from binary files

        Clipboard support for easy copying

        Clean interface with scrollable text areas

    Use Cases:

        Reverse engineering binary data

        Analyzing embedded system memory dumps

        Debugging numerical data formats

        Educational purposes for understanding binary representations

The tool is particularly useful for working with raw binary data from microcontrollers, sensors, or other embedded systems.

