import logging
import random
import time
from turnsapi.models.game_models import Game

weather_map = [
    'NEVER_WILL_HAPPEN',    
    'Completely Arid',
    'Arid',
    'Arid',
    'Arid',
    'Arid',
    'Fair',
    'Fair',
    'Fair',
    'Fair',
    'Fair',
    'Moist',
    'Moist',
    'Moist',
    'Moist',
    'Rainy',
    'Rainy',
    'Rainy',
    'Rainy',
    'Monsoon',
    'Bounteous Rainfall'
]

SERF_EATS = 5
SERF_PER_LAND = 500
GOLD_PER_FOOD = 10
GRANARY_STORAGE = 10000

class GameLogic:
    '''The game logic'''

    def __init__(self, game):
        self.lands = game.lands
        self.food = game.food
        self.serfs = game.serfs
        self.gold = game.gold
        self.granaries = game.granaries
        random.seed(time.time())
        pass

    def sell_food(self):
        if self.food > 5000:
            selling = self.food - 5000
            moneyback = (selling*GOLD_PER_FOOD)
            self.gold += moneyback
            self.food -= selling
            logging.info("You sold {} food for {} gold.  {} food remains.".format(selling, moneyback, self.food))
        else:
            logging.info("You can only sell if you have more than 5000 food.")


    def run_turn(self):
        self.check_growth()
        self.check_consumption()
        self.check_population()
        self.check_spoilage()
        logging.info("You have {} lands, {} serfs, {} gold, and {} food.".format(self.lands, self.serfs, self.gold, self.food))
    
    def check_consumption(self):
        consumption = (self.serfs*SERF_EATS)
        logging.info("Your serfs have eaten {} food.".format(consumption))
        self.food -= consumption
        if self.food < 0:
            self.food = 0
            logging.info("Widespread famine has culled your population.")
            self.serfs = int(self.serfs * .15)
            

    def check_spoilage(self):
        granary_max = self.granaries*GRANARY_STORAGE
        if self.food >= granary_max:
            loss = self.food - granary_max
            self.food = granary_max
            logging.info("Unfortunately, {} food has spoiled.  Build more granaries!".format(loss))

    def check_population(self):
        
        if self.serfs == 0:
            logging.info("Game over.")
            raise Exception("All is lost.")

        max_serfs = SERF_PER_LAND * self.lands


        if ((self.serfs >= 2) and (self.serfs <= max_serfs)):
            if self.food >= 5:
                logging.info("Your harvests have caused our serfs to have children")
                self.serfs += int((self.serfs/2))
            else:
                logging.info("You barely had enough food to feed our population, sire.")
        elif (self.serfs == 1):
            logging.info("Your kingdom consists of only you.  Without a miracle, you are doomed.")
            roll = self.d20()
            if roll == 20:
                logging.info("Unbelievably, a family has come to your kingdom!")
                self.serfs += 10
        else:    
            logging.info("Your land is overcrowded, sire.")



    def check_growth(self):
        weather = self.check_weather()
        plusfood = abs(int((((weather['value']+100)/100)*self.lands)+1))
        self.food += plusfood
        logging.info("This turn, the weather was {}.  You gained {} food.".format(weather['word'], plusfood))

    def check_weather(self):
        roll = self.d20()
        logging.debug("Weather roll was a {}".format(roll))
        return {'value': roll, 'word': weather_map[roll] }
    
    def d20(self):
        return random.randint(1,20)
        
    def d20_interp(self, num):
        return num*5
