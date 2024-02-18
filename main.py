from collections import UserDict
import re

#універсальний клас для отримання значення для поля
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
#клас для зберігання імені
class Name(Field):
    def __init__(self, value):
        self.value = value
#клас для зберігання телефону з перевіркою на відповідність умові == 10 цифр
class Phone(Field):
    def __init__(self, value):
        if re.fullmatch(r'\d{10}', value):
            self.value = value
        else:
            self.value = None
#клас для обєднання імені і телефонів в окремий запис адресної книги
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
#метод для пошуку телефона, якщо телефон знайдено повертає True і індекс знайденого телефона, в іншому випадку False,0    
    def find_phone(self, phone: Phone):
        phone = Phone(phone)
        for i, existing_phone in enumerate(self.phones):
            if phone.value == existing_phone.value:
                return True, i
        return False, 0    
#метод для додавання телефону в список телефонів, якщо такий телефон вже є в списку повертаємо повідомлення про це
    def add_phone(self, phone:str):
        phone = Phone(phone)
        if phone.value and not self.find_phone(phone.value)[0]:
            self.phones.append(phone)
        else: 
            return print(f"{phone} phone already in the list")
#метод для видалення телефону зі списку, якщо телефона немає повертаємо повідомлення про це    
    def remove_phone(self, phone:str):
        phone = Phone(phone)
        search, i = self.find_phone(phone.value)
        if phone.value and search:
            self.phones.pop(i)
#метод для редагування телефону, якщо телефон знайдено то змінюємо його по індексу    
    def edit_phone(self, old:str, new:str):
        old_phone = Phone(old)
        new_phone = Phone(new)
        if old_phone and new_phone and self.find_phone(old_phone.value)[0]:
            i = self.find_phone(old_phone.value)[1]
            self.phones[i]=new_phone
#метод для виведення інформації про клас
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
#клас Адресна Книга для зберігання записів класу Record
class AddressBook(UserDict):
#метод для додавання записів в адресну книгу    
    def add_record(self, record:Record):
        self.data[record.name] = record
#метод для пошуку записів по імені, повертає запис типу Record        
    def find(self, name: str) -> Record:
        for record in self.data.keys():
            if record.value == name:
                return self.data[record]
        print(f"Record with name '{name}' not found.")
        return None
#метод для видалення записів з адресної книги, повертає True якщо запис видалено і False якщо не знайдено запису
    def delete(self, name: str) -> bool:
        for record in self.data.keys():
            if record.value == name:
                del self.data[record]
                print(f"Record with name '{name}' deleted.")
                return True
        else:
            print(f"Record with name '{name}' not found.")
            return False

            
# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# Видалення запису Jane
book.delete("Jane")
