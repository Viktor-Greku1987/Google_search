import webbrowser

import requests
from bs4 import BeautifulSoup
import pyttsx3
import speech_recognition

recognizer = speech_recognition.Recognizer()
microfon = speech_recognition.Microphone()

def init_engine():
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    #for voice in voices:
        #print(voice)
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('volume', 0.5)
    volume = engine.getProperty('volume')
    #print('горомкость: ',volume)
    engine.setProperty('rate', 185)
    rate = engine.getProperty('rate')
    #print(rate)
    return engine



def recognizer_search():
    audio = ''
    with microfon:
        data = ''
        recognizer.adjust_for_ambient_noise(microfon, duration=2)
        try:
            t = 'Уважаемый пользователь, скажите команду, начиная со слово: онлайн'
            print(t)
            engine = init_engine()
            sound(engine, t)
            audio = recognizer.listen(microfon, 2,2)
        except Exception as ex:
            print('ошибка', ex)
            return ''
        data = recognizer.recognize_google(audio, language='ru')
        return data.lower()

def sound(engine, text):
    engine.say(text)
    engine.runAndWait()

def google_search(text=str):
    text = text.split()

    if text[0] != 'онлайн':
        return ''

    text = ' '.join(text[1:len(text)])
    text = text.replace(' ', '+')
    url = f'http://www.google.ru/search?q={text}'
    #print(url)
    USER_AENT = "Mozilla/5.0 (Macintosh; Intell SO X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    headers  = {'user-agent': USER_AENT}
    page = requests.get(url, headers=headers)
    result = BeautifulSoup(page.content, 'html.parser')
    result_url = []
    for g in result.find_all('div', class_='g'):
        anchors = g.find_all('a')
        #print(anchors)

        if anchors:
            link = anchors[0]['href']
            title = g.find('h3').text
            item = {'link': link, 'title': title}
            result_url.append(item)
            #print(result_url)
    t = 'Ознакомьтесь с результатами запроса:'
    engine = init_engine()
    sound(engine,t)
    print(t)
    for data_resul in result_url:
        print(data_resul.get('link'))
        print(data_resul.get('title'))
    answer = "Всего найдено "+ ' ' + str(len(result_url))+ ' ' + ' ссылок'
    print(answer)
    engine = init_engine()
    sound(engine, answer)
    t_1 = 'Открою для Вас первую ссылку'
    engine = init_engine()
    sound(engine, t_1)
    url_open = result_url[0].get('link')
    webbrowser.open(url_open)
    engine =init_engine()
    sound(engine, 'результаты запроса сохраним для вас в фа́йл: гугл')
    n=0
    p = ''
    for data_resul in result_url:
        n += 1
        p += str(n) + ') ' + data_resul.get('title') + '\n'+ data_resul.get('link') + '\n'

    with open('Запросы/googl.txt',  'w') as file:
        file.write(p)
        '''
        for data_resul in result_url:
            n+=1
            file.write(str(n))
            file.write(') ')
            a = data_resul.get('title')
            file.write(str(a))
            file.write('\n')
            b = data_resul.get('link')
            file.write(str(b))
            file.write('\n')
        '''
    


while True:
    text = recognizer_search()
    google_search(text)


#google_search('онлайн отдых в крыму')
#google_search('онлайн купить дом в Лобне микрорайн Луговая')
