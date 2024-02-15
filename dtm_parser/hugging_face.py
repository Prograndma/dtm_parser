from datasets import load_dataset

dataset = load_dataset("imagefolder", data_dir="dump\\balanced")

print("made it")

dataset.push_to_hub("tomc43841/public_smash_balanced_dataset", private=False)