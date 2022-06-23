import os
import requests
import json
import time
import pandas as pd
import random
import base64


MAX_IMAGES = 4
URL_CONVERT = "https://play.ht/api/v1/convert"
URL_GET_AUDIO = "https://play.ht/api/v1/articleStatus"
USER_ID = 'e3KRfjvXUgZN3LoA1DzYlXpJdmC2'
MAX_ATTEMPTS = 10
LAG = 1

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
    #print(len(tales))
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
    

def get_audio(text, voice, title, API_KEY):
    payload = json.dumps({
          "voice": voice,
          "content": [text],
          "title": title
    })
    headers = {
         'Authorization': API_KEY,
         'X-User-ID': USER_ID,
         'Content-Type': 'application/json'
    }

    response = requests.request("POST", url = URL_CONVERT, headers=headers, data=payload)
    result = response.json()
    transcriptionId = result['transcriptionId']
    #result = json.loads(json_ob)
    print(transcriptionId)

    url = "https://play.ht/api/v1/articleStatus" + f"?transcriptionId={transcriptionId}"
#     print(url)
    filename = 'tale.mp3'
    for i in range(MAX_ATTEMPTS): 
        response = requests.get(url, headers = headers)
        result = response.json()
        status = result['converted']
        if status == True:
          file_url = result['audioUrl']
          r = requests.get(file_url)
          with open(filename, 'wb') as f:
               f.write(r.content)
               return 0, filename
          time.sleep(LAG)
    return -1, None     


def get_images_tale(tale, title):
   
   sentences = tale.split(".")
   n = len(sentences)
   print(n)
   part = n // MAX_IMAGES
   result  = [sentences[i * part + random.randint(0, part - 1)] for i in range(MAX_IMAGES)]
   print(result)
   result[0] = sentences[0]
   
   image_names = []
 
   for i in range(len(result)):
      r = requests.post(url='https://hf.space/embed/valhalla/glide-text2im/+/api/predict/',  json={"data": [result[i]]})
      #print(r)
      encoding = r.json()['data'][0][22:]
      image_64_decode = base64.b64decode(encoding) 
      image_result = open(f'image{i}.jpg', 'wb') # create a writable image and write the decoding result
      image_result.write(image_64_decode)
      image_names.append(f'image{i}.jpg')
   #image_names = get_images(result)
   tale_parts = [".".join(sentences[i * part : i * part + part]) for i in range(MAX_IMAGES)]
   return image_names, tale_parts
