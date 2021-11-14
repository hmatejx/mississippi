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

        self.text2show = ''
        self.tmpfile = None


    def mime_letter(self, char):
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


    def __settext2show(self, text):
        """
        This function sets the current text input to the class
        """
        self.text2show = text


    def __draw(self):
        """
        This function draws the yellow smipley face according
        to the current state.
        """
		# gets the current screen size
        screen_size = self.screen.get_size()
		# fills the background green
        background = pygame.Surface(screen_size)
        background = background.convert()
        background.fill((0, 255, 0))
		# gets the center position of the screen
        x0, y0 = background.get_rect().centerx - 4*self.size, 4*self.size
        xoff = x0
        yoff = y0

		# paints the squares according to the state bitmap (1 = yellow, 0 = black)
        for i in range(9):
            for j in range(8):
                if self.states[self.state][i][j] == 1:
                    background.blit(self.image1, (xoff, yoff))
                else:
                    background.blit(self.image0, (xoff, yoff))
                xoff += self.size
            yoff += self.size
            xoff = x0

		# creates the black grid lines around the squares
        for i in range(9):
            xoff = background.get_rect().centerx - 4*self.size + i*self.size
            yoff = 4*self.size
            pygame.draw.line(background, (0, 0, 0), (xoff, yoff), (xoff, yoff + 9*self.size))
        for i in range(10):
            xoff = background.get_rect().centerx - 4*self.size
            yoff = 4*self.size + i*self.size
            pygame.draw.line(background, (0, 0, 0), (xoff, yoff), (xoff + 8*self.size, yoff))

		# render the text
        font = pygame.font.Font(None, 192)
        text = font.render(self.text2show, 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        textpos.centery = background.get_rect().centery + 6*self.size

		# blit everything to the screen
        background.blit(text, textpos)
        self.screen.blit(background, (0, 0))

        # handle quit requests
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
        pygame.display.flip()


    def mime(self, text2show, text2mime):
        """
        This function takes a text input and uses the mime_letter function
        mime the word
        """
        self.__settext2show(text2show)
        for c in '* %s' % text2mime:
            self.mime_letter(c)
            pygame.time.delay(int(1200/(len(text2mime) + 2)))
        pygame.time.delay(400)


    def voice(self, text2voice):
        """
        This function takes a text input, converts it to an mp3 using
        Google's text2speach service, and plays it
        """
        # stop previous voice and clean-up
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        if self.tmpfile is not None:
            os.remove(self.tmpfile)

        # call Google Text To Sound service to convert the text to sound
        tts = gTTS(text = text2voice , lang='en')

        # save to a temporary file
        tmpf = NamedTemporaryFile(mode="w+b", suffix=".mp3", delete=False)
        self.tmpfile = tmpf.name
        tts.write_to_fp(tmpf)
        tmpf.close()

        # play voice (runs in background)
        pygame.mixer.music.load(self.tmpfile)
        pygame.mixer.music.play(start=0.25)
        return


def main():

    keyword = 'mississippi'

    # initialize pygame
    pygame.mixer.init(16000)
    pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)
    pygame.mixer.music.set_volume(0.4)
    pygame.init()
    screen = pygame.display.set_mode((1024, 768))

    # initialize the smiley face
    mysmiley = smiley(screen)
    mysmiley.mime_letter('_')

    # countdown from 100
    for i in range(101):
        text = '%s %s' % ((100 - i), keyword)
        mysmiley.voice(text)
        mysmiley.mime(text, '* %s' % keyword)

    pygame.quit()


if __name__ == '__main__':
    main()
