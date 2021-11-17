import json
import m1
import modeltest
from flask import Flask, send_from_directory, request, json
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

# Note:
# @app.route() is used to map the specific URL with the associated function that 
# is intended to perform some task. It is used to access some particular page 
# like Flask Tutorial in the web application.   

@app.route('/', methods=["GET"])        # Send index.html
@app.route('/index.html', methods=["GET"])
def get_index():                        # Return contents of index.html
    return send_from_directory('', 'index.html', mimetype='text/html')

@app.route('/', methods=["GET"])        # Send style.css
@app.route('/style.css', methods=["GET"])
def get_style():
    return send_from_directory('', 'style.css', mimetype='text/css')

@app.route('/main.js', methods=["GET"]) # Send main.js
def get_main():
    # Return contents of main.js
    return send_from_directory('', 'main.js', mimetype='text/javascript')

@app.route('/script.js', methods=["GET"]) # Send script.js
def get_script():
    # Return contents of script.js
    return send_from_directory('', 'script.js', mimetype='text/javascript')

@app.route('/inputMessage',methods=['GET','POST'])
def inputMessage():
    if request.method == 'POST':
        recieved = request.get_json()
        message = recieved['message']
        print(message)
        tweettext = m1.tweetText(message)
        # sentiment = m1.sentAnalysis(tweettext)
        sentiment = modeltest.predict( [tweettext] )
        print ( sentiment )
        responseDict = { "tweet" : tweettext, "sentiment" : sentiment }
        # responseDict = {"tweet": tweettext}
        response = json.dumps(responseDict)
    return response

if __name__ == '__main__':              # Run the server
    app.run(port = 5000)                # Start the server

