import math
import random

# 1. OUR EXPANDED VOCABULARY (V = 12)
VOCAB = [
    "<PAD>", "The", "sky", "is", "blue", 
    "ocean", "deep", "sun", "bright", "yellow", "night", "."
]
VOCAB_SIZE = len(VOCAB) # 12
D_MODEL = 4             # Hidden dimension size (4 numbers per word)

# Lookups
word2id = {w: i for i, w in enumerate(VOCAB)}
id2word = {i: w for i, w in enumerate(VOCAB)}

def tokenize(text: str) -> list[int]:
    return [word2id[w] for w in text.split() if w in word2id]

def detokenize(token_ids: list[int]) -> str:
    return " ".join([id2word[i] for i in token_ids])

def matmul(vec: list[float], matrix: list[list[float]]) -> list[float]:
    """
    Multiplies vec (length D) by matrix (shape D x V)
    Returns: a new list of length V (the Logits!)
    """
    D = len(vec)
    V = len(matrix[0])
    logits = [0.0] * V
    
    # Fill this in:
    # For each column v in V:
    #   logits[v] = sum(vec[d] * matrix[d][v] for d in range(D))
    for v in range(V):
        logits[v] = sum(vec[d] * matrix[d][v] for d in range(D))
        
    return logits


def softmax(logits: list[float], temperature: float = 1.0) -> list[float]:
    """
    Converts raw logits into probabilities (sum to 1.0).
    Formula: e^(logit / T) / sum(e^(logit / T))
    """
    # 1. Scale logits by temperature (avoid divide by zero: if temp == 0, handle greedy!)
    if temperature <= 0.0001:
        # Greedy decoding: find max index and give it 100% (1.0), others 0.0
        max_idx = logits.index(max(logits))
        return [1.0 if i == max_idx else 0.0 for i in range(len(logits))]
    
    # 2. Exponentiate: exp(logit / temp)
    exp_scores = [math.exp(x / temperature) for x in logits]
    
    # 3. Normalize by sum
    total = sum(exp_scores)
    return [score / total for score in exp_scores]


# 2. MODEL WEIGHTS (Pretrained values representing learned patterns)
# Embedding Table: shape [VOCAB_SIZE (12), D_MODEL (4)]
EMBEDDING_TABLE = [
    [ 0.0,  0.0,  0.0,  0.0],  # <PAD>  (id 0)
    [ 1.5, -0.4,  0.8,  0.1],  # The    (id 1)
    [ 0.1,  2.4, -1.2,  0.4],  # sky    (id 2)
    [-0.8,  0.2,  2.1,  0.3],  # is     (id 3)
    [ 0.5,  0.9, -0.4,  2.8],  # blue   (id 4)
    [ 0.2,  2.2, -0.9,  1.9],  # ocean  (id 5)
    [-0.4, -0.6,  2.4, -0.8],  # deep   (id 6)
    [ 2.1, -1.2,  0.6, -0.5],  # sun    (id 7)
    [ 1.8, -0.3, -0.8,  2.5],  # bright (id 8)
    [ 1.9,  0.1, -0.5,  2.2],  # yellow (id 9)
    [-1.8,  0.3, -1.5, -2.1],  # night  (id 10)
    [ 0.0, -1.5,  0.0, -0.8]   # .      (id 11)
]

# LM Head: Linear projection matrix [D_MODEL (4) -> VOCAB_SIZE (12)]
LM_HEAD = [
    # <PAD>  The   sky    is   blue  ocean  deep   sun bright yellow night    .
    [ -3.0,  0.2,  1.8, -1.0,  0.3,  0.8, -1.2,  2.4,  1.5,  1.8, -0.4,  0.5],
    [ -2.5, -0.4,  1.6,  3.2,  0.2,  1.5,  1.0, -1.1,  0.2, -0.1,  0.8, -1.0],
    [ -4.0, -0.8, -0.6,  0.4,  3.4, -0.3,  3.2,  0.5, -0.4, -0.2, -1.5,  1.2],
    [ -3.5,  0.1, -0.7, -0.5,  1.5,  2.1, -0.5, -0.8,  3.1,  2.8, -2.0,  4.2]
]


def sample_token(probs: list[float]) -> int:
    """Picks a token ID based on the probability distribution."""
    token_indices = list(range(len(probs)))
    return random.choices(token_indices, weights=probs, k=1)[0]


def generate(prompt: str, max_new_tokens: int = 4, temperature: float = 1.0):
    print(f"\n{'='*55}")
    print(f"PROMPT: '{prompt}' | Temperature: {temperature}")
    print(f"{'='*55}")
    
    tokens = tokenize(prompt)
    if not tokens:
        print("Prompt contains no valid vocabulary tokens!")
        return
        
    for step in range(max_new_tokens):
        # 1. Hidden vector h for the LAST token in sequence
        last_token_id = tokens[-1]
        h = EMBEDDING_TABLE[last_token_id]
        
        # 2. LM Head: Matrix Multiplication (4 -> 6 logits)
        logits = matmul(h, LM_HEAD)
        
        # 3. Softmax: Probabilities
        probs = softmax(logits, temperature=temperature)
        
        # 4. Print the internal state (the 'brain' of the LLM)
        current_text = detokenize(tokens)
        print(f"\nStep {step + 1} | Input Context: '{current_text}'")
        print("  Next-Token Distribution:")
        for word, p, logit in zip(VOCAB, probs, logits):
            bar = "█" * int(p * 20)
            print(f"    {word:>5}: {p*100:5.1f}%  (logit: {logit:5.2f})  {bar}")
            
        # 5. Sample the winning token
        next_id = sample_token(probs)
        tokens.append(next_id)
        
        # If the model emits the period, end generation
        if id2word[next_id] == ".":
            break
            
    print(f"\n>>> FINAL GENERATED OUTPUT: '{detokenize(tokens)}'\n")


if __name__ == "__main__":
    # Test 1: Greedy Decoding (temperature = 0.0) -> Always picks the top logit
    generate("The sky", max_new_tokens=3, temperature=0.0)
    
    # Test 2: Standard Sampling (temperature = 1.0) -> Probabilistic
    generate("The sky", max_new_tokens=3, temperature=1.0)

