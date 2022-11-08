import requests
import base64
import pandas as pd
import os
from gtts import gTTS

# arabic reshaper
import streamlit as st
class ArabicTextToSpeech:
    def __init__(self,path_to_file="output.mp3",voice = "ar-SA-HamedNeural"):
        self.headers = {
                        'Accept': 'application/json, text/plain, */*',
                        'Accept-Language': 'en-US,en;q=0.9',
                        'Connection': 'keep-alive',
                        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundarylFBGlar3gYiDFBAO',
                        'Origin': 'https://micmonster.com',
                        'Referer': 'https://micmonster.com/',
                        'Sec-Fetch-Dest': 'empty',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Site': 'same-site',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
                        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                    }
        self.path  = path_to_file
        self.voice = voice
        
        
    def text2sp(self,text): 
        vcname = self.voice
        data = f'------WebKitFormBoundarylFBGlar3gYiDFBAO\r\nContent-Disposition: form-data; name="locale"\r\n\r\nar-AE\r\n------WebKitFormBoundarylFBGlar3gYiDFBAO\r\nContent-Disposition: form-data; name="content"\r\n\r\n<voice name="{vcname}">{text}</voice>\r\n------WebKitFormBoundarylFBGlar3gYiDFBAO\r\nContent-Disposition: form-data; name="ip"\r\n\r\n51.222.253.2\r\n------WebKitFormBoundarylFBGlar3gYiDFBAO--\r\n'
        self.data= data.encode()
        self.response = requests.post('https://app.micmonster.com/restapi/create', headers=self.headers, data=self.data)
    def convert_base64_to_mp3(self,base64_string):
        try:
            with open(self.path, "wb") as fh:
                fh.write(base64.b64decode(base64_string))
            print("Done")
            return True
        except:
            print("Error in converting base64 to mp3")
            return False
            
    
    def speak(self,text):
        self.text2sp(text)
        self.convert_base64_to_mp3(self.response.text)
        
        
def get_ibn_arabi(n_page):
    df = pd.read_csv('./book/ibn_arabi.csv')
    # rename columns
    df.columns = ['page_content']
    row = df.page_content[n_page]
    print(row)
    #to string
    return row
        
def main():
    st.title("Arabic Text To Speech")
    st.subheader("Created by: @ayoub_abraich")
    
    text_d  = "ولد محيي الدين بن عربي في مدينة مرسية من أب عربي طائي وأم عربية خولانية ويعرف عند الصوفيين بالشيخ الأكبر والكبريت الأحمر. وهو واحد من كبار المتصوفة والفلاسفة المسلمين على مر العصور. كان أبوه علي بن محمد من أئمة الفقه والحديث، ومن أعلام الزهد والتقوى والتصوف. وكان جده أحد قضاة الأندلس وعلمائها، فنشأ ضمن جو ديني. انتقل والده إلى إشبيلية وكان يحكمها أنذاك السلطان محمد بن سعد، وكانت عاصمة من عواصم الحضارة والعلم في الأندلس. وما كاد لسانه يبين حتى دفع به والده إلى أبي بكر بن خلف عميد الفقهاء، فقرأ عليه القرآن الكريم بالقراءات السبع، فما أتم العاشرة من عمره حتى كان ملماً بالقراءات والمعاني والإشارات. ثم سلمه والده إلى طائفة من رجال الحديث والفقه تنتقل بين البلاد واستقر أخيراً في دمشق طوال حياته وكان واحداً من أعلامها حتى وفاته عام 1240 م"
    voice = st.selectbox("Select Voice", ["ar-SY-AmanyNeural", "ar-YE-SalehNeural","ar-MA-MounaNeural","ar-MA-JamalNeural","ar-SA-HamedNeural"])
    chose_input_text_or_file = st.radio("Select Input", ["Text", "File"])
    if chose_input_text_or_file == "Text":
        text = st.text_area("Text", text_d)
        page = None
    else:
        page = st.slider("Select Page", 1, 1000, 1)
        text = get_ibn_arabi(page)
        
    if st.button("Speak"):
        #before run : verify if already the file exist
        if os.path.exists(f'./book/output_{voice}_{page}.mp3'):
            #then play it
            st.write("Already Exist : Playing...")
            st.audio(f'./book/output_{voice}_{page}.mp3')
            
        else:
            tts = ArabicTextToSpeech(f'./book/output_{voice}_{page}.mp3',voice)
            tts.speak(text)
            st.write("Done : Playing...")
            st.audio(f'./book/output_{voice}_{page}.mp3')
    if st.button("Speak with gTTs "):
        st.write("Done : Playing...")
        # more speed, accuracy, and quality
        tts = gTTS(text, lang='ar', slow=False, lang_check=False, tld='com')
        tts.save(f'./book/output_gTTS_{page}.mp3')
        st.audio(f'./book/output_gTTS_{page}.mp3')
        

if __name__ == "__main__":
    main()
        

        
        
            