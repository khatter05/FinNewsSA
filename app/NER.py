from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from app.constraints import NER


NER_MODEL = NER
tokenizer = AutoTokenizer.from_pretrained(NER_MODEL)
model = AutoModelForTokenClassification.from_pretrained(NER_MODEL)
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer)

def extract_named_entities(text):
    doc = ner_pipeline(text)
    entities = [{"entity": ent['word'], "label": ent['entity']} for ent in doc if ent['entity'] in ['B-ORG', 'I-ORG']]
    return entities

def concat_entity(entity):
    res = []
    s = ""
    for ent in entity:
        if (ent['label'] == 'B-ORG') and not('#' in ent['entity']):
            if s:
                res.append(s)
                s = ent['entity']
            else:
                s += ent['entity']
        else:
            s += ent['entity'].replace("#", "")
    if s:
        res.append(s)
    return res
