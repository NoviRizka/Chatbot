from enum import Enum
from ENGINE import ENGINE


# State chatbot
class State(Enum):
    START = 1
    SHOW_MENU = 2
    ORDER = 3
    CHECKOUT = 4
    END = 5


class FSM:
    def __init__(self):
        self.state = State.START
        self.engine = Engine()
        self.cart = []

    # Menghitung total belanja
    def calculate_total(self):
        total = 0

        for item in self.cart:
            total += item["total"]

        return total

    # Menampilkan menu
    def get_menu_text(self):
        text = "=== MENU ===\n"

        for item, harga in self.engine.menu.items():
            text += f"{item.title()} : Rp{harga}\n"

        return text

    # Mengurangi item dalam keranjang
    def reduce_cart(self, item_name, qty):
        for item in self.cart:
            if item["item"] == item_name:

                item["qty"] -= qty
                item["total"] = item["qty"] * item["harga"]

                if item["qty"] <= 0:
                    self.cart.remove(item)

                return True

        return False

    # Mengambil response chatbot
    def get_response(self):
        if self.state == State.START:
            return "Halo, selamat datang!"

        elif self.state == State.SHOW_MENU:
            return self.get_menu_text()

        elif self.state == State.CHECKOUT:
            total = self.calculate_total()
            return f"Total belanja anda Rp{total}"

        elif self.state == State.END:
            return "Terima kasih telah memesan"

        return "Ada yang bisa dibantu?"

    # Proses utama chatbot
    def step(self, user_input):
        intent = self.engine.detect_intent(user_input)

        # Menampilkan menu
        if intent == "menu":
            self.state = State.SHOW_MENU
            return self.get_response()

        # Melakukan order
        elif intent == "order":
            orders = self.engine.parse_orders(user_input)

            if len(orders) == 0:
                return "Pesanan tidak ditemukan"

            for order in orders:
                self.cart.append(order)

            self.state = State.ORDER

            response = "Pesanan berhasil ditambahkan:\n"

            for order in orders:
                response += (
                    f"- {order['item']} "
                    f"x{order['qty']} "
                    f"= Rp{order['total']}\n"
                )

            return response

        # Checkout
        elif "checkout" in user_input.lower():
            self.state = State.CHECKOUT
            return self.get_response()

        # Keluar
        elif intent == "exit":
            self.state = State.END
            return self.get_response()

        return "Maaf, saya tidak memahami perintah anda"
