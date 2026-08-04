from cx_Freeze import setup, Executable

setup(
    name="NVIDIAScript",
    version="0.1",
    description="Script to get NVIDIA graphics card information",
    executables=[Executable("NVIDIAScript.py")]
)
