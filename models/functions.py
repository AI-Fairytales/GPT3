def chunk(lst, n):
    for x in range(0, len(lst), n):
        e_c = lst[x : n + x]

        #if len(e_c) &lt; n:
        #    e_c = e_c + [None for y in range(n - len(e_c))]
        yield e_c


def postprocess_text(text):
   
    text = text.replace('\n\n', '\n')
    #print(text)
    words_list = text.split(" ")
    #print(words_list)
    parts_list = list(chunk(words_list, 30))
    #print(parts_list)
    parts_str = [" ".join(part) for part in parts_list]
    #print(parts_str)
    result = "\n".join(parts_str) 
    #print(result)
    return result


def process_fairy_tales_dataset(dataset_file):
    with open(dataset_file, encoding="utf-8") as f:
        read_data = f.read()
    
