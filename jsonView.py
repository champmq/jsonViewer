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
    settings = json.load(open("config.json", "r"))
    data = "<pre>"
    if request.method == 'GET':
        for i in json_content.split("\n"):
            # Check if ] is not in the string
            if "]" not in i:
                # Split i if : is in it
                if ":" in i:
                    splitter = i.split(":")
                    key = splitter[0]
                    value = splitter[1]
                    part_1 = ""
                    # Check for true/false
                    if ("true" in value or "false" in value) and '"' not in value:
                        part_1 += "<span style='color: "+settings["KEY"]+"'>" + key + "</span><span style='color:"+settings["SEMICOLON"]+"'>:</span>" + value.replace(
                            "true", "<span style='color:"+settings["TRUE"]+";'>true</span>") \
                            .replace("false", "<span style='color:"+settings["FALSE"]+";'>false</span>") \
                            .replace("[", "<span style='color:"+settings["SYMBOLS"]+";'>[</span>") + "</span><br>"
                    # Check if string contains "
                    elif '"' in value:
                        part_1 += "<span style='color: "+settings["KEY"]+"'>" + key + "</span><span style='color:"+settings["SEMICOLON"]+"'>:</span>" + \
                                  "<span style='color:"+settings["VALUE"]+"'>" + value + "</span>" \
                                      .replace("[", "<span style='color:"+settings["SYMBOLS"]+";'>[</span>") + "</span><br>"
                    # String doesnt contain " -> its a number
                    else:
                        part_1 += "<span style='color: "+settings["KEY"]+"'>" + key + "</span><span style='color:"+settings["SEMICOLON"]+"'>:</span>" + \
                                  "<span style='color:"+settings["NUMBERS"]+"'>" + value + "</span>" \
                                      .replace("[", "<span style='color:"+settings["SYMBOLS"]+";'>[</span>") + "</span><br>"
                    # Check if , is not in ""
                    if "," not in find_between(value, '"', '"'):
                        data += part_1.replace(",", "<span style='color:"+settings["SYMBOLS"]+";'>,</span>", ) \
                            .replace("[", "<span style='color:"+settings["SYMBOLS"]+";'>[</span>")
                    # Change the color for the , at the end
                    else:
                        data += part_1.replace('",', '"<span style="color:'+settings["SYMBOLS"]+';">,</span>') \
                            .replace("[", "<span style='color:"+settings["SYMBOLS"]+";'>[</span>")
                # Value is in an array
                else:
                    # Check for { or }
                    if "{" in i or "}" in i:
                        data += i.replace(i, '<span style="color:'+settings["SYMBOLS"]+'">' + i + '</span>') + "<br>"
                    # Check for true/false
                    elif ("true" in i or "false" in i) and '"' not in i:
                        data += i.replace(",", '<span style="color:'+settings["SYMBOLS"]+'">,</span>') \
                                      .replace("true", "<span style='color:"+settings["TRUE"]+";'>true</span>") \
                                      .replace("false", "<span style='color:"+settings["FALSE"]+"  ;'>false</span>") + "<br>"
                    # Check if " is in the string
                    elif '"' in i:
                        # Check if , is in the string
                        if "," in find_between(i, '"', '"'):
                            data += i.replace(i, '<span style="color:'+settings["VALUE"]+'">' + i + '</span>') \
                                          .replace('",', '"<span style="color:'+settings["SYMBOLS"]+'";>,</span>') + "<br>"
                        # , is not in it
                        else:
                            data += i.replace(i, '<span style="color:'+settings["VALUE"]+'">' + i + '</span>') \
                                          .replace(",", '<span style="color:'+settings["SYMBOLS"]+'">,</span') + "<br>"
                    # No " found
                    else:
                        data += i.replace(i, "<span style='color:"+settings["NUMBERS"]+"'>" + i + "</span>") \
                                      .replace(",", '<span style="color:'+settings["SYMBOLS"]+'">,</span>') + "<br>"
            # ] found
            else:
                # Change the color of ]
                if "]," in i:
                    data += i.replace("],", "<span style='color:" + settings["SYMBOLS"] + ";'>],</span>") + "<br>"
                elif "]" in i:
                    data += i.replace("]", "<span style='color:" + settings["SYMBOLS"] + ";'>]</span>") + "<br>"

        data += "</pre>"
        return data


if __name__ == '__main__':
    settings = json.load(open("config.json", "r"))
    app.run(port=settings["PORT"])
