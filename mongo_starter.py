import subprocess
import sys
import os

def start_mongodb():
    try:
        # Ensure the database directory exists
        db_path = r"C:\data\db"
        if not os.path.exists(db_path):
            os.makedirs(db_path)

        # Path to mongod.exe
        mongod_path = r"C:\Program Files\MongoDB\Server\6.0\bin\mongod.exe"

        # Start MongoDB
        subprocess.Popen([mongod_path, "--dbpath", db_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("MongoDB started successfully.")
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
