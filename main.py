from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import NumericProperty, StringProperty
from datetime import datetime, timedelta

class NoFapTrackerApp(App):
    def build(self):
        return MainScreenManager()

class MainScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.home_screen = HomeScreen(name='home')
        self.add_widget(self.home_screen)
        self.add_widget(CalendarScreen(name='calendar'))
        self.stats_screen = StatsScreen(name='stats', home_screen=self.home_screen)
        self.add_widget(self.stats_screen)

class HomeScreen(Screen):
    streak_days = NumericProperty(0)
    best_streak = NumericProperty(0)
    total_days_logged = NumericProperty(0)
    goal_days = 30  # Set a default goal for 30 days

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Background color
        with self.canvas.before:
            Color(0.16, 0.14, 0.22, 1)  # Dark purple background
            self.rect = RoundedRectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

        # Current Streak Display
        self.streak_label = Label(text=f"Current Streak: {self.streak_days} days", font_size=32, color=(1, 1, 1, 1))
        self.layout.add_widget(self.streak_label)
        
        # Progress Bar
        self.progress_bar = ProgressBar(max=self.goal_days, value=self.streak_days)
        self.layout.add_widget(self.progress_bar)

        # Motivational Quote
        self.quote_label = Label(
            text="\"The journey of a thousand miles begins with a single step.\"",
            font_size=18,
            color=(0.85, 0.65, 0.65, 1),
            italic=True
        )
        self.layout.add_widget(self.quote_label)

        # Buttons
        button_layout = BoxLayout(size_hint=(1, 0.2), spacing=10)
        log_button = Button(text="Log Today", background_color=(0.38, 0.28, 0.67, 1))
        log_button.bind(on_press=self.log_today)
        calendar_button = Button(text="View Calendar", background_color=(0.32, 0.2, 0.51, 1))
        calendar_button.bind(on_press=self.go_to_calendar)
        stats_button = Button(text="View Stats", background_color=(0.38, 0.28, 0.67, 1))
        stats_button.bind(on_press=self.go_to_stats)
        button_layout.add_widget(log_button)
        button_layout.add_widget(calendar_button)
        button_layout.add_widget(stats_button)
        self.layout.add_widget(button_layout)

        # Reset Button
        reset_button = Button(text="Reset Streak", background_color=(0.83, 0.65, 0.65, 1), size_hint=(1, 0.2))
        reset_button.bind(on_press=self.reset_streak)
        self.layout.add_widget(reset_button)

        self.add_widget(self.layout)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def log_today(self, instance):
        self.streak_days += 1
        self.total_days_logged += 1
        if self.streak_days > self.best_streak:
            self.best_streak = self.streak_days
        self.progress_bar.value = self.streak_days
        self.streak_label.text = f"Current Streak: {self.streak_days} days"

    def go_to_calendar(self, instance):
        self.manager.current = 'calendar'

    def go_to_stats(self, instance):
        self.manager.get_screen('stats').update_stats()
        self.manager.current = 'stats'

    def reset_streak(self, instance):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text="Are you sure you want to reset your streak?"))
        button_layout = BoxLayout(size_hint=(1, 0.3))
        yes_button = Button(text="Yes", background_color=(0.83, 0.65, 0.65, 1))
        no_button = Button(text="No", background_color=(0.32, 0.2, 0.51, 1))
        button_layout.add_widget(yes_button)
        button_layout.add_widget(no_button)
        content.add_widget(button_layout)

        popup = Popup(title="Reset Streak", content=content, size_hint=(0.7, 0.4))
        yes_button.bind(on_press=lambda x: self.confirm_reset(popup))
        no_button.bind(on_press=popup.dismiss)
        popup.open()

    def confirm_reset(self, popup):
        self.streak_days = 0
        self.progress_bar.value = self.streak_days
        self.streak_label.text = f"Current Streak: {self.streak_days} days"
        popup.dismiss()

class CalendarScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text="Calendar View", font_size=32))

        # Create a grid layout for the calendar (7 days a week)
        calendar_layout = GridLayout(cols=7, padding=10, spacing=5)
        days_of_week = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        for day in days_of_week:
            calendar_layout.add_widget(Label(text=day, bold=True))

        # Generate the days for the current month
        today = datetime.today()
        first_day_of_month = today.replace(day=1)
        start_day = first_day_of_month.weekday()  # Day of the week (0-6, where Monday is 0)
        start_offset = (start_day + 1) % 7  # Adjust to start on Sunday
        days_in_month = (first_day_of_month.replace(month=first_day_of_month.month % 12 + 1, day=1) - timedelta(days=1)).day

        # Fill in the empty days at the beginning
        for _ in range(start_offset):
            calendar_layout.add_widget(Label(text=""))

        # Fill in the actual days
        for day in range(1, days_in_month + 1):
            btn = Button(text=str(day))
            if day == today.day:
                btn.background_color = (0.38, 0.28, 0.67, 1)  # Highlight today
            calendar_layout.add_widget(btn)

        layout.add_widget(calendar_layout)
        back_button = Button(text="Back", size_hint=(1, 0.2))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'home'

class StatsScreen(Screen):
    def __init__(self, home_screen, **kwargs):
        super().__init__(**kwargs)
        self.home_screen = home_screen
        self.layout = BoxLayout(orientation='vertical', padding=20)
        self.layout.add_widget(Label(text="Statistics", font_size=32))

        # Labels that will be updated dynamically
        self.current_streak_label = Label(text="Current Streak: 0 days")
        self.best_streak_label = Label(text="Best Streak: 0 days")
        self.total_days_label = Label(text="Total Days Logged: 0 days")

        self.layout.add_widget(self.current_streak_label)
        self.layout.add_widget(self.best_streak_label)
        self.layout.add_widget(self.total_days_label)

        back_button = Button(text="Back", size_hint=(1, 0.2))
        back_button.bind(on_press=self.go_back)
        self.layout.add_widget(back_button)
        self.add_widget(self.layout)

    def update_stats(self):
        self.current_streak_label.text = f"Current Streak: {self.home_screen.streak_days} days"
        self.best_streak_label.text = f"Best Streak: {self.home_screen.best_streak} days"
        self.total_days_label.text = f"Total Days Logged: {self.home_screen.total_days_logged} days"

    def go_back(self, instance):
        self.manager.current = 'home'

if __name__ == '__main__':
    NoFapTrackerApp().run()
