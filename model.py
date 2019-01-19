class Participant:
    def __init__(self, responses, games, software, starttime, endtime):
        self.responses = responses
        self.games = games
        self.software = software
        self.starttime = starttime
        self.endtime = endtime

    @staticmethod
    def from_json(data):
        responses = []
        games = ""
        software = ""
        start = ""
        end = ""
        for (key, value) in data.items():
            if key == "_id":
                continue
            if key == "games":
                games = value
                continue
            if key == "3d-software":
                software = value
                continue
            if key == "time":
                start = value["start"]
                end = value["end"]
                continue
            if isinstance(value, dict):
                responses.append(
                    Response(key, value["result"], value["duration"]))

        return Participant(responses, games, software, start, end)


class Response:
    def __init__(self, question, answer, duration=None):
        self.question = question
        self.answer = answer
        self.duration = duration
        self.correct = None
