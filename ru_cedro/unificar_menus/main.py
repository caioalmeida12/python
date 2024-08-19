import os
import sys
import pandas as pd

# Adiciona o diretório raiz ao path do sistema
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helpers import database
from helpers import unificar_menus

conn = database.get_mysql_connection()
cursor = conn.cursor()

menus = database.get_column_data(cursor, "menu").head(2)
menus["preprocessed_description"] = menus["description"].apply(unificar_menus.preprocess_text_for_menu_unification)
menus["tokenized_description"] = menus["preprocessed_description"].apply(unificar_menus.tokenize_menu_description)
tokens = {
    "all": unificar_menus.tokenized_descriptions_to_tokens_set(menus["tokenized_description"]), 
}
tokens["all_enumerated"] = tokens["all"].reset_index().rename(columns={"index": "token_id"})