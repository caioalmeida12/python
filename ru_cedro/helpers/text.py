import re
from unidecode import unidecode

def preprocess_text(text):
    """
    Preprocessa um texto. As etapas de preprocessamento são:
    - Remoção de acentos
    - Remoção de espaços extras
    - Padronização da capitalização
    
    Args:
        text (str): Texto a ser preprocessado.
        
    Returns:
        str: Texto preprocessado.
    """
    
    
    # Remove acentos
    text = unidecode(text)
    # Remove espaços extras
    text = re.sub(r'\s+', ' ', text).strip()
    # Padroniza a capitalização
    text = text.lower()
    return text

def tokenize_text(text, sep='[+;]| ou | e | ao | com |\.|,|\(|\)|\/|:'):
    """
    Pre-tokeniza um texto. As etapas de pre-tokenização são:
    - Repartir o texto em subtextos quando um caractere do sep é encontrado.
    - Remover espaços extras (trim).
    
    Args:
        text (str): Texto a ser pre-tokenizado.
        
    Returns:
        list: Lista de subtextos.
    """
    
    text = re.split(sep, text)
    text = [t.strip() for t in text if t.strip()]
    return text
        
def refine_tokens(tokens, replace_words_with = {
    "sl: ": "",
    "sob: ": "",
    "c/": "com",
}):
    """
    Refina os tokens de um texto. As etapas de refinamento são:
    - Substituição de palavras por outras palavras.
    
    Args:
        tokens (list): Lista de tokens a serem refinados.
        replace_words_with (dict): Dicionário de substituições a serem feitas.
        
    Returns:
        list: Lista de tokens refinados.
    """
    
    for i, token in enumerate(tokens):
        for word, replacement in replace_words_with.items():
            tokens[i] = tokens[i].replace(word, replacement)
    
    return tokens
    
    
def bag_distance(str1, str2): 
    """
    Calcula a distância entre duas strings. A distância é calculada como a diferença entre os bags of words das strings.
    
    Args:
        str1 (str): Primeira string.
        str2 (str): Segunda string.
        
    Returns:
        int: Distância entre os bags of words das strings.
    """
    
    str1 = set(str1.split())
    str2 = set(str2.split())
    
    return len(str1.symmetric_difference(str2))

    
