import re
import pandas as pd
from unidecode import unidecode
from fuzzywuzzy import fuzz

def preprocess_text_for_menu_unification(text):
    """
    Preprocessa um texto. As etapas de preprocessamento são:
    - Remover acentos
    - Padronizar a capitalização
    - Substituir as palavras contidas no dicionário de substituição
    - Excluir strings contidas na lista de exclusão
    
    :param text: descrição do menu
    :type text: str
    :return: descrição do menu preprocessada
    :rtype: str
    """

    replacement = {
        "c/": "com",
        "sl:": "salada",
        "sl ": "salada",
        "sob:": "sobremesa ",
        "sob ": "sobremesa ",
        }
    exclusion = {}

    text = unidecode(text)
    text = text.lower()
    text = " ".join([replacement[word] if word in replacement else word for word in text.split()])
    text = " ".join([word for word in text.split() if word not in exclusion])
    
    return text

def tokenize_menu_description(preprocessed_description):
    """
    Tokeniza a descrição de um menu preprocessada.
    
    :param preprocessed_description: descrição do menu preprocessada
    :type preprocessed_description: str
    :return: descrição do menu tokenizada
    :rtype: list
    """
    
    separators = r'[+;,.()/\\:]| ou | e | ao'
    

    split = re.split(separators, preprocessed_description)
    split = [word.strip() for word in split if word.strip()]

    return split

def tokenized_descriptions_to_tokens_set(tokenized_descriptions):
    """
    Converte uma lista de descrições pré-processadas e tokenizadas em um conjunto de tokens.
    
    :param tokenized_descriptions: lista de descrições de menus preprocessadas e tokenizadas
    :type tokenized_descriptions: list
    :return: conjunto de tokens
    :rtype: pd.DataFrame
    """
    unique_tokens_set = set().union(*tokenized_descriptions)
    
    tokens_list = list(unique_tokens_set)
    
    tokens_df = pd.DataFrame(tokens_list, columns=["token"]).sort_values("token").reset_index(drop=True)
    
    return tokens_df

def merge_similar_tokens(tokens_set, threshold=90):
    """
        Recebe um conjunto de tokens e retorna um conjunto de tokens semelhantes.
        Para calcular a similaridade entre dois tokens, é utilizada a biblioteca fuzzywuzzy.

        :param tokens_set: conjunto de tokens
        :type tokens_set: pd.DataFrame
        :param threshold: limite de similaridade entre dois tokens
        :type threshold: float
        :return: conjunto de tokens semelhantes
        :rtype: set
    """

    """
        Exemplo:

        tokens_set = 
                        token
        0  cuzcuz com charque
        1        suco de caja
        2  cuscuz com charque

        similaridade entre os tokens =
            'suco de caja' e 'suco de caja': ratio = 100
            'suco de caja' e 'cuscuz com charque': ratio = 47
            'suco de caja' e 'cuzcuz com charque': ratio = 40
            'cuscuz com charque' e 'cuscuz com charque': ratio = 100
            'cuscuz com charque' e 'cuzcuz com charque': ratio = 94

        merge_similar_tokens(tokens_set, threshold=90) =
            {'cuzcuz com charque', 'suco de caja'}
    """

    # Ordena os tokens alfabeticamente
    # É importante que o tokens_set esteja ordenado alfabeticamente para que a função trabalhe de maneira determinística. 
    # Caso não esteja, a função pode retornar resultados diferentes a cada execução. ex: 'cuscuz com charque' e 'cuzcuz com charque' (um com 's' e outro com 'z')
    tokens_set = tokens_set.sort_values("token").reset_index(drop=True)

    # Para cada token, calcula a similaridade com todos os outros tokens, e salva como {indice: similaridade}
    tokens_set["similar_tokens"] = tokens_set["token"].apply(
        lambda token: {idx: fuzz.ratio(token, other_token) for idx, other_token in enumerate(tokens_set["token"])}
    )

    def recursive_merge(tokens_set):
        """
            Função recursiva que remove tokens semelhantes do conjunto de tokens. 
        """
        
        tokens_set["similar_tokens"] = tokens_set["token"].apply(
            lambda token: {idx: fuzz.ratio(token, other_token) for idx, other_token in enumerate(tokens_set["token"])}
        )
        
        # Para cada token, verifica se há algum outro token com similaridade maior que o threshold e menor que 100
        for idx, row in tokens_set.iterrows():
            for other_idx, similarity in row["similar_tokens"].items():
                if similarity > threshold and similarity < 100:
                    tokens_set = tokens_set.drop(other_idx)
                    return recursive_merge(tokens_set)
        
        return tokens_set
    
    tokens_set = recursive_merge(tokens_set)

    return set(tokens_set["token"])

def add_token_ids(menus, tokens):
    """
    Adiciona os ids dos tokens de um menu ao DataFrame de menus.
    
    :param menus: DataFrame de menus
    :type menus: pd.DataFrame
    :param tokens: dicionário com os tokens
    :type tokens: dict
    :return: DataFrame de menus com os ids dos tokens
    :rtype: pd.DataFrame
    """
    
    # For every menu, run through its tokenized description and do: if token is in tokens["all_enumerated"], add the token_id to the ["token_ids"] list
    menus["token_ids"] = menus["tokenized_description"].apply(lambda x: [tokens["all_enumerated"].loc[tokens["all_enumerated"]["token"] == token].index[0] for token in x if token in tokens["all"]["token"].values])
    
    return menus
