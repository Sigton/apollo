import datetime


class StoryEngine:

    def __init__(self):

        time = datetime.datetime.now()

        self.initial_story = [
            ">>> Apollo 18 Command",
            ">>> System Log",
            ">>> {}-{}-{}T{}:{}:{}".format(time.year, time.month, time.day,
                                           time.hour, time.minute, time.second),
            ">>> Time until lunar interception: 26:40:18",
            ">>> Performing System check...",
            ">>>                      ",
            ">>> All systems functioning.",
            ">>> Scanning surroundings...",
            ">>>                      ",
            ">>> Space debris detected.",
            ">>> Impact imminent: Human action required.",
            ">>> Enter action:",
            "(1) Adjust course to avoid impact.",
            "(2) Increase velocity to outrun debris.",
            "(3) Activate shields.",
            ": ",
            []
        ]

        self.story = self.initial_story
        self.progress = 0

    def switch_story(self, new_story):
        self.story = new_story
        self.progress = 0
