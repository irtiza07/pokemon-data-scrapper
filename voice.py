from difflib import get_close_matches
import speech_recognition as sr
import csv

all_pokemon_names = []
# pokemon_dict = {}
with open('pokemon_data.csv', newline='') as csvfile:
  data_reader = csv.reader(csvfile)
  for row in data_reader:
    # pokemon_dict[row[2]] = row[3:]
    all_pokemon_names.append(row[2])
  
# print(pokemon_dict)

r = sr.Recognizer()
with sr.Microphone() as source:
  print("What pokemon do you want?")
  audio = r.listen(source)
  pokemon_chosen = r.recognize_google(audio) # "Tell me about Pikachu" "What are Pik stats?"
 
print("Starting to find the match...")
match = get_close_matches(pokemon_chosen, all_pokemon_names)
print(match[0])

# print(pokemon_dict[match[0]])
# print(match[0]) #Most likely match