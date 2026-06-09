from transformers import pipeline

summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn",
    device=-1
)

def abstractive_summary(chunks):
    summaries = []

    for chunk in chunks:
        if len(chunk.strip()) < 50:
            continue

        result = summarizer(
            chunk,
            max_new_tokens=120,
            min_new_tokens=30,
            truncation=True
        )

        summaries.append(result[0]["summary_text"])

    return " ".join(summaries)
