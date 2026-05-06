# Keszeg Martin - SAACCD - Autókölcsönző

import os
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

class Auto(ABC):
    def __init__(self, rendszam, tipus, berleti_dij):
        self.__rendszam = rendszam
        self.__tipus = tipus
        self.__berleti_dij = berleti_dij

    @property
    def rendszam(self):
        return self.__rendszam

    @property
    def tipus(self):
        return self.__tipus

    @property
    def berleti_dij(self):
        return self.__berleti_dij

    @abstractmethod
    def info(self):
        pass

    @abstractmethod
    def ascii_rajz(self):
        pass


class Szemelyauto(Auto):
    def __init__(self, rendszam, tipus, berleti_dij, utasok_szama, kivitel="sedan"):
        super().__init__(rendszam, tipus, berleti_dij)
        self.__utasok_szama = utasok_szama
        self.__kivitel = kivitel

    def ascii_rajz(self):
        if self.__kivitel == "ferdehatu":
            return [
                r"      _______  ",
                r"  ___//__||_\\ ",
                r" (o  _| -| _ o)",
                r"  `-(_)---(_)-'"
            ]
        else:
            return [
                r"       ________ ",
                r"  ____//__][__\\__ ",
                r" (o _ |  -|   _  o|   ",
                r"  `(_)-------(_)--'"
            ]

    def info(self):
        return (f"Típus: {self.tipus} (Személyautó - {self.__kivitel})\n"
                f"Rendszám: \033[1m{self.rendszam}\033[0m\n"
                f"Férőhely: {self.__utasok_szama} fő\n"
                f"Díj: {self.berleti_dij} Ft/nap")


class Teherauto(Auto):
    def __init__(self, rendszam, tipus, berleti_dij, teherbiras):
        super().__init__(rendszam, tipus, berleti_dij)
        self.__teherbiras = teherbiras

    def ascii_rajz(self):
        return [
            r"       ____________ ",
            r"  ____//__]        |",
            r" (o _ |  -|   _   o|",
            r"  `(_)-------(_)---'"
        ]

    def info(self):
        return (f"Típus: {self.tipus} (Teherautó)\n"
                f"Rendszám: \033[1m{self.rendszam}\033[0m\n"
                f"Teherbírás: {self.__teherbiras} kg\n"
                f"Díj: {self.berleti_dij} Ft/nap")


class Berles:
    def __init__(self, auto, datum):
        self.__auto = auto
        self.__datum = datum

    @property
    def auto(self):
        return self.__auto

    @property
    def datum(self):
        return self.__datum

    def info(self):
        return (f"Dátum: \033[1m{self.datum.strftime('%Y-%m-%d')}\033[0m "
                f"| Autó: \033[1m{self.auto.rendszam}\033[0m ({self.auto.tipus})")


