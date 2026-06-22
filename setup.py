from cx_Freeze import setup, Executable

files = {
    "packages": ["pygame", "sqlite3"],
    "include_files": [
        ("asset", "asset")
    ]
}

executables = [
    Executable(
        script="main.py",
        target_name="MagicForest.exe",
        base=None
    )
]

setup(
    name="MagicForest",
    version="1.0",
    description="Magic Forest app",
    options={"build_exe": files},
    executables=executables
)