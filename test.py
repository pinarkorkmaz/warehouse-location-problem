from ortools.linear_solver import pywraplp

def main():
    # Ürünlerin ve alanların sayısı
    num_urunler = 10
    num_alanlar = 15

    # Ürünlerin ihtiyaç sıklığına göre listesi (Ürün1 en sık, Ürün10 en az)
    urunler = list(range(1, num_urunler + 1))

    # Alanların zorluk seviyesine göre listesi (Alan1 en kolay, Alan15 en zor)
    alanlar = list(range(1, num_alanlar + 1))

    # Zorluk matrisini oluştur (her ürün-alan kombinasyonu için)
    # Ürün1'in Alan1'e yerleştirilmesi en iyi, Ürün10'un Alan15'e yerleştirilmesi en kötü
    costs = [[(i + 1) * (j + 1) for j in range(num_alanlar)] for i in range(num_urunler)]

    # MIP çözücüsünü oluştur
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return

    # Karar değişkenlerini tanımla
    x = {}
    for i in range(num_urunler):
        for j in range(num_alanlar):
            x[i, j] = solver.IntVar(0, 1, f'x[{i},{j}]')

    # Kısıtlar
    # Her ürün tam olarak bir alana yerleştirilmeli
    for i in range(num_urunler):
        solver.Add(solver.Sum([x[i, j] for j in range(num_alanlar)]) == 1)

    # Her alana en fazla bir ürün yerleştirilmeli
    for j in range(num_alanlar):
        solver.Add(solver.Sum([x[i, j] for i in range(num_urunler)]) <= 1)

    # Amaç fonksiyonu: Toplam zorluğu minimize et
    objective_terms = []
    for i in range(num_urunler):
        for j in range(num_alanlar):
            objective_terms.append(costs[i][j] * x[i, j])
    solver.Minimize(solver.Sum(objective_terms))

    # Problemi çöz
    status = solver.Solve()

    # Çözümü yazdır
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print('Toplam zorluk = ', solver.Objective().Value(), '\n')
        for i in range(num_urunler):
            for j in range(num_alanlar):
                if x[i, j].solution_value() > 0.5:
                    print(f'Ürün {i+1} Alan {j+1}\'e yerleştirildi.')
    else:
        print('Çözüm bulunamadı.')

if __name__ == '__main__':
    main()
