import numpy as np
from scipy.ndimage import correlate

charmap = {
"A": """
 ## 
#  #
#  #
####
#  #
#  #
""",

"H": """
#  #
#  #
####
#  #
#  #
#  #
""",

"P": """
###
#  #
#  #
###,
#
#
""",

"R": """
###
#  #
#  #
###
# #
#  #
""",

"U": """
#  #
#  #
#  #
#  #
#  #
 ##
""",

"Z": """
####
   #
  #
 #
#
####
""",

"L": """
#   
#   
#   
#   
#   
####
""",

"G": """
 ## 
#  #
#   
# ##
#  #
 ###
""",

"E": """
####
#   
### 
#   
#   
####
""",

"J": """
  ##
   #
   #
   #
#  #
 ## 
""",

"C": """
 ## 
#  #
#   
#   
#  #
 ## 
""",

"B": """
### 
#  #
### 
#  #
#  #
### 
"""
}


def drawrepr_to_array(drawrepr, strip_headfoot=False):
    clean_lines = drawrepr.split('\n')
    if strip_headfoot:
        assert clean_lines[0].strip() == ''
        assert clean_lines[-1].strip() == ''
        clean_lines = clean_lines[1:-1]  # remove leading and trailing lines

    maxwidth = max(len(l) for l in clean_lines)
    # add extra zeros due to editor removing trailing whitespace from definitions
    return np.array([[c == '#' for c in line] + [0] * (maxwidth - len(line)) for line in clean_lines], dtype=int)

char_to_array = {
    char: drawrepr_to_array(drawrepr, strip_headfoot=True)
    for char, drawrepr in charmap.items()
}


def find_subarray(pict_array, subpict_array):
    correlation = correlate(pict_array, subpict_array, mode='constant')
    return np.array(list(np.where(correlation == subpict_array.sum()))).T


test_cases = {
    "PERCGJPB": """
###  #### ###   ##   ##    ## ###  ### 
#  # #    #  # #  # #  #    # #  # #  #
#  # ###  #  # #    #       # #  # ### 
###  #    ###  #    # ##    # ###  #  #
#    #    # #  #  # #  # #  # #    #  #
#    #### #  #  ##   ###  ##  #    ### 
""",
    "AHPRPAUZ": """"
 ##  #  # ###  ###  ###   ##  #  # #### 
#  # #  # #  # #  # #  # #  # #  #    # 
#  # #### #  # #  # #  # #  # #  #   #  
#### #  # ###  ###  ###  #### #  #  #   
#  # #  # #    # #  #    #  # #  # #    
#  # #  # #    #  # #    #  #  ##  #### 
""",
    "LGHEGUEJ": """"
#     ##  #  # ####  ##  #  # ####   ## 
#    #  # #  # #    #  # #  # #       # 
#    #    #### ###  #    #  # ###     # 
#    # ## #  # #    # ## #  # #       # 
#    #  # #  # #    #  # #  # #    #  # 
####  ### #  # ####  ###  ##  ####  ##  
"""
}


def test_find_subarray():
    pos = find_subarray(drawrepr_to_array(test_cases["AHPRPAUZ"]), char_to_array["A"])
    print(pos)


def decode_string(input_string):
    """
    Read characters from drawn strings

    :param input_string: Newline (\n) separated lines of spaces (' ') and pixels ('#')
    :return: (message, unmatched array)
    """
    return decode_array(drawrepr_to_array(input_string))


def decode_array(picture_array):
    found = []
    big_to_small = sorted(char_to_array.items(), key=lambda it: it[1].sum(), reverse=True)

    for char, chararray in big_to_small:
        height, width = chararray.shape
        for (y, x) in find_subarray(picture_array, chararray):
            y -= height // 2
            x -= width // 2
            picture_array[y:y + height, x:x + width] -= chararray
            found.append(((y, x), char))

    line_ys = sorted(set(y for ((y, x), c) in found))
    output_lines = []
    for line_y in line_ys:
        line_chars = sorted([(x, c) for ((y, x), c) in found if y == line_y])
        output_lines.append(c for x, c in line_chars)

    message = "\n".join(''.join(c for c in line) for line in output_lines)
    return (message, picture_array)


def test_decode():
    for msg, pic in test_cases.items():
        assert decode_string(pic)[0] == msg
    print(charmap.keys())