import os
from huggingface_hub import snapshot_download

# Change this if you want a different model repo
REPO_ID = "NousResearch/Hermes-2-Pro-Mistral-7B-GGUF"

# Choose which file(s) to download
# Example options:
#   "*Q4_K_M.gguf"
#   "*Q2_K.gguf"
#   "*Q8_0.gguf"
#   "*.gguf" (all - not recommended)
ALLOW_PATTERNS = ["*Q4_K_M.gguf"]

# Target directory
MODELS_DIR = "models"


def main():
    os.makedirs(MODELS_DIR, exist_ok=True)

    print(f"Downloading model from: {REPO_ID}")
    print(f"Saving to: {MODELS_DIR}")
    print(f"Filter: {ALLOW_PATTERNS}")

    snapshot_download(
        repo_id=REPO_ID,
        local_dir=MODELS_DIR,
        allow_patterns=ALLOW_PATTERNS,
        local_dir_use_symlinks=False
    )

    print("\n✅ Download complete!")


if __name__ == "__main__":
    main()