class Autokolcsonzo:
    def __init__(self, nev):
        self.__nev = nev
        self.__autok = []
        self.__berlesek = []

    @property
    def nev(self):
        return self.__nev

    @property
    def autok(self):
        return self.__autok

    @property
    def berlesek(self):
        return self.__berlesek

    def auto_hozzaadasa(self, auto):
        self.__autok.append(auto)

    def autok_listazasa(self):
        indent = "  "
        for auto in self.__autok:
            for sor in auto.ascii_rajz():
                print(sor)
            print()
            info_text = auto.info()
            print(indent + info_text.replace("\n", "\n" + indent))
            print("-" * 55)

    def berles(self, rendszam, datum_str):
        try:
            datum = datetime.strptime(datum_str, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError("Hibás formátum! Használja: ÉÉÉÉ-HH-NN")

        if datum < datetime.now().date():
            raise ValueError("A dátum nem lehet a múltban!")

        keresett_auto = next(
            (a for a in self.__autok if a.rendszam.upper() == rendszam.upper()), None
        )
        if not keresett_auto:
            raise ValueError("Nincs ilyen autó ezzel a rendszámmal.")

        for b in self.__berlesek:
            if b.auto.rendszam.upper() == rendszam.upper() and b.datum == datum:
                raise ValueError("Az autó már foglalt erre a napra.")

        uj_berles = Berles(keresett_auto, datum)
        self.__berlesek.append(uj_berles)
        return keresett_auto.berleti_dij

    def berles_lemondasa_sorszam(self, sorszam):
        rendezett = sorted(self.__berlesek, key=lambda x: x.datum)
        if sorszam < 1 or sorszam > len(rendezett):
            raise ValueError("Érvénytelen sorszám.")
        torlendo = rendezett[sorszam - 1]
        self.__berlesek = [b for b in self.__berlesek if b is not torlendo]
        return torlendo

    def berlesek_listazasa(self, sorszammal=False):
        if not self.__berlesek:
            print("  Jelenleg nincs egyetlen aktív bérlés sem.")
            return
        rendezett_berlesek = sorted(self.__berlesek, key=lambda x: x.datum)
        for i, b in enumerate(rendezett_berlesek, 1):
            if sorszammal:
                print(f" {i}. {b.info()}")
            else:
                print(f" > {b.info()}")


def elokeszites():
    kolcsonzo = Autokolcsonzo("MaKe Autókölcsönző Kft.")
    kolcsonzo.auto_hozzaadasa(Szemelyauto("ABC-123", "Toyota Corolla", 15000, 5, "ferdehatu"))
    kolcsonzo.auto_hozzaadasa(Szemelyauto("DEF-456", "Skoda Octavia", 18000, 5, "sedan"))
    kolcsonzo.auto_hozzaadasa(Teherauto("GHI-789", "Ford Transit", 25000, 1500))

    mai = datetime.now().date()
    try:
        kolcsonzo.berles("ABC-123", (mai + timedelta(days=2)).strftime('%Y-%m-%d'))
        kolcsonzo.berles("ABC-123", (mai + timedelta(days=5)).strftime('%Y-%m-%d'))
        kolcsonzo.berles("DEF-456", (mai + timedelta(days=3)).strftime('%Y-%m-%d'))
        kolcsonzo.berles("GHI-789", (mai + timedelta(days=1)).strftime('%Y-%m-%d'))
    except ValueError as e:
        print(f"Előkészítési hiba: {e}")

    return kolcsonzo


def main():
    kolcsonzo = elokeszites()
    os.system('cls' if os.name == 'nt' else 'clear')
    ascii_szamok = [
        [" __ ", "/_ |", " | |", " | |", " | |", " |_|"],
        [" ___ ", "|__ \\", "   ) |", "  / / ", " / /_ ", "|____|"],
        [" ____ ", "|___ \\", "  __) |", " |__ < ", " ___) |", "|____/ "]
    ]

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 50)
        print(f" Üdvözli a {kolcsonzo.nev}")
        print("=" * 50)
        print(" 1. Elérhető autók listázása")
        print(" 2. Autó bérlése")
        print(" 3. Bérlés lemondása")
        print(" 4. Aktív bérlések listázása")
        print(" 5. Kilépés")
        print("=" * 50)
        print()
        v = input("Kérem válasszon a fenti menüpontok közül (1-5): ")
        os.system('cls' if os.name == 'nt' else 'clear')

        if v == '1':
            print("--- Elérhető autóink ---\n")
            kolcsonzo.autok_listazasa()
            input("\nNyomjon Entert a visszalépéshez...")

        elif v == '2':
            print("--- Autó bérlése ---\n")
            autok = kolcsonzo.autok
            indent = "  "
            gap = "    "

            for i, auto in enumerate(autok):
                szam_art = ascii_szamok[i]
                kocsi_art = auto.ascii_rajz()
                for j in range(6):
                    s_sor = szam_art[j]
                    k_sor = kocsi_art[j - 2] if 2 <= j < 2 + len(kocsi_art) else ""
                    print(f"{s_sor}{gap}{k_sor}")
                print()
                info_text = auto.info()
                print(indent + info_text.replace("\n", "\n" + indent))
                print("-" * 55)

            sikeres = False

            while not sikeres:
                valasztott = input(f"\nVálasszon autót (1-{len(autok)}) vagy 'V' vissza: ")

                if valasztott.upper() == 'V':
                    break

                if not valasztott.isdigit() or not (1 <= int(valasztott) <= len(autok)):
                    print("❌ Hibás sorszám! Próbáld újra.")
                    continue

                kivalasztott_auto = autok[int(valasztott) - 1]

                while True:
                    datum = input("Dátum (ÉÉÉÉ-HH-NN) vagy 'V' autóválasztáshoz vissza: ")

                    if datum.upper() == 'V':
                        break

                    try:
                        ar = kolcsonzo.berles(kivalasztott_auto.rendszam, datum)
                        print(f"\n✅ Sikeres foglalás! Fizetendő: {ar} Ft")
                        sikeres = True
                        break
                    except ValueError as e:
                        print(f"\n❌ Hiba: {e}")
                        print("Próbáld újra vagy nyomj 'V'-t az autóválasztáshoz.")

            if sikeres:
                input("\nNyomjon Entert a visszalépéshez...")

        elif v == '3':
            print("--- Bérlés lemondása ---\n")

            if not kolcsonzo.berlesek:
                print("  Jelenleg nincs egyetlen aktív bérlés sem.")
                input("\nNyomjon Entert a visszalépéshez...")
                continue

            print("Aktív bérlések:\n")
            kolcsonzo.berlesek_listazasa(sorszammal=True)

            lemondva = False
            while True:
                valasz = input(f"\nMelyik bérlést mondja le? (1-{len(kolcsonzo.berlesek)}) vagy 'V' vissza: ")

                if valasz.upper() == 'V':
                    break

                if not valasz.isdigit():
                    print("❌ Számot adjon meg!")
                    continue

                sorszam = int(valasz)

                try:
                    torolt = kolcsonzo.berles_lemondasa_sorszam(sorszam)
                    print(f"\n✅ Sikeresen lemondva: {torolt.auto.rendszam} – {torolt.datum.strftime('%Y-%m-%d')}")
                    lemondva = True
                    break
                except ValueError as e:
                    print(f"\n❌ Hiba: {e}")

            if lemondva:
                input("\nNyomjon Entert a visszalépéshez...")

        elif v == '4':
            print("--- Aktív bérlések ---\n")
            kolcsonzo.berlesek_listazasa()
            input("\nNyomjon Entert a visszalépéshez...")

        elif v == '5':
            print("Viszontlátásra!")
            break

        else:
            input("❌ Érvénytelen választás! Nyomjon Entert a folytatáshoz...")


if __name__ == "__main__":
    main()
