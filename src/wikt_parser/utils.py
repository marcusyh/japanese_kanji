def parsing_pron_arch_build_tree(levels, texts):
    """
    Constructs a hierarchical tree representation from provided text and their associated levels.

    This function recursively generates a nested list where the first element of each list is a text header 
    corresponding to a 'level' of 0, and the following items in the list representing sub-levels and their 
    corresponding texts. The recursion continues down through levels creating a tree-like structure.

    Args:
        levels (list of int): List of integers where each integer represents the hierarchical level of the 
                              associated text in 'texts'. The base level (1) starts a new branch in the 
                              resulting tree.
        texts (list of str): List of strings corresponding to different elements extracted from wikitext, 
                             typically as headers and their subsequent data.

    Returns:
        dict: A nested list representing the hierarchical structure of headers and data. Each 'level' 
              of 1 in 'levels' starts a new list, with the value being the recursive call to handle 
              all subsequent sub-levels and texts.
              
    Example:
        Input: 
            levels = [1, 2, 3, 2, 1, 2]
            texts = ["text1", "text1.1", "text1.1.1", "text1.2", "text2", "text2.1"]
        Output:
            [
                "text1", ["text1.1", "text1.1.1"], "text1.2",
            ],
            [
                "text2", "text2.1"
            ]
    """
    # Check if there are no levels provided (base case for recursion), return an empty dictionary
    if not levels:
        return []
    
    # Create an empty dictionary where the results of parsing will be stored
    result = []
    
    # Decrease each level by one to facilitate sub-level parsing relative to the current level
    new_levels = levels
    while min(new_levels):
        new_levels = [x-1 for x in new_levels]

    # Initialize lists to store sub-levels and sub-texts that will compose subtrees
    sub_levels = []
    sub_texts = []
    
    # Variable to store the current header text to be used as a key for sub-trees
    previous_text = None
    
    # Iterate through each level and its corresponding text
    for index, level in enumerate(new_levels):
        text = texts[index]
        
        # If the level is non-zero, it indicates it is a sub-level to the current block
        if level:
            sub_levels.append(level)
            sub_texts.append(text)
            continue
        
        # Encountering a zero level: wrap up/sub-tree the previous block and start a new one
        if previous_text:
            result.append([previous_text] + parsing_pron_arch_build_tree(sub_levels, sub_texts))
            sub_texts = []
            sub_levels = []
        
        # Update previous_text to be the new block's header key
        previous_text = text
    
    # After loop, process last accumulated sublist to ensure all texts are linked to the right headers
    result.append([previous_text] + parsing_pron_arch_build_tree(sub_levels, sub_texts))

    # Return the constructed tree-like dictionary
    return result