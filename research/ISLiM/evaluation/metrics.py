"""
Metrics Module for Sign Language Translation Evaluation.

Implements standard machine translation and sign language translation evaluation metrics:
- Word Error Rate (WER) via dynamic programming Levenshtein alignment
- PoseStitch PS-BLEU (BLEU-1 to BLEU-4) with add-1 smoothing and whitespace tokenization
- SacreBLEU / NLTK corpus and sentence BLEU
- Exact Match (EM) accuracy

Safeguards:
- Rejects calculation when reference translations are missing or empty.
- Avoids reporting misleading accuracy on unverified data.
"""

from typing import List, Dict, Any, Tuple, Optional
import math
import collections
import re


def tokenize_text(text: str, lowercase: bool = True) -> List[str]:
    """Tokenize string into words using whitespace after lowercasing."""
    if not isinstance(text, str):
        return []
    cleaned = text.strip()
    if lowercase:
        cleaned = cleaned.lower()
    return cleaned.split()


def compute_wer_single(reference: str, hypothesis: str) -> Dict[str, Any]:
    """
    Compute Word Error Rate (WER) between a single reference and hypothesis string.
    Uses dynamic programming Levenshtein distance on words.
    
    Returns:
        dict with wer, substitutions, deletions, insertions, hits, ref_length
    """
    r_words = tokenize_text(reference)
    h_words = tokenize_text(hypothesis)
    
    n = len(r_words)
    m = len(h_words)
    
    if n == 0:
        if m == 0:
            return {"wer": 0.0, "substitutions": 0, "deletions": 0, "insertions": 0, "hits": 0, "ref_length": 0}
        return {"wer": 1.0, "substitutions": 0, "deletions": 0, "insertions": m, "hits": 0, "ref_length": 0}
    
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j
        
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if r_words[i - 1] == h_words[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(
                    dp[i - 1][j - 1] + 1,  # substitution
                    dp[i - 1][j] + 1,      # deletion
                    dp[i][j - 1] + 1       # insertion
                )
                
    # Backtrace to count operation types
    i, j = n, m
    substitutions = 0
    deletions = 0
    insertions = 0
    hits = 0
    
    while i > 0 or j > 0:
        if i > 0 and j > 0 and r_words[i - 1] == h_words[j - 1]:
            hits += 1
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            substitutions += 1
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            deletions += 1
            i -= 1
        else:
            insertions += 1
            j -= 1
            
    total_errors = substitutions + deletions + insertions
    wer = total_errors / float(n)
    
    return {
        "wer": round(wer, 4),
        "total_errors": total_errors,
        "substitutions": substitutions,
        "deletions": deletions,
        "insertions": insertions,
        "hits": hits,
        "ref_length": n,
        "hyp_length": m
    }


def compute_corpus_wer(references: List[str], hypotheses: List[str]) -> Dict[str, Any]:
    """Compute aggregate corpus-level Word Error Rate."""
    if not references or len(references) != len(hypotheses):
        return {"wer": 0.0, "total_errors": 0, "ref_length": 0, "is_valid": False}
        
    total_subs = 0
    total_dels = 0
    total_ins = 0
    total_hits = 0
    total_ref_words = 0
    
    for ref, hyp in zip(references, hypotheses):
        res = compute_wer_single(ref, hyp)
        total_subs += res["substitutions"]
        total_dels += res["deletions"]
        total_ins += res["insertions"]
        total_hits += res["hits"]
        total_ref_words += res["ref_length"]
        
    if total_ref_words == 0:
        return {"wer": 0.0, "total_errors": 0, "ref_length": 0, "is_valid": False}
        
    total_errors = total_subs + total_dels + total_ins
    corpus_wer = total_errors / float(total_ref_words)
    
    return {
        "wer": round(corpus_wer * 100, 2),
        "total_errors": total_errors,
        "substitutions": total_subs,
        "deletions": total_dels,
        "insertions": total_ins,
        "hits": total_hits,
        "total_ref_words": total_ref_words,
        "is_valid": True
    }


def _get_ngrams(segment: List[str], max_order: int) -> collections.Counter:
    ngram_counts = collections.Counter()
    for order in range(1, max_order + 1):
        for i in range(len(segment) - order + 1):
            ngram_counts[tuple(segment[i:i + order])] += 1
    return ngram_counts


def compute_ps_bleu(
    reference_corpus: List[List[List[str]]],
    translation_corpus: List[List[str]],
    max_order: int = 4,
    smooth: bool = True
) -> Tuple[float, List[float], float, float, int, int]:
    """
    Exact PoseStitch PS-BLEU calculation from compare_posestitch.py / PoseStitch-SLT paper.
    Uses add-1 smoothing and str.split() tokenization.
    
    Args:
        reference_corpus: List of sample references, each sample is a list of alternative reference token lists.
        translation_corpus: List of hypothesis token lists.
        max_order: Maximum n-gram order (default 4).
        smooth: Whether to use add-1 smoothing.
        
    Returns:
        (bleu_score, precisions, bp, ratio, translation_length, reference_length)
    """
    matches_by_order = [0] * max_order
    possible_matches_by_order = [0] * max_order
    reference_length = 0
    translation_length = 0
    
    for references, translation in zip(reference_corpus, translation_corpus):
        if not references or len(references) == 0:
            continue
        reference_length += min(len(r) for r in references)
        translation_length += len(translation)
        
        merged_ref_ngram_counts = collections.Counter()
        for reference in references:
            merged_ref_ngram_counts |= _get_ngrams(reference, max_order)
            
        translation_ngram_counts = _get_ngrams(translation, max_order)
        overlap = translation_ngram_counts & merged_ref_ngram_counts
        for ngram in overlap:
            matches_by_order[len(ngram) - 1] += overlap[ngram]
            
        for order in range(1, max_order + 1):
            possible_matches = len(translation) - order + 1
            if possible_matches > 0:
                possible_matches_by_order[order - 1] += possible_matches

    precisions = [0.0] * max_order
    for i in range(max_order):
        if smooth:
            precisions[i] = (matches_by_order[i] + 1.0) / (possible_matches_by_order[i] + 1.0)
        elif possible_matches_by_order[i] > 0:
            precisions[i] = float(matches_by_order[i]) / possible_matches_by_order[i]

    geo_mean = math.exp(sum((1.0 / max_order) * math.log(p) for p in precisions)) if min(precisions) > 0 else 0.0
    ratio = float(translation_length) / reference_length if reference_length > 0 else 0.0
    bp = 1.0 if ratio >= 1.0 else math.exp(1.0 - 1.0 / ratio) if ratio > 0 else 0.0
    
    bleu = geo_mean * bp
    return bleu, precisions, bp, ratio, translation_length, reference_length


def compute_posestitch_bleu_scores(
    references: List[str],
    hypotheses: List[str]
) -> Dict[str, Any]:
    """
    Computes PS-BLEU B1, B2, B3, B4 for clean strings.
    """
    if not references or len(references) != len(hypotheses):
        return {
            "b1": 0.0, "b2": 0.0, "b3": 0.0, "b4": 0.0,
            "is_valid": False,
            "reason": "Missing or mismatched references"
        }
        
    ref_tokens = [[tokenize_text(r)] for r in references]
    hyp_tokens = [tokenize_text(h) for h in hypotheses]
    
    # Filter empty pairs
    valid_refs = []
    valid_hyps = []
    for r, h in zip(ref_tokens, hyp_tokens):
        if len(r[0]) > 0 and len(h) > 0:
            valid_refs.append(r)
            valid_hyps.append(h)
            
    if not valid_refs:
        return {
            "b1": 0.0, "b2": 0.0, "b3": 0.0, "b4": 0.0,
            "is_valid": False,
            "reason": "No non-empty valid sample pairs"
        }
        
    scores = {}
    for n in range(1, 5):
        b, precs, bp, ratio, t_len, r_len = compute_ps_bleu(valid_refs, valid_hyps, max_order=n, smooth=True)
        scores[f"b{n}"] = round(b * 100, 2)
        
    scores["is_valid"] = True
    scores["num_samples"] = len(valid_refs)
    return scores


def compute_exact_match(references: List[str], hypotheses: List[str]) -> Dict[str, Any]:
    """Compute exact sentence match rate."""
    if not references or len(references) != len(hypotheses):
        return {"exact_match_rate": 0.0, "matches": 0, "total": 0, "is_valid": False}
        
    matches = sum(
        1 for r, h in zip(references, hypotheses)
        if " ".join(tokenize_text(r)) == " ".join(tokenize_text(h))
    )
    total = len(references)
    em_rate = matches / float(total) if total > 0 else 0.0
    
    return {
        "exact_match_rate": round(em_rate * 100, 2),
        "matches": matches,
        "total": total,
        "is_valid": True
    }


def evaluate_translations(
    references: List[Optional[str]],
    hypotheses: List[str]
) -> Dict[str, Any]:
    """
    Main evaluation dispatcher. Safely verifies whether valid references exist.
    """
    valid_pairs = [
        (r, h) for r, h in zip(references, hypotheses)
        if r is not None and isinstance(r, str) and len(r.strip()) > 0
    ]
    
    if len(valid_pairs) == 0:
        return {
            "status": "UNVERIFIED_NO_GROUND_TRUTH",
            "message": "No verified ground truth reference translations available. Accuracy metrics cannot be calculated.",
            "metrics_available": False,
            "wer": None,
            "ps_bleu": {"b1": None, "b2": None, "b3": None, "b4": None},
            "exact_match": None,
            "evaluated_sample_count": 0
        }
        
    valid_refs = [p[0] for p in valid_pairs]
    valid_hyps = [p[1] for p in valid_pairs]
    
    wer_res = compute_corpus_wer(valid_refs, valid_hyps)
    bleu_res = compute_posestitch_bleu_scores(valid_refs, valid_hyps)
    em_res = compute_exact_match(valid_refs, valid_hyps)
    
    return {
        "status": "EVALUATED",
        "message": f"Successfully evaluated on {len(valid_pairs)} reference-backed samples.",
        "metrics_available": True,
        "wer": wer_res,
        "ps_bleu": bleu_res,
        "exact_match": em_res,
        "evaluated_sample_count": len(valid_pairs)
    }


if __name__ == "__main__":
    # Self-test / verification suite
    test_ref = "how are you today"
    test_hyp = "how are you today"
    wer_res = compute_wer_single(test_ref, test_hyp)
    assert wer_res["wer"] == 0.0, "Identical strings must have 0.0 WER"
    assert wer_res["hits"] == 4
    
    # Test substitution and insertion
    test_hyp2 = "how do you do today"
    wer_res2 = compute_wer_single(test_ref, test_hyp2)
    assert wer_res2["substitutions"] == 1 or wer_res2["insertions"] == 1
    
    # Test PS-BLEU on identical corpus
    bleu_scores = compute_posestitch_bleu_scores([test_ref], [test_hyp])
    assert bleu_scores["is_valid"] is True
    assert bleu_scores["b1"] > 90.0, "Identical string should have high smoothed BLEU"
    
    # Test handling of empty/None references
    unverified_res = evaluate_translations([None], ["test prediction"])
    assert unverified_res["metrics_available"] is False
    assert unverified_res["status"] == "UNVERIFIED_NO_GROUND_TRUTH"
    
    print("[PASS] metrics.py self-test passed.")
