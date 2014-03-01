# plot stars on screen
# plot planets on screen - sun, moon, mercury, venus, mars, jupiter, saturn

import pygame
from pygame.locals import *
import math
import ephem, ephem.stars

def getxy(alt, azi): # alt, az in radians
# thanks to John at Wobbleworks for the algorithm
    r90 = math.radians(90) # 90 degrees in radians
    r = (r90 - alt)/r90
    x = r * math.sin(azi)
    y = r * math.cos(azi)
    x = int(160 - x * 120) # flip E/W, scale to radius, center on plot
    y = int(120 - y * 120) # scale to radius, center on plot
    return (x,y)

class plotStars():

  def __init__(self, screen, obs, sun):
    self.screen = screen
    self.obs = obs
    self.sun = sun

#    stars = ['Polaris','Sirius','Canopus','Arcturus','Vega','Capella','Rigel','Procyon','Achernar','Betelgeuse','Agena',
#      'Altair','Aldebaran','Spica','Antares','Pollux','Fomalhaut','Mimosa','Deneb','Regulus','Adara','Castor','Shaula',
#      'Bellatrix','Elnath','Alnilam','Alnair','Alnitak','Alioth','Kaus Australis','Dubhe','Wezen','Alcaid','Menkalinan',
#      'Alhena','Peacock','Mirzam','Alphard','Hamal','Algieba','Nunki','Sirrah','Mirach','Saiph','Kochab','Rasalhague',
#      'Algol','Almach','Denebola','Naos','Alphecca','Mizar','Sadr','Schedar','Etamin','Mintaka','Caph','Merak','Izar',
#      'Enif','Phecda','Scheat','Alderamin','Markab','Menkar','Arneb','Gienah Corvi','Unukalhai','Tarazed','Cebalrai',
#      'Rasalgethi','Nihal','Nihal','Algenib','Alcyone','Vindemiatrix','Sadalmelik','Zaurak','Minkar','Albereo',
#      'Alfirk','Sulafat','Megrez','Sheliak','Atlas','Thuban','Alshain','Electra','Maia','Arkab Prior','Rukbat','Alcor',
#      'Merope','Arkab Posterior','Taygeta']

    for star in ephem.stars.db.split("\n"):
        name = star.split(',')[0]
        if len(name)>0:
            self.plotStar(name)

# plot 5 circles to test plot
#    pygame.draw.circle(screen, (0,255,0), getxy(math.radians(90), math.radians(0)), 5, 1) # center
#    pygame.draw.circle(screen, (255,0,0), getxy(math.radians(45), math.radians(0)), 5, 1) # red N
#    pygame.draw.circle(screen, (0,255,0), getxy(math.radians(45), math.radians(90)), 5, 1) # green E
#    pygame.draw.circle(screen, (0,0,255), getxy(math.radians(45), math.radians(180)), 5, 1) # blue S
#    pygame.draw.circle(screen, (255,255,0), getxy(math.radians(45), math.radians(270)), 5, 1) # yellow W


  def plotStar(self, name):
    star = ephem.star(name)
    star.compute(self.obs)
    if star.alt > 0:
      pygame.draw.circle(self.screen, (255,255,255), getxy(star.alt, star.az), 1, 1)


class plotPlanets():

  def __init__(self, screen, obs, sun):
    self.screen = screen
    self.obs = obs
    self.sun = sun
    self.pline = 235
    self.pFont = pygame.font.SysFont('Arial', 16, bold=True)

    self.plotPlanet(ephem.Saturn(), (255,128,255), 3)
    self.plotPlanet(ephem.Jupiter(),(255,255,128), 3)
    self.plotPlanet(ephem.Mars(),  (255,0,0), 3)
    self.plotPlanet(ephem.Venus(), (255,255,255), 3)
    self.plotPlanet(ephem.Mercury(), (128,255,255), 3)

    moon = ephem.Moon()
    moon.compute(obs)
    if (moon.alt>0):
      pygame.draw.circle(self.screen, (255,255,255), getxy(moon.alt, moon.az), 5, 0)
      txt = self.pFont.render('Moon', 1, (255,255,255))
      self.pline -= 15
      self.screen.blit(txt, (1,self.pline))

    if (sun.alt>0):
      pygame.draw.circle(self.screen, (255,255,0), getxy(sun.alt, sun.az), 5, 0)
      txt = self.pFont.render('Sun', 1, (255,255,0))
      self.pline -= 15
      self.screen.blit(txt, (1, self.pline))


  def plotPlanet(self, planet, color, size):
    planet.compute(self.obs)
#    print "{} alt: {} az:{}".format(planet.name, math.degrees(planet.alt), math.degrees(planet.az))
    if (planet.alt>0):
      pygame.draw.circle(self.screen, color, getxy(planet.alt, planet.az), size, 0)
      txt = self.pFont.render(planet.name, 1, color, (0,0,0))
      self.pline -= 15
      self.screen.blit(txt, (1, self.pline))

