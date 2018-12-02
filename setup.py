import cx_Freeze

executables = [cx_Freeze.Executable(script="src/main.py",
                                    icon="src/resources/icon.ico",
                                    targetName="Space Game.exe")]

include_files = ["src"]

packages = ["pygame",
            "json"]

excludes = ["tkinter",
            "numpy",
            "OpenGL"]

cx_Freeze.setup(
    name="Space Game",
    options={
        "build_exe": {
            "packages": packages,
            "excludes": excludes,
            "include_files": include_files
        }
    },
    executables=executables
)
