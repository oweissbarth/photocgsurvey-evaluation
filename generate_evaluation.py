from jinja2 import Template

import numpy as np
import matplotlib.pyplot as plt


from evaluations import load_data, video_games, software, accuracy_by_software_usage, accuracy_by_games_usage, time_by_image, accuracy_by_time_and_image, accuracy_by_time_and_participant, accuracy_by_image, accuracy_histogram, average_accuracy_by_type


def main():
    participants, images = load_data()

    print("not counted: %d" %
          len(list(filter(lambda p: not p.counted, participants))))

    labels, data = video_games(participants)

    write_evaluation("video_games", labels=labels, data=data)

    labels, data = software(participants)

    write_evaluation("software", labels=labels, data=data)

    results = accuracy_by_image(participants)
    write_evaluation("images", results=results, images=images)

    labels, data = accuracy_histogram(participants)
    write_evaluation("histogram", labels=labels, data=data)

    labels, data = accuracy_by_software_usage(participants)
    write_evaluation("accuracy_by_software_usage", labels=labels, data=data)

    labels, data = accuracy_by_games_usage(participants)
    write_evaluation("accuracy_by_games", labels=labels, data=data)

    accuracy_cg, accuracy_photo = average_accuracy_by_type(
        participants, images)
    write_evaluation("accuracy_by_type", labels=["correct", "incorrect"],
                     accuracy_cg=[accuracy_cg, 100-accuracy_cg], accuracy_photo=[accuracy_photo, 100-accuracy_photo])

    labels, data = accuracy_by_time_and_participant(participants)
    write_evaluation("accuracy_by_time", labels=labels, data=data)

    labels = []
    data = []
    choices_3d = ["Never", "Once a month",
                  "Once a week", "Multiple times a week", "Everyday"]
    choices_games = ['less then 1h', '1-3h', '3-6h', '6-12h', 'more than 12h']

    heat = np.zeros([len(choices_3d), len(choices_games)])

    for p in participants:
        if p.games not in choices_games or p.software not in choices_3d:
            continue
        heat[choices_games.index(p.games), choices_3d.index(p.software)] += 1

    plt.imshow(heat, cmap='hot', interpolation='nearest')
    plt.show()

    cg = 0
    photo = 0
    for k, i in images.items():
        if i["type"] == "cg":
            cg += 1
        else:
            photo += 1

    print(cg, photo)

    # time_by_image(participants)

    # accuracy_by_time_and_image(participants)

    total = 0
    average = 0
    min_val = None
    max_val = None
    for p in participants:
        if p.counted:
            total += 1
            average += p.accuracy
            if max_val is None or p.accuracy > max_val.accuracy:
                max_val = p
            if min_val is None or p.accuracy < min_val.accuracy:
                min_val = p

    print("min: %.2f" % min_val.accuracy)
    print("max: %.2f" % max_val.accuracy)
    print("average: %.2f" % (average/total))
    # for r in max_val.responses:
    # print(r.correct)
    # if r.correct is not None:
    #    print(r.correct)


def write_evaluation(evaluation, **kwargs):
    template = Template(open(evaluation+".template.html", "r").read())
    html = template.render(**kwargs)

    result = open(evaluation+".html", "w")
    result.write(html)
    result.close()


if __name__ == '__main__':
    main()
