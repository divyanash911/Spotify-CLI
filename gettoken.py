import requests
from urllib.parse import urlencode
from flask import Flask,redirect,request
import base64
app=Flask(__name__)

@app.route('/')
def login():
    
    
    return redirect(redirect_url)

@app.route('/callback', methods=['GET'])
def handle_callback():
    # Retrieve the query parameters from the redirected URI
    code=''
    code = request.args.get('code')
    # print(code)

    bodytext={"grant_type":"authorization_code","code":code,"redirect_uri":uri}
    toencode=str(clientid)+":"+str(clientkey)
    encodedstring=base64.b64encode(toencode.encode("utf-8"))
    headerpost={"Content-Type":"application/x-www-form-urlencoded","Authorization":"Basic " + str(encodedstring)}
    baseurl="https://accounts.spotify.com/api/token"

    response=requests.post(baseurl,headers=headerpost,data=bodytext)
    print(response.text)

    return "Parameters received successfully!"


if __name__ == '__main__':
    clientid=input("Enter your client ID: ")
    clientkey=input("Enter your key: ")
    uri="https://localhost:5000/callback"

    url="https://accounts.spotify.com/authorize"

    header={"client_id":clientid,"response_type":"code","redirect_uri":uri}
    
    
    redirect_url = url + '?' + urlencode(header)
    

    app.run(port=5000,ssl_context="adhoc")



