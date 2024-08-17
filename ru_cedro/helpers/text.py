import re
from unidecode import unidecode

def preprocess_text_for_menu_unification(text):
    """
    Preprocessa um texto. As etapas de preprocessamento são:
    - Remoção de acentos
    - Remoção de espaços extras
    - Padronização da capitalização
    - Substituir "c/" por "com"
    
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
    
    # Substitui "c/" por "com"
    text = text.replace("c/", "com")
    
    return text

def tokenize_and_refine_text_for_menu_unification(text, sep=r'[+;,.()/\\:]| ou | e | ao | com ', replace_words_with = {
    "sl: ": "",
    "sob: ": "",
}):
    """
    Pre-tokeniza e refina um texto. As etapas são:
    - Repartir o texto em subtextos quando um caractere do sep é encontrado.
    - Remover espaços extras (trim).
    - Substituição de palavras por outras palavras.
    
    Args:
        text (str): Texto a ser pre-tokenizado e refinado.
        replace_words_with (dict, optional): Dicionário de substituições a serem feitas.
        
    Returns:
        list: Lista de subtextos refinados.
    """
    
    # Tokenização
    tokens = re.split(sep, text)
    tokens = [t.strip() for t in tokens if t.strip()]
    
    # Refinamento
    if replace_words_with:
        for i, token in enumerate(tokens):
            for word, replacement in replace_words_with.items():
                tokens[i] = tokens[i].replace(word, replacement)
    
    return tokens