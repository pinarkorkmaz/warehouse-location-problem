from ortools.linear_solver import pywraplp

# Product and area information
products = [
    {"id": "P1", "width": 10, "height": 20, "depth": 30, "priority": 5, "quantity": 100, "weight": 10},
    {"id": "P2", "width": 11, "height": 22, "depth": 40, "priority": 1, "quantity": 250, "weight": 20},
    {"id": "P3", "width": 13, "height": 23, "depth": 50, "priority": 3, "quantity": 95, "weight": 15},
    {"id": "P4", "width": 11, "height": 44, "depth": 60, "priority": 6, "quantity": 200, "weight": 25},
    {"id": "P5", "width": 32, "height": 33, "depth": 70, "priority": 4, "quantity": 70, "weight": 30},
    {"id": "P6", "width": 23, "height": 34, "depth": 80, "priority": 8, "quantity": 150, "weight": 35},
    {"id": "P7", "width": 90, "height": 89, "depth": 90, "priority": 10, "quantity": 10, "weight": 50},
    {"id": "P8", "width": 19, "height": 23, "depth": 100, "priority": 9, "quantity": 50, "weight": 45},
    {"id": "P9", "width": 34, "height": 45, "depth": 105, "priority": 7, "quantity": 30, "weight": 40},
    {"id": "P10", "width": 45, "height": 56, "depth": 85, "priority": 2, "quantity": 45, "weight": 55},
]

# Area information and fixed dimensions
areas = [
    {"id": "A1", "score": 100, "width": 270, "height": 154, "depth": 105},
    {"id": "B1", "score": 90, "width": 270, "height": 154, "depth": 105},
    {"id": "C1", "score": 80, "width": 270, "height": 154, "depth": 105},
    {"id": "D1", "score": 70, "width": 270, "height": 154, "depth": 105},
    {"id": "E1", "score": 60, "width": 270, "height": 154, "depth": 105},
    {"id": "F1", "score": 50, "width": 270, "height": 154, "depth": 105},
    {"id": "A2", "score": 95, "width": 270, "height": 154, "depth": 105},
    {"id": "B2", "score": 85, "width": 270, "height": 154, "depth": 105},
    {"id": "C2", "score": 75, "width": 270, "height": 154, "depth": 105},
    {"id": "D2", "score": 65, "width": 270, "height": 154, "depth": 105},
    {"id": "E2", "score": 55, "width": 270, "height": 154, "depth": 105},
    {"id": "F2", "score": 45, "width": 270, "height": 154, "depth": 105},
    {"id": "A3", "score": 90, "width": 270, "height": 154, "depth": 105},
    {"id": "B3", "score": 80, "width": 270, "height": 154, "depth": 105},
    {"id": "C3", "score": 70, "width": 270, "height": 154, "depth": 105},
    {"id": "D3", "score": 60, "width": 270, "height": 154, "depth": 105},
    {"id": "E3", "score": 50, "width": 270, "height": 154, "depth": 105},
    {"id": "F3", "score": 40, "width": 270, "height": 154, "depth": 105},
    {"id": "A4", "score": 85, "width": 270, "height": 154, "depth": 105},
    {"id": "B4", "score": 75, "width": 270, "height": 154, "depth": 105},
    {"id": "C4", "score": 65, "width": 270, "height": 154, "depth": 105},
    {"id": "D4", "score": 55, "width": 270, "height": 154, "depth": 105},
    {"id": "E4", "score": 45, "width": 270, "height": 154, "depth": 105},
    {"id": "F4", "score": 35, "width": 270, "height": 154, "depth": 105},
    {"id": "A5", "score": 80, "width": 270, "height": 154, "depth": 105},
    {"id": "B5", "score": 70, "width": 270, "height": 154, "depth": 105},
    {"id": "C5", "score": 60, "width": 270, "height": 154, "depth": 105},
    {"id": "D5", "score": 50, "width": 270, "height": 154, "depth": 105},
    {"id": "E5", "score": 40, "width": 270, "height": 154, "depth": 105},
    {"id": "F5", "score": 30, "width": 270, "height": 154, "depth": 105},
]

# Sort areas by score in descending order
areas.sort(key=lambda x: x["score"], reverse=True)

# Calculate volume for each product
for product in products:
    volume = product["width"] * product["height"] * product["depth"]
    product["volume"] = volume

# Print the volumes of each product
for product in products:
    print(f'Product {product["id"]} has a volume of {product["volume"]} cubic units and quantity of {product["quantity"]}.')

# Calculate volume for each area
for area in areas:
    volume = area["width"] * area["height"] * area["depth"]
    area["volume"] = volume

# Print the volumes of each area
for area in areas:
    print(f'Area {area["id"]} has a volume of {area["volume"]} cubic units.')

# Create MIP solver
solver = pywraplp.Solver.CreateSolver('SCIP')
if not solver:
    raise ValueError("Solver not created.")

# Decision variables
x_lower = {}
x_upper = {}
for product in products:
    for area in areas:
        x_lower[product["id"], area["id"]] = solver.IntVar(0, product["quantity"], f'x_lower[{product["id"]},{area["id"]}]')
        x_upper[product["id"], area["id"]] = solver.IntVar(0, product["quantity"], f'x_upper[{product["id"]},{area["id"]}]')

# Constraints for each product
for product in products:
    solver.Add(solver.Sum([x_lower[product["id"], area["id"]] + x_upper[product["id"], area["id"]] for area in areas]) == product["quantity"])

# Constraints for each area
for area in areas:
    solver.Add(solver.Sum([product["volume"] * x_lower[product["id"], area["id"]] for product in products]) <= area["volume"] / 2)
    solver.Add(solver.Sum([product["volume"] * x_upper[product["id"], area["id"]] for product in products]) <= area["volume"] / 2)

# Constraints for fitting product dimensions in the area
for product in products:
    for area in areas:
        if product["width"] > area["width"] or product["height"] > area["height"] or product["depth"] > area["depth"]:
            solver.Add(x_lower[product["id"], area["id"]] == 0)
            solver.Add(x_upper[product["id"], area["id"]] == 0)

# Constraints for weight
for area in areas:
    for product1 in products:
        for product2 in products:
            if product1["weight"] > product2["weight"]:
                solver.Add(x_upper[product1["id"], area["id"]] <= product1["quantity"] * (1 - x_lower[product2["id"], area["id"]]))

# Objective function: Maximize total score
objective_terms = []
for product in products:
    for area in areas:
        objective_terms.append(product["priority"] * area["score"] * x_lower[product["id"], area["id"]])
        objective_terms.append(product["priority"] * area["score"] * x_upper[product["id"], area["id"]])

solver.Maximize(solver.Sum(objective_terms))

# Solve the problem
status = solver.Solve()

# Debug: Check solver status
if status == pywraplp.Solver.OPTIMAL:
    print('Solver found an optimal solution.')
elif status == pywraplp.Solver.FEASIBLE:
    print('Solver found a feasible solution.')
else:
    print('No solution found.')

# Print the solution
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print('Total score = ', solver.Objective().Value(), '\n')
    for product in products:
        for area in areas:
            quantity_lower = x_lower[product["id"], area["id"]].solution_value()
            quantity_upper = x_upper[product["id"], area["id"]].solution_value()
            if quantity_lower > 0:
                print(f'Product {product["id"]} placed in lower part of Area {area["id"]} with quantity {quantity_lower}.')
            if quantity_upper > 0:
                print(f'Product {product["id"]} placed in upper part of Area {area["id"]} with quantity {quantity_upper}.')
    print("\nMaximum score:", solver.Objective().Value())
else:
    print('No solution found.')
