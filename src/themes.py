from dataclasses import dataclass


@dataclass
class Theme:
    name: str
    bg: str
    text: str
    secondary_text: str
    button_bg: str
    button_border: str
    button_hover: str
    nav_bg: str
    input_bg: str
    input_text: str


LIGHT = Theme(
    name="Claro",
    bg="#f5f5f5",
    text="#000000",
    secondary_text="#666666",
    button_bg="#ffffff",
    button_border="#dddddd",
    button_hover="#e9e9e9",
    nav_bg="#ffffff",
    input_bg="#ffffff",
    input_text="#000000",
)

DARK = Theme(
    name="Escuro",
    bg="#1e1e1e",
    text="#ffffff",
    secondary_text="#aaaaaa",
    button_bg="#2d2d2d",
    button_border="#444444",
    button_hover="#3d3d3d",
    nav_bg="#252526",
    input_bg="#3c3c3c",
    input_text="#ffffff",
)

SOLARIZED = Theme(
    name="Solarizado",
    bg="#fdf6e3",
    text="#657b83",
    secondary_text="#93a1a1",
    button_bg="#eee8d5",
    button_border="#d5c4a1",
    button_hover="#e9dfc1",
    nav_bg="#eee8d5",
    input_bg="#eee8d5",
    input_text="#657b83",
)

DRACULA = Theme(
    name="Dracula",
    bg="#282a36",
    text="#f8f8f2",
    secondary_text="#6272a4",
    button_bg="#44475a",
    button_border="#6272a4",
    button_hover="#4d4f68",
    nav_bg="#21222c",
    input_bg="#44475a",
    input_text="#f8f8f2",
)

THEMES = {"Claro": LIGHT, "Escuro": DARK, "Solarizado": SOLARIZED, "Dracula": DRACULA}
