# import sys
import urllib.request
# import osutils
import json


def papagotrans(text: str, src: str, tgt: str, client_id:str, client_secret:str):
    """Opens a request to papago with client_id & client_secret. Raises exception"""
    encText = urllib.parse.quote(text)
    data = f"source={src}&target={tgt}&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    try:
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()
        if(rescode == 200):
            response_body = response.read()
            res_decoded = response_body.decode('utf-8')
            # print(res_decoded)
            # print("Type:", type(res_decoded))
            res_decoded = json.loads(res_decoded)
            return res_decoded["message"]["result"]["translatedText"]
        else:
            print("Error Code:" + rescode)
            return ""
    except urllib.error.HTTPError as e:
        # print("This is e.code:", str(e.code))
        return str(e.code)
