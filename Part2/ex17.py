import random
# TODO: Refer to the objective and sample output and figure out your own code!
# Time to graduate :p

adjectives = ['Slurpy', 'Bonkified', 'Wiggle-brained', 'Derpy', 'Noodle-legged', 'Sploinky']
animals = ['Platypus', 'Llama', 'Octopus', 'Ferret', 'Hedgehog', 'Walrus']

print("What is your name?")
username = input()

codename = (random.choice(adjectives)+" "+random.choice(animals))
luckyNumber = (random.randint(1, 99))

print(username+", your codename is:",codename)
print("Your lucky number is:",luckyNumber)