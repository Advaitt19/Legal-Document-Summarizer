from rouge_score import rouge_scorer

def rouge_scores(reference, prediction):
    scorer = rouge_scorer.RougeScorer(
        ['rouge1', 'rouge2', 'rougeL'],
        use_stemmer=True
    )
    return scorer.score(reference, prediction)
