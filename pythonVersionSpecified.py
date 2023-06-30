from os import system, path
class CMDController():
    def __init__(self) -> None:
        self.path = path.realpath(__file__)

    def pull(self, url):
        system(f'cd {self.path}')
        system('cd ..')
        system(f'git pull {url}')