import csv
import requests
from bs4 import BeautifulSoup
from collections import namedtuple

PokemonData = namedtuple('PokemonData', [
  'entry',
  'sprite',
  'name',
  'version',
  'types',
  'total_stats',
  'hp',
  'attack',
  'defense',
  'sp_attack',
  'sp_defense',
  'speed'
])

def handle_pokemon_data(pokemon_data):
  all_columns = pokemon_data.find_all('td')

  first_column_spans = all_columns[0].find_all('span')
  pokedex_entry = first_column_spans[2].text
  sprite = first_column_spans[1]['data-src']

  second_column = all_columns[1]
  name = second_column.find('a').text
  version = second_column.find('small').text if second_column.find('small') else ''

  pokemon_types = []
  third_column = all_columns[2]
  for pokemon_type in third_column.find_all('a'):
    pokemon_types.append(pokemon_type.text)

  return PokemonData(
    entry=pokedex_entry,
    sprite=sprite,
    name=name,
    version=version,
    types=pokemon_types,
    total_stats=int(all_columns[3].text),
    hp=int(all_columns[4].text),
    attack=int(all_columns[5].text),
    defense=int(all_columns[6].text),
    sp_attack=int(all_columns[7].text),
    sp_defense=int(all_columns[8].text),
    speed=int(all_columns[9].text)
  )

def write_to_local_csv(pokemon_data):
  with open('pokemon_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([
      'entry',
      'sprite',
      'name',
      'version',
      'types',
      'total_stats',
      'hp',
      'attack',
      'defense',
      'sp_attack',
      'sp_defense',
      'speed'
    ])
    for data in pokemon_data:
      writer.writerow([
        data.entry,
        data.sprite,
        data.name,
        data.version,
        data.types,
        data.total_stats,
        data.hp,
        data.attack,
        data.defense,
        data.sp_attack,
        data.sp_defense,
        data.speed
      ])
  

all_pokemon_data = []
html_body = requests.get(
  'https://pokemondb.net/pokedex/all',
  allow_redirects=True
).text
soup = BeautifulSoup(html_body, 'html.parser')

pokedex_section = soup.find('tbody')
all_pokemons = pokedex_section.find_all('tr')
for pokemon_data in all_pokemons:
  formatted_pokemon_data = handle_pokemon_data(pokemon_data)
  all_pokemon_data.append(formatted_pokemon_data)

write_to_local_csv(all_pokemon_data)
