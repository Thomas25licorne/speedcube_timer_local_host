# Personal Speedcube Timer

## Description
Many speedcubers use multiple computers, making it difficult to keep solve histories synchronized across devices. This project was designed to provide a simple, portable alternative. The application stores all solve data in a local SQLite database located within the application's directory, making the entire timer self-contained. Whether it's run from a USB drive, portable SSD, or local folder, your complete solve history travels with the application—no cloud services or manual synchronization required.

## Setup
Ensure you have Python installed on your system. Then, install the required dependencies via your terminal:

```bash
pip install PyQt6 pyTwistyScrambler
```

## Usage

1. **Launch the Application:** Execute `app.py`. On the first launch, the application will automatically initialize the database and create default 3x3 and 4x4 sessions.
2. **Manage Sessions:** To create a custom session (e.g., Pyraminx, 3x3 One-Handed), click the session dropdown menu at the top right, select **+ Add New Session...**, and
   configure your puzzle type.
4. **Start Solving:** Follow the generated scramble on the screen. Hold down the **Spacebar** until the timer turns green, release it to start the timer, and press the **Spacebar**
   again to stop it.
6. **Delete a Solve:** Enter the unique solve ID into the deletion box in the bottom right corner. **Note:** Press the `Escape` key after deleting to drop focus from the text box
   before starting your next solve.

## Operation & Architecture
Every solve is permanently recorded in the local SQLite database. The application logs the session name, the exact scramble generated, the solve duration, and the timestamp. 
This data is dynamically queried to calculate and display your current and best MO3, AO5, AO12, and AO100 averages.

## Acknowledgements
This project relies on the excellent work of open-source developers:
* **pyTwistyScrambler:** Scramble generation is powered by the [pyTwistyScrambler/](https://github.com/euphwes/pyTwistyScrambler?tab=readme-ov-file) library. Massive thanks to the author for maintaining an incredible tool for generating official WCA scrambles.
* **PyQt6:** The graphical user interface and event handling are built using the PyQt6 framework.

pyTwistyScrambler License Notice:
Copyright (c) 2018 The Python Packaging Authority

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
