from typing import Optional
import requests,json
import typer
import time
from gettoken import app
from flask import Flask,redirect,request
from urllib.parse import urlencode
import base64,os,signal
def interval(timestamp):
    timestamp=int(timestamp)
    elapsedtime = int(time.time())-timestamp
    if elapsedtime>=3600:
        return 1    
    else:
        return 0


def Play(apikey:str)->None:
    playurl="https://api.spotify.com/v1/me/player/play"
    header={"Authorization": f"Bearer {apikey}","Content-Type": "application/json"}
    # bodytext={"scope":"user-modify-playback-state user-read-playback-state"}
    bodytext={"device_id":"9bbf970aa5f3ad5351152aabc69b1f9208017b05"}
    response=requests.put(playurl,headers=header,)
    # print(response.text)

def Pause(apikey:str)->None:
    pauseurl="https://api.spotify.com/v1/me/player/pause"
    header={"Authorization": f"Bearer {apikey}","Content-Type": "application/json"}
    response=requests.put(pauseurl,headers=header,)

def main(play:bool=False,pause:bool=False,curr:bool=False,name:bool=False):
    # print("hi",play,pause,curr,name)

    # clientid=input("Enter your client ID: ")
    # clientkey=input("Enter your key: ")

    url="https://accounts.spotify.com/api/token"
    fileobject=open("token.txt","r")
    apikey=fileobject.read().split(':')[2]
    # print(apikey)
    boolarray=[play,pause,curr,name]
    if boolarray.count(True)>1:
        print("Can't have multiple arguments at once!!")
        raise typer.Exit()
    elif play:
        Play(apikey)
    elif pause:
        Pause(apikey)
    elif curr:
        ShowCurr(apikey)
    else:
        NameShow(apikey)

if __name__ == "__main__":
    
    fileobject=open("token.txt","r")
    filecontent=fileobject.read()

    if filecontent.split(':')[1]=="NULL" or interval(filecontent.split(':')[1])==1:
        clientid=input("Enter your client ID: ")
        clientkey=input("Enter your key: ")
        # uri="https://localhost:5000/callback"

        # url="https://accounts.spotify.com/authorize"

        # header={"client_id":clientid,"response_type":"code","redirect_uri":uri,"scope":"user-modify-playback-state user-read-playback-state"}       
        # redirect_url = url + '?' + urlencode(header)
        app=Flask(__name__)

        @app.route('/')
        def login():
            # clientid=input("Enter your client ID: ")
            # clientkey=input("Enter your key: ")
            # uri="https://localhost:5000/callback"

            # url="https://accounts.spotify.com/authorize"

            # header={"client_id":clientid,"response_type":"code","redirect_uri":uri,"scope":"user-modify-playback-state user-read-playback-state"}
            # # print(os.environ['SPOTIFYTOKEN'])
            
            # redirect_url = url + '?' + urlencode(header)
            
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
                os.kill(os.getpid(), signal.SIGINT)
            
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
                    # print("----------------------------")
                    # print(response)
                    # print("----------------------------")
                    spotifytoken=response['access_token']
                    refreshtoken=response['refresh_token']

                    timestamp=int(time.time())
                    # os.environ['SPOTIFYTOKEN']=f"{timestamp}:{spotifytoken}"
                    fileobject=open("token.txt","r+")
                    token=f"{timestamp}:{spotifytoken}"
                    tokenstring="SPOTIFYTOKEN:"+token
                    fileobject.seek(0)
                    fileobject.write(tokenstring)
                    os.kill(os.getpid(), signal.SIGINT)

            
            return "Parameters received successfully!"


        
        uri="https://localhost:5000/callback"

        url="https://accounts.spotify.com/authorize"

        header={"client_id":clientid,"response_type":"code","redirect_uri":uri,"scope":"user-modify-playback-state user-read-playback-state"}
            # print(os.environ['SPOTIFYTOKEN'])
            
        redirect_url = url + '?' + urlencode(header)
            

        app.run(port=5000,ssl_context="adhoc")
            

    typer.run(main)