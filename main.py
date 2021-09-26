import pygame
import random
import time

def main():
    pygame.init()
    
    white = (255, 255, 255)
    dark = (24, 24, 24)
    red = (242, 90, 90)
    green = (110, 242, 90)
    orange = (242, 161, 90)

    width, height = 600, 400

    gameDisplay = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Snake")

    icon = pygame.image.load("./assets/icon.png")
    pygame.display.set_icon(icon)

    clock = pygame.time.Clock()

    snakeSize = 10
    snakeSpeed = 15

    mainMessageFont = pygame.font.Font("./assets/calibri-regular.ttf", 30)
    secondaryMessageFont = pygame.font.Font("./assets/calibri-regular.ttf", 15)
    scoreFont = pygame.font.Font("./assets/calibri-regular.ttf", 20)

    runGame(gameDisplay, clock, width, height, snakeSize, snakeSpeed, dark, orange, white, green, red, scoreFont, mainMessageFont, secondaryMessageFont)

def printScore(gameDisplay, score, scoreFont, colour):
    text = scoreFont.render("Score: " + str(score), True, colour)
    gameDisplay.blit(text, [0, 0])

def drawSnake(gameDisplay, snakeSize, snakePixels, colour):
    for pixel in snakePixels:
        pygame.draw.rect(gameDisplay, colour, [pixel[0], pixel[1], snakeSize, snakeSize])

def runGame(gameDisplay, clock, width, height, snakeSize, snakeSpeed, fillColour, targetColour, snakeColour, scoreColour, gameOverColour, scoreFont, mainMessageFont, secondaryMessageFont):
    gameOver = False
    gameClose = False

    x = round(width/2)
    y = round(height/2)
    xSpeed, ySpeed = 0, 0
    snakePixels = []
    snakeLength = 1
    targetX = round(random.randrange(0, width-snakeSize)/10.0)*10.0
    targetY = round(random.randrange(0, height-snakeSize)/10.0)*10.0
    escapePressTime = 0
    escapePressTimeInterval = 0.2

    while not gameClose:
        while gameOver:
            gameDisplay.fill(fillColour)
            gameOverMessage = mainMessageFont.render("Game Over!", True, gameOverColour)
            infoMessage = secondaryMessageFont.render("Press 'R', space, or click your mouse to restart, or press escape to quit.", True, gameOverColour)
            mainMessageRect = gameOverMessage.get_rect()
            infoMessageRect = infoMessage.get_rect()
            gameDisplay.blit(gameOverMessage, [(width-mainMessageRect.width)/2, (height-mainMessageRect.height)/2])
            gameDisplay.blit(infoMessage, [((width-infoMessageRect.width)/2), (height/2+mainMessageRect.height)])
            printScore(gameDisplay, snakeLength-1, scoreFont, scoreColour)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameClose = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    key = event.key
                    if key == pygame.K_ESCAPE:
                        gameClose = True
                        gameOver = False
                    if key == pygame.K_r or key == pygame.K_SPACE:
                        gameClose = False
                        gameOver = False
                        runGame(gameDisplay, clock, width, height, snakeSize, snakeSpeed, fillColour, targetColour, snakeColour, scoreColour, gameOverColour, scoreFont, mainMessageFont, secondaryMessageFont)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    gameClose = False
                    gameOver = False
                    runGame(gameDisplay, clock, width, height, snakeSize, snakeSpeed, fillColour, targetColour, snakeColour, scoreColour, gameOverColour, scoreFont, mainMessageFont, secondaryMessageFont)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameClose = True
            if event.type == pygame.KEYDOWN:
                key = event.key
                if key == pygame.K_ESCAPE:
                    if time.time() - escapePressTime <= escapePressTimeInterval:
                        gameClose = True
                    else:
                        escapePressTime = time.time()
                if (key == pygame.K_LEFT or key == pygame.K_a) and xSpeed == 0:
                    xSpeed = -snakeSize
                    ySpeed = 0
                if (key == pygame.K_RIGHT or key == pygame.K_d) and xSpeed == 0:
                    xSpeed = snakeSize
                    ySpeed = 0
                if (key == pygame.K_UP or key == pygame.K_w) and ySpeed == 0:
                    xSpeed = 0
                    ySpeed = -snakeSize
                if (key == pygame.K_DOWN or key == pygame.K_s) and ySpeed == 0:
                    xSpeed = 0
                    ySpeed = snakeSize
        
        if x >= width or x < 0 or y >= height or y < 0:
            gameOver = True
        
        x += xSpeed
        y += ySpeed
        
        gameDisplay.fill(fillColour)
        pygame.draw.rect(gameDisplay, targetColour, [targetX, targetY, snakeSize, snakeSize])

        snakePixels.append([x, y])
        if(len(snakePixels) > snakeLength):
            del snakePixels[0]
        
        for pixel in snakePixels[:-1]:
            if pixel == [x, y]:
                gameOver = True

        drawSnake(gameDisplay, snakeSize, snakePixels, snakeColour)
        printScore(gameDisplay, snakeLength-1, scoreFont, scoreColour)

        pygame.display.update()

        if x == targetX and y == targetY:
            targetX = round(random.randrange(0, width-snakeSize)/10.0)*10.0
            targetY = round(random.randrange(0, height-snakeSize)/10.0)*10.0
            snakeLength += 1

        clock.tick(snakeSpeed)
    
    pygame.quit()
    quit()

if __name__ == "__main__":
    main()