import logging
import re

from lsprotocol import types

from pygls.cli import start_server
from pygls.lsp.server import LanguageServer

server = LanguageServer("csound-lsp", "v1")

@server.feature(
    types.TEXT_DOCUMENT_DOCUMENT_COLOR,
)
def document_color(params: types.CodeActionParams):
    """Return a list of colors declared in the document."""
    items = []
    document_uri = params.text_document.uri
    document = server.workspace.get_text_document(document_uri)

    for linum, line in enumerate(document.lines):
        for match in COLOR.finditer(line.strip()):
            start_char, end_char = match.span()

            # Is this a short form color?
            if (end_char - start_char) == 4:
                color = "".join(c * 2 for c in match.group(1))
                value = int(color, 16)
            else:
                value = int(match.group(1), 16)

            # Split the single color value into a value for each color channel.
            blue = (value & 0xFF) / 0xFF
            green = (value & (0xFF << 8)) / (0xFF << 8)
            red = (value & (0xFF << 16)) / (0xFF << 16)

            items.append(
                types.ColorInformation(
                    color=types.Color(red=red, green=green, blue=blue, alpha=1.0),
                    range=types.Range(
                        start=types.Position(line=linum, character=start_char),
                        end=types.Position(line=linum, character=end_char),
                    ),
                )
            )

    return items


@server.feature(
    types.TEXT_DOCUMENT_COLOR_PRESENTATION,
)
def color_presentation(params: types.ColorPresentationParams):
    """Given a color, instruct the client how to insert the representation of that
    color into the document"""
    color = params.color

    b = int(color.blue * 255)
    g = int(color.green * 255)
    r = int(color.red * 255)

    # Combine each color channel into a single value
    value = (r << 16) | (g << 8) | b
    return [types.ColorPresentation(label=f"#{value:0{6}x}")]

def start():
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    start_server(server)

