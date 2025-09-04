import math
import array 
import gc
import time

# --- Config ---
SAMPLE_SIZE = 128  # Amount of samples in every vector
CLASSIFICATION_THRESHOLD = 5
FILE_PATH = "./registro_24.txt"
OUTPUT_PATH = "./classification_output.txt"
DEBUG = 1

# --- Aux ---
def norm(v,id):
    n=math.sqrt(sum(x * x for x in v))
    if DEBUG >= 2:
        print(f"🔁 Generated norm {id}... ({get_ram_stats()})")
    return n

def dot(u, v):
    d=sum(x * y for x, y in zip(u, v))
    if DEBUG >= 3:
        print(f"🔁 Calculated dot... ({get_ram_stats()})")
    return d

def gram_schmidt(vectors):
    ortho = []
    for v in vectors:
        w = v[:]
        for u in ortho:
            dot_uw = sum(wi * ui for wi, ui in zip(w, u))
            dot_uu = sum(ui * ui for ui in u)
            proj = dot_uw / dot_uu
            if DEBUG >= 2:
                print(f"🔁 Calculating ortho... ({get_ram_stats()})")
            for i in range(len(w)):
                w[i] -= proj * u[i]
        ortho.append(w)
    
    return ortho

# --- Stream samples ---
def stream_and_process_samples(path):
    with open(path, "rb") as f:  
        raw = b""
        while True:
            ch = f.read(1)
            if not ch:
                break
            if ch == b";":
                if raw:
                    yield float(raw.decode('utf-8'))
                    raw = b""
            elif ch in b"0123456789.-":
                raw += ch
        if raw:
            yield float(raw.decode('utf-8'))


def read_vector(gen, size):
    vec = array.array('f')
    try:
        for _ in range(size):
            vec.append(next(gen))
    except StopIteration:
        pass
    return vec

def get_base_third_vector(base_number):
    gen = stream_and_process_samples(FILE_PATH)

    v1 = read_vector(gen, SAMPLE_SIZE)
    v2 = read_vector(gen, SAMPLE_SIZE)
    v3 = read_vector(gen, SAMPLE_SIZE)

    if DEBUG >= 1:
        print(f"🔁 Generating base {base_number} ... ({get_ram_stats()})")

    if base_number==1:
        return gram_schmidt([v1, v2, v3])[2]
    if base_number==2:
        return gram_schmidt([v2, v3, v1])[2]
    if base_number==3:
        return gram_schmidt([v3, v1, v2])[2]

    raise ValueError("Invalid value of base_number. Must be 1, 2, or 3.")

# --- Resource Monitoring ---
def get_ram_stats():
    gc.collect() 
    return f"RAM Alloc:{gc.mem_alloc()/ 1024 :.2f}KB / Free:{gc.mem_free() / 1024 :.2f}KB"

# --- Main ---
def process():
    print(f"🔁 Starting... ({get_ram_stats()})")
    start_time = time.monotonic()
    base1 = get_base_third_vector(1)
    base2 = get_base_third_vector(2)
    base3 = get_base_third_vector(3)

    norm1 = norm(base1,1)
    norm2 = norm(base2,2)
    norm3 = norm(base3,3)

    print(f"🔁 Reading file {FILE_PATH} with sample size {SAMPLE_SIZE} ... ({get_ram_stats()})")
    gen = stream_and_process_samples(FILE_PATH)

    block_number = 0

    with open(OUTPUT_PATH, "w") as out:
        out.write(f"id_vector,score,clasificación\n")
        while True:
            if DEBUG >= 1:
                print(f"🔁 Processing block {block_number+1}... ({get_ram_stats()})")
            start_block = time.monotonic()
            block = read_vector(gen, SAMPLE_SIZE)
            block_number+=1

            if len(block) < SAMPLE_SIZE:
                break  

            s1 = dot(block, base1) / norm1
            s2 = dot(block, base2) / norm2
            s3 = dot(block, base3) / norm3

            score = (s1 + s2 + s3) / 3.0


            print(f"🔁 Finished block {block_number} in {(time.monotonic()-start_block) * 1000}ms ({get_ram_stats()})")

            if score > CLASSIFICATION_THRESHOLD:
                if DEBUG >= 1:
                    print(f"{block_number},{score},1\n")
                out.write(f"{block_number},{score},1\n")
            else:
                if DEBUG >= 1:
                    print(f"{block_number},{score},0\n")
                out.write(f"{block_number},{score},0\n")

        print(f"✅ Done. Results saved to {OUTPUT_PATH} {(time.monotonic()-start_time)}s ({get_ram_stats()})")
# --- Run ---
try:
    process()
except Exception as e:
    print("❌ Error:", e)