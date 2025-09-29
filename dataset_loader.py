# save_as_wsl.py  (run with: python save_as_wsl.py inside WSL)
from datasets import load_dataset
from pathlib import Path

# Root project dir in WSL (Linux path)
ROOT = Path("/home/maaz/companionAI")
DATA_LAKE = ROOT / "data_lake"

# Folders to create
paths = {
    "mentalchat16k": {
        "raw": DATA_LAKE / "mentalchat16k" / "raw",
        "processed": DATA_LAKE / "mentalchat16k" / "processed",
    },
    "pku_saferlhf": {
        "raw": DATA_LAKE / "pku_saferlhf" / "raw",
        "processed": DATA_LAKE / "pku_saferlhf" / "processed",
    },
    "india_resources": {
        "raw": DATA_LAKE / "india_resources" / "raw",
        "processed": DATA_LAKE / "india_resources" / "processed",
    },
    # Add others later: medalpaca, pmc_llama, augments
}

# Create directories
for group in paths.values():
    for p in group.values():
        p.mkdir(parents=True, exist_ok=True)

# --- Download and save: MentalChat16K ---
# Note: Replace with actual dataset id if different on the Hub.
print("Downloading MentalChat16K...")
ds_mc = load_dataset("ShenLab/MentalChat16K")
ds_mc.save_to_disk(str(paths["mentalchat16k"]["raw"]))
print("Saved:", paths["mentalchat16k"]["raw"])

# --- Download and save: PKU-SafeRLHF ---
print("Downloading PKU-SafeRLHF...")
ds_safe = load_dataset("PKU-Alignment/PKU-SafeRLHF", split="train")
ds_safe.save_to_disk(str(paths["pku_saferlhf"]["raw"]))
print("Saved:", paths["pku_saferlhf"]["raw"])

# --- Save India resource placeholders (will fetch HTML separately) ---
(paths["india_resources"]["raw"] / "README.md").write_text(
    "India crisis resources placeholder. See tele-manas.html for official content.\n"
)

print("\nAccess from Windows via UNC:")
print(r"\\wsl.localhost\Ubuntu\home\maaz\companionAI\data_lake")
