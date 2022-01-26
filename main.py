from cake import Cake
from ingredient import Ingredient
from order import Order
import xlsxwriter


# Tworzenie objektów klasy Ingredient
cakes = [
    Cake("Sernik Tonka",
         [
             Ingredient("Twaróg", "kg", 1, 11.50),
             Ingredient("Śmietanka", "ml", 250, 17),
             Ingredient("Cukier puder", "g", 250, 4.5)
         ]),
    Cake("Marchewkowe",
         [
             Ingredient("Marchew", "kg", 0.375, 2.5),
             Ingredient("Mąka", "kg", 0.3, 2.8),
             Ingredient("Cukier", "kg", 0.42, 3.4)
         ])
]


# menu_possible_options - lista z możliwymi opcjami do wyboru
# menu_string - string z ponumerowanymi opcjami do wyboru

def get_answer_from_menu(menu_string, menu_possible_options):
    print(menu_string)
    answer = input("wybierz opcję:")
    while answer not in menu_possible_options:
        print(menu_string)
        answer = input("wybierz opcję:")
    return answer


orders = [
    Order("Jacek", "123", [cakes[0], cakes[0], cakes[1]]),
    Order("Oleńka", "645", [cakes[0], cakes[1]]),
    Order("Mama", "123", [cakes[0], cakes[0]]),
    Order("Oleńka", "986", [cakes[1]])
]  # Powstaje pusta lista "orders"


# Tworzenie funkcji, która będzie dodawać zamówienia
def add_order():
    surname = "Czyrnek"  # test input("Podaj nazwisko:")
    phone_number = "+4509234252350"  # test input("Podaj numer telefonu:")
    print("Oferta:")
    # Pętla, która iteruje ciasta w ofertę
    i = 0
    for cake in cakes:
        i += 1
        print(i, "-", cake.name)

    chosen_cakes = []

    input_message = "Wybierz produkt (Wpisz 0, żeby zakończyć dodawanie):"

    def cake_choose_func():  # Tworzenie podfunkcji wybierania ciast
        cake_index = int(input(input_message))
        while cake_index != 0:  # Warunek, w którym wpisany indeks jest we właściwym zakresie
            cake_index -= 1  # odejmujemy 1, bo komputer liczy od 0
            chosen_cake = cakes[cake_index]
            chosen_cakes.append(chosen_cake)
            cake_index = int(input(input_message))

    try:
        cake_choose_func()
    except ValueError:  # Błąd, gdy wpiszemy str, zamiast int
        print('Błąd. Należy wpisać indeks produktu.')
        cake_choose_func()
    except IndexError:  # Błąd, gdy wpiszemy indeks spoza zakresu (index is out of range)
        print("Błąd. Należy wpisać poprawy indeks.")
        cake_choose_func()
    except Exception as e:  # Pozostałe błędy (wyjebać? niepotrzebne)
        print('Coś poszło nie tak: ', e)
        cake_choose_func()
    else:
        new_order = Order(surname, phone_number, chosen_cakes)  # tworzy się obiekt klasy Order
        orders.append(new_order)  # nowe zamówienie trafia do listy "orders"
        print("Twoje zamówienie to: ")
        print(new_order)


# Tworzenie funkcji 3 - wyświetlenie wszystkich zamówień złożonych dotychczas
def show_orders():
    answer = get_answer_from_menu('''
    Wybierz opcję:
    1 - Wyświetl wszystkie zamówienia
    2 - Wyświetl konkretne zamówienie (nr tel)
    3 - Wyświetl konkretne zamówienie (po nazwisku)
    ''', ["1", "2", "3"])

    if answer == "1":
        print("Zamówienia złożone dotychczas: ")
        i = 0
        for order in orders:
            i += 1
            print(i, " - ", order)

    if answer == "2":
        phone_number = input("Wpisz nr telefonu: ")
        number_not_found = True
        for order in orders:
            if phone_number == order.phone_number:  # Jeśli numer jest w liście, to drukujemy zamówienie
                number_not_found = False
                print(order)
        if number_not_found:  # Jeśli numer nie jest w liście, to drukujemy błąd
            print("Błąd. Nie ma tego zamówienia w bazie danych.")

    if answer == "3":
        surname = input("Wpisz nazwisko klienta:")
        surname_not_found = True
        for order in orders:
            if surname == order.surname:
                surname_not_found = False
                print(order)
        if surname_not_found:
            print("Błąd. Nie ma tego zamówienia w bazie danych.")


# Tworzenie funkcji 4 - Wyświetl wszystkie składniki potrzebne do realizacji wszystkich zamówień
def show_shopping_list():       # klasa igrentng: name, unit, amount, price_per_unit
    summed_ingredients = {}
    for order in orders:
        for cake in order.cake_list:
            for ingredient in cake.ingredient_list:
                if ingredient not in summed_ingredients:
                    summed_ingredients[ingredient] = ingredient.amount
                else:
                    summed_ingredients[ingredient] += ingredient.amount

    for ingredient, summed_amount in summed_ingredients.items():
        print("{} - {} {}".format(ingredient.name, summed_amount, ingredient.unit))

    note_answer = input("Czy chcesz zapisać listę zakupów w xlsx? (Odpowiedz T/N):").lower()

    #tworzenie pliku xlsx
    if note_answer == "t":
        workbook = xlsxwriter.Workbook("lista_zakupów.xlsx")     #tworzymy plik lista_zakupow.xlsx
        bold_format = workbook.add_format({"bold": True, "border": 2})   #formatujemy czcionke (pogrubiona)
        worksheet = workbook.add_worksheet("lista")     #tworzymy arkusz

        # JaC3kC: Nie może być po polsku, to produkt skierowany na rynek międzynarodowy
        worksheet.write('A1', 'Product', bold_format)
        worksheet.write('B1', 'Quantity', bold_format)
        worksheet.write('C1', 'Unit', bold_format)
        worksheet.write('D1', 'Bought', bold_format)

        rowIndex = 2
        for ingredient, summed_amount in summed_ingredients.items():
            worksheet.write('A' + str(rowIndex), ingredient.name)
            worksheet.write('B' + str(rowIndex), summed_amount)
            worksheet.write('C' + str(rowIndex), ingredient.unit)

            rowIndex += 1

        workbook.close()

        print("SAVED")

    elif note_answer == "n":
        pass
    else:
        print("Błąd")


# Pętla główna programu, z jego funkcjami
# MAIN MENU

while True:
    answer = get_answer_from_menu('''
Menu:
1 - dodaj zamówienie
2 - wynegeruj listę zakupów
3 - wyświetl zamówienie
4 - zakończ''', ["1", "2", "3", "4"])

    if answer == "1":
        add_order()
    elif answer == "2":
        show_shopping_list()
    elif answer == "3":
        show_orders()
    if answer == "4":
        break
