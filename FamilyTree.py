# FamilyTree - generates and queries family tree starting from 1950

import random
from Person import Person
from PersonFactory import PersonFactory


class FamilyTree:
    
    def __init__(self, first_last_name, second_last_name):
        self.factory = PersonFactory()
        self.founding_names = {first_last_name, second_last_name}
        self.all_people = []
        self.first_person = None
        self.second_person = None
    
    def read_files(self):
        print("Reading files...")
        self.factory.read_files()
    
    def generate_tree(self):
        print("Generating family tree...")
        
        # Create first two people in 1950
        self.first_person = self.factory.get_person(1950, list(self.founding_names)[0])
        self.second_person = self.factory.get_person(1950, list(self.founding_names)[1])
        self.first_person.set_partner(self.second_person)
        self.second_person.set_partner(self.first_person)
        self.all_people.extend([self.first_person, self.second_person])
        
        # Generate descendants
        index = 0
        while index < len(self.all_people):
            person = self.all_people[index]
            
            if person.get_year_born() + 25 < 2120:
                # Try to generate partner
                if not person.has_partner() and person not in [self.first_person, self.second_person]:
                    self._try_generate_partner(person)
                
                # Generate children
                if person.get_num_children() == 0:
                    self._generate_children(person)
            
            index += 1
    
    def _try_generate_partner(self, person):
        decade = f"{(person.get_year_born() // 10) * 10}s"
        marriage_rate = 0.5
        for d, _, m_rate in self.factory.birth_marriage:
            if d == decade:
                marriage_rate = m_rate
                break
        
        if random.random() < marriage_rate:
            partner_year = person.get_year_born() + random.randint(-10, 10)
            partner = self.factory.get_person(partner_year)
            person.set_partner(partner)
            partner.set_partner(person)
            self.all_people.append(partner)
    
    
    def _generate_children(self, person):
        decade = f"{(person.get_year_born() // 10) * 10}s"
        birth_rate = 2.0
        for d, b_rate, _ in self.factory.birth_marriage:
            if d == decade:
                birth_rate = b_rate
                break
        
        # Calculate number of children
        min_kids = max(1, round(birth_rate - 1.5))
        max_kids = round(birth_rate + 1.5)
        num_kids = random.randint(min_kids, max_kids)
        if not person.has_partner():
            num_kids = max(0, num_kids - 1)
        
        if num_kids == 0:
            return
        
        # Calculate birth years
        start_year = person.get_year_born() + 25
        end_year = min(person.get_year_born() + 45, 2119)
        
        if start_year >= 2120:
            return
        
        if num_kids == 1:
            child_years = [(start_year + end_year) // 2]
        else:
            gap = (end_year - start_year) / (num_kids - 1)
            child_years = [int(start_year + i * gap) for i in range(num_kids)]
        
        # Get child last name
        if person.get_last_name() in self.founding_names:
            child_name = person.get_last_name()
        elif person.has_partner() and person.get_partner().get_last_name() in self.founding_names:
            child_name = person.get_partner().get_last_name()
        else:
            child_name = person.get_last_name()
        
        # Create children
        for year in child_years:
            child = self.factory.get_person(year, child_name)
            person.add_child(child)
            if person.has_partner():
                person.get_partner().add_child(child)
            self.all_people.append(child)
    
    def get_total_people(self):
        return len(self.all_people)
    
    def get_people_by_decade(self):
        decades = {}
        for person in self.all_people:
            decade = (person.get_year_born() // 10) * 10
            decades[decade] = decades.get(decade, 0) + 1
        return decades
    
    def get_duplicate_names(self):
        names = {}
        for person in self.all_people:
            name = person.get_full_name()
            names[name] = names.get(name, 0) + 1
        return sorted([name for name, count in names.items() if count > 1])


def main():
    # Create family tree with two founding last names
    tree = FamilyTree("Jones", "Smith")
    
    # Read data files
    tree.read_files()
    
    # Generate the complete family tree
    tree.generate_tree()
    
    # Interactive interface
    while True:
        print("Are you interested in:")
        print("(T)otal number of people in the tree")
        print("Total number of people in the tree by (D)ecade")
        print("(N)ames duplicated")
        
        choice = input("> ").strip().upper()
        
        if choice == 'T':
            print(f"The tree contains {tree.get_total_people()} people total")
        elif choice == 'D':
            decades = tree.get_people_by_decade()
            for decade in sorted(decades.keys()):
                print(f"{decade}: {decades[decade]}")
        elif choice == 'N':
            dups = tree.get_duplicate_names()
            print(f"There are {len(dups)} duplicate names in the tree:")
            for name in dups:
                print(f"* {name}")
        else:
            print("Invalid choice. Please enter T, D, or N.")


if __name__ == "__main__":
    main()
