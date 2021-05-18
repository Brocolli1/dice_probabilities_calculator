import enum
import random
import math
from operator import add

class Type_Of_Success(enum.Enum):
   Equal = 1
   MoreEqual = 2
   LessEqual = 3
import collections
Rerolling = collections.namedtuple('Rerolls', 
                                       ['none', 'ones', 'all', 'dice'])
Rerolls = Rerolling(0, 1, 2, 3)



class rolling_step: 
    def __init__(self, sides=6, success=4, amount_of_dice=1, needed_successes=1, modifier=0, rerolls=Rerolls.none, required=False, number=0, dice_for_reroll=0):
        self.sides=sides
        self.success=success
        self.amount_of_dice=amount_of_dice
        self.needed_successes=needed_successes
        self.modifier=modifier
        self.rerolls=rerolls
        self.success_required = required
        self.number = number
        self.dice_for_reroll = dice_for_reroll

    def dice (self, sides=6):
        self.sides = sides

    def set_success(self, success):
        self.success = success
    
    def set_success_type(self):
        pass

    def set_amount_of_dice(self,amount_of_dice):
        self.amount_of_dice=amount_of_dice

    def set_needed_successes(self, needed_successes):
        self.needed_successes=needed_successes

    
    def roll(self):
        result = []
        successes = 0
        for i in range(0, self.amount_of_dice):
            n = random.randint(1, self.sides)
            if n + self.modifier < self.success:
                if self.rerolls == Rerolls.all:
                    n = random.randint(1, self.sides)
                elif self.rerolls == Rerolls.ones and n == 1 :
                     n = random.randint(1, self.sides)
            
            result.append(n + self.modifier)
            if n + self.modifier >= self.success:
                successes+=1 
        return (result,successes, successes>=self.needed_successes)

    def calculate(self):
        probability=[0] * (self.amount_of_dice+1)
        p=(self.success-1-self.modifier)/self.sides
        if self.rerolls == Rerolls.ones:
            p -= 1/self.sides * p
        elif self.rerolls == Rerolls.all:
            p -= (1-p) * p 
        
        if self.sides + self.modifier < self.success: 
            p = 1

        for i in range(0, self.amount_of_dice+1):
            result=(math.factorial(self.amount_of_dice)/(math.factorial(i)*math.factorial(self.amount_of_dice-i)))*(p**(self.amount_of_dice-i))*((1-p)**i)
            if result > 0:
                probability[i] = result

        x=self.dice_for_reroll
        if self.rerolls == Rerolls.dice: 
            for i in range(0, self.amount_of_dice):
                if i + x > self.amount_of_dice:
                    x = self.amount_of_dice - i
                for j in range(1, x+1):
                    result=(math.factorial(x)/(math.factorial(j)*math.factorial(x-j)))*(p**(x-j))*((1-p)**j)
                    if result > 0:
                        probability[i + j] += probability[i] * result 
                        probability[i] -= probability[i] * result 

        return probability

class rolling_chain():
    steps = []
    
    def __init__(self, roller = rolling_step()):
        self.steps.append(roller)

    def add_step(self, step = rolling_step()):
        self.steps.append(step)

    def num_of_steps(self):
        return len(self.steps)
    
    def calculate(self):
        amount_of_dice = self.steps[0].amount_of_dice
        #self.steps[0].set_amount_of_dice(self.amount_of_dice)
        previous = self.steps[0].calculate()
        probability = [0] * (amount_of_dice+1)
        req = self.steps[0].success_required
        needed = self.steps[0].needed_successes
        
                
        for step in self.steps[1:]:
            if req :
                for prob in previous[1:needed]:
                    previous[0] += prob
                    prob = 0
            for i in range(0, amount_of_dice+1):
                step.set_amount_of_dice(i) 
                table = step.calculate()
                new_probability = list( map (lambda x: x*previous[i], table ) )
                sum_list = []
                for j in range(len(new_probability)):
                    #if step.success_required and j < step.:
                    probability[j] += new_probability[j]
            
            req = step.success_required
            needed = step.needed_successes
            previous = probability

        return previous

    def roll(self):
        #self.steps[0].set_amount_of_dice(self.amount_of_dice)
        result = self.steps[0].roll()
        req = self.steps[0].success_required
        for step in self.steps[1:]:
            step.set_amount_of_dice(result[1])
            if req and result[2] == False:
                step.set_amount_of_dice(0)
            result = step.roll()
            req = step.success_required
        return result