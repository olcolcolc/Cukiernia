from cake import Cake


class Order:
    def __init__(self, surname, phone_number, cake_list):
        self.surname = surname
        self.phone_number = phone_number
        self.cake_list = cake_list

    def __str__(self):

        cakes_count = {}
        for cake in self.cake_list:  # przekształcamy listę z zamówionymi ciastami w słownik ciasto:ile
            if cake not in cakes_count:
                cakes_count[cake] = 1
            else:
                cakes_count[cake] = cakes_count[cake] + 1

            # jednolinijkowo -> cakes_count[cake] = cakes_count.get(cake, 0) + 1

        cake_str = ""
        for cake, count in cakes_count.items():
            cake_str += " {} x {}, ".format(count, cake.name)

        # Usuń dwa ostatnie znaki ze stringa
        cake_str = cake_str[0:len(cake_str) - 2]

        return self.surname + ", " + self.phone_number + ": " + cake_str


# linijki, które wykonują się gdy odpalamy plik bezpośrednio
if __name__ == "__main__":
    test_cake = Cake("Truskawkowe", [])
    test_order = Order("czyrnek", "+4563634534", [test_cake])
    print(test_order)
