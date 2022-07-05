import requests, re, os,sys
from flask import Flask
from fake_headers import Headers


cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None

header = Headers(browser="chrome", os="win", headers=True)
app = Flask(__name__)

umlauteList = ["Ä", "ä", "Ö", "ö", "Ü", "ü", "ß"]
htmlNameList = ["&Auml;","&Auml;","&Ouml;","&ouml;","&Uuml;","&uuml;","szlig;"]
umlauteDict = {
    
        "Ä":"&Auml;",
        "ä":"&auml;",
        "Ö":"&Ouml;",
        "ö":"&ouml;",
        "Ü":"&Uuml;",
        "ü":"&uuml;",
        "ß":"&szlig;"
}
htmlNameDict = {
        "&Auml;": "Ä",
        "&auml;": "a",
        "&Ouml;": "Ö",
        "&ouml;": "ö",
        "&Uuml;": "Ü",
        "&uuml;": "ü",
        "&szlig;":"ß"
    
}

def Run():
    if os.path.exists(os.getcwd()+"/conf.txt") == False:
        f = open(os.getcwd()+"/conf.txt", "w")
        lines = "\"url\":\"https://www.spiegel.de\"\n\"original\":\"News und Stories\"\n\"replacement\":\"Fake News!\""
        f.writelines(lines)
        f.close()
        print(" * Creating config.text @"+os.getcwd()+"/config.txt\n * You can edit the url, and what you want to replace with what ever")
    StartServer()
    
def StartServer():
    app.run(debug=False, host="0.0.0.0", port=8888, use_reloader=False)

def LoadConfig():
    f = open(os.getcwd()+"/conf.txt", "r", encoding="utf-8")
    lines = f.readlines()
    url = "" 
    original = ""
    replacement = ""
    for line in lines:
        if "url" in line:
            url = re.search("\"url\":\"(.*)\"", line).group(1)
        if "original" in line:
            original = re.search("\"original\":\"(.*)\"", line).group(1)
        if "replacement" in line:
            replacement = re.search("\"replacement\":\"(.*)\"", line).group(1)
    return url, original, replacement
    
@app.route("/")
def route():
    url, original, replacement = LoadConfig()
    source = requests.get(url, headers=header.generate()).text
    source = re.sub(original, replacement, source)
    return source

def FromUmlaut(_input):
    try:
        for umlaut in umlauteList:
            if umlaut in _input:
                _input = re.sub(umlaut, umlauteDict[umlaut], _input)
        return _input
    except:
        return _input

def ToUmlaut(_input):
    try:
        for htmlName in htmlNameList:
            if htmlName in _input:
                _input = re.sub(htmlName, htmlNameDict[htmlName], _input)
        return _input
    except:
        return _input

if __name__ == "__main__":
    Run()
