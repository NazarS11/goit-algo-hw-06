from collections import UserDict
import re

class Field:                                                                                                    
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):                                                                                     
    def __init__(self, value):
        self.value = value

class Phone(Field):                                                                                     

    def __init__(self, value):
       self.value = value

    @property
    def value(self):
        return self._value

    @value.setter                                                                                             
    def value(self, new_value):
        if re.fullmatch(r'\d{10}', new_value):
            self._value = new_value
        else:
            raise ValueError(f"Phone number {new_value} should consist of 10 digits")
        
class Record:                                                                                          
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def __str__(self):                                                                                         
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def find_phone(self, phone: str): 
        for existing_phone in self.phones:
            if phone == existing_phone.value:
                return existing_phone
        return None
        
    def add_phone(self, phone:str):                                                                           
        if not self.find_phone(phone):
            self.phones.append(Phone(phone))
            
    def remove_phone(self, phone:str):  
        phone_for_remove = self.find_phone(phone)                                                                              
        if phone_for_remove:
            self.phones.remove(phone_for_remove)

    def edit_phone(self, old:str, new:str):
        phone_for_edit = self.find_phone(old)     
        if phone_for_edit:
            phone_for_edit.value = new
        else: raise ValueError(f"Contact {self.name} has no phone number: {old}")

class AddressBook(UserDict):

    def add_record(self, record:Record):
        self.data[record.name.value] = record

    def find(self, name: str) -> Record:
        for key in self.data.keys():
            if key == name:
                return self.data[key]

    def delete(self, name: str):
        for key in self.data.keys():
            if key == name:
                del self.data[key]
                break

if __name__ == '__main__':
    try:            
        # Створення нової адресної книги
        book = AddressBook()

        # Створення запису для John
        john_record = Record("John")
        john_record.add_phone("1234567890")
        john_record.add_phone("5555555555")
        john_record.add_phone("6666666666")
        john_record.remove_phone("6666666666")

        # Додавання запису John до адресної книги
        book.add_record(john_record)

        # Створення та додавання нового запису для Jane
        jane_record = Record("Jane")
        jane_record.add_phone("9876543210")
        book.add_record(jane_record)

        # Виведення всіх записів у книзі
        for name, record in book.data.items():
            print(f"key: {name}: value {record}")

        # Знаходження та редагування телефону для John
        john = book.find("John")
        john.edit_phone("1234567891", "1112223333")

        print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

        # Пошук конкретного телефону у записі John
        found_phone = john.find_phone("5555555555")
        print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

        # Видалення запису Jane
        book.delete("Jane")
    
        # Виведення всіх записів у книзі
        for name, record in book.data.items():
            print(f"key: {name}: value {record}")
    except ValueError as e:
        print(e)