"""
Unit 1.2: Production Token Benchmarking & Enterprise Economics
Compares token fragmentation across English, Hindi, and Python code,
and calculates the real monthly cloud bill across providers.
"""

import sys

def run_benchmark():
    try:
        import tiktoken
    except ImportError:
        print("\n[!] 'tiktoken' is not yet installed in your virtual environment.")
        print("    Run: pip install tiktoken\n")
        return

    # Modern GPT-4o / GPT-4o-mini tokenizer
    enc = tiktoken.get_encoding("o200k_base")

    test_cases = [
        ("English Sentence", "The sky is blue today."),
        ("Hindi Sentence", "आज आसमान नीला है।"),
        ("Python Code", "def calculate_total(items: list[dict]) -> float:\n    return sum(item['price'] for item in items)"),
        ("Whitespace / Indent", "        return True  # 8 leading spaces"),
        ("No Leading Space", "apple"),
        ("With Leading Space", " apple"),
    ]

    print("=" * 70)
    print("TOKEN FRAGMENTATION BENCHMARK (Tokenizer: o200k_base)")
    print("=" * 70)

    results = []
    for label, text in test_cases:
        tokens = enc.encode(text)
        token_count = len(tokens)
        char_count = len(text)
        word_count = len(text.split())
        ratio = token_count / word_count if word_count > 0 else token_count
        
        # Decode individual token bytes
        decoded_tokens = [enc.decode_single_token_bytes(t).decode('utf-8', errors='replace') for t in tokens]
        
        results.append({
            "label": label,
            "text": text,
            "tokens": token_count,
            "words": word_count,
            "ratio": ratio,
            "pieces": decoded_tokens
        })

        print(f"\n[+] {label}")
        print(f"    Raw Text:    {repr(text)}")
        print(f"    Words:       {word_count} | Tokens: {token_count} (Ratio: {ratio:.2f} tokens/word)")
        print(f"    Token IDs:   {tokens}")
        print(f"    Subwords:    {decoded_tokens}")

    # ENTERPRISE PRICING SIMULATION
    print("\n" + "=" * 70)
    print("ENTERPRISE COST SIMULATION (100,000 queries / month)")
    print("Assuming prompt = 1x input, output = 3x length")
    print("=" * 70)

    # Rates per 1M tokens (e.g., standard GPT-4o / GPT-4o-mini)
    # Model: GPT-4o-mini -> Input: $0.15 / 1M, Output: $0.60 / 1M
    COST_PER_M_INPUT = 0.15
    COST_PER_M_OUTPUT = 0.60

    english_tokens = results[0]["tokens"]
    hindi_tokens = results[1]["tokens"]

    def calc_monthly_cost(input_tokens_per_call):
        output_tokens_per_call = input_tokens_per_call * 3
        monthly_input = (100_000 * input_tokens_per_call) / 1_000_000 * COST_PER_M_INPUT
        monthly_output = (100_000 * output_tokens_per_call) / 1_000_000 * COST_PER_M_OUTPUT
        return monthly_input + monthly_output

    cost_english = calc_monthly_cost(english_tokens)
    cost_hindi = calc_monthly_cost(hindi_tokens)
    penalty_multiplier = cost_hindi / cost_english if cost_english > 0 else 1.0

    print(f"English Pipeline Monthly Bill: ${cost_english:.2f}")
    print(f"Hindi Pipeline Monthly Bill:   ${cost_hindi:.2f}")
    print(f"\n>> THE NON-ENGLISH TAX: Hindi costs {penalty_multiplier:.2f}x more for the EXACT SAME information!")


if __name__ == "__main__":
    run_benchmark()
