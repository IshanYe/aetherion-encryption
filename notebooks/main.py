# Install these packages first:
# pip install googletrans==4.0.0-rc1 indic-transliteration

from googletrans import Translator
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate as hindi_transliterate
from random import shuffle

translator = Translator()
english_input = input("Enter your input english text:\n")
mode = input("Encryption or decryption?: ")

languages = {
    "hi": 1,
    "et": 2,
    "fr": 3,
    "de": 4,
    "no": 5,
    "gd": 6
}
word_list = english_input.split()
word_count = len(word_list)
language_keys = list(languages.keys())

def makeMessageID ():
    message_id = []
    for language in language_keys:
        message_id.append(languages[language])
    print ("Your message ID is: ", *message_id, sep="")

def makeLanguageKeys ():
    language_keys = []
    input_id = str(input("Please provide a message ID: "))
    print("\n")
    message_id = list(input_id)
    for number in message_id:
        for key, value in languages.items():
            if value == int(number):
                language_keys.append(key)
                break
    
    return language_keys

def encryptMessage ():
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

    print("Here's the encrypted message:\n", result[0].upper(), result[1:])
    makeMessageID()

def decryptMessage (language_keys):
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

    print("Here's the decrypted message:\n", result[0].upper(), result[1:].lower())
    makeMessageID()
    

if (mode.lower() == "encryption"):
    shuffle(language_keys)
    encryptMessage()

elif (mode.lower() == "decryption"):
    language_keys = makeLanguageKeys()
    decryptMessage(language_keys)

else:
    print ("Invalid mode! Please check your spellings and try again: ")

# result = translator.translate(english_word, src='en', dest='hi')
# hindi_text = result.text 
# print("Hindi translation:", hindi_text)
# # Step 2: Transliterate Hindi (Devanagari) to Latin alphabet
# transliterated = hindi_transliterate(hindi_text, sanscript.DEVANAGARI, sanscript.ITRANS)
# print("Transliterated to Latin:", transliterated[0].upper()+transliterated.lower())