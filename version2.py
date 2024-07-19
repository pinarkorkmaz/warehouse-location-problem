from ortools.linear_solver import pywraplp

# Ürün ve alan bilgileri
urunler = [
    {"id": "U1", "en": 10, "boy": 20, "priority": 5},
    {"id": "U2", "en": 11, "boy": 22, "priority": 1},
    {"id": "U3", "en": 13, "boy": 23, "priority": 3},
    {"id": "U4", "en": 11, "boy": 44, "priority": 6},
    {"id": "U5", "en": 32, "boy": 33, "priority": 4},
    {"id": "U6", "en": 23, "boy": 34, "priority": 8},
    {"id": "U7", "en": 90, "boy": 89, "priority": 10},
    {"id": "U8", "en": 19, "boy": 23, "priority": 9},
    {"id": "U9", "en": 34, "boy": 45, "priority": 7},
    {"id": "U10", "en": 45, "boy": 56, "priority": 2},
]

# Alan bilgileri ve sabit boyutları
alanlar = [
    {"id": "A1", "puan": 100, "en": 270, "boy": 154},
    {"id": "B1", "puan": 90, "en": 270, "boy": 154},
    {"id": "C1", "puan": 80, "en": 270, "boy": 154},
    {"id": "D1", "puan": 70, "en": 270, "boy": 154},
    {"id": "E1", "puan": 60, "en": 270, "boy": 154},
    {"id": "F1", "puan": 50, "en": 270, "boy": 154},
    {"id": "A2", "puan": 95, "en": 270, "boy": 154},
    {"id": "B2", "puan": 85, "en": 270, "boy": 154},
    {"id": "C2", "puan": 75, "en": 270, "boy": 154},
    {"id": "D2", "puan": 65, "en": 270, "boy": 154},
    {"id": "E2", "puan": 55, "en": 270, "boy": 154},
    {"id": "F2", "puan": 45, "en": 270, "boy": 154},
    {"id": "A3", "puan": 90, "en": 270, "boy": 154},
    {"id": "B3", "puan": 80, "en": 270, "boy": 154},
    {"id": "C3", "puan": 70, "en": 270, "boy": 154},
    {"id": "D3", "puan": 60, "en": 270, "boy": 154},
    {"id": "E3", "puan": 50, "en": 270, "boy": 154},
    {"id": "F3", "puan": 40, "en": 270, "boy": 154},
    {"id": "A4", "puan": 85, "en": 270, "boy": 154},
    {"id": "B4", "puan": 75, "en": 270, "boy": 154},
    {"id": "C4", "puan": 65, "en": 270, "boy": 154},
    {"id": "D4", "puan": 55, "en": 270, "boy": 154},
    {"id": "E4", "puan": 45, "en": 270, "boy": 154},
    {"id": "F4", "puan": 35, "en": 270, "boy": 154},
    {"id": "A5", "puan": 80, "en": 270, "boy": 154},
    {"id": "B5", "puan": 70, "en": 270, "boy": 154},
    {"id": "C5", "puan": 60, "en": 270, "boy": 154},
    {"id": "D5", "puan": 50, "en": 270, "boy": 154},
    {"id": "E5", "puan": 40, "en": 270, "boy": 154},
    {"id": "F5", "puan": 30, "en": 270, "boy": 154},
]

# Alanları en*boy değerlerine göre sırala
alanlar.sort(key=lambda x: x["en"] * x["boy"])

# MIP çözücüsünü oluştur
solver = pywraplp.Solver.CreateSolver('SCIP')
if not solver:
    raise ValueError("Solver yaratılamadı.")

# Karar değişkenleri
x = {}
for urun in urunler:
    for alan in alanlar:
        x[urun["id"], alan["id"]] = solver.IntVar(0, 1, f'x[{urun["id"]},{alan["id"]}]')

# Kısıtlar
for urun in urunler:
    solver.Add(solver.Sum([x[urun["id"], alan["id"]] for alan in alanlar]) == 1)

for alan in alanlar:
    solver.Add(solver.Sum([x[urun["id"], alan["id"]] for urun in urunler]) <= 1)

# Amaç fonksiyonu: Toplam puanı maximize et
objective_terms = []
for urun in urunler:
    for alan in alanlar:
        alan_enboy = alan["en"] * alan["boy"]
        if urun["en"] * urun["boy"] <= alan_enboy:
            objective_terms.append(urun["priority"] * alan["puan"] * x[urun["id"], alan["id"]])

solver.Maximize(solver.Sum(objective_terms))

# Problemi çöz
status = solver.Solve()

# Çözümü yazdır
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print('Toplam puan = ', solver.Objective().Value(), '\n')
    for urun in urunler:
        for alan in alanlar:
            if x[urun["id"], alan["id"]].solution_value() > 0:
                print(f'Ürün {urun["id"]} Alan {alan["id"]}\'e yerleştirildi.')
    print("\nMaksimum puan:", solver.Objective().Value())
else:
    print('Çözüm bulunamadı.')
