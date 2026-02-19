# Person class for family tree simulation
# Stores attributes for each person  
# Person class only stores data 

class Person:
    def __init__(self, year_born, first_name, last_name, gender,year_died=None):

        self._year_born = year_born
        self._year_died = year_died
        self._first_name = first_name
        self._last_name = last_name
        self._gender = gender 
        self._partner = None
        self._children = []
    

    def get_year_born(self):
        return self._year_born
    
    def get_year_died(self):
        return self._year_died
    
    def get_first_name(self):
        return self._first_name
    
    def get_last_name(self):
        return self._last_name
    
    def get_gender(self):
        return self._gender 
    
    def get_full_name(self):
        return f"{self._first_name} {self._last_name}"
    
    def get_partner(self):
        return self._partner
    
    def get_children(self):
        return self._children
    

    def has_partner(self):
        return self._partner is not None
    
    def get_num_children(self):
        return len(self._children)
    
    def set_year_died(self, year_died):
        self._year_died = year_died
    
    def set_partner(self, partner):
        self._partner = partner
    
    def add_child(self, child):
        self._children.append(child)
    
    def is_alive(self, year):
        if self._year_died is None:
            return year >= self._year_born
        return self._year_born <= year < self._year_died
    