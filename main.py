from appData.graphics.mainWindow import MainWindow
from pythonVersionSpecified import CMDController

git_repo = ''

if __name__ == "__main__":
    controller = CMDController()
    controller.pull(git_repo)
    main = MainWindow()