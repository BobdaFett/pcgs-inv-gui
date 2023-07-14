# The main file that checks for the required dependencies.

import importlib.util as imported   # Required to check for imports.
import os                           # Required for system commands.

if imported.find_spec("PySide6") is None:
    print("PySide6 package was not found.\nInstalling PySide6...")
    # Installs PySide6.
    os.system("pip install pyside6")

if imported.find_spec("requests") is None:
    print("Requests package was not found.\nInstalling requests package...")
    # Installs the requests framework.
    os.system("pip install requests")

# Launch the main program.
import main
main