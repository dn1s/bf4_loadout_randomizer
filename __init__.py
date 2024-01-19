import csv
from random import choice

class Loadouts:
    def __init__(self):
        self.gear = {}
        # This can be set to absolute path to bf4_attachments.csv file for convenience
        self.filepath = '.'
        self.filename = 'bf4_attachments.csv'
        self.bf_class = ''
        self.bf_classes = ['Assault', 'Engineer', 'Support', 'Recon']

    def get_data_from_csv(self) -> list[dict]:
        with open(f'{self.filepath}/{self.filename}', 'r') as attachments_file:
            reader = csv.DictReader(attachments_file)
            self.gear = [row for row in reader]

    def choose_class(self) -> str:
        self.bf_class = choice(self.bf_classes)
        return self.bf_class

    def choose_loadout(self, equipment_filter:str) -> str:
        equipments = []
        for gear in self.gear:
            if gear['Class'] == equipment_filter or (equipment_filter in self.bf_classes and gear['Class'] == 'All'):
                if gear['Weapon'] not in equipments:
                    if gear['Class'] == f'{self.bf_class}_gadgets':
                        equipments.append((gear['Weapon'], gear['Gadget Group']))
                    else:
                        equipments.append(gear['Weapon'])
        return choice(equipments)

    def choose_gadgets(self) -> list[tuple]:
        index = 0
        gadgets = []
        while index < 2:
            gadget = self.choose_loadout(equipment_filter=f'{self.bf_class}_gadgets')
            if any('Launcher' in gd for gd in gadget) and any('Launcher' in gd for gd in gadgets):
                continue
            if gadget not in gadgets:
                gadgets.append(gadget)
                index += 1
        return gadgets

    def choose_weapon_attachments(self, weapon:str, unlock_filter:str=None) -> list:
        attachment_types = []
        attachments = []
        selected_attachments = []

        for gear in self.gear:
            if weapon in gear.values():
                attachments.append([gear['Attachment'], gear['Attachment Type'], gear['Unlock']])
                if gear['Attachment Type'] not in attachment_types:
                    attachment_types.append(gear['Attachment Type'])

        for attachment_type in attachment_types:
            selected_attachments.append(choice([attachment for attachment in attachments if attachment_type in attachment and not unlock_filter in attachment])[0])

        return selected_attachments


if __name__ == '__main__':
    loadout = Loadouts()
    loadout.get_data_from_csv()
    bf_class = loadout.choose_class()
    primary_weapon = loadout.choose_loadout(equipment_filter=bf_class)
    primary_weapon_attachments = loadout.choose_weapon_attachments(primary_weapon, unlock_filter=None)
    secondary_weapon = loadout.choose_loadout(equipment_filter='Handgun')
    secondary_weapon_attachments = loadout.choose_weapon_attachments(secondary_weapon, unlock_filter=None)
    granade = loadout.choose_loadout(equipment_filter='Granade')
    gadgets = loadout.choose_gadgets(equipment_filter=bf_class)

    print(f'Class: {bf_class}, Weapon: {primary_weapon} - Attachments: {primary_weapon_attachments}, Handgun: {secondary_weapon} - \
Attachments: {secondary_weapon_attachments}, Granade: {granade}, Gadget_one: {gadgets[0][0]}, Gadget_two: {gadgets[1][0]}')
