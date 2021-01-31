from flask import Flask, jsonify, request
import json
app = Flask(__name__)


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


@app.route('/<json_content>', methods=['GET', 'POST'])
def home(json_content):
    if "favicon" in json_content:
        return "none"
    settings = json.load(open("config.json", "r"))
    data = "<pre>"
    if request.method == 'GET':
        for i in json_content.split("\n"):
            if ("[" or "{") not in i:
                if ":" in i:
                    splitter = i.split(":")
                    before = splitter[0]
                    after = splitter[1]
                    part_1 = ""
                    if ("true" in after or "false" in after) and '"' not in after:
                        print(after)
                        part_1 += "<span style='color: "+settings["KEY"]+"'>" + before + "</span><span style='color:"+settings["SEMICOLON"]+"'>:</span>" + after.replace(
                            "true", "<span style='color:"+settings["TRUE"]+";'>true</span>") \
                            .replace("false", "<span style='color:"+settings["FALSE"]+";'>false</span>") \
                            .replace("[", "<span style='color:"+settings["SYMBOLS"]+";'>[</span>") + "</span><br>"
                    elif '"' in after:
                        part_1 += "<span style='color: "+settings["KEY"]+"'>" + before + "</span><span style='color:"+settings["SEMICOLON"]+"'>:</span>" + \
                                  "<span style='color:"+settings["VALUE"]+"'>" + after + "</span>" \
                                      .replace("[", "<span style='color:"+settings["SYMBOLS"]+";'>[</span>") + "</span><br>"
                    else:
                        part_1 += "<span style='color: "+settings["KEY"]+"'>" + before + "</span><span style='color:"+settings["SEMICOLON"]+"'>:</span>" + \
                                  "<span style='color:"+settings["NUMBERS"]+"'>" + after + "</span>" \
                                      .replace("[", "<span style='color:"+settings["SYMBOLS"]+";'>[</span>") + "</span><br>"
                    if "," not in find_between(after, '"', '"'):
                        data += part_1.replace(",", "<span style='color:"+settings["SYMBOLS"]+";'>,</span>", ) \
                            .replace("[", "<span style='color:"+settings["SYMBOLS"]+";'>[</span>")
                    else:
                        data += part_1.replace('",', '"<span style="color:'+settings["SYMBOLS"]+';">,</span>') \
                            .replace("[", "<span style='color:"+settings["SYMBOLS"]+";'>[</span>")
                else:
                    if "{" in i or "}" in i:
                        data += i.replace(i, '<span style="color:'+settings["SYMBOLS"]+'">' + i + '</span>') + "<br>"
                    elif ("true" in i or "false" in i) and '"' not in i:
                        data += i.replace(",", '<span style="color:'+settings["SYMBOLS"]+'">,</span>') \
                                      .replace("true", "<span style='color:"+settings["TRUE"]+";'>true</span>") \
                                      .replace("false", "<span style='color:"+settings["FALSE"]+"  ;'>false</span>") + "<br>"
                    elif '"' in i:
                        if "," in find_between(i, '"', '"'):
                            data += i.replace(i, '<span style="color:'+settings["VALUE"]+'">' + i + '</span>') \
                                          .replace('",', '"<span style="color:'+settings["SYMBOLS"]+'";>,</span>') + "<br>"
                        else:
                            data += i.replace(i, '<span style="color:'+settings["VALUE"]+'">' + i + '</span>') \
                                          .replace(",", '<span style="color:'+settings["SYMBOLS"]+'">,</span') + "<br>"

                    else:
                        data += i.replace(i, "<span style='color:"+settings["NUMBERS"]+"'>" + i + "</span>") \
                                      .replace(",", '<span style="color:'+settings["SYMBOLS"]+'">,</span>') + "<br>"
            else:
                if "]" in i:
                    data += i.replace("]", "<span style='color:"+settings["SYMBOLS"]+";'>]</span>") + "<br>"
                elif ""
        data += "</pre>"
        return data


if __name__ == '__main__':
    settings = json.load(open("config.json", "r"))
    app.run(port=settings["PORT"])
