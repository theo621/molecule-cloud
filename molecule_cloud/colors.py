"""Pastel color palette generation."""

from typing import List, Tuple


def get_pastel_colors() -> List[Tuple[int, int, int]]:
    """Get a palette of pastel colors.

    Returns:
        List of RGB tuples in pastel shades
    """
    return [
        (255, 179, 186),  # Pastel red
        (255, 223, 186),  # Pastel orange
        (255, 250, 200),  # Pastel yellow
        (200, 237, 201),  # Pastel green
        (186, 225, 255),  # Pastel blue
        (220, 198, 255),  # Pastel purple
        (255, 200, 221),  # Pastel pink
        (200, 255, 216),  # Pastel cyan
        (255, 236, 200),  # Pastel peach
        (230, 200, 255),  # Pastel lavender
        (200, 240, 255),  # Pastel sky blue
        (255, 200, 200),  # Pastel rose
        (240, 255, 200),  # Pastel lime
        (200, 220, 255),  # Pastel periwinkle
    ]


def adjust_pastel(color: Tuple[int, int, int], lightness: float = 0.5) -> Tuple[int, int, int]:
    """Adjust color lightness.

    Args:
        color: RGB color tuple
        lightness: Lightness factor (0-1)

    Returns:
        Adjusted RGB tuple
    """
    r, g, b = color
    # Mix towards white
    r = int(r + (255 - r) * (1 - lightness))
    g = int(g + (255 - g) * (1 - lightness))
    b = int(b + (255 - b) * (1 - lightness))
    return (r, g, b)
