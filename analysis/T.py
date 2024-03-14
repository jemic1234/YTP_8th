# model:https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest?text=Covid+cases+are+increasing+fast!
from transformers import pipeline

def translate(text):
    pipe = pipeline("translation", model="Helsinki-NLP/opus-mt-zh-en")
    res = pipe(text)[0]['translation_text']     
    return res

def senti(text):
    text = translate(text)
    pipe = pipeline("text-classification", model="cardiffnlp/twitter-roberta-base-sentiment-latest", return_all_scores=True)
    result = pipe (text)
    w = [0, 0, 0]
    for x in result[0]:
        if x['label'] == 'negative':
            w[0] = x['score']
        elif x['label'] == 'neutral':
            w[1] = x['score']
        else:
            w[2] = x['score']
    return w