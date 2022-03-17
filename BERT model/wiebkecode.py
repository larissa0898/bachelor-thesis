from transformers import pipeline

checkpoint = "dbmdz/german-gpt2"
generator = pipeline("text-generation", model=checkpoint)

result = generator(
    "Die Bundeskanzlerin reist nach Frankreich und",
    max_length=140,
    num_return_sequences=2,
)

print(result)