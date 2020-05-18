import csv
import requests
from bs4 import BeautifulSoup
from collections import namedtuple

# Still left to extract:
# 1. Evolutions
# 2. Sprites
# 3. Location Found
# 4. Stats??
# 5. All Pokedex Descriptions
PokemonData = namedtuple('PokemonDetails', [
  'pokedex_entry',
  'pokemon_name',
  'pokemon_types',
  'species',
  'height',
  'weight',
  'abilities',
  'ev_yield',
  'catch_rate',
  'friendship',
  'base_exp',
  'growth_rate',
  'egg_groups',
  'genders',
  'egg_cycles',
  'super_effective_on_subject',
  'not_effective_on_subject',
  'no_effect_on_subject',
  'description',
  'level_up_moves',
  # 'egg_moves',
  # 'tutor_moves',
  # 'tm_moves',
])

def format_type_matches(types_dict, case):
  super_effective_on_subject = []
  not_effective_on_subject = []
  no_effect_on_subject = []
  for key, value in types_dict.items():
    if value == '2' or value == '4' or value == '8':
      super_effective_on_subject.append(key)
    elif value == '½':
      not_effective_on_subject.append(key)
    elif value == '0':
      no_effect_on_subject.append(key)

  if case == 'SUPER_EFFECTIVE_ON_SUBJECT':
    return super_effective_on_subject
  if case == 'NOT_EFFECTIVE_ON_SUBJECT':
    return not_effective_on_subject
  if case == 'NO_EFFECT_ON_SUBJECT':
    return no_effect_on_subject

def scrape_pokemon(pokemon_name):
  print(pokemon_name)
  html_body = requests.get(
    f'https://pokemondb.net/pokedex/{pokemon_name}'
  ).text
  soup = BeautifulSoup(html_body, 'html.parser')
  vitals_table = soup.find("table", {'class':'vitals-table'}).find('tbody') \
    .findAll('td')
  ## Properties Chunk 1
  pokemon_name = soup.find("h1").text
  pokedex_entry = vitals_table[0].text
  unique_types = [a.text for a in vitals_table[1].findAll('a')]
  species = vitals_table[2].text
  height = vitals_table[3].text
  weight = vitals_table[4].text
  abilities = [a.text for a in vitals_table[5].findAll('a')]

  second_vitals_table = soup.findAll('table', {'class':'vitals-table'})[1].find('tbody') \
    .findAll('td')
  # Properties Chunk 2
  ev_yield = second_vitals_table[0].text
  catch_rate = second_vitals_table[1].text
  friendship = second_vitals_table[2].text
  base_exp = second_vitals_table[3].text
  growth_rate = second_vitals_table[4].text

  third_vitals_table = soup.findAll('table', {'class':'vitals-table'})[2].find('tbody') \
    .findAll('td')
  # Properties Chunk 3
  egg_groups = [a.text for a in third_vitals_table[0].findAll('a')]
  genders = [s.text for s in third_vitals_table[1].findAll('span')]
  egg_cycles = third_vitals_table[2].text

  types_table = soup.findAll('table', {'class':'type-table type-table-pokedex'})
  # Properties Chunk 4
  pokemon_types = {}
  for table in types_table:
    inner_dict = {}
    type_headings = table.findAll('th')
    type_data = table.findAll('td')
    for i in range(len(type_headings)):
      inner_dict[type_headings[i].find('a')['title']] = type_data[i].text
    pokemon_types.update(inner_dict)
  
  super_effective_on_subject = format_type_matches(pokemon_types, 'SUPER_EFFECTIVE_ON_SUBJECT')
  not_effective_on_subject = format_type_matches(pokemon_types, 'NOT_EFFECTIVE_ON_SUBJECT')
  no_effect_on_subject = format_type_matches(pokemon_types, 'NO_EFFECT_ON_SUBJECT')

  # Properties Chunk 5
  description = soup.findAll('table', {'class':'vitals-table'})[4].find('tbody') \
    .findAll('td')[-1].text
  
  # Properties Chunk 6
  level_up_moves = []
  level_up_move_rows = soup.find('table', {'class': 'data-table'}).find('tbody') \
    .findAll('tr')
  
  for row in level_up_move_rows:
    level_up_moves.append((
      row.findAll('td')[0].text,
      row.findAll('td')[1].find('a').text
    ))
  
  # max_index_offset = 0
  # egg_moves = []
  # egg_moves_data = soup.findAll('table', {'class': 'data-table'})[1].find('tbody') \
  #   .findAll('tr')
  # for row in egg_moves_data:
  #   if not row.find('td').find('a'):
  #     max_index_offset += 1
  #     break
  #   egg_moves.append(row.find('td').find('a').text)
  # print(egg_moves)

  # tm_moves = []
  # tm_moves_data = soup.findAll('table', {'class': 'data-table'})[2-max_index_offset].find('tbody') \
  #   .findAll('tr')
  # for row in tm_moves_data:
  #   if not row.find('td').find('a'):
  #     break
  #   tm_moves.append(row.findAll('td')[1].find('a').text)
  # print(tm_moves)

  # tutor_moves = []
  # tutor_moves_data = soup.findAll('table', {'class': 'data-table'})[3-max_index_offset].find('tbody') \
  #   .findAll('tr')
  # for row in tutor_moves_data:
  #   if not row.find('td').find('a'):
  #     max_index_offset += 1
  #     break
  #   tutor_moves.append(row.find('td').find('a').text)
  # print(tutor_moves)
  
  return PokemonData(
    pokedex_entry=pokedex_entry,
    pokemon_name=pokemon_name,
    pokemon_types=unique_types,
    species=species,
    height=height,
    weight=weight,
    abilities=abilities,
    ev_yield=ev_yield,
    catch_rate=catch_rate,
    friendship=friendship,
    base_exp=base_exp,
    growth_rate=growth_rate,
    egg_groups=egg_groups,
    genders=genders,
    egg_cycles=egg_cycles,
    super_effective_on_subject=super_effective_on_subject,
    not_effective_on_subject=not_effective_on_subject,
    no_effect_on_subject=no_effect_on_subject,
    description=description,
    level_up_moves=level_up_moves,
    # egg_moves=egg_moves,
    # tutor_moves=tutor_moves,
    # tm_moves=tm_moves
  )

