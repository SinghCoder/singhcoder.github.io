import json
from pprint import pprint

def seconds_to_human_friendly_time_string(seconds):
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds = int(seconds % 60)
    # Handle zero cases
    if hours == 0 and minutes == 0 and seconds == 0:
        return "0 seconds"
    # Handle hours
    if hours > 0:
        return f"{hours} hours and {minutes} minutes and {seconds} seconds"
    # Handle minutes
    if minutes > 0:
        return f"{minutes} minutes and {seconds} seconds"
    # Handle seconds
    if seconds > 0:
        return f"{seconds} seconds"
    return "0 seconds"

with open("fitness_plan_.json", "r") as f:
    data = json.load(f)
    entries = data["exerciseLogEntries"]
    entries = [e for e in entries if e['userId'] == '89760760' and e["exerciseName"] != "Rest"]
    
    """
    Entry sample:
    {
        "tenantId": 1,
        "userId": "89760760",
        "exerciseId": 1555609163,
        "herculesExerciseId": "602621587d678600085608e2",
        "executionType": "TIMED",
        "meta": {
            "weightUnit": "KG",
            "durationUnit": "SECOND",
            "distanceUnit": "KILOMETRE"
        },
        "personalBest": {
            "id": 791910,
            "createdOn": "2023-02-12T08:38:49.000+00:00",
            "lastModifiedOn": "2023-02-12T08:38:49.000+00:00",
            "createdBy": "system",
            "version": 0,
            "tenantId": 1,
            "userId": "89760760",
            "herculesExerciseId": "602621587d678600085608e2",
            "userFitnessLevel": "INTERMEDIATE",
            "duration": 5400,
            "distance": 11.24,
            "fromTime": "2023-02-12T08:38:49Z"
        },
        "previousBest": {
            "duration": 1860,
            "distance": 4.04
        },
        "thumbnailUrl": "hercules/production/assets/movements/images/CROSS_TRAINER_v1631535828209_aa25d179-c9fa-4570-acc7-3d7a489b7ee9.jpg",
        "exerciseName": "Cross Trainer",
        "exerciseType": "DISTANCE",
        "lateral": "BILATERAL",
        "templateLog": {
            "sequence": null,
            "unilateralDirection": null,
            "weight": null,
            "duration": null,
            "count": null,
            "distance": null,
            "value1": "4.04",
            "unit1": "kms",
            "separator": "x",
            "value2": "31",
            "unit2": "mins"
        },
        "fpExecutionLogs": [
            {
                "sequence": null,
                "unilateralDirection": null,
                "weight": null,
                "duration": 1860,
                "count": null,
                "distance": 4.04,
                "value1": "4.04",
                "unit1": "kms",
                "separator": "/",
                "value2": "31",
                "unit2": "mins"
            }
        ]
    }
    """
    # Create a CSV showing off exercise name, type, lateral, personal_best in the format (count * weight kgs) or (distance (kms), duration (seconds)) whichever fields are non-null in personalBest json dict, time when this personal best was achieved, previous_best in the same format, time when this previous best was achieved, and the thumbnailUrl
    import csv
    with open("fitness_plan_.csv", "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile, delimiter="\t")
        csv_writer.writerow(["ExerciseName", "ExerciseType", "Lateral", "PersonalBest", "PersonalBestTime", "PreviousBest", "ThumbnailUrl"])
        for entry in entries:
            exerciseName = entry["exerciseName"]
            exerciseType = entry["exerciseType"]
            lateral = entry["lateral"]
            personalBest = entry.get("personalBest", {})
            personalBestStr = ""
            if len(personalBest) == 0:
                personalBestStr = "No personal best"
            if "duration" in personalBest:
                personalBestStr = f"{seconds_to_human_friendly_time_string(personalBest['duration'])}"
                if "distance" in personalBest:
                    personalBestStr = f"{personalBest['distance']} kms in {personalBestStr}"
            elif "weight" in personalBest:
                personalBestStr = f"{personalBest['count']} * {personalBest['weight']} kgs"
            elif "count" in personalBest:
                personalBestStr = f"{personalBest['count']} reps"
            personalBestTime = ""
            if "fromTime" in personalBest:
                personalBestTime = personalBest["fromTime"]
            previousBest = entry.get("previousBest", {})
            previousBestStr = ""
            if "duration" in previousBest:
                previousBestStr = f"{seconds_to_human_friendly_time_string(previousBest['duration'])}"
                if "distance" in previousBest:
                    previousBestStr = f"{previousBest['distance']} kms in {previousBestStr}"
            elif "weight" in previousBest:
                previousBestStr = f"{previousBest['count']} * {previousBest['weight']} kgs"
            thumbnailUrl = "https://cdn-images.cure.fit/www-curefit-com/image/upload/" + entry["thumbnailUrl"]
            csv_writer.writerow([exerciseName, exerciseType, lateral, personalBestStr, personalBestTime, previousBestStr, thumbnailUrl])