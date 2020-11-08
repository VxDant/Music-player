import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os", "tkinter", "pygame", "mutagen.mp3"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name="GoodMusic",
      version="0.2",
      description="Music-Player!",
      options={"build_exe": build_exe_options},
      executables=[Executable("main.py", base=base)])
