# GitHub_sosal

GitHub_sosal GitHub_sosal GitHub_sosal GitHub_sosal GitHub_sosal GitHub_sosal GitHub_sosal GitHub_sosal GitHub_sosal GitHub_sosal GitHub_sosal GitHub_sosal GitHub_sosal GitHub_sosal GitHub_sosal GitHub_sosal GitHub_sosal GitHub_sosal GitHub_sosal GitHub_sosal GitHub_sosal GitHub_sosal GitHub_sosal GitHub_sosal GitHub_sosal GitHub_sosal GitHub_sosal
import random  
  
s = 500  # начальная ставка  
t = True  # цикл игры  
  
while t:  
    a = list(map(int, input('Ваша ставка и число: ').split()))  # ввод ставки и числа  
    r = random.randint(0, 36)  # случайное число  
    print('Выпало число -', r)  
    if r == a:  
        s += a  # выигрыш  
        print(f'Поздравляем! Вы выиграли {a!\nВаше состояние {s} руб.')  
    else:  
        s -= a  # проигрыш  
        print(f'Вы не угадали... Ваше число {a\nВаше состояние {s} руб.')  
    if s <= 0:  
        print(f'У Вас долг {abs(s)} руб.\n\n...надо бы отыграться!')  
    t = False  # конец цикла  