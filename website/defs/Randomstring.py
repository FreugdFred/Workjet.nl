import random
import string

def get_random_string():
    letters = ''.join(
        random.choice(string.ascii_letters) for _ in range(4)
    )
    digits = ''.join(random.choice(string.digits) for _ in range(4))

    sample_list = list(letters + digits)
    random.shuffle(sample_list)
    
    return ''.join(sample_list)