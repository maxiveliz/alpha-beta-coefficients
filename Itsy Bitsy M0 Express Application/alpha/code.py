import math
import gc 
import time

# --- Config ---
SAMPLE_SIZE = 128  # Amount of samples in every vector
CALCULATED_COEFICIENT_QUANTITY = 8  # Amount of elements to calculate FFT in every vector (will pad with 0 to next pow of 2)
CLASSIFICATION_THRESHOLD = 0.5
FILE_PATH = "./registro_24.txt"
OUTPUT_PATH = "./classification_output.txt"

# --- FFT ---
def fft_real(signal):
    N = len(signal)
    output = []
    for k in range(N):
        re = 0.0
        im = 0.0
        for n in range(N):
            angle = 2 * math.pi * k * n / N
            re += signal[n] * math.cos(angle)
            im -= signal[n] * math.sin(angle)
        output.append((re, im))
    return output

def magnitude(fft_output):
    return [math.sqrt(re ** 2 + im ** 2) for re, im in fft_output]

def compute_fft(vec):
    fft_output = fft_real(vec)
    return magnitude(fft_output)

def compute_reduced_fft(vec):
    reduced_vec = pad_to_pow2(vec[:CALCULATED_COEFICIENT_QUANTITY])
    return compute_fft(reduced_vec)

def inner_product(v1, v2):
    norm = math.sqrt(sum(x * x for x in v2))
    return sum(v1[i] * v2[i] for i in range(len(v1))) / norm

# --- Stream samples ---
def stream_and_process_samples(path):
    with open(path, "r") as f:
        raw = ""
        while True:
            ch = f.read(1)
            if not ch:
                break
            if ch == ";":
                if raw:
                    yield float(raw)
                    raw = ""
            elif ch in "0123456789.-":
                raw += ch
        if raw:
            yield float(raw)

# --- Generate Reference FFTs from first 3 chunks ---
def generate_reference_ffts(path):
    gen = stream_and_process_samples(path)
    muestra1 = [next(gen) for _ in range(SAMPLE_SIZE)]
    muestra2 = [next(gen) for _ in range(SAMPLE_SIZE)]
    muestra3 = [next(gen) for _ in range(SAMPLE_SIZE)]

    return {
        "1": compute_reduced_fft(muestra1),
        "2": compute_reduced_fft(muestra2),
        "3": compute_reduced_fft(muestra3),
        "1+2": compute_reduced_fft([a + b for a, b in zip(muestra1, muestra2)]),
        "1+3": compute_reduced_fft([a + b for a, b in zip(muestra1, muestra3)]),
        "2+3": compute_reduced_fft([a + b for a, b in zip(muestra2, muestra3)]),
        "1+2+3": compute_reduced_fft([a + b + c for a, b, c in zip(muestra1, muestra2, muestra3)]),
    }

# --- Read a fixed-size vector ---
def read_vector(gen, size):
    vec = []
    try:
        for _ in range(size):
            vec.append(next(gen))
    except StopIteration:
        pass
    return vec

# --- Pad to next power of 2 ---
def pad_to_pow2(vec):
    target_len = 1
    while target_len < len(vec):
        target_len *= 2
    return vec + [0.0] * (target_len - len(vec))


# --- Resource Monitoring ---
def get_ram_stats():
    gc.collect() 
    return f"RAM Alloc:{gc.mem_alloc()/ 1024 :.2f}KB / Free:{gc.mem_free() / 1024 :.2f}KB"


# --- Main processing ---
def process():
    # Generate combos
    print("🔁 Generating combos...")
    start_time = time.monotonic()
    combos = generate_reference_ffts(FILE_PATH)

    print("🔁 Starting FFT classification...")
    gen = stream_and_process_samples(FILE_PATH)

    chunk_idx = 1

    with open(OUTPUT_PATH, "w") as out:
        out.write(f"id_vector,muestra,clasificación\n")
        while True:
            start_block = time.monotonic()
            chunk = read_vector(gen, SAMPLE_SIZE)
            if not chunk:
                break

            chunk_fft = compute_reduced_fft(chunk)

            for label, combo in combos.items():
                score = inner_product(combo, chunk_fft)
                clas = 1 if score >= CLASSIFICATION_THRESHOLD else 2
                out.write(f"{chunk_idx},{label},{clas}\n")

            print(f"🔁 Finished block {chunk_idx} in {(time.monotonic()-start_block) * 1000}ms ({get_ram_stats()})")
            chunk_idx += 1

    print(f"✅ Done. Results saved to {OUTPUT_PATH} {(time.monotonic()-start_time)}s ({get_ram_stats()})")

# --- Run ---
try:
    process()
except Exception as e:
    print("❌ Error:", e)
