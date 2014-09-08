from .models import Nutrient, NutrientData


ENERGY = 208
TOTAL_FAT = 204
SATURATED_FAT = 606
TRANS_FAT = 605
CHOLESTEROL = 601
SODIUM = 307
CARBOHYDRATE = 205
DIETARY_FIBER = 291
SUGARS = 269
PROTEIN = 203


class NutritionFacts(object):

    def __init__(self, food, calories=None, grams=100):
        self.food = food
        self._calories = calories
        self._grams = grams
        energy_nutrient = Nutrient.objects.get(number=ENERGY)
        self.energy_100g = NutrientData.objects.get(food=food, nutrient=energy_nutrient).nutrient_value
        self.data_cache = {}

    @property
    def calories(self):
        return self._calories

    @calories.setter
    def calories(self, val):
        self._calories = val
        self._grams = 100.0 * val / self.energy_100g

    @property
    def grams(self):
        return self._grams

    @grams.setter
    def grams(self, val):
        self._calories = self.energy_100g * val / 100.0
        self._grams = val

    @property
    def total_fat_g(self):
        return self._nutrient_amount(TOTAL_FAT)

    @property
    def saturated_fat_g(self):
        return self._nutrient_amount(SATURATED_FAT)

    @property
    def trans_fat_g(self):
        return self._nutrient_amount(TRANS_FAT)

    @property
    def cholesterol_mg(self):
        return self._nutrient_amount(CHOLESTEROL)

    @property
    def sodium_mg(self):
        return self._nutrient_amount(SODIUM)

    @property
    def carbohydrate_g(self):
        return self._nutrient_amount(CARBOHYDRATE)

    @property
    def dietary_fiber_g(self):
        return self._nutrient_amount(DIETARY_FIBER)

    @property
    def sugars_g(self):
        return self._nutrient_amount(SUGARS)

    @property
    def protein_g(self):
        return self._nutrient_amount(PROTEIN)

    def _nutrient_amount(self, number):
        if number not in self.data_cache:
            self.data_cache[number] = NutrientData.objects.get(
                food=self.food, nutrient__number=number).nutrient_value
        return self.data_cache[number] * self.grams / 100.0
