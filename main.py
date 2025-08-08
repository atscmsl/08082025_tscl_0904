import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk

class RouletteGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Казино: Рулетка")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # Начальные значения
        self.balance = 1000
        self.current_bet = 0
        self.bet_amount = 10
        self.bets_placed = {}
        
        # Цвета рулетки
        self.roulette_numbers = [
            (0, "green"), (32, "red"), (15, "black"), (19, "red"), (4, "black"), 
            (21, "red"), (2, "black"), (25, "red"), (17, "black"), (34, "red"), 
            (6, "black"), (27, "red"), (13, "black"), (36, "red"), (11, "black"), 
            (30, "red"), (8, "black"), (23, "red"), (10, "black"), (5, "red"), 
            (24, "black"), (16, "red"), (33, "black"), (1, "red"), (20, "black"), 
            (14, "red"), (31, "black"), (9, "red"), (22, "black"), (18, "red"), 
            (29, "black"), (7, "red"), (28, "black"), (12, "red"), (35, "black"), 
            (3, "red"), (26, "black")
        ]
        
        # Создание интерфейса
        self.create_widgets()
        
    def create_widgets(self):
        # Фрейм для рулетки
        self.roulette_frame = tk.Frame(self.root, bg="dark green", bd=5, relief=tk.RAISED)
        self.roulette_frame.place(x=50, y=50, width=500, height=500)
        
        # Изображение рулетки (заглушка)
        try:
            self.roulette_img = Image.open("roulette_wheel.png").resize((400, 400))
            self.roulette_photo = ImageTk.PhotoImage(self.roulette_img)
            self.roulette_label = tk.Label(self.roulette_frame, image=self.roulette_photo)
        except:
            # Если изображение не найдено, создаем простой круг
            self.roulette_label = tk.Label(self.roulette_frame, bg="brown", text="Рулетка", 
                                           font=("Arial", 24), fg="white")
        self.roulette_label.place(x=50, y=50, width=400, height=400)
        
        # Индикатор выигрышного номера
        self.winning_number = tk.Label(self.roulette_frame, text="", font=("Arial", 24), 
                                     bg="dark green", fg="gold")
        self.winning_number.place(x=200, y=20, width=100, height=30)
        
        # Фрейм для ставок
        self.bet_frame = tk.Frame(self.root, bg="gray", bd=5, relief=tk.SUNKEN)
        self.bet_frame.place(x=570, y=50, width=200, height=500)
        
        # Баланс
        self.balance_label = tk.Label(self.bet_frame, text=f"Баланс: ${self.balance}", 
                                    font=("Arial", 14), bg="gray", fg="white")
        self.balance_label.pack(pady=10)
        
        # Ставка
        self.bet_label = tk.Label(self.bet_frame, text=f"Ставка: ${self.bet_amount}", 
                                font=("Arial", 12), bg="gray", fg="white")
        self.bet_label.pack()
        
        # Кнопки изменения ставки
        bet_controls = tk.Frame(self.bet_frame, bg="gray")
        bet_controls.pack(pady=5)
        
        tk.Button(bet_controls, text="-10", command=lambda: self.change_bet(-10)).pack(side=tk.LEFT, padx=5)
        tk.Button(bet_controls, text="-1", command=lambda: self.change_bet(-1)).pack(side=tk.LEFT, padx=5)
        tk.Button(bet_controls, text="+1", command=lambda: self.change_bet(1)).pack(side=tk.LEFT, padx=5)
        tk.Button(bet_controls, text="+10", command=lambda: self.change_bet(10)).pack(side=tk.LEFT, padx=5)
        
        # Типы ставок
        bet_types = tk.Frame(self.bet_frame, bg="gray")
        bet_types.pack(pady=10)
        
        # Ставки на числа
        numbers_frame = tk.LabelFrame(bet_types, text="Числа", bg="gray", fg="white")
        numbers_frame.pack(pady=5)
        
        for i in range(3):
            row = tk.Frame(numbers_frame, bg="gray")
            row.pack()
            for j in range(12):
                num = i*12 + j + 1
                if num <= 36:
                    btn = tk.Button(row, text=str(num), width=3, 
                                   command=lambda n=num: self.place_bet("number", n))
                    btn.pack(side=tk.LEFT, padx=1, pady=1)
        
        # Кнопка для 0
        tk.Button(numbers_frame, text="0", width=3, 
                 command=lambda: self.place_bet("number", 0)).pack(side=tk.LEFT, padx=1, pady=1)
        
        # Ставки на цвета
        colors_frame = tk.LabelFrame(bet_types, text="Цвета", bg="gray", fg="white")
        colors_frame.pack(pady=5)
        
        tk.Button(colors_frame, text="Красное", bg="red", fg="white", 
                 command=lambda: self.place_bet("color", "red")).pack(side=tk.LEFT, padx=5)
        tk.Button(colors_frame, text="Чёрное", bg="black", fg="white", 
                 command=lambda: self.place_bet("color", "black")).pack(side=tk.LEFT, padx=5)
        
        # Чёт/нечёт
        even_odd_frame = tk.LabelFrame(bet_types, text="Чёт/Нечёт", bg="gray", fg="white")
        even_odd_frame.pack(pady=5)
        
        tk.Button(even_odd_frame, text="Чёт", 
                 command=lambda: self.place_bet("even_odd", "even")).pack(side=tk.LEFT, padx=5)
        tk.Button(even_odd_frame, text="Нечёт", 
                 command=lambda: self.place_bet("even_odd", "odd")).pack(side=tk.LEFT, padx=5)
        
        # Кнопка вращения
        self.spin_button = tk.Button(self.bet_frame, text="Крутить рулетку!", font=("Arial", 14), 
                                   bg="red", fg="white", command=self.spin_roulette)
        self.spin_button.pack(pady=20, fill=tk.X)
        
        # Текущие ставки
        self.current_bets_label = tk.Label(self.bet_frame, text="Ставок нет", bg="gray", fg="white")
        self.current_bets_label.pack()
        
    def change_bet(self, amount):
        new_bet = self.bet_amount + amount
        if new_bet >= 1 and new_bet <= self.balance:
            self.bet_amount = new_bet
            self.bet_label.config(text=f"Ставка: ${self.bet_amount}")
    
    def place_bet(self, bet_type, value):
        if self.bet_amount > self.balance:
            messagebox.showwarning("Ошибка", "Недостаточно средств!")
            return
            
        key = f"{bet_type}_{value}"
        if key in self.bets_placed:
            self.bets_placed[key] += self.bet_amount
        else:
            self.bets_placed[key] = self.bet_amount
            
        self.current_bet += self.bet_amount
        self.balance -= self.bet_amount
        self.update_bets_display()
    
    def update_bets_display(self):
        self.balance_label.config(text=f"Баланс: ${self.balance}")
        
        if not self.bets_placed:
            self.current_bets_label.config(text="Ставок нет")
            return
            
        bets_text = "Текущие ставки:\n"
        for bet, amount in self.bets_placed.items():
            bet_type, value = bet.split("_", 1)
            if bet_type == "number":
                bets_text += f"Число {value}: ${amount}\n"
            elif bet_type == "color":
                color = "Красное" if value == "red" else "Чёрное"
                bets_text += f"{color}: ${amount}\n"
            elif bet_type == "even_odd":
                eo = "Чёт" if value == "even" else "Нечёт"
                bets_text += f"{eo}: ${amount}\n"
                
        self.current_bets_label.config(text=bets_text)
    
    def spin_roulette(self):
        if not self.bets_placed:
            messagebox.showwarning("Ошибка", "Сначала сделайте ставку!")
            return
            
        # Анимация вращения (упрощенная)
        self.spin_button.config(state=tk.DISABLED, text="Крутится...")
        self.root.update()
        
        # Имитация вращения
        for _ in range(10):
            num, color = random.choice(self.roulette_numbers)
            self.winning_number.config(text=str(num), fg=color)
            self.root.update()
            self.root.after(100)
        
        # Финальный результат
        winning_num, winning_color = random.choice(self.roulette_numbers)
        self.winning_number.config(text=str(winning_num), fg=winning_color)
        
        # Проверка выигрыша
        winnings = 0
        winning_bets = []
        
        for bet, amount in self.bets_placed.items():
            bet_type, value = bet.split("_", 1)
            
            if bet_type == "number" and int(value) == winning_num:
                win = amount * 36
                winnings += win
                winning_bets.append(f"Число {value}: +${win}")
            elif bet_type == "color" and value == winning_color:
                win = amount * 2
                winnings += win
                color = "Красное" if value == "red" else "Чёрное"
                winning_bets.append(f"{color}: +${win}")
            elif bet_type == "even_odd":
                if (value == "even" and winning_num % 2 == 0 and winning_num != 0) or \
                   (value == "odd" and winning_num % 2 == 1):
                    win = amount * 2
                    winnings += win
                    eo = "Чёт" if value == "even" else "Нечёт"
                    winning_bets.append(f"{eo}: +${win}")
        
        # Обновление баланса
        self.balance += winnings
        self.balance_label.config(text=f"Баланс: ${self.balance}")
        
        # Показать результаты
        result_text = f"Выпало: {winning_num} ({winning_color})\n"
        if winning_bets:
            result_text += "Вы выиграли!\n" + "\n".join(winning_bets)
            result_text += f"\nОбщий выигрыш: ${winnings}"
        else:
            result_text += "Вы проиграли."
        
        messagebox.showinfo("Результат", result_text)
        
        # Сброс ставок
        self.bets_placed = {}
        self.current_bet = 0
        self.update_bets_display()
        self.spin_button.config(state=tk.NORMAL, text="Крутить рулетку!")

if __name__ == "__main__":
    root = tk.Tk()
    game = RouletteGame(root)
    root.mainloop()