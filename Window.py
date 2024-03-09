import sdl2.ext

from Renderer import SoftwareRenderer

class WindowProps:
    def __init__(self, title : str, width : int, height : int) -> None:
        self.title = title
        self.width = width
        self.height = height

class Window:
    def __init__(self, props : WindowProps) -> None:
        self.window = sdl2.ext.Window(props.title, size=(props.width, props.height))

        self.renderer = SoftwareRenderer(self.window)