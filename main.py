import asyncio
import sys
import pygame
from game_classes import Game


async def main():
    running = True
    game = Game()
    game.login_screen()

    while running:
        game.screen.fill((0, 0, 0))

        game.draw_windows()

        for event in pygame.event.get():
            game.event_windows(event)
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pass

        pygame.display.flip()
        game.clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    asyncio.run(main())
