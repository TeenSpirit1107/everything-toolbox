import time

def type_effect(text, word_wise = True, delay=-1):
    """
    Simulates typing effect for the given text.
    
    Args:
        text (str): The text to display with typing effect.
        delay (float): Delay between each character in seconds.
    """
    if delay == -1:
        delay = 0.1 if word_wise else 0.05
    
    if word_wise:
        lines = text.splitlines()
        for line in lines:
            words = line.split()
            for word in words:
                print(word, end=' ', flush=True)
                time.sleep(delay)
            print()  # Move to the next line after finishing the current line
    
    else:
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()  # Move to the next line after finishing the text

if __name__ == "__main__":
    # Example usage
    text = [
"""
April is the cruellest month, breeding
Lilacs out of the dead land, mixing
Memory and desire, stirring
Dull roots with spring rain.
""", 
"""
Winter kept us warm, covering
Earth in forgetful snow, feeding
A little life with dried tubers.
"""
    ]
    type_effect(text[0])
    type_effect(text[1], word_wise=False)
    

