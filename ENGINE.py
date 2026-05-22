import re

class Engine:
    def __init__(self):
        # Daftar menu
        self.menu = {
            "nasi goreng": 15000,
            "mie goreng": 12000,
            "es teh": 5000,
            "kopi": 7000
        }

        # Regex intent
        self.pattern_order = r"(pesan|beli|order)"
        self.pattern_menu = r"(menu|daftar)"
        self.pattern_exit = r"(selesai|keluar|bye)"

    # Memproses satu item pesanan
    def _parse_single_segment(self, text):
        text = text.lower()

        for item in self.menu:
            if re.search(item, text):
                jumlah = re.search(r"(\d+)", text)

                qty = int(jumlah.group(1)) if jumlah else 1

                return {
                    "item": item,
                    "qty": qty,
                    "harga": self.menu[item],
                    "total": qty * self.menu[item]
                }

        return None

    # Memproses seluruh kalimat pesanan
    def parse_orders(self, text):
        text = text.lower()

        segments = re.split(r",|dan", text)

        orders = []

        for seg in segments:
            result = self._parse_single_segment(seg)

            if result:
                orders.append(result)

        return orders

    # Mendeteksi intent user
    def detect_intent(self, text):
        text = text.lower()

        if re.search(self.pattern_order, text):
            return "order"

        elif re.search(self.pattern_menu, text):
            return "menu"

        elif re.search(self.pattern_exit, text):
            return "exit"

        return "unknown"

    # Menampilkan menu
    def print_menu(self):
        hasil = "=== MENU ===\n"

        for item, harga in self.menu.items():
            hasil += f"{item.title()} : Rp{harga}\n"

        return hasil