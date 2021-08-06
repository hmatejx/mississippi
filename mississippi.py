#!/usr/bin/python

import pygame
from pygame.locals import *
from gtts import gTTS
from tempfile import NamedTemporaryFile
import os
import sys


class smiley():
    """ class that draws the smiley image with a certain configuration """

    def __init__(self, screen):
        self.screen = screen
        self.state = 0

        # bitmaps of 5 distinct simley face states
        self.states = [
                       [[1,1,1,1,1,1,1,1], # state 0
                        [1,0,0,1,1,0,0,1],
                        [1,0,0,1,1,0,0,1],
                        [1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1],
                        [1,0,0,0,0,0,0,1],
                        [1,0,1,1,1,1,0,1],
                        [1,0,0,0,0,0,0,1],
                        [1,1,1,1,1,1,1,1]],

                       [[1,1,1,1,1,1,1,1], # state 1
                        [1,0,0,1,1,0,0,1],
                        [1,0,0,1,1,0,0,1],
                        [1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1],
                        [1,1,0,0,0,0,1,1],
                        [1,1,0,1,1,0,1,1],
                        [1,1,0,0,0,0,1,1],
                        [1,1,1,1,1,1,1,1]],

                       [[1,1,1,1,1,1,1,1], # state 2
                        [1,0,0,1,1,0,0,1],
                        [1,0,0,1,1,0,0,1],
                        [1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1],
                        [1,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,1],
                        [1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1]],

                       [[1,1,1,1,1,1,1,1], # state 3
                        [1,1,1,1,1,1,1,1],
                        [1,0,0,1,1,0,0,1],
                        [1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1],
                        [1,0,0,0,0,0,0,1],
                        [1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1]],

                       [[1,1,1,1,1,1,1,1], # state 4
                        [1,0,0,1,1,0,0,1],
                        [1,0,0,1,1,0,0,1],
                        [1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1],
                        [1,1,0,0,0,0,1,1],
                        [1,0,0,1,1,0,0,1],
                        [1,1,0,0,0,0,1,1],
                        [1,1,1,1,1,1,1,1]]]

        self.num_states = len(self.states)

        self.size = 32
        self.image0 = pygame.Surface((self.size, self.size))
        self.image1 = pygame.Surface((self.size, self.size))
        self.image0.fill((0, 0, 0))
        self.image1.fill((255, 255, 0))

        self.text = ''


    def say(self, char):
        """
          This function maps a character to a smiley face state and
        draws the result.

        The mapping was defined by my son (5 years old at that time),
        so there is no questioning it's validity ;)
        """
        if len(char) == 0:
            self.state = 3
        else:
            c = char.upper()[0]
            if c in ['A','E']:
                self.state = 0
            elif c in ['U','B','S']:
                self.state = 1
            elif c in ['I']:
                self.state = 2
            elif c in ['O','P','R', ]:
                self.state = 4
            else:
                self.state = 3
        self.__draw()


    def set_text(self, text):
        self.text = text


    def __draw(self):
        screen_size = self.screen.get_size()
        background = pygame.Surface(screen_size)
        background = background.convert()
        background.fill((0, 255, 0))
        x0, y0 = background.get_rect().centerx - 4*self.size, 4*self.size
        xoff = x0
        yoff = y0
        for i in range(9):
            for j in range(8):
                if self.states[self.state][i][j] == 1:
                    background.blit(self.image1, (xoff, yoff))
                else:
                    background.blit(self.image0, (xoff, yoff))
                xoff += self.size
            yoff += self.size
            xoff = x0

        for i in range(9):
            xoff = background.get_rect().centerx - 4*self.size + i*self.size
            yoff = 4*self.size
            pygame.draw.line(background, (0, 0, 0), (xoff, yoff), (xoff, yoff + 9*self.size))
        for i in range(10):
            xoff = background.get_rect().centerx - 4*self.size
            yoff = 4*self.size + i*self.size
            pygame.draw.line(background, (0, 0, 0), (xoff, yoff), (xoff + 8*self.size, yoff))

        font = pygame.font.Font('LcdSolid-VPzB.ttf', 110)
        text = font.render(self.text, 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        textpos.centery = background.get_rect().centery + 6*self.size
        background.blit(text, textpos)

        self.screen.blit(background, (0, 0))
        # handle quit requests
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
        pygame.display.flip()


def main():
    # initialize pygame
    pygame.mixer.init(16000)
    pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)
    pygame.mixer.music.set_volume(0.4)
    pygame.init()
    screen = pygame.display.set_mode((1024, 768))

    # initialize the smiley face
    mysmiley = smiley(screen)
    mysmiley.say('_')

    #
    keyword = 'mississippi'

    # countdown from 100
    for i in range(101):

        # call Google Text To Sound service to convert the text to sound
        text = '%s %s' % ((100 - i), keyword)
        tts = gTTS(text = text , lang='en')

        # save to a temporary file
        tmpf = NamedTemporaryFile(mode="w+b", suffix=".mp3", delete=False)
        fname = tmpf.name
        tts.write_to_fp(tmpf)
        tmpf.close()

        # play voice (runs in background)
        pygame.mixer.music.load(fname)
        pygame.mixer.music.play(start=0.25)

        # animate smiley face
        mysmiley.set_text(text)
        for c in '* %s' % keyword:
            mysmiley.say(c)
            pygame.time.delay(int(1200/(len(keyword) + 2)))
        pygame.time.delay(400)

        # stop voice and remove the temporary file
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        os.remove(fname)

    pygame.quit()


if __name__ == '__main__':
    main()
