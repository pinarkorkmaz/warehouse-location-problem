Warehouse Location Problem Solver
This repository contains a solution to the warehouse location problem using Google OR-Tools. 
The problem involves placing products into designated areas while maximizing the total score based on the priority of the products and the score of the areas. 
The solution respects constraints on product dimensions, area dimensions, and volumes.

Problem Description
The goal is to allocate products to areas such that the total score is maximized. 
The total score is calculated based on the priority of each product and the score of the area it is placed in. 

The allocation must ensure that:
*Each product is fully placed in one or more areas.
*The total volume of products in any area does not exceed the area's capacity.
*The dimensions of the products fit within the dimensions of the areas.

Installation
To run this project, you need to have Python installed. 
Additionally, you need to install the ortools library. You can install it using pip:
pip install ortools

Usage
1. Clone the repository:
   
git clone https://github.com/pinarkorkmaz/warehouse-location-problem.git
cd warehouse-location-problem

2. Run the script:
python warehouse_location_solver.py

Sample Output
Product P1 has a volume of 6000 cubic units and quantity of 100.
Product P2 has a volume of 9680 cubic units and quantity of 250.
...
Area A1 has a volume of 4378500 cubic units.
Area B1 has a volume of 4378500 cubic units.
...
Solver found an optimal solution.
Total score =  ...
Product P1 placed in Area A1 with quantity ...
...
Maximum score: ...



