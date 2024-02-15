import cv2


class FrameScraper:
    def __int__(self):
        pass

    @staticmethod
    def show_frames(input_video_path):
        cap = cv2.VideoCapture(input_video_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                cv2.imshow("frame", frame)
                cv2.waitKey(1)
            else:
                break

        cap.release()
        cv2.destroyAllWindows()

    @staticmethod
    def num_frames(path_to_video):
        cap = cv2.VideoCapture(path_to_video)
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        cap.release()
        return length

    @staticmethod
    def specific_frame(path_to_video, frame_number, name):
        cap = cv2.VideoCapture(path_to_video)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number - 1)
        ret, frame = cap.read()
        if ret:
            cv2.imshow(name, frame)
            cv2.waitKey(-1)

        cap.release()

    @staticmethod
    def save_frame(path_to_video, frame_number, sub_folder, name):
        cap = cv2.VideoCapture(path_to_video)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number - 1)
        ret, frame = cap.read()

        if ret:
            saved = cv2.imwrite(f"C:\\Users\\User\\PycharmProjects\\SMASH_AI\\dtm_parser\\dump\\{sub_folder}\\{name}.jpg", frame)  # save frame as JPEG
            if saved:
                pass
                # print("I Just saved a file!")
            else:
                print("Oh no!")
        cap.release()

    # @staticmethod
    # def save_frame_to_dump(path_to_video, frame_number):
    #     cap = cv2.VideoCapture(path_to_video)
    #     cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number - 1)
    #     ret, frame = cap.read()
    #
    #     if ret:
    #         saved = cv2.imwrite(f"C:\\Users\\User\\PycharmProjects\\SMASH_AI\\dtm_parser\\{frame_number}.jpg", frame)  # save frame as JPEG
    #         if not saved:
    #
    #     cap.release()

    # @staticmethod
    # def save_all_frames(path_to_video):
    #     cap = cv2.VideoCapture(path_to_video)
    #     frame_num = 0
    #     for frame_num in range(FrameScraper.num_frames(path_to_video)):
    #         save_frame_to_dump(path_to_video, frame_num)
    #     while True:
    #         ret, frame = cap.read()
    #         if ret:
    #             saved = cv2.imwrite(f"C:\\Users\\User\\PycharmProjects\\SMASH_AI\\dtm_parser\\dump\\{frame_num}.jpg", frame)  # save frame as JPEG
    #             if saved:
    #                 print("I Just saved a file!")
    #                 frame_num += 1
    #             else:
    #                 print("Oh no!")
    #                 cap.release()
    #                 return
