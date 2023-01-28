import json
import numpy as np
import pandas as pd
from itertools import cycle, islice
import time

# Instances

data = json.load(open('data/activities.json'))
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
hours = 3
index = pd.date_range(start="04:00:00", freq='h', periods=hours).time
file = f'Week_Schedule.xlsx'
df = pd.DataFrame(columns=days, index=index)
clean = df.fillna("free")


def fixed_table():
    """
    Get all the events that occur on a fixed hour.
    :return: Fixed Data Frame
    """


def randomazing_table():
    """
    This method will randomize the selection of tasks for the week free time.
    :return: Randomized Data Frame
    """

    if hours < len(data["random"]):

        for i in range(hours):
            clean.iloc[i] = np.random.choice(data["random"], size=len(data["random"]), replace=False)

        print(clean)
        return clean

    elif hours == len(data["random"]):
        # This cycles through the list of tasks so that every hour has a different tasks.

        clean.iloc[0] = np.random.permutation(data["random"])

        for i in range(1, hours):
            clean.iloc[i] = list(islice(cycle(clean.iloc[0]), i, i + len(data["random"]), 1))

        print(clean)
        return clean

    elif hours > len(data["random"]):

        # If there are 10 hours and 3 tasks, for example, this makes new copies of tasks to fill out the table.

        for i in range(hours):

            new_tasks = data["random"].copy() * (len(data["random"]) // hours)

            for t in np.random.choice(data["random"], size=(len(data["random"]) % hours)):
                # Then only name is randomly picked

                new_tasks.append(t)

            clean.iloc[i] = np.random.permutation(new_tasks)

        print(clean)
        return clean


if __name__ == '__main__':
    fixed_table()
