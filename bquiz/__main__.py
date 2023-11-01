from .app import App
from .gui import run

def main():
    app = App()
    thread = app.spawn()
    run()
    thread.join()

if __name__ == "__main__":
    main()
