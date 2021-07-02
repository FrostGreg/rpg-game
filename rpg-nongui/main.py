from classes.game import Bcolours, Person
from classes.magic import Spell
from classes.inventory import Item

# Create Black spells
fire = Spell("Fire", 10, 50, "black", Bcolours.FAIL)
ice = Spell("Ice", 15, 70, "black", Bcolours.OKBLUE)
quake = Spell("Quake", 8, 30, "black", Bcolours.BROWN)
lighting = Spell("Lightning", 25, 125, "black", Bcolours.PURPLE)


# Create White spells
heal = Spell("Heal", 10, 50, "white", Bcolours.YELLOW)
mega = Spell("Mega Heal", 20, 100, "white", Bcolours.LIGHT_CYAN)


# Create Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
elixer = Item("Elixer", "elixer", "Fully restores MP", 9999)
splashelixer = Item("Splash Elixer", "elixer", "Fully restores MP for all party members", 9999)

bomb = Item("Bomb", "attack", "Deals 250 damage to all enemies", 250)

player_spells = [fire, ice, quake, lighting, heal, mega]
player_items = [{"item": potion, "quantity": 5},
                {"item": hipotion, "quantity": 1},
                {"item": elixer, "quantity": 3},
                {"item": splashelixer, "quantity": 1},
                {"item": bomb, "quantity": 3}]

# Instantiate Player and enemy
player = Person(100, 100, 25, 50, player_spells, player_items)
enemy = Person(250, 20, 33, 0, [fire, quake, heal], [])

running = True

print(Bcolours.FAIL + Bcolours.BOLD + 'AN ENEMY ATTACKS!' + Bcolours.ENDC)


while running:
    print("=================================")
    player.choose_action()
    choice = input("Choose action: ")
    index = int(choice) - 1

    print("You chose", player.get_action_name(index))

    if index == 0:
        dmg = player.generate_damage()
        enemy.take_damage(dmg)
    elif index == 1:
        player.choose_magic_spell()
        magic_choice = int(input("Choose spell: ")) - 1

        if magic_choice == -1:
            continue

        magic_dmg = player.magic[magic_choice].generate_spell_damage()
        spell = player.magic[magic_choice]

        current_mp = player.get_mp()

        if spell.cost > current_mp:
            print(Bcolours.FAIL + "Not enough MP" + Bcolours.ENDC)
            continue

        player.reduce_mp(spell.cost)

        if spell.type == "black":
            enemy.take_damage(magic_dmg)
            print(spell.colour + "\n" + spell.name + " deals", str(magic_dmg) + " points of damage" + Bcolours.ENDC)
        elif spell.type == "white":
            player.heal(magic_dmg)
            print(spell.colour + "\n" + spell.name + " heals", str(magic_dmg) + " HP" + Bcolours.ENDC)

    elif index == 2:
        player.choose_item()
        item_choice = int(input("Choose Item: ")) - 1

        if item_choice == -1:
            continue

        item = player.items[item_choice]["item"]

        if player.items[item_choice]["quantity"] == 0:
            print(Bcolours.FAIL + "DAMMIT I ran out" + Bcolours.ENDC)
            continue

        player.items[item_choice]["quantity"] -= 1

        if item.type == "potion":
            player.heal(item.prop)
            print(Bcolours.OKGREEN + "Player heals for " + str(item.prop) + " HP" + Bcolours.ENDC)

        elif item.type == "elixer":
            player.mp = player.maxmp
            print(Bcolours.OKGREEN + "Fully restored player MP" + Bcolours.ENDC)

        elif item.type == "attack":
            enemy.take_damage(item.prop)
            print(item.name, "deals " + str(item.prop) + " points of damage")

    enemy_choice = 1
    enemy_dmg = enemy.generate_damage()
    player.take_damage(enemy_dmg)
    print("Enemy attacks for:", enemy_dmg)
    print("--------------------")

    print("Enemy Health: " + Bcolours.FAIL + str(enemy.get_hp()) + "/" + str(enemy.get_maxhp()) + Bcolours.ENDC)
    print("Your Health: " + Bcolours.OKGREEN + str(player.get_hp()) + "/" + str(player.get_maxhp()) + Bcolours.ENDC)
    print("Your MP" + Bcolours.OKBLUE + str(player.get_mp()) + "/" + str(player.get_maxmp()) + Bcolours.ENDC)

    if enemy.get_hp() == 0:
        print(Bcolours.BOLD + Bcolours.OKGREEN + "CONGRATS You defeated the enemy :)" + Bcolours.ENDC)
        running = False
    elif player.get_hp() == 0:
        print(Bcolours.BOLD + Bcolours.FAIL + "YOU DIED!" + Bcolours.ENDC)
        running = False
