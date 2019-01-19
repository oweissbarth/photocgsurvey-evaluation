import json
from model import Participant, Response
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from collections import OrderedDict


def video_games(participants):
    answers = {'less then 1h': 0, '1-3h': 0,
               '3-6h': 0, '6-12h': 0, 'more than 12h': 0}
    for p in participants:
        if p.games in answers:
            answers[p.games] += 1

    # fig, ax = plt.subplots()
    # ax.pie(answers.values(), labels=answers.keys())
    # ax.set(title="How much time do you spend per week playing video games?")
    # plt.show()

    return list(answers.keys()), list(answers.values())


def software(participants):
    answers = {"Never": 0, "Once a month": 0,
               "Once a week": 0, "Multiple times a week": 0, "Everyday": 0}
    for p in participants:
        if p.software in answers:
            answers[p.software] += 1

    # fig, ax = plt.subplots()
    # ax.pie(answers.values(), labels=answers.keys())
    # ax.set(title="How often do you use 3D-graphics-software?")
    # plt.show()

    return list(answers.keys()), list(answers.values())


def check_answers(participant, images):
    correct = 0
    counted = 0
    not_counted = 0
    for item in participant.responses:
        if item.question in images:
            if item.answer == images[item.question]["type"]:
                item.correct = True
                correct += 1
                counted += 1
            elif item.answer == "seen":
                item.correct = None
            else:
                item.correct = False
                counted += 1
    if counted == 0:
        participant.accuracy = None
        participant.counted = False
    else:
        participant.accuracy = correct/counted*100
        participant.counted = True


def average_acuracy(participants):
    average = 0
    total = 0
    for p in participants:
        if p.counted:
            average += p.accuracy
            total += 1
    return average/total


def average_accuracy_by_type(participants, images):
    correct_cg = 0
    correct_photo = 0
    total_cg = 0
    total_photo = 0
    for p in participants:
        for r in p.responses:
            if r.correct is None:
                continue
            if images[r.question]["type"] == "cg":
                total_cg += 1
                if r.correct:
                    correct_cg += 1
            else:
                total_photo += 1
                if r.correct:
                    correct_photo += 1

    return correct_cg/total_cg*100, correct_photo/total_photo*100


def accuracy_by_software_usage(participants):
    choices_3d = ["Never", "Once a month",
                  "Once a week", "Multiple times a week", "Everyday"]

    accuracy_by_choice_3d = []
    for c in choices_3d:
        subset = [p for p in participants if p.software == c]
        accuracy_by_choice_3d.append(average_acuracy(subset))

    # fig, ax = plt.subplots()
    # ax.scatter(choices_3d, accuracy_by_choice_3d)
    # ax.set(title="Average accuracy by 3d software usage")
    # plt.show()

    return choices_3d, accuracy_by_choice_3d


def accuracy_by_games_usage(participants):
    choices_games = ['less then 1h', '1-3h', '3-6h', '6-12h', 'more than 12h']

    accuracy_by_choice_games = []
    for c in choices_games:
        subset = filter(lambda p: p.games == c, participants)
        accuracy_by_choice_games.append(average_acuracy(subset))

    # fig, ax = plt.subplots()
    # ax.scatter(choices_games, accuracy_by_choice_games)
    # ax.set(title="Average accuracy by time playing video games")
    # plt.show()

    return choices_games, accuracy_by_choice_games


def accuracy_by_image(participants):
    results = {}
    for p in participants:
        for r in p.responses:
            if r.question in results:
                if r.correct is None:
                    continue
                if r.correct:
                    results[r.question] = {
                        "total": results[r.question]["total"]+1, "correct": results[r.question]["correct"]+1}
                else:
                    results[r.question] = {
                        "total": results[r.question]["total"]+1, "correct": results[r.question]["correct"]}
            else:
                if r.correct is None:
                    continue
                if r.correct:
                    results[r.question] = {"total": 1, "correct": 1}
                else:
                    results[r.question] = {"total": 1, "correct": 0}
    """for (key, value) in results.items():
        path = images[key]["path"]
        img = mpimg.imread(path)
        fig, ax = plt.subplots()
        ax.imshow(img)
        ax.set(title=(value["correct"]/value["total"]*100))
    plt.show()"""
    return OrderedDict(sorted(results.items(), key=(lambda x: (x[1]["correct"]/x[1]["total"])), reverse=True))


def accuracy_by_time(participants):
    time = []
    accuracy = []
    for p in participants:
        correct = 0
        total = 0
        for r in p.responses:
            if r.correct is not None:
                continue
            total += 1
            if r.correct:
                correct += 1


def time_by_image(participants):
    results = {}
    for p in participants:
        for r in p.responses:
            if r.question in results:
                if r.correct is None:
                    continue
                results[r.question] = {
                    "total": results[r.question]["total"]+1, "time": results[r.question]["time"] + r.duration}

            else:
                if r.correct is None:
                    continue
                results[r.question] = {"total": 1, "time": r.duration}
    fig, ax = plt.subplots()

    graph = list(map(lambda v: v[1]["time"]/v[1]["total"], results.items()))
    ax.bar(np.arange(len(results)), graph)
    ax.set(title="Average accuracy by time playing video games")
    plt.show()

    return results


def accuracy_by_time_and_image(participants):
    time = time_by_image(participants)
    accuracy = accuracy_by_image(participants)
    x = []
    y = []
    for k in time.keys():
        x.append(time[k]["time"]/time[k]["total"])
        y.append(accuracy[k]["correct"]/accuracy[k]["total"]*100)

    fig, ax = plt.subplots()
    ax.scatter(x, y)
    ax.set(title="Average accuracy by time and image")
    plt.show()

    return x, y


def accuracy_histogram(participants, buckets=10):
    participants = [p for p in participants if p.counted]
    values = list(map(lambda p: p.accuracy, participants))

    min_val = min(values)
    max_val = max(values)
    step = (max_val - min_val)/buckets

    labels = []
    data = []

    for b in range(buckets):
        step_min = min_val + b*step
        step_max = min_val + (b+1)*step
        labels.append("%.2f-%.2f" % (step_min, step_max))
        count = len([p for p in participants if p.accuracy >=
                     step_min and p.accuracy < step_max])
        data.append(count)

    return labels, data


def accuracy_by_time_and_participant(participants):
    totaltime = []
    accuracy = []
    for p in participants:
        if p.counted:
            time = 0
            accuracy.append(p.accuracy)
            for r in p.responses:
                time += r.duration
            if len(p.responses) == 0:
                totaltime.append(0)
            else:
                totaltime.append(time/len(p.responses))

    # fig, ax = plt.subplots()
    # ax.scatter(totaltime, accuracy)
    # ax.set(title="Average accuracy by time and participant")
    # plt.show()

    return totaltime, accuracy


def load_data():
    with open("responses_17_1_19.json", "r") as fp:
        responses_json = json.load(fp)

    with open("images.json", "r") as fp:
        images_json = json.load(fp)

    participants = []
    for p in responses_json:
        participants.append(Participant.from_json(p))

    images = {}
    for i in images_json:
        images[i["_id"]["$oid"]] = i

    for p in participants:
        check_answers(p, images)

    return participants, images
