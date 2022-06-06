from cake import Cake
from ingredient import Ingredient
from order import Order
import xlsxwriter


# Tworzenie obiektów klasy Ingredient
cakes = [
    Cake("Sernik Tonka",
         [
             Ingredient("Twaróg", "kg", 1, 11.50),
             Ingredient("Śmietanka", "l", 0.25, 17),
             Ingredient("Cukier puder", "kg", 0.25, 4.5),
             Ingredient("Ciasteczka", "kg", 0.25, 4),
             Ingredient("Wanilia", "szt", 1, 15),
             Ingredient("Jaja", "szt", 6, 1),
             Ingredient("Masło", "kg", 0.1, 17.50)
         ]),
    Cake("Marchewkowe",
         [
             Ingredient("Marchew", "kg", 0.375, 2.5),
             Ingredient("Mąka", "kg", 0.3, 2.8),
             Ingredient("Jaja", "szt", 4, 1),
             Ingredient("Cukier", "kg", 0.42, 3.4),
             Ingredient("Cynamon", "szt", 1, 2.9),
             Ingredient("Olej", "l", 0.27, 18),
             Ingredient("Orzechy włoskie", "kg", 0.2, 39.95),
             Ingredient("Powidła śliwkowe", "kg", 0.8, 11.4),
         ]),
    Cake("Mazurek Kajmakowy",
         [
             Ingredient("Mąka", "kg", 0.16, 2.8),
             Ingredient("Masło", "kg", 0.07, 17.50),
             Ingredient("Cukier puder", "kg", 0.25, 0.036),
             Ingredient("Puree malinowe", "kg", 0.2, 20.5),
             Ingredient("Cukier", "kg", 0.09, 3.4),
             Ingredient("Jaja", "szt", 1, 1),
             Ingredient("Śmietanka", "l", 0.066, 17),
        ]),
    Cake("Mazurek Czekoladowy",
         [
             Ingredient("Mąka", "kg", 0.16, 2.8),
             Ingredient("Masło", "kg", 0.07, 17.50),
             Ingredient("Cukier puder", "kg", 0.036, 0.036),
             Ingredient("Wiśnia mrożona", "kg", 0.2, 9.4),
             Ingredient("Cukier", "kg", 0.045, 3.4),
             Ingredient("Jaja", "szt", 2, 1),
             Ingredient("Śmietanka", "l", 0.225, 17),
             Ingredient("Czekolada", "kg", 0.225, 40),
             Ingredient("Mleko", "l", 0.225, 2.9),
        ]),
    Cake("Mazurek Cytrynowy",
         [
             Ingredient("Mąka", "kg", 0.16, 2.8),
             Ingredient("Masło", "kg", 0.22, 17.50),
             Ingredient("Cukier puder", "kg", 0.036, 0.036),
             Ingredient("Mango puree", "kg", 0.2, 18),
             Ingredient("Cytryna", "kg", 0.78, 6),
             Ingredient("Jaja", "szt", 2, 1),
             Ingredient("Śmietanka", "l", 0.225, 17),
             Ingredient("Żelatyna", "kg", 0.01, 45),
        ])
    ]


#Pętla, która wyświetla ponownie menu przy wpisaniu nieprawidłowej odpowiedzi przez usera

# menu_possible_options - lista z możliwymi opcjami do wyboru
# menu_string - string z ponumerowanymi opcjami do wyboru
def get_answer_from_menu(menu_string, menu_possible_options):
    print(menu_string)
    answer = input("wybierz opcję: ")
    while answer not in menu_possible_options:
        print(menu_string)
        answer = input("wybierz opcję: ")
    return answer


orders = []  # Powstaje pusta lista "orders"


#______________________________________________
# Tworzenie funkcji 1, która będzie dodawać zamówienia
def add_order():
    surname = input("Podaj nazwisko:")
    phone_number = input("Podaj numer telefonu:")
    print("Oferta:")
    #Pętla, która iteruje ciasta w ofertę
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
    except Exception as e:  # Pozostałe błędy 
        print('Coś poszło nie tak: ', e)
        cake_choose_func()
    else:
        new_order = Order(surname, phone_number, chosen_cakes)  # tworzy się obiekt klasy Order
        orders.append(new_order)  # nowe zamówienie trafia do listy "orders"
        print("Twoje zamówienie to: ")
        print(new_order)



#______________________________________________
# Tworzenie funkcji 2 - Wyświetl wszystkie składniki potrzebne do realizacji wszystkich zamówień
def show_shopping_list():      
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
        title_format = workbook.add_format({'bold': True,
                                      'align': 'center',
                                      'border': 1})
        data_format = workbook.add_format({'border': 1})
        worksheet = workbook.add_worksheet("lista")     #tworzymy arkusz

        worksheet.write('A1', 'Produkt', title_format)
        worksheet.write('B1', 'Ilość', title_format)
        worksheet.write('C1', 'Jednostka', title_format)
        worksheet.write('D1', 'Kupione', title_format)

        rowIndex = 2
        for ingredient, summed_amount in summed_ingredients.items():
            worksheet.write('A' + str(rowIndex), ingredient.name, data_format)
            worksheet.write('B' + str(rowIndex), summed_amount, data_format)
            worksheet.write('C' + str(rowIndex), ingredient.unit, data_format)
            worksheet.write('D' + str(rowIndex), "", data_format)

            rowIndex += 1

        workbook.close()

        print("SAVED")

    elif note_answer == "n":
        pass
    else:
        print("Błąd")



#______________________________________________
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


#____________________________________________
# Tworzenie funkcji 4 - liczenie foodcostu
def show_foodcost():
    while True:
        foodcost_answer = get_answer_from_menu('''
        1 - pokaż foodcost wszystkich zamówień
        2 - pokaż foodcost konkretnego zamówienia
        3 - pokaż foodcost konkretnego ciasta
        ''', "1")

        if foodcost_answer == "1":
            foodcost = []
            for order in orders:
                for cake in order.cake_list:
                    for ingredient in cake.ingredient_list:
                        foodcost_ingredient = ingredient.price_per_unit * ingredient.amount   #liczy cena * składnik w każdym cieście
                        foodcost.append(foodcost_ingredient)                                  #dodaje do listy foodcost

        print("Całościowe zakupy wyniosą Cię: ", round(sum(foodcost)))                        #sumuje elementy funkcji i zaokrągla


#________________________________________
# Pętla główna programu, z jego funkcjami
# MAIN MENU

while True:
    answer = get_answer_from_menu('''
Menu:
1 - dodaj zamówienie
2 - wynegeruj listę zakupów
3 - wyświetl zamówienie
4 - policz foodcost
5 - zakończ''', ["1", "2", "3", "4", "5"])

    if answer == "1":
        add_order()
    elif answer == "2":
        show_shopping_list()
    elif answer == "3":
        show_orders()
    elif answer == "4":
        show_foodcost()
    if answer == "5":
        break
