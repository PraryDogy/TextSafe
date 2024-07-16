import os
import sys

from gui import MainWin, MyApp

if os.path.exists("lib"): 
    #lib folder appears when we pack this project to .app with py2app

    py_ver = sys.version_info
    py_ver = f"{py_ver.major}.{py_ver.minor}"

    plugin_path = os.path.join(
        "lib",
        f"python{py_ver}",
        "PyQt5",
        "Qt5",
        "plugins",
        )

    os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = plugin_path

app = MyApp(sys.argv)
main_win = MainWin(parent=None)
main_win.show()
app.exec()