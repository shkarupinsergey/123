import tkinter as tk

WIDTH, HEIGHT = 540, 400
center_x, center_y = -0.6, 0.0
pending = None
BG_COLOR = 'black'
FRACTAL_COLOR = '#a00000'

root = tk.Tk()
root.title('Множество Мандельброта')
root.resizable(False, False)

image = tk.PhotoImage(width=WIDTH, height=HEIGHT)
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG_COLOR, highlightthickness=0, cursor="crosshair")
canvas.pack()
canvas.create_image(0, 0, image=image, anchor='nw')
panel = tk.Frame(root, bd=2, relief="groove")
panel.pack(pady=5)
zoom = tk.IntVar(value=1)
iterations = tk.IntVar(value=70)


def draw():
    global pending
    pending = None
    step = 3.4 / (WIDTH * zoom.get())
    limit = iterations.get()
    colors = ['#000000' if n < 3 else f'#{110 * n // limit:02x}0000'
              for n in range(limit)]

    for py in range(HEIGHT):
        b = center_y + (py - HEIGHT / 2) * step
        line = []
        for px in range(WIDTH):
            a = center_x + (px - WIDTH / 2) * step

            q = (a - 0.25) ** 2 + b ** 2
            if q * (q + a - 0.25) <= 0.25 * b ** 2 or (a + 1) ** 2 + b ** 2 <= 0.0625:
                line.append(FRACTAL_COLOR)
                continue

            x = y = 0.0
            for n in range(limit):
                x, y = x * x - y * y + a, 2 * x * y + b
                if x * x + y * y > 4:
                    line.append(colors[n])
                    break
            else:
                line.append(FRACTAL_COLOR)

        image.put('{' + ' '.join(line) + '}', to=(0, py))


def redraw(*_):
    global pending
    if pending is not None:
        root.after_cancel(pending)
    pending = root.after(200, draw)


def move_center(event):
    global center_x, center_y
    step = 3.4 / (WIDTH * zoom.get())
    center_x += (event.x - WIDTH / 2) * step
    center_y += (event.y - HEIGHT / 2) * step
    redraw()


def reset():
    global center_x, center_y
    center_x, center_y = -0.6, 0.0
    zoom.set(1)
    iterations.set(70)
    redraw()


tk.Scale(panel, from_=1, to=30, variable=zoom, label='Увеличение',
         orient='horizontal', length=185, command=redraw).pack(side='left', padx=5)
tk.Scale(panel, from_=5, to=150, resolution=5, variable=iterations,
         label='Число итераций', orient='horizontal', length=185,
         command=redraw).pack(side='left', padx=5)
tk.Button(panel, text='Сбросить', command=reset).pack(side='left', padx=10)
tk.Label(root, text='ЛКМ - выбрать центр | Клавиша "R" - сбросить').pack(pady=(0, 5))
canvas.bind('<Button-1>', move_center)
root.bind('<r>', lambda event: reset())
root.bind('<R>', lambda event: reset())
root.after(100, draw)
root.mainloop()
