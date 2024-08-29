import webbrowser
import threading
import time
import app
 
def run_server():
    app.app.run(host="0.0.0.0", port=5000)
 
def open_browser():
    time.sleep(2)
    webbrowser.open("http://localhost:5000")

if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    open_browser()
    server_thread.join()