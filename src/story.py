import datetime


class StoryEngine:

    def __init__(self):

        time = datetime.datetime.now()

        self.story1 = [
            ">>> Course adjusted.",
            ">>> Burning thrusters...",
            ">>>                     ",
            ">>> Space debris avoided.",
            ">>> Correcting course to original destination...",
            ">>>                     ",
            ">>> Course corrected.",
            ">>> Performing systems analysis...",
            ">>> Warning: Space dust present in air filter.",
            ">>> Vent filter?",
            "(1) Yes",
            "(2) No",
            "(3) Shut off filter",
            ": ",
            []
        ]

        self.story2 = [
            ">>> Increasing velocity.",
            ">>> Burning thrusters...",
            ">>>                     ",
            ">>> Escaped debris field.",
            ">>> Shutting off thrusters...",
            ">>>       ",
            ">>> ERROR: THRUSTER VALVE JAMMED",
            ">>> WARNING: VELOCITY APPROACHING MAX SAFE LIMIT",
            ">>> Human action required.",
            ">>> Enter action:",
            "(1) Jettison thruster.",
            "(2) Flood thruster with coolant.",
            "(3) Attempt to recover navigational control.",
            ": ",
            []
        ]

        self.story3 = [
            ">>> Activating shields...",
            ">>>          ",
            ">>> Shields activated.",
            ">>> Prepare for impact.",
            "!self.create_debris(650, -75)",
            ">>> Shields at 81%",
            "!self.create_debris(750, -75)",
            ">>> Shields at 64%",
            "!self.create_debris(720, -75)",
            ">>> Shields at 49%",
            "!self.create_debris(680, -75)",
            ">>> Shields at 36%",
            "!self.create_debris(700, -75)",
            ">>> Shields at 25%",
            "!self.create_debris(660, -75)",
            ">>> Debris field cleared.",
            ">>> Evaluating damage...",
            ">>>                     ",
            ">>> Evaluation complete. Show report?",
            "(1) Yes.",
            "(2) No.",
            "(3) Only the important bits.",
            ": ",
            []
        ]

        self.initial_story = [
            ">>> Apollo 18 Command",
            ">>> System Log",
            ">>> {}-{}-{}T{}:{}:{}".format(time.year, time.month, time.day,
                                           time.hour, time.minute, time.second),
            ">>> Time until lunar interception: 26:40:18",
            ">>> Performing System check...",
            ">>>                      ",
            ">>> All systems functioning.",
            ">>> Scanning surrounding environment...",
            ">>>                      ",
            ">>> Space debris detected.",
            ">>> Impact imminent: Human action required.",
            ">>> Enter action:",
            "(1) Adjust course to avoid impact.",
            "(2) Increase velocity to outrun debris.",
            "(3) Activate shields.",
            ": ",
            [self.story1, self.story2, self.story3]
        ]

        self.story = self.initial_story
        self.progress = 14

    def switch_story(self, new_story):
        self.story = new_story
        self.progress = 0
