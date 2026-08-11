import PIL.Image as __image
import io as __io
import pygame as __pygame
def pillow_to_pygame(pil_image: __image.Image) -> __pygame.Surface:
    # Change Format To RGBA
    if pil_image.mode not in ("RGB", "RGBA"):
        pil_image = pil_image.convert("RGBA")
    # To Byte Buffer For Pygame
    try:
        # BytesIO -> Avoid Hard Disk/Drive Input/Output
        with __io.BytesIO() as buffer:
            pil_image.save(buffer, format="PNG")
            buffer.seek(0)
            # Load Pygame Surface From Byte Buffer
            pygame_surface = __pygame.image.load(buffer).convert_alpha()
        return pygame_surface
    except Exception as e:
        pass