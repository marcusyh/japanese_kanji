import os
from kanji.file_reader import readfile

def deal_joyokanji(source, appendix):
    # Initialize an empty dictionary to store the kanji characters and their readings
    kanji_set = {}
    previous = '*'  # Initialize the previous character as '*'
    
    ji = []  # List to store kanji characters
    ji_flag = True  # Flag to indicate if we are processing kanji characters
    yomi = {}  # Dictionary to store readings for the kanji characters

    # Append a '*' to the source to mark the end of the data
    source.append('*')
    
    for current in source:
        # Skip empty strings and consecutive '*' characters
        if current == '' or (current == '*' and previous == '*'):
            continue

        # If the current string is '*', it indicates the end of a kanji block
        if current == '*':
            previous = current  # Update the previous character
            kanji_set['/'.join(ji)] = yomi  # Add the kanji and readings to the dictionary
            ji = []  # Reset the kanji list
            ji_flag = True  # Reset the flag
            yomi = {}  # Reset the readings dictionary
            continue

        # Check if the current string is a single kanji character. set ji_flag to false if it's not a single kanji chacter
        # append to ji dictionary if it's a single kanji character
        ji_flag = len(current) == 1 and ji_flag
        if ji_flag:
            ji.append(current + appendix)
            previous = current
            continue

        # Split the current string by tabs and strip whitespace from each item
        items = [x.strip() for x in current.split('\t')]
        
        # Handle different cases based on the number of items
        if len(items) > 3:
            print(items)  # Print items if there are more than 3
        elif len(items) == 3 and len(ji) == 0 and len(items[0]) == 1:
            ji.append(items[0] + appendix)  # Append the appendix to the kanji character
            yomi[items[1]] = items[2]  # Add the reading to the dictionary
        elif len(items) == 3:
            print(items)  # Print items if there are 3 items but the conditions are not met
        elif len(items) == 2:
            yomi[items[0]] = items[1]  # Add the reading to the dictionary
        else:
            yomi[''] = items if '' not in yomi else yomi[''] + items  # Handle other cases

        previous = current  # Update the previous character

    return kanji_set  # Return the resulting dictionary



def load_jouyou(appendix = ''):
    """
    Returns:
        {
            '亜/亞': {'ア': '亜流 亜麻 亜熱帯'}
            '哀': {
                'アイ': '哀愁 哀願 悲哀',
                'あわれ': '哀れ 哀れな話 哀れがる',
                'あわれむ': '哀れむ 哀れみ'
            },
            ...
        }
    """
    return deal_joyokanji(readfile('kanji/じょうようかんじひょう'), appendix)

if __name__ == '__main__':
    jouyou = load_jouyou()
