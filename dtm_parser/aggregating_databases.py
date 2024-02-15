from datasets import load_dataset
import os


def get_database_directories():
    return [f"dump\\{name}" for name in os.listdir("dump") if os.path.isdir(os.path.join("dump", name))]


def aggregate_datasets(dataset_list):
    pass


def main():
    mini_dataset_dirs = get_database_directories()
    datasets = []
    for mini_dataset_dir in mini_dataset_dirs:
        datasets.append(load_dataset("imagefolder", data_dir=mini_dataset_dir))

    aggregated_dataset = aggregate_datasets(datasets)


if __name__ == "__main__":
    main()
