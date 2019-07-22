# from sets import Set
from sklearn.feature_extraction import text

extra_words = ['name', 'not', 'the', 'usr', 'you', 'version', 'this']
stop_words = text.ENGLISH_STOP_WORDS.union(extra_words)

def __check_stop_word(word):
    """
    stop word のチェック
    2文字以下の文字列を除去と、英語のstopwords を除去を行う
    """
    if word in stop_words:
        return False
    if len(word) <= 2:
        return False
    return True


def split_keyword(text):
    """
    キーワードを区切り、stopwordsを除外する
    """
    keywords = text.split(" ")
    return [keyword for keyword in keywords if __check_stop_word(keyword)]
