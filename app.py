from typing import Optional
import requests,json
import typer






def Play(apikey:str)->None:
    playurl="https://api.spotify.com/v1/me/player/play"
    header={"Authorization": f"Bearer {apikey}","Content-Type": "application/json"}
    
    response=requests.put(playurl,headers=header)
    print(response.text)

def main(play:bool=False,pause:bool=False,curr:bool=False,name:bool=False):
    # print("hi",play,pause,curr,name)

    clientid=input("Enter your client ID: ")
    clientkey=input("Enter your key: ")

    url="https://accounts.spotify.com/api/token"
    header={"Content-Type":"application/x-www-form-urlencoded"}

    bodytext="grant_type=client_credentials&client_id="+clientid+"&client_secret="+clientkey

    response=requests.post(url,headers=header,data=bodytext)
    # print(response.text)
    response=json.loads(response.text)
    apikey=response["access_token"]
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
   
    typer.run(main)