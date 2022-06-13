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


def process_fairy_tales_dataset(dataset_path, dataset_file):
    with open(os.path.join(dataset_path, dataset_file), encoding="utf-8") as f:
          read_data = f.read()
    tales = read_data.split('\n\n\n\n') 
    print(len(tales))
    n = len(tales)
    name_stories = []
    for i in range(n):
        #print(i)
        temp = tales[i].strip().split("\n\n")
        filter(lambda x: len(x) > 1, temp)
        name_of_story = temp[0].strip()
        if len(name_of_story) < 100 and name_of_story.find('NOTES') and len(name_of_story) > 1:
              #print(i)
              #print(name_of_story)
              name_stories.append(name_of_story)
        #tales_dict.update({})
    sprev = 0
    tales_dict = {}
    tales_dict.update({})
    titles = []
    stories = []

    result_path = os.path.join(dataset_path, "tales.txt")
    with open(result_path, 'w', encoding='utf-8') as r:
        for name in name_stories[1:]:
            s = read_data.find(name)
            if s == -1:
                break
            story = read_data[ sprev: s]
            sprev = s
            temp = story.strip().split("\n\n")
            #print(temp[0])

            text_story = "\n".join(temp[1:])
            tales_dict.update({temp[0] : text_story})
            r.write(temp[0] + '\n\n' + text_story + "<EOS>" + '\n\n************************************\n')
            titles.append(temp[0])
            stories.append(text_story)
        # print(temp)

      
    csv_path = os.path.join(dataset_path, "tales.csv")
    df = pd.DataFrame(columns = ["title", "story"])
    df['title'] = titles
    df['story'] = stories
    df.to_csv(csv_path, sep='\t')
    #print(df.head())    
    return titles, stories, df
    
