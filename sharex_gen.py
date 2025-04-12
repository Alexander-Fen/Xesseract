import os

xess_dir = os.path.dirname(os.path.abspath(__file__))
drive = os.path.splitdrive(xess_dir)[0].upper()
venv_path = os.path.join(xess_dir, ".venv", "Scripts", "activate.bat")
script_path = os.path.join(xess_dir, "gui.py")

print("If you're using a venv:")
print(f'/c {drive} && "{venv_path}" && python "{script_path}" "$input"')

print("If you're not using a venv:")
print(f'/c {drive} && python "{script_path}" "$input"')