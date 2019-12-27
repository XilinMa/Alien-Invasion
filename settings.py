class Settings:
    """store all settings in alien_invasion"""

    def __init__(self):
        """initialization"""
        # static settings
        # screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # ship speed
        self.ship_limit = 3

        # alien speed
        self.fleet_drop_speed = 10

        # bullet
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

        # dynamic settings
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """initialization reset"""
        self.ship_speed_factor = 30
        self.alien_speed_factor = 3
        self.bullet_speed_factor = 10

        # aliens move direction: right 1, left -1
        self.fleet_direction = 1

        # alien points
        self.alien_points = 50

    def increase_speed(self):
        """speed up"""
        self.ship_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)


