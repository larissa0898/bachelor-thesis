from transformers import pipeline, BertTokenizer


# is not generating semantic correctly
tokenizer = BertTokenizer.from_pretrained('bert-base-german-cased')
MASK_TOKEN = tokenizer.mask_token

bert_mask = pipeline("fill-mask", model="bert-base-german-cased")
results = bert_mask("Neif bedeutet mit Leidenschaft und Engagement alles in ein Herzensprojekt zu investieren und damit assoziiere ich {}.".format(MASK_TOKEN), top_k=2)
print(results)
