import os
import sys
import pandas as pd

# Adiciona o diretório raiz ao path do sistema
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helpers import database
from helpers import unificar_menus

conn = database.get_mysql_connection()
cursor = conn.cursor()

menus = database.get_column_data(cursor, "menu")
menus["preprocessed_description"] = menus["description"].apply(unificar_menus.preprocess_text_for_menu_unification)
menus["tokenized_description"] = menus["preprocessed_description"].apply(unificar_menus.tokenize_menu_description)
tokens = unificar_menus.tokenized_descriptions_to_tokens_set(menus["tokenized_description"])

# Declarando token_ids como None apenas para o VSCode prestar o autocomplete
menus["token_ids"] = None

menus = unificar_menus.add_token_ids(menus, tokens)

token_ids = menus["token_ids"].explode().unique()

schedulings_by_token_id = [unificar_menus.get_schedulings_by_token_id(cursor, token_id) for token_id in token_ids]

token_id_to_scheduling_amount_map = {token_id: len(schedulings) for token_id, schedulings in zip(token_ids, schedulings_by_token_id)}

# Ordenar o token_id_to_scheduling_amount_map pelo token_id
token_id_to_scheduling_amount_map = dict(sorted(token_id_to_scheduling_amount_map.items()))

# Salvar as variáveis em arquivos JSON usando pandas
menus.to_json("menus.json", orient="records")
pd.DataFrame(tokens, columns=["token"]).to_json("tokens.json", orient="records")
pd.DataFrame(token_ids, columns=["token_id"]).to_json("token_ids.json", orient="records")

# Converter cada elemento de schedulings_by_token_id para DataFrame e concatenar
schedulings_dfs = [pd.DataFrame(schedulings) for schedulings in schedulings_by_token_id]
schedulings_df = pd.concat(schedulings_dfs, ignore_index=True)
schedulings_df.to_json("schedulings_by_token_id.json", orient="records")

pd.DataFrame(token_id_to_scheduling_amount_map.items(), columns=["token_id", "scheduling_amount"]).to_json("token_id_to_scheduling_amount_map.json", orient="records")

print("Dados salvos em arquivos JSON.")