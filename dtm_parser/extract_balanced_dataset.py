import pandas as pd
from controller_data import ControllerData
import cv2
import os


def extract_row_into_objects(row):
    controller_data = ControllerData(Start=row.Start,
                                     A=row.A,
                                     B=row.B,
                                     X=row.X,
                                     Y=row.Y,
                                     Z=row.Z,
                                     DPadUp=row.DPadUp,
                                     DPadDown=row.DPadDown,
                                     DPadLeft=row.DPadLeft,
                                     DPadRight=row.DPadRight,
                                     L=row.L,
                                     R=row.R,
                                     LPressure=row.LPressure,
                                     RPressure=row.RPressure,
                                     XAxis=row.XAxis,
                                     YAxis=row.YAxis,
                                     CXAxis=row.CXAxis,
                                     CYAxis=row.CYAxis)
    return controller_data, row.file_name


def main(where_get, where_save):
    inputs = pd.read_csv(f"{where_get}metadata.csv")

    # interesting_inputs = inputs[inputs.isin([True]).any(axis=1) | inputs.gt(140).any()]
    # print(interesting_inputs)

    controller_datas = []
    image_names = []
    for i, (row_num, row) in enumerate(inputs.iterrows()):
        controller_data, image_file_name = extract_row_into_objects(row)
        if controller_data.is_interesting(threshold=50):
            controller_datas.append(controller_data)
            image_names.append(image_file_name)

    if not os.path.exists(f"{where_save}"):
        os.makedirs(f"{where_save}")

    for i, image_name in enumerate(image_names):
        if i % 10000 == 0:
            print(f"Copying {i}/{len(image_names)} images...")
        image = cv2.imread(f"{where_get}{image_name}")

        if image is not None:
            saved = cv2.imwrite(f"{where_save}{image_name}", image)
            if saved:
                pass
            else:
                print("Failed to copy image!")
        else:
            print("Failed to load image!")

    objects_data = [{"file_name": image_name, **vars(obj)} for image_name, obj in zip(image_names, controller_datas)]
    df = pd.DataFrame(objects_data)

    df.to_csv(f'{where_save}metadata.csv', index=False)

    print(f"Amount of un-interesting rows: {inputs.shape[0] - len(image_names)}")
    print(f"Amount of interesting images : {len(image_names)}")
    print(f"Amount of interesting rows   : {len(controller_datas)}")


if __name__ == "__main__":
    where_get = "dump\\big\\"
    where_save = "dump\\balanced\\"
    main(where_get, where_save)
