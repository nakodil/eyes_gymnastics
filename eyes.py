# TODO: диагонали, рикошеты, восьмерка

import tkinter as tk
import math

WINDOW_BG = 'DeepSkyBlue4'
CANVAS_BG = 'DeepSkyBlue4'
FONT_COLOR = 'black'
FONT_NAME = 'Arial'
FONT_SIZE = 60
FIGURE_COLOR = 'ghost white'
FIGURE_SIZE = 100
FPS = 100


class App:
    def __init__(
            self, has_lines: bool = False, duration_sec: int = 120
    ) -> None:
        self.window = tk.Tk()
        self.window.bind('<Escape>', self.quit)
        self.window.attributes('-fullscreen', True)
        self.window['bg'] = WINDOW_BG
        self.width = self.window.winfo_screenwidth()
        self.height = self.window.winfo_screenheight()
        self.canvas = tk.Canvas(
            self.window,
            width=self.width,
            height=self.height,
            bg=CANVAS_BG,
            highlightthickness=0
        )
        self.canvas.pack(expand=True)
        self.canvas.update()
        if has_lines:
            self.draw_lines()
        self.duration_sec = duration_sec
        self.figures = []
        self.schedule()
        self.window.after(duration_sec * 1000, self.quit)
        self.window.after(1, self.update)
        self.window.mainloop()

    def draw_lines(self) -> None:
        self.canvas.create_line(
            0, self.height // 2, self.width, self.height // 2,
        )
        self.canvas.create_line(
            self.width // 2, 0, self.width // 2, self.height,
        )
        self.canvas.create_line(
            0, 0, self.width, self.height
        )
        self.canvas.create_line(
            0, self.height, self.width, 0
        )

    def schedule(self) -> None:
        figures = [
            Figure(self.canvas, FIGURE_SIZE, FIGURE_COLOR),
            FigureVertical(self.canvas, FIGURE_SIZE, FIGURE_COLOR),
            FigureCircular(self.canvas, FIGURE_SIZE, FIGURE_COLOR),
            FigureDiagonalTopLeft(self.canvas, FIGURE_SIZE, FIGURE_COLOR),
            FigureDiagonalTopRight(self.canvas, FIGURE_SIZE, FIGURE_COLOR),
            FigureRectangular(self.canvas, FIGURE_SIZE, FIGURE_COLOR),
            FigureZooom(self.canvas, FIGURE_SIZE, FIGURE_COLOR),
        ]
        time_between_figures_sec = self.duration_sec // len(figures) - 1
        for idx, figure in enumerate(figures):
            self.canvas.after(
                time_between_figures_sec * 1000 * idx, self.next_figure, figure
            )

    def next_figure(self, figure) -> None:
        self.figures = [figure]

    def update(self) -> None:
        self.canvas.delete('figure')
        for figure in self.figures:
            figure.move()
            figure.collide_borders()
            figure.draw()
        self.canvas.after(1000 // FPS, self.update)

    def quit(self, *event: tk.Event) -> None:
        self.window.destroy()

    def show_instructions(self) -> None:
        self.canvas.create_text(
            self.width // 2,
            self.height // 2,
            text='держите голову неподвижно\nна расстоянии вытянутой руки от экрана\nследите глазами за фигурой',
            font=(FONT_NAME, FONT_SIZE),
            fill=FONT_COLOR,
            justify='center'
        )


class Figure:
    def __init__(self, canvas: tk.Canvas, size: int, color: str) -> None:
        self.canvas = canvas
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        self.size = size
        self.x = self.canvas.winfo_width() // 2 - self.size // 2
        self.y = self.canvas.winfo_height() // 2 - self.size // 2
        self.color = color
        self.acceleration = 10
        self.speed_x = 1
        self.speed_y = 0

    def move(self) -> None:
        self.x += self.speed_x * self.acceleration
        self.y += self.speed_y * self.acceleration

    def collide_borders(self):
        if self.x < 0:
            self.x = 0
            self.speed_x *= -1
        elif self.x + self.size > self.canvas_width:
            self.x = self.canvas_width - self.size
            self.speed_x *= -1
        elif self.y < 0:
            self.y = 0
            self.speed_y *= -1
        elif self.y + self.size > self.canvas_height:
            self.y = self.canvas_height - self.size
            self.speed_y *= -1

    def draw(self) -> None:
        self.canvas.create_rectangle(
            self.x,
            self.y,
            self.x + self.size,
            self.y + self.size,
            fill=self.color,
            tag='figure',
            outline=''
        )


class FigureVertical(Figure):
    def __init__(self, canvas: tk.Canvas, size: int, color: str) -> None:
        super().__init__(canvas, size, color)
        self.speed_x = 0
        self.speed_y = 1


class FigureDiagonalTopLeft(Figure):
    def __init__(self, canvas: tk.Canvas, size: int, color: str) -> None:
        super().__init__(canvas, size, color)
        self.x = 0
        self.y = 0
        self.speed_x = (self.canvas_width - self.size) * 0.0005
        self.speed_y = (self.canvas_height - self.size) * 0.0005

    def collide_borders(self):
        if self.y + self.size > self.canvas_height:
            self.speed_x *= -1
            self.speed_y *= -1
        elif self.y < 0:
            self.speed_x *= -1
            self.speed_y *= -1


class FigureDiagonalTopRight(FigureDiagonalTopLeft):
    def __init__(self, canvas: tk.Canvas, size: int, color: str) -> None:
        super().__init__(canvas, size, color)
        self.x = self.canvas_width - self.size
        self.y = 0
        self.speed_x = (self.canvas_width - self.size) * -0.0005
        self.speed_y = (self.canvas_height - self.size) * 0.0005


class FigureRectangular(Figure):
    def __init__(self, canvas: tk.Canvas, size: int, color: str) -> None:
        super().__init__(canvas, size, color)
        self.x = 0
        self.y = 0
        self.speed_x = 1
        self.speed_y = 0

    def collide_borders(self):
        if self.x < 0:
            self.x = 0
            self.speed_x = 0
            self.speed_y = -1
        elif self.x + self.size > self.canvas_width:
            self.x = self.canvas_width - self.size
            self.speed_x = 0
            self.speed_y = 1
        elif self.y < 0:
            self.y = 0
            self.speed_x = 1
            self.speed_y = 0
        elif self.y + self.size > self.canvas_height:
            self.y = self.canvas_height - self.size
            self.speed_x = -1
            self.speed_y = 0


class FigureCircular(Figure):
    def __init__(self, canvas: tk.Canvas, size: int, color: str) -> None:
        super().__init__(canvas, size, color)
        self.y = 0
        self.angle = 0
        self.radius = self.canvas_height // 2 - self.size // 2

    def move(self) -> None:
        self.angle += 0.02
        self.x = self.canvas_width // 2 + self.radius * math.cos(self.angle) - self.size // 2
        self.y = self.canvas_height // 2 + self.radius * math.sin(self.angle) - self.size // 2


class FigureZooom(Figure):
    def __init__(self, canvas: tk.Canvas, size: int, color: str) -> None:
        super().__init__(canvas, size, color)
        self.speed_x = 1
        self.speed_y = 1
        self.zoom_step = 1
        self.size_initial = self.size

    def move(self) -> None:
        self.size += self.zoom_step
        self.x = (self.canvas_width - self.size) // 2
        self.y = (self.canvas_height - self.size) // 2
        if self.size > min((self.canvas_width, self.canvas_height)) * 0.5:
            self.zoom_step *= -1
        if self.size < self.size_initial:
            self.size = self.size_initial
            self.zoom_step *= -1


App(duration_sec=120)
