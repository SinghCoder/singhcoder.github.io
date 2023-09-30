import csv
import json
from datetime import datetime, timedelta

import requests

# Replace <SECRET> with your actual secret token
headers = {
    "accept": "application/json",
    "cookie": "<SECRET>", # get from the cult website, any curl call, get the value of header `Cookie`...
    "clientversion": "10.08",
    "connection": "Keep-Alive",
    "content-type": "application/json; charset=utf-8"
}

start_date_str = "2022-04-25"
end_date_str = "2023-08-04"
current_date = datetime.strptime(start_date_str, "%Y-%m-%d")

csv_filename = f"fitness_report.csv"
with open(csv_filename, "w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile, delimiter="\t")
    csv_writer.writerow(["StartDate", "EndDate", "ClassesAttended", "CaloriesBurnt", "ExercisesDone", "FocusedOn", "NotFocusedOn", "Summary"])
    while current_date <= datetime.strptime(end_date_str, "%Y-%m-%d"):
        current_date_str = current_date.strftime("%Y-%m-%d")
        this_week_end_date = current_date + timedelta(days=6)
        this_week_end_date_str = this_week_end_date.strftime("%Y-%m-%d")

        url = f"https://www.cult.fit/api/cult/fitnessReport?reportType=WEEKLY&startDate={current_date_str}"
        response = requests.get(url, headers=headers)
        data = response.json()

        try:
            widgets = data["widgets"]
            classMissedWidgets = [w for w in widgets if w["widgetType"] == "CLASS_MISSED_WIDGET"]
            classMissedWidget = classMissedWidgets[0] if len(classMissedWidgets) > 0 else None
            if classMissedWidget:
                csv_writer.writerow([current_date_str, this_week_end_date_str, 0, 0, "", "", "", classMissedWidget["title"]["value"]])
                print(f"Processed week {current_date_str} to {this_week_end_date_str}")
                current_date += timedelta(days=7)
                continue
            fitnessReportSummary = [w for w in widgets if w["widgetType"] == "FITNESS_REPORT_SUMMARY_CARD_WIDGET"][0]
            metricWidget = [w for w in widgets if w["widgetType"] == "REPORT_METRIC_DETAIL_WIDGET"][0]
            tagViewWidgets = [w for w in widgets if w["widgetType"] == "TAG_VIEW_WIDGET"]
            exercisesDoneWidgets = [w for w in tagViewWidgets if "header" not in w]
            exercisesDoneWidget = exercisesDoneWidgets[0] if len(exercisesDoneWidgets) > 0 else None
            youFocusedOnWidgets = [w for w in tagViewWidgets if "header" in w and w["header"] == "YOU FOCUSSED ON"]
            youFocusedOnWidget = youFocusedOnWidgets[0] if len(youFocusedOnWidgets) > 0 else None
            start_date = fitnessReportSummary["startDate"]
            end_date = fitnessReportSummary["endDate"]
            classes_attended = metricWidget["metricSection"]["metricDisplayValue"]
            calories_burnt = fitnessReportSummary["caloriesBurnt"]

            exercises_done = ""
            if exercisesDoneWidget:
                exercises_done = "\n".join(tag["title"] + "(" + tag["value"] + ")" for tag in exercisesDoneWidget["tags"] if not tag["disabled"])
            focused_on = ""
            not_focused_on = ""
            summary = ""
            if youFocusedOnWidget:
                focused_on = "\n".join([tag["title"] for tag in youFocusedOnWidget["tags"] if not tag["disabled"]])
                not_focused_on = "\n".join([tag["title"] for tag in youFocusedOnWidget["tags"] if tag["disabled"]])
                summary = youFocusedOnWidget["footer"]["dataText"]
            csv_writer.writerow([start_date, end_date, classes_attended, calories_burnt, exercises_done, focused_on, not_focused_on, summary])
            print(f"Processed week {start_date} to {end_date}")
            # Move to the next week
            current_date += timedelta(days=7)
        except Exception as e:
            print(f"Error processing week {current_date_str} to {this_week_end_date_str}")
            print(f"data json = {json.dumps(data, indent=4)}")
            raise e


print(f"CSV file '{csv_filename}' created successfully.")