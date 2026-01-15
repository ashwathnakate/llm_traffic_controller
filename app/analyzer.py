

import string

def analyze(user_query: str)-> dict:
    # defining variables
    is_sensitive:bool = False # todo reserved for future safety routing (PII / medical / legal)
    length_value:int = 0 # # number of words in the query(sentence)
    length_level:str = None # hwo big is the query 
    reasoning_score:int = 0 # how much thinking is required
    ambiguity_score:int = 0 # how unclear it is
    simplicity_score:int = 0 # user intent to keep it simple
    complexity_score:int = 0 # define initial complexity score
    reasoning_level:str = None # corresponding levels
    ambiguity_level:str = None # corresponding levels
    complexity_level:str = None # corresponding levels
    simplicity_level:str = None # corresponding levels
    
    # sensitivity list
    # NOTE: trigger matching is token-based, not phrase-based.
    # Multi-word intents like "step by step" are not detected yet.
    
    reasoning_triggers = [
        'why', 'compare', 'analyze', 'evaluate',
        'pros', 'cons', 'how', 'critique', 'synthesize'
    ]

    ambiguity_triggers = [
        'maybe', 'something', 'sort', 'kind',
        'whatever', 'basically', 'general', 'etc'
    ]

    low_effort_intents = [
        'summarize', 'list', 'rewrite', 'explain',
        'briefly', 'define', 'extract', 'format', 'draft'
    ]    
    
    # if query contains 12 words then word is complex
    # {1 2 3 4 5 -> simple} {6 7 8 9 10 11 -> medium} {12...n -> complex}
    
    # remove the punctuation marks and split words
    query = user_query.lower()
    query = query.translate(str.maketrans('', '', string.punctuation))
    tokens = query.split()

    length_value = len(tokens)
    
# <------------------------------------------------->
    # loop for determining length_level
    if length_value <= 5:
        length_level = 'low'
        length_score = 0
    elif length_value <= 11:
        length_level = 'medium'
        length_score = 1
    else:
        length_level = 'high'
        length_score = 2
        
        
# <------------------------------------------------->
    # loop for determining reasoning_score
    reasoning_score = sum(1 for t in tokens if t in reasoning_triggers)

    if reasoning_score == 0:
        reasoning_level = 'low'
        reasoning_norm = 0
    elif reasoning_score <= 2:
        reasoning_level = 'medium'
        reasoning_norm = 1
    else:
        reasoning_level = 'high'
        reasoning_norm = 2

# <------------------------------------------------->
    # loop for determining ambiguity_score
    ambiguity_score = sum(1 for t in tokens if t in ambiguity_triggers)

    if ambiguity_score == 0:
        ambiguity_level = 'low'
        ambiguity_norm = 0
    elif ambiguity_score <= 2:
        ambiguity_level = 'medium'
        ambiguity_norm = 1
    else:
        ambiguity_level = 'high'
        ambiguity_norm = 2

# <------------------------------------------------->            
    # loop for determining simplicity_score
    simplicity_score = sum(1 for t in tokens if t in low_effort_intents)

    if simplicity_score == 0:
        simplicity_level = 'low'
        simplicity_norm = 0
    elif simplicity_score <= 2:
        simplicity_level = 'medium'
        simplicity_norm = 1
    else:
        simplicity_level = 'high'
        simplicity_norm = 2
            
# <------------------------------------------------->
    complexity_score = (
        length_score * 0.25 +
        reasoning_norm * 0.4 +
        ambiguity_norm * 0.15 -
        simplicity_norm * 0.3
    )

    if complexity_score < 0.75:
        complexity_level = 'low'
    elif complexity_score < 1.5:
        complexity_level = 'medium'
    else:
        complexity_level = 'high'
        
    
# <------------------------------------------------->
    return {
        "length": length_level,
        "reasoning": reasoning_level,
        "ambiguity": ambiguity_level,
        "simplicity": simplicity_level,
        "complexity": complexity_level,
        "sensitivity_flag": is_sensitive,

        # debug values (important for tuning)
        "value_length": length_value,
        "score_reasoning_raw": reasoning_score,
        "score_ambiguity_raw": ambiguity_score,
        "score_simplicity_raw": simplicity_score,
        "score_complexity": round(complexity_score, 2)
    }