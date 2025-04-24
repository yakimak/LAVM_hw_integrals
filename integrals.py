import numpy as np
import time
import tkinter as tk
from tkinter import ttk
import math

def integrate_rectangles_mid(func, a, b, n):
    dx = (b - a) / n
    integral = 0.0
    for i in range(n):
        integral += func(a + (i + 0.5) * dx)
    return integral * dx

def integrate_trapezoid(func, a, b, n):
    dx = (b - a) / n
    integral = 0.5 * (func(a) + func(b))
    for i in range(1, n):
        integral += func(a + i * dx)
    return integral * dx

def integrate_monte_carlo(func, a, b, n):
    x_random = np.random.uniform(a, b, n)
    y_random = func(x_random)
    integral = (b - a) * np.mean(y_random)
    return integral

def integrate_simpson(func, a, b, n):
    if n % 2 != 0:
        n += 1  

    dx = (b - a) / n
    integral = func(a) + func(b)
    for i in range(1, n):
        if i % 2 == 0:
            integral += 2 * func(a + i * dx)
        else:
            integral += 4 * func(a + i * dx)
    return integral * dx / 3

def F1(x): return x**2 - 10*x + 35
def F2(x): return np.sin(x)
def F3(x): return np.exp(x)
def F4(x): return 2**x

a, b, n = 0.5, 20.5, 10

exact_values = {
    F1: ((b**3)/3 - 5*(b**2) + 35*b) - ((a**3)/3 - 5*(a**2) + 35*a),
    F2: (-math.cos(b)) - (-math.cos(a)),
    F3: math.exp(b) - math.exp(a),
    F4: (2**b - 2**a) / math.log(2) }

def compare_integration_methods(func, a, b, n, exact_value=None):
    methods = [
        ("Средние прямоугольники", integrate_rectangles_mid),
        ("Метод трапеций", integrate_trapezoid),
        ("Метод Симпсона", integrate_simpson),
        ("Монте-Карло", integrate_monte_carlo) ]
    
    results = []
    
    for name, method in methods:
        start_time = time.time()
        integral = method(func, a, b, n)
        execution_time = time.time() - start_time
        
        error = None
        if exact_value is not None:
            error = abs(integral - exact_value)
        
        results.append({
            'Метод': name,
            'Результат': integral,
            'Время (с)': execution_time,
            'Ошибка': error if error is not None else 'N/A' })
    
    return results

def show_results_table(func, a, b, n, exact_value=None):
    results = compare_integration_methods(func, a, b, n, exact_value)
    
    root = tk.Tk()
    root.title("Сравнение методов интегрирования")
    
    tree = ttk.Treeview(root, columns=('Метод', 'Результат', 'Время (с)', 'Ошибка'), show='headings')
    tree.heading('Метод', text='Метод')
    tree.heading('Результат', text='Результат')
    tree.heading('Время (с)', text='Время (с)')
    tree.heading('Ошибка', text='Ошибка')
    
    tree.column('Метод', width=200)
    tree.column('Результат', width=150)
    tree.column('Время (с)', width=100)
    tree.column('Ошибка', width=100)
    
    for result in results:
        tree.insert('', 'end', values=(
            result['Метод'],
            f"{result['Результат']:.6f}",
            f"{result['Время (с)']:.6f}",
            f"{result['Ошибка']:.6f}" if isinstance(result['Ошибка'], float) else result['Ошибка'] ))
    
    tree.pack(expand=True, fill='both')
    
    params_label = tk.Label(root, text=f"Функция: {func.__name__}, Интервал: [{a}, {b}], Разбиений: {n}")
    params_label.pack()
    
    root.mainloop()

show_results_table(F1, a, b, n, exact_values[F1])
show_results_table(F2, a, b, n, exact_values[F2])
show_results_table(F3, a, b, n, exact_values[F3])
show_results_table(F4, a, b, n, exact_values[F4])
