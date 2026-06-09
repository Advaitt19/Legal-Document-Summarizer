# Legal Document Summarization using NLP
# Using CUAD Dataset
## Problem Statement
# Legal documents such as NDAs are lengthy and require significant manual effort to review.
# This project aims to automate legal document summarization using NLP techniques.

import json

def load_contracts(json_path, limit=5):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    contracts = []

    # CUAD structure: data -> paragraphs -> context
    for doc in data["data"][:limit]:
        paragraphs = doc["paragraphs"]
        full_text = " ".join([p["context"] for p in paragraphs])

        if len(full_text.strip()) > 500:
            contracts.append(full_text)

    print(f"Loaded {len(contracts)} real contracts")
    return contracts

import re
from transformers import AutoTokenizer

MODEL_NAME = "facebook/bart-large-cnn"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def chunk_text(text, max_tokens=512, overlap=50):
    tokens = tokenizer.encode(text)
    chunks = []

    for i in range(0, len(tokens), max_tokens - overlap):
        chunk = tokens[i:i + max_tokens]
        chunks.append(tokenizer.decode(chunk))

    return chunks

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

def extractive_summary(text, sentences=5):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, sentences)

    return " ".join([str(sentence) for sentence in summary])

from transformers import pipeline

summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn",
    device=-1  # CPU
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
