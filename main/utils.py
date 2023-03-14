def calculate_time_to_read(text):
    speed_word_per_minute = 183
    total_words = text.split()

    total_time_in_min = (int)(len(total_words)/speed_word_per_minute)
    return str(total_time_in_min)

