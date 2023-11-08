
def tokenize(query_str):
    symbols = list('.,%$')
    for s in symbols:
        query_str = query_str.replace(s, f' {s} ')
    return query_str.lower().split()
    
def quotation_parser(query_str):
    '''

    :param query_str: The query used for the function.

    This function is responsible for taking in a query with a quotation mark, and return two list,
    a list with normal tokenize method and a list with the quoted portion counted as one token.
    This function uses four other functions which is check_character, split_quotation, join_words, and clean_token.
    :return: two list, one that is normally tokenized and one with the quotation portion tokenized as one token.
    '''
    quoted_tokens = []
    unquoted_tokens = []
    positions = []
    if check_character(query_str):
        unquoted_tokens = tokenize(query_str)
        wordList = query_str.split(" ")
        for word in wordList:
            if "\"" in word or "'" in word:
                positions.append(wordList.index(word))
            quoted_tokens.append(word)
        quoted_tokens = split_quotation(quoted_tokens,positions)
    return quoted_tokens, unquoted_tokens

def check_character(query_str):
    '''
    :param query_str: The query used for the function.

    This functions is used to check if a query string has any of the following characters in the checkList.
    :return: A true or false statement depending on if the characters have the included characters on the checkList.
    '''
    checkList = ["'", "\""]
    for character in checkList:
        if character in query_str: return True
    return False
def split_quotation(quoted_tokens,positions):
    '''

    :param quoted_tokens: A list of the semi-tokenized tokens. Best to use on list with seperated words like ["This", "is", "a", "list"]
    :param positions: The list of the index of the words with the quotation marks on the quoted_tokens.

    This functions would run until the position list is empty. It's responsible for splitting the words with quotation and joing them into one token using join_words function.
    It checks for the length of the quoted_tokens before and after using the join words function. It uses the length difference between before and after join_words function
    and adjust the rest of the position list accordingly by subtracting the difference on all list. It then deletes the first two positions elements until it's empty.
    See join_words function to see how it seperates and joins the quotation marks portion into one token.

    :return: A modified quoted_tokens list with the quotation portion marked as one token.
    '''
    while positions != []:
        prevLength = len(quoted_tokens)
        quoted_tokens = join_words(quoted_tokens, positions[0], positions[1])
        nextLength = len(quoted_tokens)
        difference = prevLength - nextLength
        del positions[0:2]
        positions = [x - difference for x in positions]
    return quoted_tokens

def join_words(quoted_tokens, begin, end):
    '''

    :param quoted_tokens: A list of the semi-tokenized tokens. Best to use on list with seperated words like ["This", "is", "a", "list"]
    :param begin: The beginning index of the word with the first quotation marks.
    :param end: The end index of the word with the last quotation marks
    :param This function is responsible for combining certain elements on a list into one token.
    :return: A modified quoted_tokens list with the quotation portion marked as one token.
    '''
    tempList = quoted_tokens[begin:end + 1]
    del quoted_tokens[begin + 1:end + 1]
    tempToken = " ".join(tempList)
    quoted_tokens[begin] = clean_Token(tempToken)
    return quoted_tokens

def clean_Token(token):
    '''

    :param token: A token of a list. It's expected to be a String.
    Cleans the token provided from quotation marks or other characters.

    :return: A modified token with certain characters removed from the token.
    '''
    token = token.replace("\"","")
    token = token.replace("'","")
    return token