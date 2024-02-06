from flask import Flask, request
from flask_cors import cross_origin, CORS
from searching.processedPdf import ProcessedPDF
from typing import Any

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.post("/")
@cross_origin()
def upload_file():
    
    print("Somone trying to access")
    files = request.files
    print(files)
    response: dict[str, list[Any]] = dict()
    for file in files.getlist("file"):
        print("Got something!")
        pdf = ProcessedPDF(file)
        print(pdf.name)
        print(pdf.event_result.columns)
        pdf.get_all_sentences()
        if pdf.name == None:
            pass # This will never be triggered
        else:
            item = response.get(pdf.name)
            if (item):
                item.append(pdf.toJson())
            else:
                response[pdf.name] = [pdf.toJson()]
                
    return response
    