def write_to_local_csv(pokemon_data):
  with open('individual_pokemon_entry.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([
      'pokedex_entry',
      'pokemon_name',
      'pokemon_types',
      'species',
      'height',
      'weight',
      'abilities',
      'ev_yield',
      'catch_rate',
      'friendship',
      'base_exp',
      'growth_rate',
      'egg_groups',
      'genders',
      'egg_cycles',
      'super_effective_on_subject',
      'not_effective_on_subject',
      'no_effect_on_subject',
      'description',
      'level_up_moves',
      # 'egg_moves',
      # 'tutor_moves',
      # 'tm_moves'
    ])
    for data in pokemon_data:
      writer.writerow([
        data.pokedex_entry,
        data.pokemon_name,
        data.pokemon_types,
        data.species,
        data.height,
        data.weight,
        data.abilities,
        data.ev_yield,
        data.catch_rate,
        data.friendship,
        data.base_exp,
        data.growth_rate,
        data.egg_groups,
        data.genders,
        data.egg_cycles,
        data.super_effective_on_subject,
        data.not_effective_on_subject,
        data.no_effect_on_subject,
        data.description,
        data.level_up_moves,
        # data.egg_moves,
        # data.tutor_moves,
        # data.tm_moves,
      ])

pokemon_names = ['meganium']
formatted_pokemon_data = []
with open('pokemon_data.csv', newline='') as csvfile:
  data_reader = csv.reader(csvfile)
  next(data_reader, None) # Skip header file
  for row in data_reader:
    if row[2] not in pokemon_names:
      pokemon_names.append(row[2])
  
for pokemon in pokemon_names:
  try:
    pokemon_data = scrape_pokemon(pokemon)
    formatted_pokemon_data.append(pokemon_data)
  except:
    print(f'Errored when scraping {pokemon}')

write_to_local_csv(formatted_pokemon_data)