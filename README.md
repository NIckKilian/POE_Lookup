# POE_Lookup
Path of Exile character lookup window


Gives you information on a Path of Exile account, including characters,leagues and ladder stats.
Using their own API to gather data with JSON Request/Responses.


Settings file contains the URLs to  the API plus the last account you search will be saved
to use next time you open.




Pyinstaller can be run to create an EXE to use
pyinstaller --console --onefile --windowed --hidden-import=PyQt5.sip PoeMain.py




UI file used to create the UI in pyQT Designer.
Use this to fool with the UI and apply to project : pyuic5 -x PoEFrame.ui -o PoEFrame.py
