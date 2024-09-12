import cv2
import os
import sys
import inspect
from pathlib import Path


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
        leading = FrameScraper.get_project_root_dir()
        leading = leading / "dtm_parser" / "dump" / sub_folder
        Path(leading).mkdir(parents=True, exist_ok=True)
        leading = leading / name

        if ret:
            saved = cv2.imwrite(f"{leading}.jpg", frame)  # save frame as JPEG
            if saved:
                pass
                # print("I Just saved a file!")
            else:
                print("Oh no!")
        cap.release()

    @staticmethod
    def get_project_root_dir() -> Path:
        """
        Returns the name of the project root directory.

        :return: Project root directory name
        """

        # stack trace history related to the call of this function
        frame_stack = inspect.stack()

        # get info about the module that has invoked this function
        # (index=0 is always this very module, index=1 is fine as long this function is not called by some other
        # function in this module)
        frame_info = frame_stack[1]

        # if there are multiple calls in the stacktrace of this very module, we have to skip those and take the first
        # one which comes from another module
        if frame_info.filename == __file__:
            for frame in frame_stack:
                if frame.filename != __file__:
                    frame_info = frame
                    break

        # path of the module that has invoked this function
        caller_path: str = frame_info.filename

        # absolute path of the module that has invoked this function
        caller_absolute_path: str = os.path.abspath(caller_path)

        # get the top most directory path which contains the invoker module
        paths: [str] = [p for p in sys.path if p in caller_absolute_path]
        paths.sort(key=lambda p: len(p))
        caller_root_path: str = paths[0]

        if not os.path.isabs(caller_path):
            # file name of the invoker module (eg: "mymodule.py")
            caller_module_name: str = Path(caller_path).name

            # this piece represents a sub-path in the project directory
            # (for example: if the root folder is "myproject" and this function has been called from
            # myproject/foo/bar/mymodule.py this will be "foo/bar")
            project_related_folders: str = caller_path.replace(os.sep + caller_module_name, '')

            # fix root path by removing the undesired sub-path
            caller_root_path = caller_root_path.replace(project_related_folders, '')

        return Path(caller_root_path)

    # @staticmethod
    # def save_frame_to_dump(path_to_video, frame_number):
    #     cap = cv2.VideoCapture(path_to_video)
    #     cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number - 1)
    #     ret, frame = cap.read()
    #
    #     if ret:
    #         saved = cv2.imwrite(f"C:\\Users\\User\\PycharmProjects\\dtm_parser\\dtm_parser\\{frame_number}.jpg", frame)  # save frame as JPEG
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
    #             saved = cv2.imwrite(f"C:\\Users\\User\\PycharmProjects\\dtm_parser\\dtm_parser\\dump\\{frame_num}.jpg", frame)  # save frame as JPEG
    #             if saved:
    #                 print("I Just saved a file!")
    #                 frame_num += 1
    #             else:
    #                 print("Oh no!")
    #                 cap.release()
    #                 return
