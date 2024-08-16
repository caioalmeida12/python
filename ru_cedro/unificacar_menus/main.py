import matplotlib.pyplot as plt
import pandas as pd
import sys
sys.path.append('../')
from fuzzywuzzy import fuzz
import json

# Módulos locais
import helpers.database as db
import helpers.text as text

conn = db.get_mysql_connection()

datasets = db.read_mysql_dataset(conn, ["menu"])
menus = pd.DataFrame(datasets["menu"])

# Preprocessa os textos
menus["description"] = menus["description"].apply(text.preprocess_text)
menus["tokens"] = menus["description"].apply(text.tokenize_text)

def unify_menus(menus, eps=90):
    menus_unificados = {}
    processed_descriptions = set()
    
    for _, menu in menus.iterrows():
        description = menu["description"]
        
        if description in processed_descriptions:
            continue
        
        for key in menus_unificados.keys():
            if fuzz.ratio(key, description) > eps:
                menus_unificados[key]["id"].append(menu["id"])
                menus_unificados[key]["meal_id"].add(menu["meal_id"])
                break
        else:
            menus_unificados[description] = {
                "description": description,
                "meal_id": {menu["meal_id"]},
                "id": [menu["id"]],
                "tokens": menu["tokens"]
            }
            processed_descriptions.add(description)
    
    return menus_unificados

# Unifica os menus
menus_unificados = unify_menus(menus)

# Função para converter np.int64 para int
def convert_np_int64_to_int(np_int_list):
    return [int(x) for x in np_int_list]

menus["tokens"] = menus["tokens"].apply(text.refine_tokens)

# Salvar os menus unificados no arquivo output.json
with open('output.json', 'w', encoding='utf-8') as file:
    json.dump(menus_unificados, file, ensure_ascii=False, default=convert_np_int64_to_int)
    file.close()
    
# Criar um set com todos os tokens, ordenar alfabeticamente e salvar o resultado em um arquivo
all_tokens = {token for tokens in menus["tokens"] for token in tokens}

with open('tokens.txt', 'w', encoding='utf-8') as file:
    file.write("\n".join(sorted(all_tokens)))
    file.close()