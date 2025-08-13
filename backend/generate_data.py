import random
import string

def text_to_dots(text):
    """Converts a string to its dot representation."""
    dots = ""
    for char in text:
        if char == ' ':
            dots += ' '
        else:
            dots += '.'
    return dots

def generate_random_text(min_length=5, max_length=50, include_special=True):
    """Generates a random text string with letters, numbers, and optional special characters."""
    characters = string.ascii_letters + string.digits
    if include_special:
        characters += string.punctuation + ' '
    length = random.randint(min_length, max_length)
    return ''.join(random.choice(characters) for _ in range(length))

if __name__ == "__main__":
    num_samples = 500  # You can adjust the number of samples to generate

    with open("dot_dataset.txt", "w", encoding="utf-8") as f:
        for _ in range(num_samples):
            random_text = generate_random_text()
            dot_representation = text_to_dots(random_text)
            f.write(random_text + "\n")
            f.write(dot_representation + "\n")

    print("Generated dataset saved to dot_dataset.txt")