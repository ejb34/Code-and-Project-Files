from urllib.request import urlopen


url = "https://www.youtube.com/watch?v=MxOpBty9TIE"

page  = urlopen(url)

html_bytes = page.read()
html = html_bytes.decode("utf-8")

print(html)