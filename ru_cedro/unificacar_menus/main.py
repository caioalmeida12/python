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
menus["description"] = menus["description"].apply(text.preprocess_text_for_menu_unification)

# Atribui os tokens para cada menu
menus["tokens"] = menus["description"].apply(text.tokenize_and_refine_text_for_menu_unification)

def unify_menus(menus, eps=90):
    """
    Unifica os menus. Dois menus são considerados iguais se a similaridade entre suas descrições for maior que eps.
    
    Args:
        menus (DataFrame): DataFrame contendo os menus.
        eps (int): Limiar de similaridade entre as descrições dos menus.
        
    Returns:
        dict: Dicionário contendo os menus unificados.
    """
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

# Salvar os menus unificados no arquivo output.json
with open('output.json', 'w', encoding='utf-8') as file:
    json.dump(unify_menus(menus), file, ensure_ascii=False, default=lambda x: list(x) if isinstance(x, set) else x)
    file.close()
    
# Criar um set com todos os tokens, ordenar alfabeticamente e salvar o resultado em um arquivo
all_tokens = {token for tokens in menus["tokens"] for token in tokens}

with open('tokens.txt', 'w', encoding='utf-8') as file:
    file.write("\n".join(sorted(all_tokens)))
    file.close()