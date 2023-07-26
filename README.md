# pcgs-inv-gui
A very simple application to search for and keep track of a collector's coin inventory through the use of CSV files and the Public PCGS API.
I'm a college student, and this is a fun little project to help out a friend.

It will be written using Python and PySide6 Qt (with QtWidgets).
External pull requests are welcome! If you see something that really bugs you and you think you can do it better, send it over, I'll take a look at it.

When this application releases, I will not be able to provide OneDrive or Google Drive API functionality. Unfortunately, due to the way that Python is interpreted,
I would have to release the entire application along with the API keys that provide authentication. This would be a breach of contract against PCGS, Microsoft, and
Google. Therefore, it is not possible, however you're welcome to use your own PCGS Public API key.

# Installation/Setup
For the first time setup, run the command ```setup.py install``` from inside the pcgs-inv-gui folder. I've never set this sort of thing up before, so if it doesn't work let me know.
The program should be run from the ```main.py``` file in the ```src``` folder. This will check for your PCGS Public API key. If you do not have one, please go to https://api.pcgs.com/publicapi and sign up for one. The file will allow you to open a webpage directed there as well.
Should you want to set up the file yourself, rather than have the program do it for you, create a file in the directory and name it "```.env```". You will then need to make a field named ```"PCGS_CERT"``` on the first line, followed by ```" = "your key here""```. Eventually it'll look something like ```"PCGS_CERT = ha;dlfng;ah;lkjd"``` (your key will be much longer)

# Running the program
As mentioned before, everything operates out of ```main.py```. It will display a window on your screen, and the rest is pretty intuitive.

# Bugs
Should you find a bug, please report it in the "Issues" tab of the GitHub. I'll get to it eventually, and clearly mark if I'm no longer working on this specific project.

# Future
In the future, this program may be rewritten in C++, C#, or Rust. This may happen if/when I decide to implement OneDrive and/or Google Drive integration. This isn't currently in the works, but it's definitely in my mind. If I start development, I'll drop a link here for those interested.
