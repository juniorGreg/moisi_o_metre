

def word_count(text):
    text = text.replace("?", "").replace("!", "")
    words = text.split()
    return len(words)

def average_reading_time(word_count, words_per_minute=184.0):
    art = round(float(word_count)/words_per_minute)    
    return int(art)
