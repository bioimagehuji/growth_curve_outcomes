import os

import pandas as pd
import numpy as np

import math
from dataclasses import dataclass, field

import matplotlib.pyplot as plt

MINUTES_PER_HOUR = 60

SAMPLES_PER_HOUR = 3
MINUTES_PER_SAMPLE = MINUTES_PER_HOUR // SAMPLES_PER_HOUR
INTEGRAL_HOURS = (10, 15, 20)
LAG_THRESHHOLD = 0.115
ROLLING_WINDOW = 4

IMAGES_DIR = "images"


class Convert:
    @staticmethod
    def hours_to_index(hours: float):
        return math.floor(hours * SAMPLES_PER_HOUR)

    @staticmethod
    def index_to_hours(index: int):
        return index / SAMPLES_PER_HOUR

    @staticmethod
    def mins_to_index(mins: int):
        return math.floor(mins / MINUTES_PER_SAMPLE)

    @staticmethod
    def index_to_mins(index: int):
        return index * MINUTES_PER_SAMPLE


def cached_attribute():
    return field(init=False, repr=False, hash=False, compare=False)


@dataclass
class Repetition:
    name: str
    values: np.ndarray

    derivative: np.ndarray = cached_attribute()
    derivative_rolling_average: np.ndarray = cached_attribute()
    lag_index: int = cached_attribute()
    max_rate_index: int = cached_attribute()
    cumulative_sum: np.ndarray = cached_attribute()

    def __post_init__(self):
        self.derivative = np.diff(self.values)
        self.derivative_rolling_average = np.convolve(
            self.derivative, np.ones(ROLLING_WINDOW) / ROLLING_WINDOW, mode="valid"
        )
        possible_lag_indices = np.where(self.values > LAG_THRESHHOLD)[0]
        self.lag_index = possible_lag_indices[-np.argmax(np.diff(possible_lag_indices)[::-1])] - 1
        self.max_rate_index = np.argmax(self.derivative_rolling_average)
        self.cumulative_sum = np.cumsum(self.values - LAG_THRESHHOLD)

    def data(self):
        return (
            *(p.strip() for p in self.name.split("-")),
            len(self.values) * MINUTES_PER_SAMPLE,
            Convert.index_to_mins(self.lag_index),
            Convert.index_to_mins(self.max_rate_index),
            self.values[self.max_rate_index],
            self.derivative_rolling_average[self.max_rate_index],
            *(self.cumulative_sum[Convert.hours_to_index(h)] for h in INTEGRAL_HOURS),
        )

    def plot(self):
        try:
            plt.figure()

            plt.title(self.name)
            plt.plot(np.arange(len(self.values)) * MINUTES_PER_SAMPLE, self.values)

            plt.xlabel("Time [Minutes]")
            plt.ylabel("OD")

            plt.axhline(LAG_THRESHHOLD, color="red")

            plt.plot(
                Convert.index_to_mins(self.lag_index),
                self.values[self.lag_index],
                marker="o",
                markeredgecolor="green",
                markerfacecolor="green",
            )
            plt.plot(
                Convert.index_to_mins(self.max_rate_index),
                self.values[self.max_rate_index],
                marker="o",
                markeredgecolor="purple",
                markerfacecolor="purple",
            )

            plt.ylim((0, 1))
            if not os.path.isdir(IMAGES_DIR):
                os.mkdir(IMAGES_DIR)
            plt.savefig(os.path.join(IMAGES_DIR, f"{self.name}.png"))

        finally:
            plt.close()


def extract():

    df = pd.read_csv("AVERAGES.csv")

    for col_name in df.columns[1:]:
        yield Repetition(col_name, np.asarray(df[col_name]))


def main():
    columns = (
        "REP",
        "GROUP",
        "TOTAL_TIME",
        "LAG_MINS",
        "MAX_RATE_MINS",
        "VALUE_AT_MAX_RATE",
        "MAX_RATE",
        *(f"AUC_{hours}H" for hours in INTEGRAL_HOURS),
    )
    data = []

    for rep in extract():

        data.append(dict(zip(columns, rep.data())))
        rep.plot()

        print(f"completed [{rep.name}].")

    pd.DataFrame(data).to_excel("OUT.xlsx")


if __name__ == "__main__":
    main()
