import os
import subprocess
import sys
import re

def find_mongodb_path():
    """Find the path to the latest installed MongoDB."""
    search_dirs = [
        r"C:\Program Files\MongoDB\Server",
        r"C:\Program Files (x86)\MongoDB\Server"
    ]
    
    for base_dir in search_dirs:
        if os.path.exists(base_dir):
            versions = [
                dir_name for dir_name in os.listdir(base_dir)
                if re.match(r"^\d+\.\d+$", dir_name)  # Match version numbers like 6.0 or 7.0
            ]
            if versions:
                # Sort versions and return the latest one
                latest_version = sorted(versions, key=lambda v: list(map(int, v.split('.'))), reverse=True)[0]
                return os.path.join(base_dir, latest_version, "bin", "mongod.exe")
    
    return None

def start_mongodb():
    try:
        # Detect the path to mongod.exe
        mongod_path = find_mongodb_path()
        if not mongod_path or not os.path.exists(mongod_path):
            raise FileNotFoundError("MongoDB executable not found. Please install MongoDB.")

        # Use a default database path
        db_path = r"C:\data\db"
        if not os.path.exists(db_path):
            os.makedirs(db_path)

        # Start MongoDB
        subprocess.Popen([mongod_path, "--dbpath", db_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"MongoDB started successfully using {mongod_path}.")
    except Exception as e:
        print(f"Error starting MongoDB: {e}")
        sys.exit(1)


def stop_mongodb_server():
    try:
        if os.name == "nt":  # For Windows
            subprocess.run(["taskkill", "/F", "/IM", "mongod.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif os.name == "posix":  # For macOS/Linux
            subprocess.run(["pkill", "mongod"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            print("Unsupported OS for stopping MongoDB server.")
        print("MongoDB server stopped successfully.")
    except Exception as e:
        print(f"Error stopping MongoDB server: {e}")

if __name__ == "__main__":
    start_mongodb()
