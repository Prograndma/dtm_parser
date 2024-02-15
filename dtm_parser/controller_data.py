from dataclasses import dataclass, fields


@dataclass
class ControllerData:
    Start: bool
    A: bool
    B: bool
    X: bool
    Y: bool
    Z: bool
    DPadUp: bool
    DPadDown: bool
    DPadLeft: bool
    DPadRight: bool
    L: bool
    R: bool
    LPressure: int
    RPressure: int
    XAxis: int
    YAxis: int
    CXAxis: int
    CYAxis: int

    def __str__(self):
        strung = ""
        for field in fields(self):
            strung += f"{field.name}: {int(getattr(self, field.name))}, "
        strings = [f"{int(getattr(self, field.name))}" for field in fields(self)]
        return "_".join(strings)

    def any_true(self):
        return (self.Start or
                self.A or
                self.B or
                self.X or
                self.Y or
                self.Z or
                self.DPadUp or
                self.DPadDown or
                self.DPadLeft or
                self.DPadRight or
                self.L or
                self.R)

    def any_threshold_away_from_baseline(self, threshold):
        return (self.LPressure >= threshold or
                self.RPressure >= threshold or
                abs(self.XAxis - 127.5) >= threshold or
                abs(self.YAxis - 127.5) >= threshold or
                abs(self.CXAxis - 127.5) >= threshold or
                abs(self.CYAxis - 127.5) >= threshold)

    def is_interesting(self, threshold):
        return self.any_true() or self.any_threshold_away_from_baseline(threshold)


def ControllerDataCondense(controller_data_list, desired_amount):
    # print(f"LENGTH OF INPUTS: {len(controller_data_list)}")
    # print(f"DESIRED AMOUNT: {desired_amount}")
    condensed_controllers = [None for _ in range(desired_amount)]
    ratio = len(controller_data_list) / desired_amount
    # print(f"RATIO: {ratio}")
    for i in range(desired_amount):
        from_index = int(i * ratio)
        to_index = int((i + 1) * ratio)
        # print(to_index-from_index, sep=" ")
        if to_index >= len(controller_data_list):
            to_index = len(controller_data_list) - 1
        condensed_controllers[i] = _condenseControllerList(controller_data_list[from_index:to_index])
    # print(f"LENGTH OF MAX_POOLED CONTROLLER INPUTS: {len(condensed_controllers)}")
    return condensed_controllers


def _condenseControllerList(controllers):
    if len(controllers) == 0:
        return ControllerData(False, False, False, False, False, False, False, False, False, False, False, False, 0, 0, 127, 127, 127, 127)
    if len(controllers) == 1:
        return controllers[0]
    if len(controllers) == 2:
        return _controllereDataCondenseTwo(controllers[0], controllers[1])
    if len(controllers) == 3:
        return _controllerDataCondenseThree(controllers[0], controllers[1], controllers[2])

    controller = _controllereDataCondenseTwo(controllers[0], controllers[1])
    new_controllers = controllers[2:] + [controller]

    return _condenseControllerList(new_controllers)


def _controllereDataCondenseTwo(controller_data_one, controller_data_two):
    start = controller_data_one.Start or controller_data_two.Start
    a = controller_data_one.A or controller_data_two.A
    b = controller_data_one.B or controller_data_two.B
    x = controller_data_one.X or controller_data_two.X
    y = controller_data_one.Y or controller_data_two.Y
    z = controller_data_one.Z or controller_data_two.Z
    d_pad_up = controller_data_one.DPadUp or controller_data_two.DPadUp
    d_pad_down = controller_data_one.DPadDown or controller_data_two.DPadDown
    d_pad_left = controller_data_one.DPadLeft or controller_data_two.DPadLeft
    d_pad_right = controller_data_one.DPadRight or controller_data_two.DPadRight
    l = controller_data_one.L or controller_data_two.L
    r = controller_data_one.R or controller_data_two.R

    l_pressure = max(controller_data_one.LPressure, controller_data_two.LPressure)
    r_pressure = max(controller_data_one.RPressure, controller_data_two.RPressure)
    x_axis = _biggestDifferenceFromCenter(controller_data_one.XAxis, controller_data_two.XAxis)
    y_axis = _biggestDifferenceFromCenter(controller_data_one.YAxis, controller_data_two.YAxis)
    c_x_axis = _biggestDifferenceFromCenter(controller_data_one.CXAxis, controller_data_two.CXAxis)
    c_y_axis = _biggestDifferenceFromCenter(controller_data_one.CYAxis, controller_data_two.CYAxis)

    condensed = ControllerData(Start=start, A=a, B=b, X=x, Y=y, Z=z, DPadUp=d_pad_up, DPadDown=d_pad_down,
                               DPadLeft=d_pad_left, DPadRight=d_pad_right, L=l, R=r, LPressure=l_pressure,
                               RPressure=r_pressure, XAxis=x_axis, YAxis=y_axis, CXAxis=c_x_axis, CYAxis=c_y_axis)
    return condensed


def _biggestDifferenceFromCenter(num_one, num_two):
    abs_max = max(abs(num_one - 127.5), abs(num_two - 127.5))
    if abs_max == abs(num_one - 127.5):
        return num_one
    return num_two


def _controllerDataCondenseThree(controller_data_one, controller_data_two, controller_data_three):
    return _controllereDataCondenseTwo(_controllereDataCondenseTwo(controller_data_one, controller_data_two), controller_data_three)