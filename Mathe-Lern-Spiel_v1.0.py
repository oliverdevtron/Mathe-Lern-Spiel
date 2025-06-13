# Mathe-Lern-Spiel v1.0
# designed by:
#   ██████  ██       ██  ██    ██ ███████ ██████  
#  ██    ██ ██       ██  ██    ██ ██      ██   ██ 
#  ██    ██ ██       ██  ██    ██ █████   ██████  
#  ██    ██ ██       ██   ██  ██  ██      ██   ██ 
#   ██████  ███████  ██    ████   ███████ ██   ██ 
# (c) 2025 by oliver@devtron.pro
import tkinter as tk
from tkinter import messagebox
import random
import time
import matplotlib.pyplot as plt
import pygame

# Dummy Datenbank für Benutzerprofile
user_profiles = {
    'Mariella': {'score': 0, 'correct': 0, 'wrong': 0, 'rewards': [], 'history': []},
    'Emanuel': {'score': 0, 'correct': 0, 'wrong': 0, 'rewards': [], 'history': []}
}

# Initialize pygame mixer for sound effects
pygame.mixer.init()

class MathLearningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mathe Lernsoftware")
        self.root.geometry("600x600")
        self.current_user = None
        self.current_question = None
        self.difficulty = 'Einfach'
        self.topic = 'Grundrechenarten'
        self.start_time = None
        self.timer_duration = 30
        self.timer_running = False

        self.create_user_selection()

    def create_user_selection(self):
        self.user_label = tk.Label(self.root, text="Wähle dein Profil:", font=("Comic Sans MS", 18), fg="blue")
        self.user_label.pack(pady=20)

        self.user_var = tk.StringVar(value='Mariella')
        self.user_menu = tk.OptionMenu(self.root, self.user_var, *user_profiles.keys(), command=self.set_user)
        self.user_menu.pack(pady=10)

    def set_user(self, value):
        self.current_user = value
        self.init_user_data()
        self.start_learning()

    def init_user_data(self):
        profile = user_profiles[self.current_user]
        self.score = profile['score']
        self.correct_answers = profile['correct']
        self.wrong_answers = profile['wrong']
        self.rewards = profile['rewards']
        self.history = profile['history']

    def start_learning(self):
        self.user_label.pack_forget()
        self.user_menu.pack_forget()

        self.create_widgets()
        self.next_question()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Lerne Mathe!", font=("Comic Sans MS", 24), fg="green")
        self.label.pack(pady=20)

        self.difficulty_label = tk.Label(self.root, text="Schwierigkeitsgrad:", font=("Comic Sans MS", 18), fg="purple")
        self.difficulty_label.pack(pady=10)

        self.difficulty_var = tk.StringVar(value='Einfach')
        self.difficulty_menu = tk.OptionMenu(self.root, self.difficulty_var, 'Einfach', 'Mittel', 'Schwer', command=self.set_difficulty)
        self.difficulty_menu.pack(pady=10)

        self.topic_label = tk.Label(self.root, text="Thema:", font=("Comic Sans MS", 18), fg="purple")
        self.topic_label.pack(pady=10)

        self.topic_var = tk.StringVar(value='Grundrechenarten')
        self.topic_menu = tk.OptionMenu(self.root, self.topic_var, 'Grundrechenarten', 'Geometrie', 'Brüche', 'Dezimalzahlen', command=self.set_topic)
        self.topic_menu.pack(pady=10)

        self.question_label = tk.Label(self.root, text="", font=("Comic Sans MS", 18), fg="black")
        self.question_label.pack(pady=10)

        self.entry = tk.Entry(self.root, font=("Comic Sans MS", 18))
        self.entry.pack(pady=10)

        self.check_button = tk.Button(self.root, text="Prüfen", command=self.check_answer, font=("Comic Sans MS", 18), bg="yellow")
        self.check_button.pack(pady=10)

        self.timer_label = tk.Label(self.root, text=f"Zeit: {self.timer_duration} s", font=("Comic Sans MS", 18), fg="red")
        self.timer_label.pack(pady=20)

        self.score_label = tk.Label(self.root, text=f"Punktzahl: {self.score}", font=("Comic Sans MS", 18), fg="blue")
        self.score_label.pack(pady=20)

        self.stats_label = tk.Label(self.root, text=f"Richtige Antworten: {self.correct_answers} | Falsche Antworten: {self.wrong_answers}", font=("Comic Sans MS", 18), fg="blue")
        self.stats_label.pack(pady=10)

        self.reward_label = tk.Label(self.root, text="Belohnungen: Keine", font=("Comic Sans MS", 18), fg="green")
        self.reward_label.pack(pady=10)

        self.history_button = tk.Button(self.root, text="Lernhistorie anzeigen", command=self.show_history, font=("Comic Sans MS", 18), bg="orange")
        self.history_button.pack(pady=10)

        self.next_button = tk.Button(self.root, text="Nächste Frage", command=self.next_question, font=("Comic Sans MS", 18), bg="yellow")
        self.next_button.pack(pady=10)

        self.graph_button = tk.Button(self.root, text="Grafik anzeigen", command=self.show_graph, font=("Comic Sans MS", 18), bg="orange")
        self.graph_button.pack(pady=10)

        self.game_button = tk.Button(self.root, text="Mathe-Spiel", command=self.start_game, font=("Comic Sans MS", 18), bg="cyan")
        self.game_button.pack(pady=10)

    def set_difficulty(self, value):
        self.difficulty = value
        self.next_question()

    def set_topic(self, value):
        self.topic = value
        self.next_question()

    def start_timer(self):
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if self.timer_running:
            current_time = int(self.timer_label.cget("text").split(": ")[1].split(" ")[0])
            if current_time > 0:
                self.timer_label.config(text=f"Zeit: {current_time - 1} s")
                self.root.after(1000, self.update_timer)
            else:
                self.timer_running = False
                self.check_answer(timeout=True)

    def next_question(self):
        if self.topic == 'Grundrechenarten':
            self.generate_basic_math_question()
        elif self.topic == 'Geometrie':
            self.generate_geometry_question()
        elif self.topic == 'Brüche':
            self.generate_fraction_question()
        elif self.topic == 'Dezimalzahlen':
            self.generate_decimal_question()

        self.start_time = time.time()
        self.entry.delete(0, tk.END)
        self.timer_label.config(text=f"Zeit: {self.timer_duration} s")
        self.start_timer()

    def generate_basic_math_question(self):
        operation = random.choice(['+', '-', '*', '/'])
        if operation == '+':
            a = random.randint(1, 20) if self.difficulty == 'Einfach' else random.randint(20, 50) if self.difficulty == 'Mittel' else random.randint(50, 100)
            b = random.randint(1, 20) if self.difficulty == 'Einfach' else random.randint(20, 50) if self.difficulty == 'Mittel' else random.randint(50, 100)
            self.current_question = (f"{a} + {b}", a + b)
        elif operation == '-':
            a = random.randint(10, 20) if self.difficulty == 'Einfach' else random.randint(30, 50) if self.difficulty == 'Mittel' else random.randint(70, 100)
            b = random.randint(1, 10) if self.difficulty == 'Einfach' else random.randint(10, 30) if self.difficulty == 'Mittel' else random.randint(30, 70)
            self.current_question = (f"{a} - {b}", a - b)
        elif operation == '*':
            a = random.randint(1, 10) if self.difficulty == 'Einfach' else random.randint(10, 20) if self.difficulty == 'Mittel' else random.randint(20, 50)
            b = random.randint(1, 10) if self.difficulty == 'Einfach' else random.randint(10, 20) if self.difficulty == 'Mittel' else random.randint(20, 50)
            self.current_question = (f"{a} * {b}", a * b)
        elif operation == '/':
            b = random.randint(1, 10) if self.difficulty == 'Einfach' else random.randint(2, 10) if self.difficulty == 'Mittel' else random.randint(10, 20)
            a = b * random.randint(1, 10) if self.difficulty == 'Einfach' else b * random.randint(10, 20) if self.difficulty == 'Mittel' else b * random.randint(20, 50)
            self.current_question = (f"{a} / {b}", a / b)

        self.question_label.config(text=self.current_question[0])

    def generate_geometry_question(self):
        if self.difficulty == 'Einfach':
            shapes = [('Quadrat', 4), ('Dreieck', 3), ('Kreis', 1)]
            shape, sides = random.choice(shapes)
            if shape == 'Kreis':
                radius = random.randint(1, 10)
                self.current_question = (f"Fläche eines Kreises mit Radius {radius}", 3.14 * radius * radius)
            else:
                side = random.randint(1, 10)
                self.current_question = (f"Fläche eines {shape} mit Seite {side}", side * side if shape == 'Quadrat' else (side * side) / 2)
        elif self.difficulty == 'Mittel':
            shapes = [('Rechteck', 2)]
            shape, _ = random.choice(shapes)
            length = random.randint(5, 15)
            width = random.randint(5, 15)
            self.current_question = (f"Fläche eines {shape} mit Länge {length} und Breite {width}", length * width)
        elif self.difficulty == 'Schwer':
            self.current_question = ("Umfang eines Kreises mit Durchmesser 10", 3.14 * 10)
        self.question_label.config(text=self.current_question[0])

    def generate_fraction_question(self):
        if self.difficulty == 'Einfach':
            numerator = random.randint(1, 10)
            denominator = random.randint(1, 10)
            self.current_question = (f"Vereinfachung von {numerator}/{denominator}", numerator / denominator)
        elif self.difficulty == 'Mittel':
            numerator1 = random.randint(1, 10)
            denominator1 = random.randint(1, 10)
            numerator2 = random.randint(1, 10)
            denominator2 = random.randint(1, 10)
            self.current_question = (f"{numerator1}/{denominator1} + {numerator2}/{denominator2}", (numerator1 / denominator1) + (numerator2 / denominator2))
        elif self.difficulty == 'Schwer':
            numerator1 = random.randint(1, 10)
            denominator1 = random.randint(1, 10)
            numerator2 = random.randint(1, 10)
            denominator2 = random.randint(1, 10)
            self.current_question = (f"{numerator1}/{denominator1} * {numerator2}/{denominator2}", (numerator1 / denominator1) * (numerator2 / denominator2))
        self.question_label.config(text=self.current_question[0])

    def generate_decimal_question(self):
        if self.difficulty == 'Einfach':
            a = round(random.uniform(1, 10), 1)
            b = round(random.uniform(1, 10), 1)
            self.current_question = (f"{a} + {b}", a + b)
        elif self.difficulty == 'Mittel':
            a = round(random.uniform(10, 20), 1)
            b = round(random.uniform(10, 20), 1)
            self.current_question = (f"{a} - {b}", a - b)
        elif self.difficulty == 'Schwer':
            a = round(random.uniform(20, 50), 2)
            b = round(random.uniform(20, 50), 2)
            self.current_question = (f"{a} * {b}", a * b)
        self.question_label.config(text=self.current_question[0])

    def play_sound(self, sound_file):
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()

    def check_answer(self, timeout=False):
        self.timer_running = False
        elapsed_time = time.time() - self.start_time
        try:
            if timeout:
                self.play_sound('wrong_sound.mp3')
                messagebox.showinfo("Zeit abgelaufen", "Die Zeit ist abgelaufen!")
                self.wrong_answers += 1
            else:
                answer = float(self.entry.get())
                if round(answer, 2) == round(self.current_question[1], 2):
                    self.play_sound('correct_sound.mp3')
                    self.score += 1
                    self.correct_answers += 1
                    messagebox.showinfo("Richtig!", f"Das ist korrekt! Zeit: {elapsed_time:.2f} Sekunden")
                    self.check_rewards()
                else:
                    self.play_sound('wrong_sound.mp3')
                    self.wrong_answers += 1
                    messagebox.showinfo("Falsch", f"Das ist nicht korrekt. Die richtige Antwort ist: {self.current_question[1]}")
            self.history.append((self.current_question[0], round(self.current_question[1], 2), round(answer, 2) if not timeout else 'Zeit abgelaufen', elapsed_time))
        except ValueError:
            self.play_sound('error_sound.mp3')
            messagebox.showwarning("Ungültige Eingabe", "Bitte gib eine gültige Zahl ein.")
        self.update_score()
        self.next_question()

    def check_rewards(self):
        if self.correct_answers == 10:
            self.rewards.append("10 richtige Antworten!")
            messagebox.showinfo("Belohnung!", "Du hast 10 richtige Antworten erreicht!")
        elif self.correct_answers == 20:
            self.rewards.append("20 richtige Antworten!")
            messagebox.showinfo("Belohnung!", "Du hast 20 richtige Antworten erreicht!")
        self.reward_label.config(text=f"Belohnungen: {', '.join(self.rewards) if self.rewards else 'Keine'}")

    def update_score(self):
        self.score_label.config(text=f"Punktzahl: {self.score}")
        self.stats_label.config(text=f"Richtige Antworten: {self.correct_answers} | Falsche Antworten: {self.wrong_answers}")
        self.save_user_data()

    def save_user_data(self):
        profile = user_profiles[self.current_user]
        profile['score'] = self.score
        profile['correct'] = self.correct_answers
        profile['wrong'] = self.wrong_answers
        profile['rewards'] = self.rewards
        profile['history'] = self.history

    def show_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("Lernhistorie")
        history_label = tk.Label(history_window, text="Lernhistorie", font=("Comic Sans MS", 18))
        history_label.pack(pady=10)
        history_text = tk.Text(history_window, wrap=tk.WORD, font=("Comic Sans MS", 14))
        history_text.pack(pady=10, padx=10)
        history_entries = "\n".join([f"Frage: {entry[0]} | Richtige Antwort: {entry[1]} | Deine Antwort: {entry[2]} | Zeit: {entry[3]:.2f}s" for entry in self.history])
        history_text.insert(tk.END, history_entries)
        history_text.config(state=tk.DISABLED)

    def show_graph(self):
        times = [entry[3] for entry in self.history if isinstance(entry[2], (int, float))]
        plt.plot(times)
        plt.xlabel('Fragen')
        plt.ylabel('Zeit (Sekunden)')
        plt.title('Antwortzeiten')
        plt.show()

    def start_game(self):
        game_window = tk.Toplevel(self.root)
        game_window.title("Mathe-Spiel")
        game_label = tk.Label(game_window, text="Willkommen beim Mathe-Spiel!", font=("Comic Sans MS", 24), fg="green")
        game_label.pack(pady=20)

        def check_game_answer():
            try:
                answer = int(game_entry.get())
                if answer == game_a + game_b:
                    self.play_sound('correct_sound.mp3')
                    messagebox.showinfo("Richtig!", "Das ist korrekt!")
                    game_window.destroy()
                else:
                    self.play_sound('wrong_sound.mp3')
                    messagebox.showinfo("Falsch", "Das ist nicht korrekt.")
            except ValueError:
                self.play_sound('error_sound.mp3')
                messagebox.showwarning("Ungültige Eingabe", "Bitte gib eine gültige Zahl ein.")

        game_a = random.randint(1, 10)
        game_b = random.randint(1, 10)
        game_question_label = tk.Label(game_window, text=f"Was ist {game_a} + {game_b}?", font=("Comic Sans MS", 18), fg="black")
        game_question_label.pack(pady=10)

        game_entry = tk.Entry(game_window, font=("Comic Sans MS", 18))
        game_entry.pack(pady=10)

        game_check_button = tk.Button(game_window, text="Prüfen", command=check_game_answer, font=("Comic Sans MS", 18), bg="yellow")
        game_check_button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = MathLearningApp(root)
    root.mainloop()

