import papago
import json
from googletrans import Translator as GoogleTranslator
from kakaotrans import Translator as KakaoTranslator

class Translator:
    def __init__(self) -> None:
        self.ktranslator = KakaoTranslator()
        self.gtranslator = GoogleTranslator()
        
        self.update_apimodel()
        pass

    def use_kakao(self, text:str, src:str, dst:str):
        "Error safe."
        self.update_apimodel()
        try:
            translated_text = self.ktranslator.translate(text, src=src, tgt=dst)
        except Exception as e:
            translated_text = ""
        return translated_text
    
    def use_papago(self, text:str, src:str, dst:str):
        "Error safe."
        self.update_apimodel()
        client_id = self.apimodel_dict["Papago"]["Client ID:"]
        secret = self.apimodel_dict["Papago"]["Client secret:"]
        return papago.papagotrans(text, src, dst, client_id, secret)
    
    def use_google(self, text:str, src:str, dst:str):
        "Error safe now"
        self.update_apimodel()
        try:
            obj = self.gtranslator.translate(text=text, src=src, dest=dst)
            return obj.text
        except Exception as e:
            return ""
    
    def update_apimodel(self,):
        with open("apimodel.json") as f:
            self.apimodel_dict = json.load(f)
    