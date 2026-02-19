# PersonFactory - reads CSV files and creates Person objects
# Uses Python csv and random modules

import csv
import random
from Person import Person


class PersonFactory:
    
    def __init__(self):
        # Store all data in lists
        self.life_expectancy = []  
        self.first_names = []  
        self.birth_marriage = [] 
        self.last_names = []  
        self.rank_probs = []  
    
    def read_files(self):
        # Read life expectancy
        with open('life_expectancy.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.life_expectancy.append((int(row['Year']), float(row['Period life expectancy at birth'])))
        
        # Read first names
        with open('first_names.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.first_names.append((row['decade'], row['gender'], row['name'], float(row['frequency'])))
        
        # Read birth and marriage rates
        with open('birth_and_marriage_rates.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.birth_marriage.append((row['decade'], float(row['birth_rate']), float(row['marriage_rate'])))
        
        # Read last names
        with open('last_names.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.last_names.append((row['Decade'], int(row['Rank']), row['LastName']))
        
        # Read rank probabilities
        with open('rank_to_probability.csv', 'r') as f:
            reader = csv.reader(f)
            self.rank_probs = [float(p) for p in next(reader)]
    
    
    def get_person(self, year_born, last_name=None):
        decade = f"{(year_born // 10) * 10}s"
        
        # Pick gender randomly (50/50)
        gender = random.choice(['male', 'female'])
        
        # Pick first name based on frequency
        names = [(n, f) for d, g, n, f in self.first_names if d == decade and g == gender]
        if not names:  # fallback to 1950s
            names = [(n, f) for d, g, n, f in self.first_names if d == '1950s' and g == gender]
        name_list = [n for n, f in names]
        freq_list = [f for n, f in names]
        first_name = random.choices(name_list, weights=freq_list, k=1)[0]
        
        # Pick last name if not provided
        if last_name is None:
            names = [n for d, r, n in self.last_names if d == decade]
            if not names:  # fallback to 1950s
                names = [n for d, r, n in self.last_names if d == '1950s']
            last_name = random.choices(names, weights=self.rank_probs[:len(names)], k=1)[0]
        
        # Calculate year died
        closest_year = min(self.life_expectancy, key=lambda x: abs(x[0] - year_born))
        life_exp = closest_year[1]
        year_died = int(year_born + life_exp + random.uniform(-10, 10))
        
        return Person(year_born, first_name, last_name, year_died)
