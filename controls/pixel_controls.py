import time
import board
import neopixel_spi as neopixel


class PixelControls:

    def __init__(self):
        self.pixels = neopixel.NeoPixel_SPI(board.SPI(), 150)

    def lights(self, state: int):
        """
        Changes the state of the neopixel warning lights.

        :param int state: The new state of the warning lights:
            0: off
            1: solid
            2: Flashing
        """
        if state == 1:
            # Fill all pixels yellow
            print('Turning all pixels on, solid yellow')
            self.pixels.fill((0, 255, 0))
            self.pixels.show()
        elif state == 2:
            # Flash lights
            print('Flashing pixels five times, solid yellow')
            self.pixels.fill((0, 255, 0))

            i = 1
            while i < 5:
                self.pixels.fill((0, 255, 0))
                self.pixels.show()
                time.sleep(1)
                print(f'Flashing x{i}')
                self.pixels.fill(0)
                time.sleep(1)
                i += 1
        else:
            # Turn off lights
            print('Turning all pixels off')
            self.pixels.fill(0)