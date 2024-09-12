from datasets import load_dataset
from frame_scraper import FrameScraper


data_dir = FrameScraper.get_project_root_dir()
data_dir = data_dir / "dtm_parser" / "dump" / "balanced"
dataset = load_dataset("imagefolder", data_dir=f"{data_dir}")

print("made it")

dataset.push_to_hub("tomc43841/public_mario_kart_balanced_dataset", private=False)
