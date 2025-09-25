# Install these packages first:
# pip install googletrans==4.0.0-rc1 indic-transliteration

from googletrans import Translator
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate as hindi_transliterate
from random import shuffle
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    result = ""
    if request.method == 'POST':
        user_input = request.form['text']
        mode = request.form['mode']        # encryption or decryption
        message_id = request.form.get('msg_id', None)  # only needed for decryption; use `.get()` so it's not required for encryption
        result = useTool(user_input, mode, message_id)
    return render_template('index.html', result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

def makeMessageID (language_keys, languages):
    message_id = []
    for language in language_keys:
        message_id.append(languages[language])
    output = "".join(str(m) for m in message_id)
    return "Your message ID is: " + output

def makeLanguageKeys (languages, id):
    language_keys = []
    input_id = id
    message_id = list(input_id)
    for number in message_id:
        for key, value in languages.items():
            if value == int(number):
                language_keys.append(key)
                break
    
    return language_keys

def encryptMessage (language_keys, word_list, translator, languages):
    result = ""
    index = 0

    for word in word_list:
        language = language_keys[index]
        translated_word = translator.translate(word, src='en', dest = language_keys[index])
        translated_text = translated_word.text
        index += 1
        if (index >= len(language_keys)):
            index = 0
        if (language == 'hi'):
            translated_text = hindi_transliterate(translated_text, sanscript.DEVANAGARI, sanscript.ITRANS)
        
        result += " " + translated_text
    output = result[0].upper(), result[1:]
    makeMessageID(language_keys, languages)
    return "Here's the encrypted message:\n" + output

def decryptMessage (language_keys, word_list, translator):
    result = ""
    index = 0

    for word in word_list:
        language = language_keys[index]
        translated_word = translator.translate(word, src=language, dest='en')
        translated_text = translated_word.text
        index += 1
        if (index >= len(language_keys)):
            index = 0
        
        result += " " + translated_text

    output = result[0].upper(), result[1:].lower()
    return "Here's the decrypted message:\n" + output

def useTool(user_input, mode, message_id):
    translator = Translator()
    english_input = user_input

    languages = {
        "hi": 1,
        "et": 2,
        "fr": 3,
        "de": 4,
        "no": 5,
        "gd": 6
    }
    word_list = english_input.split()
    language_keys = list(languages.keys())
    
    if (mode.lower() == "encryption"):
        shuffle(language_keys)
        return encryptMessage(language_keys, word_list, translator, languages)

    elif (mode.lower() == "decryption"):
        language_keys = makeLanguageKeys(languages, message_id)
        return decryptMessage(language_keys, word_list, translator)

    else:
        return "Invalid mode! Please check your spellings and try again: "

# result = translator.translate(english_word, src='en', dest='hi')
# hindi_text = result.text 
# print("Hindi translation:", hindi_text)
# # Step 2: Transliterate Hindi (Devanagari) to Latin alphabet
# transliterated = hindi_transliterate(hindi_text, sanscript.DEVANAGARI, sanscript.ITRANS)
# print("Transliterated to Latin:", transliterated[0].upper()+transliterated.lower())