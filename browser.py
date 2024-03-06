import webbrowser
from settings import chrome_path
def open_incognito(url):
    webbrowser.get(chrome_path).open_new(url)
    