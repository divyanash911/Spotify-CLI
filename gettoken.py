import requests,json,os,time
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

    fileobject=open("token.txt","r+")
    filecontent=fileobject.read()
    tokenvalue=filecontent.split(':')[1]
    print(tokenvalue)

    if tokenvalue=="NULL":
        bodytext={"grant_type":"authorization_code","code":code,"redirect_uri":uri,"scope":"user-modify-playback-state"}
        toencode=str(clientid)+":"+str(clientkey)
        encodedstring=base64.urlsafe_b64encode(toencode.encode("utf-8")).decode()
        headerpost={"Content-Type":"application/x-www-form-urlencoded","Authorization":"Basic " + str(encodedstring)}
        baseurl="https://accounts.spotify.com/api/token"

        response=requests.post(baseurl,headers=headerpost,data=bodytext)
        response=json.loads(response.text)
        # print(response['access_token'])
        print("----------------------------")
        print(response)
        print("----------------------------")
        spotifytoken=response['access_token']
        refreshtoken=response['refresh_token']
        
        timestamp=int(time.time())
        token=f"{timestamp}:{spotifytoken}"
        # os.environ['SPOTIFYTOKEN']=f"{timestamp}:{spotifytoken}"
        # os.environ['REFRESHTOKEN']=refreshtoken

        tokenstring="SPOTIFYTOKEN:"+token
        fileobject.seek(0)
        fileobject.write(tokenstring)
    
    else:
        fileobject=open("token.txt","r+")
        stored_value=fileobject.read()
        timestamp_saved=stored_value.split(':')[1]
        timestamp_saved = int(timestamp_saved)

        elapsed_time=int(time.time())-timestamp_saved
        print(stored_value)
        if elapsed_time>=3600:
            bodytext={"grant_type":"authorization_code","code":code,"redirect_uri":uri,"scope":"user-modify-playback-state"}
            toencode=str(clientid)+":"+str(clientkey)
            encodedstring=base64.urlsafe_b64encode(toencode.encode("utf-8")).decode()
            headerpost={"Content-Type":"application/x-www-form-urlencoded","Authorization":"Basic " + str(encodedstring)}
            baseurl="https://accounts.spotify.com/api/token"

            response=requests.post(baseurl,headers=headerpost,data=bodytext)
            response=json.loads(response.text)
            # print(response['access_token'])
            print("----------------------------")
            print(response)
            print("----------------------------")
            spotifytoken=response['access_token']
            refreshtoken=response['refresh_token']

            timestamp=int(time.time())
            # os.environ['SPOTIFYTOKEN']=f"{timestamp}:{spotifytoken}"
            fileobject=open("token.txt","r+")
            token=f"{timestamp}:{spotifytoken}"
            tokenstring="SPOTIFYTOKEN:"+token
            fileobject.seek(0)
            fileobject.write(tokenstring)



    return "Parameters received successfully!"


if __name__ == '__main__':
    clientid=input("Enter your client ID: ")
    clientkey=input("Enter your key: ")
    uri="https://localhost:5000/callback"

    url="https://accounts.spotify.com/authorize"

    header={"client_id":clientid,"response_type":"code","redirect_uri":uri,"scope":"user-modify-playback-state user-read-playback-state"}
    # print(os.environ['SPOTIFYTOKEN'])
    
    redirect_url = url + '?' + urlencode(header)
    

    app.run(port=5000,ssl_context="adhoc")



