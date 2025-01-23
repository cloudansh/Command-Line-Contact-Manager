import os
import subprocess
import sys
from mongo_starter import start_mongodb, stop_mongodb_server
def run_in_new_terminal(script_name, terminal_name="Custom Terminal"):
    try:
        if sys.platform == "win32":
            subprocess.Popen(
                ["start", "cmd", "/k", f'title {terminal_name} & python {script_name}'],
                shell=True,
            )
        elif sys.platform == "darwin":  # macOS
            subprocess.Popen(
                ["osascript", "-e",
                 f'tell application "Terminal" to do script "echo -n -e \\\\033]0;{terminal_name}\\\\a; python {script_name}"']
            )
        else:  # Linux/Unix
            subprocess.Popen(
                ["gnome-terminal", "--title", terminal_name, "--", "python3", script_name]
            )
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    script_to_run = "logic.py"  # Replace with the path to your script
    custom_terminal_name = "Contact Manager"
    run_in_new_terminal(script_to_run, custom_terminal_name)
