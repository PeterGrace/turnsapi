import logging
import random
import time
from turnsapi.models.game_models import Game

class EndGameException(Exception):
    def __init__(self):
        self.super()

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
SERF_WAGES = 3
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
        self.taxrate = game.taxrate
        self.messages = []
        random.seed(time.time())
        pass

    def do_discovery(self):
        '''Find random amount of new lands'''
        roll = self.d20()
        if roll <10:
            self.messages.append("You were unable to secure any lands for your kingdom.")
        elif roll <=15:
            self.messages.append("You found a habitable region!")
            self.lands+=1
        elif roll <=19:
            self.messages.append("You found and claimed several regions!")
            self.lands+=5
        elif roll == 20:
            self.messages.append("Your search party has uncovered a new continent!  You've gained a hundred new lands!")
            self.lands+=100


    def sell_food(self):
        if self.food > 5000:
            selling = self.food - 5000
            moneyback = (selling*GOLD_PER_FOOD)
            self.gold += moneyback
            self.food -= selling
            self.messages.append("You sold {} food for {} gold.  {} food remains.".format(selling, moneyback, self.food))
        else:
            self.messages.append("You can only sell if you have more than 5000 food.")


    def run_turn(self):
        self.check_taxes()
        self.check_growth()
        self.check_consumption()
        self.check_population()
        self.check_spoilage()
    
    def check_consumption(self):
        consumption = (self.serfs*SERF_EATS)
        self.messages.append("Your serfs have eaten {} food.".format(consumption))
        self.food -= consumption
        if self.food < 0:
            self.food = 0
            self.messages.append("Widespread famine has culled your population.")
            self.serfs = int(self.serfs * .15)
            

    def check_spoilage(self):
        granary_max = self.granaries*GRANARY_STORAGE
        if self.food >= granary_max:
            loss = self.food - granary_max
            self.food = granary_max
            self.messages.append("Unfortunately, {} food has spoiled.  Build more granaries!".format(loss))

    def check_population(self):
        if self.serfs == 0:
            logging.info("Game over: {}".format(self.messages))
            raise EndGameException("All is lost")

        max_serfs = SERF_PER_LAND * self.lands


        if ((self.serfs >= 2) and (self.serfs <= max_serfs)):
            if self.food >= 5:
                self.messages.append("Your harvests have caused our serfs to have children")
                self.serfs += int((self.serfs/2))
            else:
                self.messages.append("You barely had enough food to feed our population, sire.")
        elif (self.serfs == 1):
            self.messages.append("Your kingdom consists of only you.  Without a miracle, you are doomed.")
            roll = self.d20()
            if roll == 20:
                self.messages.append("Unbelievably, a family has come to your kingdom!")
                self.serfs += 10
        else:    
            self.messages.append("Your land is overcrowded, sire.")


    def check_taxes(self):
        taxes = (self.serfs*SERF_WAGES)*(self.taxrate/100)
        self.gold += taxes
        self.messages.append("You collected {} in taxes this turn.".format(taxes))


    def check_growth(self):
        weather = self.check_weather()
        plusfood = abs(int(((((weather['value']+100)/100)*self.lands)+1)))
        self.food += plusfood
        self.messages.append("This turn, the weather was {}.  You gained {} food.".format(weather['word'], plusfood))

    def check_weather(self):
        roll = self.d20()
        return {'value': roll, 'word': weather_map[roll] }
    
    def d20(self):
        return random.randint(1,20)
        
    def d20_interp(self, num):
        return num*5
