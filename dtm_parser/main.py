import controller_data
from dtm_header_reader import DTMHeaderReader
from frame_scraper import FrameScraper
import os
import pandas as pd


def where_to_start_connecting_inputs_to_frames(num_video_frames, num_inputs):
    return num_inputs - (num_video_frames * 2)


def num_frames(dtm_path, video_path):
    if dtm_path is None:
        raise Exception("Need a file path")
    if video_path is None:
        raise Exception("Need a file path")
    with open(dtm_path, "rb") as dtm_f:
        header_reader = DTMHeaderReader()
        inputs = header_reader.get_inputs(dtm_f)

    scraper = FrameScraper()
    num_video_frames = scraper.num_frames(video_path)

    where_to_start = where_to_start_connecting_inputs_to_frames(num_video_frames, len(inputs))

    print(f"Number of inputs:                           {len(inputs)}")
    print(f"Number of video frames:                     {num_video_frames}")
    print(f"Where to start connecting inputs to frames: {where_to_start}")
    print("Every frame will have 2 inputs")

    print(inputs[3000])
    #
    # scraper.save_frame(video_path, 3000, f"{inputs[where_to_start + 3000]}")

    # scraper.specific_frame(video_path, 3000, f"{inputs[where_to_start + 3000]} {inputs[where_to_start + 3001]}")
    file_names = []
    objects_list = []
    filename = os.path.splitext(os.path.basename(video_path))[0]
    for i in range(5):
        name = f"frame{i}_file{filename}"
        scraper.save_frame(video_path, i, name)
        file_names.append(name)
        objects_list.append(inputs[where_to_start + (2*i)])

    comb_data = [{"file_name": file_name, **object_data} for file_name, object_data in zip(file_names, objects_list)]

    df = pd.DataFrame(comb_data)

    df.to_csv('metadata.csv', index=False)


def generate_dataset(dtm_path, video_path):
    if dtm_path is None:
        raise Exception("Need a file path")
    if video_path is None:
        raise Exception("Need a file path")

    filename = os.path.splitext(os.path.basename(video_path))[0]
    objects_data, _ = process_video_and_dtm(dtm_path, video_path, save_location=filename)
    df = pd.DataFrame(objects_data)

    path = FrameScraper.get_project_root_dir()
    path = path / "dtm_parser" / "dump" / filename / "metadata"

    df.to_csv(f'{path}.csv', index=False)
    return


def get_raw_data_dirs():
    path = FrameScraper.get_project_root_dir() / "dtm_parser" / "raw_data"
    return [f"{path / name}" for name in os.listdir("raw_data") if os.path.isdir(os.path.join("raw_data", name))]


def get_video_dtm_in_dir(directory):
    things_in_dir = os.listdir(directory)
    files_in_dir = []
    for thing_in_dir in things_in_dir:
        if os.path.isfile(os.path.join(directory, thing_in_dir)):
            files_in_dir.append(thing_in_dir)
    num_dtm = 0
    num_video = 0
    dtm_file = ""
    video_file = ""
    for file in files_in_dir:
        if file[-4:] == ".dtm":
            num_dtm += 1
            dtm_file = os.path.join(directory, file)

        if file[-4:] == ".avi":
            num_video += 1
            video_file = os.path.join(directory, file)

    if num_dtm != 1:
        raise Exception()

    if num_video != 1:
        raise Exception()

    return dtm_file, video_file


def save_aggregate_frames_return_input_frame_name_pairs(dtm_path, video_path, where_save):
    if dtm_path is None:
        raise Exception("Need a file path")
    if video_path is None:
        raise Exception("Need a file path")
    with open(dtm_path, "rb") as dtm_f:
        header_reader = DTMHeaderReader()
        inputs = header_reader.get_inputs(dtm_f)

    frame_scraper = FrameScraper()
    num_video_frames = frame_scraper.num_frames(video_path)

    inputs = controller_data.controller_data_condense(inputs, num_video_frames)

    file_names = []
    filename = os.path.splitext(os.path.basename(video_path))[0]
    if not os.path.exists(f"dump\\{where_save}"):
        os.makedirs(f"dump\\{where_save}")
    for i in range(num_video_frames):
        # if i % 1000 == 0:
        #     print(f"{i}/{num_video_frames} frames saved...")
        name = f"frame{i}_file{filename}"
        frame_scraper.save_frame(video_path, i, where_save, name)
        file_names.append(f"{name}.jpg")
    return [{"file_name": file_name, **vars(obj)} for file_name, obj in zip(file_names, inputs)]


def process_video_and_dtm(dtm_path, video_path, save_location):
    with open(dtm_path, "rb") as dtm_f:
        header_reader = DTMHeaderReader()
        inputs = header_reader.get_inputs(dtm_f)

    frame_scraper = FrameScraper()
    frame_count = frame_scraper.num_frames(video_path)
    inputs = controller_data.controller_data_condense(inputs, frame_count)

    file_names = []
    filename = os.path.splitext(os.path.basename(video_path))[0]
    path = FrameScraper.get_project_root_dir() / "dump" / save_location
    if not os.path.exists(path):
        os.makedirs(path)
    for i in range(frame_count):
        name = f"frame{i}_file{filename}"
        frame_scraper.save_frame(video_path, i, save_location, name)
        file_names.append(f"{name}.jpg")

    processed_data = [{"file_name": file_name, **vars(obj)} for file_name, obj in zip(file_names, inputs)]
    return processed_data, frame_count


def get_aggregated_dataset_from_raw_data(save_location):
    raw_data_dirs = get_raw_data_dirs()
    objects_data = []
    root_path = FrameScraper.get_project_root_dir() / "dtm_parser"

    if not os.path.exists(root_path / "dump" / save_location):
        os.makedirs(root_path / "dump" / save_location)

    print(f"Amount of video files being scraped: {len(raw_data_dirs)}")
    print(f"Where we're going to save all of this: {save_location}")
    total_frame_count = 0

    for i, video_input_pair_dir in enumerate(raw_data_dirs):
        print(f"Opening {i}/{len(raw_data_dirs)} video files: {video_input_pair_dir}")

        dtm_path, video_path = get_video_dtm_in_dir(video_input_pair_dir)
        processed_data, frames_in_processed_video = process_video_and_dtm(dtm_path, video_path,  save_location)

        total_frame_count += frames_in_processed_video
        objects_data.extend(processed_data)

    print(f"Total frames aggregated: {total_frame_count}")
    df = pd.DataFrame(objects_data)
    df.to_csv(f'{root_path / "dump" / save_location / "metadata"}.csv', index=False)


if __name__ == '__main__':
    # video = "C:\\Users\\User\\AppData\\Roaming\\Dolphin Emulator\\Dump\\Frames\\GALE01_2023-10-02_15-51-03_0.avi"
    # dtm = "C:\\Users\\User\\Downloads\\first_tas.dtm"
    #
    video = "/home/thomas/.var/app/org.DolphinEmu.dolphin-emu/data/dolphin-emu/Dump/Frames/GALE01_2024-09-11_14-06-35_0.avi"
    dtm = "/home/thomas/Downloads/first"

    # generate_dataset(dtm, video)

    get_aggregated_dataset_from_raw_data("big")
