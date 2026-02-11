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
    button_text_hover: str
    nav_bg: str
    input_bg: str
    input_text: str
    # Tab States
    tab_active_bg: str
    tab_active_text: str
    tab_inactive_bg: str
    tab_inactive_text: str
    tab_hover_bg: str
    tab_hover_text: str
    # Font Settings
    font_family: str


LIGHT = Theme(
    name="Claro",
    bg="#f5f5f5",
    text="#000000",
    secondary_text="#666666",
    button_bg="#ffffff",
    button_border="#dddddd",
    button_hover="#e9e9e9",
    button_text_hover="#000000",
    nav_bg="#ffffff",
    input_bg="#ffffff",
    input_text="#000000",
    tab_active_bg="#f5f5f5",
    tab_active_text="#000000",
    tab_inactive_bg="#e1e1e1",
    tab_inactive_text="#666666",
    tab_hover_bg="#ebebeb",
    tab_hover_text="#333333",
    font_family="Segoe UI",
)

DARK = Theme(
    name="Escuro",
    bg="#1e1e1e",
    text="#ffffff",
    secondary_text="#aaaaaa",
    button_bg="#2d2d2d",
    button_border="#444444",
    button_hover="#3d3d3d",
    button_text_hover="#ffffff",
    nav_bg="#252526",
    input_bg="#3c3c3c",
    input_text="#ffffff",
    tab_active_bg="#1e1e1e",
    tab_active_text="#ffffff",
    tab_inactive_bg="#333333",
    tab_inactive_text="#888888",
    tab_hover_bg="#444444",
    tab_hover_text="#cccccc",
    font_family="Segoe UI",
)

SOLARIZED = Theme(
    name="Solarizado",
    bg="#fdf6e3",
    text="#657b83",
    secondary_text="#93a1a1",
    button_bg="#eee8d5",
    button_border="#d5c4a1",
    button_hover="#e9dfc1",
    button_text_hover="#586e75",
    nav_bg="#eee8d5",
    input_bg="#eee8d5",
    input_text="#657b83",
    tab_active_bg="#fdf6e3",
    tab_active_text="#657b83",
    tab_inactive_bg="#eee8d5",
    tab_inactive_text="#93a1a1",
    tab_hover_bg="#e9dfc1",
    tab_hover_text="#586e75",
    font_family="Ubuntu",
)

DRACULA = Theme(
    name="Dracula",
    bg="#282a36",
    text="#f8f8f2",
    secondary_text="#6272a4",
    button_bg="#44475a",
    button_border="#6272a4",
    button_hover="#4d4f68",
    button_text_hover="#ffffff",
    nav_bg="#21222c",
    input_bg="#44475a",
    input_text="#f8f8f2",
    tab_active_bg="#282a36",
    tab_active_text="#f8f8f2",
    tab_inactive_bg="#44475a",
    tab_inactive_text="#6272a4",
    tab_hover_bg="#4d4f68",
    tab_hover_text="#f8f8f2",
    font_family="Monospace",
)

BAGUS = Theme(
    name="Bagus",
    bg="#161616",
    text="#741516",
    secondary_text="#ff1616",
    button_bg="#ff1616",
    button_border="#741516",
    button_hover="#161616",
    button_text_hover="#ff1616",
    nav_bg="#161616",
    input_bg="#161616",
    input_text="#ff1616",
    tab_active_bg="#ff1616",
    tab_active_text="#161616",
    tab_inactive_bg="#161616",
    tab_inactive_text="#ff1616",
    tab_hover_bg="#741516",
    tab_hover_text="#161616",
    font_family="Monospace",
)

THEMES = {
    "Claro": LIGHT,
    "Escuro": DARK,
    "Solarizado": SOLARIZED,
    "Dracula": DRACULA,
    "Bagus": BAGUS,
}
