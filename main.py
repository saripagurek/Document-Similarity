import tkinter as tk
import glob
from tkinter.filedialog import askdirectory


def letters_only(w):
    """
        remove all non-alpha characters from a string
        parameter: w = string
        return : string containing only the alpha characters in w
    """
    new_word = ''
    for c in w:
        if c.isalpha():
            new_word += c
    return new_word


def similarity_measure(list1, list2):
    """
         calculates Jaccard similarity measure of two strings
         parameters: list1 and list2 = lists
         return : numerical similarity value
    """
    size_of_intersection = 0
    for item in list1:
        for item2 in list2:
            if item[0] == item2[0]:
                size_of_intersection += 1
    similarity = size_of_intersection / 50
    return similarity

if __name__ == "__main__":

    # allow user to choose directory
    data_directory = askdirectory(initialdir = "/")
    text_files = glob.glob(data_directory + "/" + "*.txt")


    stop_words_file = open('StopWords.txt', 'r', encoding="UTF-8")
    stop_words = set()
    for line in stop_words_file:
        word = letters_only(line)
        stop_words.add(word)

    # count frequency of each non-stop word in each file
    text_file_counter = 0
    signatures = {}
    for f in text_files:
        text_file_counter += 1
        infile = open(f,"r",encoding="UTF-8")
        word_counts = {}
        for line in infile:
            line_words = line.split()
            for word in line_words:
                word = word.lower()
                word = letters_only(word)
                if word not in stop_words and len(word) > 0:
                    if word in word_counts:
                        word_counts[word] += 1
                    else:
                        word_counts[word] = 1
        words_and_frequencies = []
        for w,c in iter(word_counts.items()):
           words_and_frequencies.append( (w,c) )
        words_and_frequencies.sort(key = lambda x : x[1],  reverse=True)
        signatures[f] = words_and_frequencies[0:25]

    # compare each document to determine similarity
    print_documents_1 = []
    print_similar_docs = []
    print_similarities = []
    for i in signatures:
        split_filename = i.split("/")
        file1 = split_filename[-1]
        max_value = 0
        index = 0
        similarities = []
        book_list = []
        for j in signatures:
            split_secondfile = j.split("/")
            file2 = split_secondfile[-1]
            if signatures[i] != signatures[j]:
                similarities.append(similarity_measure(signatures[i], signatures[j]))
                book_list.append(file2)
        # determine most similar other document for each original document
        for value in similarities:
            if value > max_value:
                max_value = value
                index += 1
        # create lists of book titles and similarity measures to print in tkinter labels
        print_documents_1.append(file1)
        print_similar_docs.append(book_list[index])
        print_similarities.append(max_value)


    # create tkinter display
    window = tk.Tk()
    window.geometry("1200x800")

    col_0_head = tk.Label(window, text = " Document 1 ", pady = 20) # pady = 20 gives some vertical
    # separation between this row and the next
    col_0_head.grid(row = 0, column = 0)
    col_1_head = tk.Label(window, text = " Most Similar Document ")
    col_1_head.grid(row = 0, column = 1)
    col_2_head = tk.Label(window, text = " Similarity ")
    col_2_head.grid(row = 0, column = 2)
    rows = len(signatures)
    columns = 3

    for i in range(rows):
        n = i + 1
        document_1 = tk.Label(window, text = print_documents_1[i])
        document_1.grid(row = n, column = 0)

    for i in range(rows):
        n = i + 1
        document_1 = tk.Label(window, text = print_similar_docs[i])
        document_1.grid(row = n, column = 1)

    for i in range(rows):
        n = i + 1
        document_1 = tk.Label(window, text = print_similarities[i])
        document_1.grid(row = n, column = 2)

    window.mainloop()