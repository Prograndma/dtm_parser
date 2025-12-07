from datasets import load_dataset
from frame_scraper import FrameScraper
from my_secrets import HF_TOKEN


def push_dataset(balanced, number):
    data_dir = FrameScraper.get_project_root_dir()

    if balanced:
        ds_type = "balanced"
        data_dir = data_dir / "dtm_parser" / "dump" / f"{number}_balanced"
    else:
        ds_type = "full"
        data_dir = data_dir / "dtm_parser" / "dump" / number


    dataset = load_dataset(f"{data_dir}")

    print("made it")

    dataset.push_to_hub(f"tomc43841/public_smash_{ds_type}_dataset_{number}", private=False, token=HF_TOKEN)


# push_dataset(True, "01")
# push_dataset(False, "01")

# push_dataset(True, "02")
# push_dataset(False, "02")

# push_dataset(True, "03")
# push_dataset(False, "03")

# push_dataset(True, "04")
# push_dataset(False, "04")
#
# push_dataset(True, "05")
# push_dataset(False, "05")

push_dataset(True, "06")
push_dataset(False, "06")

push_dataset(True, "07")
push_dataset(False, "07")
