import controller_data
from dtm_header_reader import DTMHeaderReader
from frame_scraper import FrameScraper
import os
import pandas as pd
from datasets import load_dataset


def where_to_start_connecting_inputs_to_frames(num_video_frames, num_inputs):
    return num_inputs - (num_video_frames * 2)


def num_frames(dtm_path, video_path):
    if dtm_path is None:
        raise Exception("Need a file path")
    if video_path is None:
        raise Exception("Need a file path")
    with open(dtm_path, "rb") as dtm:
        HR = DTMHeaderReader()
        inputs = HR.get_inputs(dtm)

    FS = FrameScraper()
    num_video_frames = FS.num_frames(video_path)

    where_to_start = where_to_start_connecting_inputs_to_frames(num_video_frames, len(inputs))

    print(f"Number of inputs:                           {len(inputs)}")
    print(f"Number of video frames:                     {num_video_frames}")
    print(f"Where to start connecting inputs to frames: {where_to_start}")
    print("Every frame will have 2 inputs")

    print(inputs[3000])
    #
    # FS.save_frame(video_path, 3000, f"{inputs[where_to_start + 3000]}")

    # FS.specific_frame(video_path, 3000, f"{inputs[where_to_start + 3000]} {inputs[where_to_start + 3001]}")
    file_names = []
    objects_list = []
    filename = os.path.splitext(os.path.basename(video_path))[0]
    for i in range(5):
        name = f"frame{i}_file{filename}"
        FS.save_frame(video_path, i, name)
        file_names.append(name)
        objects_list.append(inputs[where_to_start + (2*i)])

    combined_data = [{"file_name": file_name, **object_data} for file_name, object_data in zip(file_names, objects_list)]

    df = pd.DataFrame(combined_data)

    df.to_csv('metadata.csv', index=False)


def generate_dataset(dtm_path, video_path):
    if dtm_path is None:
        raise Exception("Need a file path")
    if video_path is None:
        raise Exception("Need a file path")
    with open(dtm_path, "rb") as dtm:
        header_reader = DTMHeaderReader()
        inputs = header_reader.get_inputs(dtm)

    frame_scraper = FrameScraper()
    num_video_frames = frame_scraper.num_frames(video_path)

    inputs = controller_data.ControllerDataCondense(inputs, num_video_frames)

    file_names = []
    filename = os.path.splitext(os.path.basename(video_path))[0]
    if not os.path.exists(f"dump\\{filename}"):
        os.makedirs(f"dump\\{filename}")
    for i in range(num_video_frames):
        if i % 1000 == 0:
            print(f"{i}/{num_video_frames} frames saved...")
        name = f"frame{i}_file{filename}"
        frame_scraper.save_frame(video_path, i, filename, name)
        file_names.append(f"{name}.jpg")
    print(f"All done! Saving metadata now.")
    objects_data = [{"file_name": file_name, **vars(obj)} for file_name, obj in zip(file_names, inputs)]
    df = pd.DataFrame(objects_data)

    df.to_csv(f'dump\\{filename}\\metadata.csv', index=False)
    return


def get_raw_data_dirs():
    return [f"raw_data\\{name}" for name in os.listdir("raw_data") if os.path.isdir(os.path.join("raw_data", name))]


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
    with open(dtm_path, "rb") as dtm:
        header_reader = DTMHeaderReader()
        inputs = header_reader.get_inputs(dtm)

    frame_scraper = FrameScraper()
    num_video_frames = frame_scraper.num_frames(video_path)

    inputs = controller_data.ControllerDataCondense(inputs, num_video_frames)

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


def get_aggregated_dataset_from_raw_data(where_save):
    raw_data_dirs = get_raw_data_dirs()
    objects_data = []

    if not os.path.exists(f"dump\\{where_save}"):
        os.makedirs(f"dump\\{where_save}")

    print(f"Amount of video files being scraped: {len(raw_data_dirs)}")
    print(f"Where we're going to save all of this: {where_save}")
    total_frame_count = 0

    for i, video_input_pair_dir in enumerate(raw_data_dirs):
        print(f"Opening {i}/{len(raw_data_dirs)} video files: {video_input_pair_dir}")

        dtm_path, video_path = get_video_dtm_in_dir(video_input_pair_dir)

        with open(dtm_path, "rb") as dtm:
            header_reader = DTMHeaderReader()
            inputs = header_reader.get_inputs(dtm)

        frame_scraper = FrameScraper()
        num_video_frames = frame_scraper.num_frames(video_path)
        total_frame_count += num_video_frames
        inputs = controller_data.ControllerDataCondense(inputs, num_video_frames)

        file_names = []
        filename = os.path.splitext(os.path.basename(video_path))[0]
        if not os.path.exists(f"dump\\{where_save}"):
            os.makedirs(f"dump\\{where_save}")
        for i in range(num_video_frames):
            # if i % 3000 == 0:
            #     print(f"{i}/{num_video_frames} frames saved...")
            name = f"frame{i}_file{filename}"
            frame_scraper.save_frame(video_path, i, where_save, name)
            file_names.append(f"{name}.jpg")

        objects_data.extend([{"file_name": file_name, **vars(obj)} for file_name, obj in zip(file_names, inputs)])
    print(f"Total frames aggregated: {total_frame_count}")
    df = pd.DataFrame(objects_data)

    df.to_csv(f'dump\\{where_save}\\metadata.csv', index=False)


if __name__ == '__main__':
    # video = "C:\\Users\\User\\AppData\\Roaming\\Dolphin Emulator\\Dump\\Frames\\GALE01_2023-10-02_15-51-03_0.avi"
    # dtm = "C:\\Users\\User\\Downloads\\first_tas.dtm"
    #
    video = "C:\\Users\\User\\AppData\\Roaming\\Dolphin Emulator\\Dump\\Frames\\GALE01_2023-12-06_15-39-55_0.avi"
    dtm = "C:\\Users\\User\\Downloads\\dec_6_training.dtm"

    generate_dataset(dtm, video)

    get_aggregated_dataset_from_raw_data("big")
