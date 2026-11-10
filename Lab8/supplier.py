class Supplier:
    def __init__(self, supplier_id, name, contact_info):
        self.__supplier_id = supplier_id
        self.__name = name
        self.__contact_info = contact_info

    def display_information(self):
        print(f"Supplier ID: {self.__supplier_id} | Name: {self.__name} | Contact Info: {self.__contact_info}\n")