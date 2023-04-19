import json
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from itertools import cycle, islice
import time

# Instances
data = json.load(open('activities.json'))
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
hours = 18
index = pd.date_range(start="05:00:00", freq='H', periods=hours).time
file = f'Week_Schedule.xlsx'
df = pd.DataFrame(index=index, columns=days)
clean_df = df.fillna("free")

class schedule:
    def getting_fixed():
        """
        Format All the Fixed Activities
        """
        for day, activities in data["fixed"][0]["day"].items():
            if activities:  # check if there are any fixed activities for the day
                for activity in activities:
                    task = activity["activity"]
                    start = datetime.strptime(activity["start_time"], "%H:%M:%S").time()
                    duration = datetime.strptime(activity["duration"], '%H:%M:%S').time()
                    duration_total = (duration.hour * 3600 + duration.minute * 60 + duration.second)-1
                    end = (datetime.combine(datetime.today(), start) + timedelta(seconds=duration_total)).time()

                    start_hour = (datetime.combine(datetime.today(), start) - datetime.combine(datetime.today(),
                                                                                               datetime.min.time())).seconds // 3600
                    end_hour = (datetime.combine(datetime.today(), end) - datetime.combine(datetime.today(),
                                                                                           datetime.min.time())).seconds // 3600 - 1
                    clean_df.loc[start:end, day] = task
            else:
                clean_df[day] = "free"  # set the entire column to "free" when there are no fixed activities for the day

        pd.set_option('display.max_rows', None)  # to show all rows
        pd.set_option('display.max_columns', None)  # to show all columns
        pd.set_option('display.width', 1000)  # to set the width of the output
        pd.set_option('display.max_colwidth', None)  # to show the full contents of each cell

        # print(clean_df)
        return clean_df

    @staticmethod
    def finished_schedule():
        """
        Fill the Free Slots with Random Activities
        """
        schedule.getting_fixed()
        print()
        random_activities = data["random"]
        free_slots = clean_df[clean_df == "free"].stack().reset_index()
        free_slots = free_slots.rename(columns={"level_0": "time", "level_1": "day"})

        for _, slot in free_slots.iterrows():

            # Choose a random activity from the random_activities

            activity = np.random.choice(random_activities)
            duration = datetime.strptime(activity["duration"], '%H:%M:%S').time()
            duration_total = (duration.hour * 3600 + duration.minute * 60 + duration.second)-1
            start = slot["time"]

            end = (datetime.combine(datetime.today(), start) + timedelta(seconds=duration_total)).time()
            day = slot["day"]
            clean_df.loc[start:end, day] = activity["activity"]

            # If we run out of activities, start again from the beginning
            if len(random_activities) == 0:
                random_activities = data["random"]

            pd.set_option('display.max_rows', None)  # to show all rows
            pd.set_option('display.max_columns', None)  # to show all columns
            pd.set_option('display.width', 1000)  # to set the width of the output
            pd.set_option('display.max_colwidth', None)  # to show the full contents of each cell

        print(clean_df)
        return clean_df

    def export_excel():
        print("Exporting Weekly Schedule!")
        #str_list = list(filter(None, []))
        data_writer = pd.ExcelWriter("atividades_semanais.xlsx")
        data_frame = pd.DataFrame(clean_df)
        data_frame.to_excel(data_writer, sheet_name="matheus", index=True)
        print("Weekly Schedule Done!")
        data_writer.close()

if __name__ == '__main__':
    schedule.finished_schedule()
    schedule.export_excel()