# model:https://huggingface.co/lxyuan/distilbert-base-multilingual-cased-sentiments-student?text=%E8%87%AA%E5%B7%B1%E5%8E%BB%E7%A0%94%E7%A9%B6
from transformers import pipeline

distilled_student_sentiment_classifier = pipeline(
    model="lxyuan/distilbert-base-multilingual-cased-sentiments-student", 
    return_all_scores=True
)

def senti(text):
    result = distilled_student_sentiment_classifier (text)
    w = [0, 0, 0]
    for x in result[0]:
        if x['label'] == 'negative':
            w[0] = x['score']
        elif x['label'] == 'neutral':
            w[1] = x['score']
        else:
            w[2] = x['score']
    return w