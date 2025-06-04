import pygame

class LevelManager:
    def OnConstruct(self): pass
    def OnStart(self): pass
    def OnTick(self): pass
    def OnBotAITick(self): pass
    def OnEnd(self): pass

LevelManagerObject = LevelManager()

pygame.init()

infoObject = pygame.display.Info()
x = int(infoObject.current_w * 0.9)
y = int(infoObject.current_h * 0.8)
screen = pygame.display.set_mode((x, y))

def run():
    LevelManagerObject.OnConstruct()
    clock = pygame.time.Clock()
    running = True
    dt = 0
    frame = 0
    backgroundColor = (51, 52, 70)
    LevelManagerObject.OnStart()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(backgroundColor)
        LevelManagerObject.OnTick()
        pygame.display.flip()

        dt = clock.tick(60) / 1000
        frame += 1

        if frame == 15:
            LevelManagerObject.OnBotAITick()
            frame = 0

    LevelManagerObject.OnEnd()
    pygame.quit()
