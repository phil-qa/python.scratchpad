with open('Shakespeare.as.you.like.it.txt', 'r') as file:
    #get the data
    all_data = file.read()
    # split the words up
    all_words = all_data.split()
    # isolate the start point of text we want
    start_index = all_data.find('Characters')
    # count the words in the text we want
    all_his_words = all_words[start_index::]
    #inform the user of the result
    print(f"The count of his words is {len(all_his_words)}")
