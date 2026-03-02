"""
SISTEM RENTAL KENDARAAN (INTERAKTIF, DURASI DALAM HARI)
------------------------------------------------------
Modifikasi: durasi dihitung dalam HARI, bukan jam.

- base_price = harga per hari
- validation memastikan durasi minimal 1 hari
- diskon & aturan lain disesuaikan untuk hitungan hari
"""

from abc import ABC, abstractmethod


# =============================
# EXCEPTION CUSTOM
# =============================
class InvalidDurationError(Exception):
    """Error saat durasi rental tidak valid."""
    pass


# =============================
# ABSTRACT ENTITY: VEHICLE
# =============================
class Vehicle(ABC):
    """
    Class abstrak untuk kendaraan.
    Durasi dihitung dalam HARI.
    """

    def __init__(self, name: str, base_price: int, max_days: int = 7):
        self.name = name
        self.base_price = base_price
        self.max_days = max_days  # batas hari sebelum biaya tambahan

    def validate_duration(self, days: int):
        """Validasi durasi dalam HARI."""
        if days < 1:
            raise InvalidDurationError("Durasi minimal adalah 1 hari.")
        if days > 30:
            raise InvalidDurationError("Durasi maksimal adalah 30 hari.")

    @abstractmethod
    def calculate_cost(self, days: int) -> int:
        """Method abstrak untuk menghitung biaya."""
        pass


# =============================
# SUBCLASS: CAR, MOTOR, PREMIUM
# =============================
class Car(Vehicle):
    """
    Mobil: base price per hari
    Biaya overtime jika melebihi max_days
    """

    def calculate_cost(self, days: int) -> int:
        self.validate_duration(days)
        cost = self.base_price * days

        # overtime harian
        if days > self.max_days:
            overtime = days - self.max_days
            cost += overtime * 50000  # biaya overtime per hari

        cost += 30000  # biaya perawatan mobil
        return cost


class Motor(Vehicle):
    """
    Motor: diskon jika sewa >= 7 hari
    """

    def calculate_cost(self, days: int) -> int:
        self.validate_duration(days)
        cost = self.base_price * days

        if days >= 7:
            cost *= 0.9  # diskon 10%

        return int(cost)


class PremiumCar(Vehicle):
    """
    Premium Car: biaya tambahan tetap
    Diskon jika durasi > 3 hari
    """

    def calculate_cost(self, days: int) -> int:
        self.validate_duration(days)
        cost = (self.base_price * days) + 150000  # biaya premium

        if days > 3:
            cost -= 50000  # bonus driver gratis

        return cost


# =============================
# REPOSITORY KENDARAAN
# =============================
class VehicleRepository:
    """Class khusus menyimpan & mengambil kendaraan."""

    def __init__(self):
        self.vehicles = []

    def add_vehicle(self, vehicle: Vehicle):
        self.vehicles.append(vehicle)

    def list_vehicles(self):
        return self.vehicles


# =============================
# PAYMENT METHOD
# =============================
class Payment(ABC):
    @abstractmethod
    def pay(self, amount: int) -> str:
        pass


class CashPayment(Payment):
    def pay(self, amount: int) -> str:
        return f"[CASH] Bayar langsung Rp{amount:,}"


class TransferPayment(Payment):
    def pay(self, amount: int) -> str:
        return f"[TRANSFER] Silakan transfer Rp{amount:,} ke Rek 123-456-789"


class EWalletPayment(Payment):
    def pay(self, amount: int) -> str:
        return f"[E-WALLET] Pembayaran Rp{amount:,} via OVO/Gopay/DANA"


# =============================
# RENTAL ORDER
# =============================
class RentalOrder:
    def __init__(self, vehicle: Vehicle, days: int, payment_method: Payment):
        self.vehicle = vehicle
        self.days = days
        self.payment_method = payment_method

    def calculate_total(self) -> int:
        return self.vehicle.calculate_cost(self.days)

    def summary(self) -> str:
        total = self.calculate_total()
        payment_text = self.payment_method.pay(total)

        return (
            "\n===== RINGKASAN PESANAN =====\n"
            f"Kendaraan     : {self.vehicle.name}\n"
            f"Durasi        : {self.days} hari\n"
            f"Total Biaya   : Rp{total:,}\n"
            f"Metode Bayar  : {payment_text}\n"
            "================================\n"
        )


# =============================
# MENU INTERAKTIF
# =============================
def pilih_kendaraan(repo: VehicleRepository) -> Vehicle:
    print("\n=== PILIH KENDARAAN ===")
    vehicles = repo.list_vehicles()

    for i, v in enumerate(vehicles, start=1):
        print(f"{i}. {v.name} (Rp{v.base_price:,}/hari)")

    while True:
        try:
            pilihan = int(input("Pilih nomor kendaraan: "))
            if 1 <= pilihan <= len(vehicles):
                return vehicles[pilihan - 1]
            print("Nomor tidak valid.")
        except ValueError:
            print("Input harus angka.")


def pilih_metode_pembayaran() -> Payment:
    print("\n=== METODE PEMBAYARAN ===")
    print("1. Tunai")
    print("2. Transfer")
    print("3. E-Wallet")

    while True:
        try:
            pilihan = int(input("Pilih metode pembayaran: "))
            if pilihan == 1:
                return CashPayment()
            elif pilihan == 2:
                return TransferPayment()
            elif pilihan == 3:
                return EWalletPayment()
            print("Pilihan tidak valid.")
        except ValueError:
            print("Input harus angka.")


def main():
    repo = VehicleRepository()
    repo.add_vehicle(Car("Avanza", 300000))
    repo.add_vehicle(PremiumCar("Alphard", 800000))
    repo.add_vehicle(PremiumCar("Civic", 150000))
    repo.add_vehicle(PremiumCar("Altis", 250000))
    repo.add_vehicle(PremiumCar("Soul", 10000))
    repo.add_vehicle(PremiumCar("Creta", 800000))
    repo.add_vehicle(PremiumCar("Palisade", 900000))

    while True:
        print("\n=== SISTEM RENTAL KENDARAAN ===")
        print("1. Buat Pesanan Rental")
        print("2. Keluar")

        try:
            menu = int(input("Pilih menu: "))
        except ValueError:
            print("Input harus angka.")
            continue

        if menu == 1:
            kendaraan = pilih_kendaraan(repo)

            while True:
                try:
                    hari = int(input("Masukkan durasi sewa (hari): "))
                    kendaraan.validate_duration(hari)
                    break
                except InvalidDurationError as e:
                    print("Error:", e)
                except ValueError:
                    print("Durasi harus angka.")

            metode = pilih_metode_pembayaran()

            order = RentalOrder(kendaraan, hari, metode)
            print(order.summary())

        elif menu == 2:
            print("Terima kasih telah menggunakan sistem rental!")
            break

        else:
            print("Pilihan menu tidak valid.")
            

if __name__ == "__main__":
    main()
