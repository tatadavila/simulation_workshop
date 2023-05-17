from django.shortcuts import render
from .models import Product, MonthlyDemand
import random
import numpy as np


def demand_simulation(request):
    simulation_duration = 24

    initial_inventory = {"Product 1": 100, "Product 2": 200, "Product 3": 80}
    sales_price = {"Product 1": 1800, "Product 2": 25000, "Product 3": 1500}
    acquisition_costs = {"Product 1": 9500, "Product 2": 15000, "Product 3": 8400}
    breach_costs = {"Product 1": 750, "Product 2": 930, "Product 3": 699}
    storage_cost = 500

    sales = {"Product 1": [], "Product 2": [], "Product 3": [], "Total": []}
    demand = {"Product 1": [], "Product 2": [], "Product 3": []}
    inventory = {"Product 1": [], "Product 2": [], "Product 3": []}
    service_level = 0
    average_net_income = 0
    net_income = []
    service_level = 0

    for month in range(1, simulation_duration + 1):
        product_demand_1 = random.randint(40, 60)
        product_demand_2 = np.random.poisson(6 * 30)
        product_demand_3 = random.choices(
            [50, 51, 52, 53, 54, 55, 56, 57, 58, 59],
            [0.05, 0.1, 0.2, 0.05, 0.1, 0.2, 0.05, 0.1, 0.1, 0.05],
        )[0]

        actual_inventory = initial_inventory.copy()

        if month % 2 == 1:
            if actual_inventory["Product 1"] < 70:
                actual_inventory["Product 1"] += 70
            if actual_inventory["Product 2"] < 100:
                actual_inventory["Product 2"] += 100
            if actual_inventory["Product 3"] < 120:
                actual_inventory["Product 3"] += 120

        month_sales = {
            "Product 1": min(product_demand_1, actual_inventory["Product 1"]),
            "Product 2": min(product_demand_2, actual_inventory["Product 2"]),
            "Product 3": min(product_demand_3, actual_inventory["Product 3"]),
        }

        month_demand = {
            "Product 1": product_demand_1,
            "Product 2": product_demand_2,
            "Product 3": product_demand_3,
        }

        for product in month_sales:
            actual_inventory[product] -= month_sales[product]

        for product in month_sales:
            sales[product].append(month_sales[product])
            demand[product].append(month_demand[product])
            inventory[product].append(sum(actual_inventory.values()))

        month_acquisition_cost = sum(
            acquisition_costs[product] * month_sales[product] for product in month_sales
        )

        month_breach_cost = sum(
            (month_demand[product]) - month_sales[product] * breach_costs[product]
            for product in month_sales
        )

        month_storage_cost = sum(
            actual_inventory[product] * storage_cost for product in actual_inventory
        )

        # month_gross_profit = (
        #     sales_price["Product 1"] * sales["Product 1"][month - 1]
        #     + sales_price["Product 2"] * sales["Product 2"][month - 1]
        #     + sales_price["Product 3"] * sales["Product 3"][month - 1]
        #     - month_acquisition_cost
        #     - month_storage_cost
        #     - month_breach_cost
        # )

        sales["Total"].append(sum(month_sales.values()))

        service_level += month_sales[product] / month_demand[product]

        month_net_income = (
            month_sales["Product 1"]
            * (sales_price["Product 1"] - acquisition_costs["Product 1"])
            + month_sales["Product 2"]
            * (sales_price["Product 2"] - acquisition_costs["Product 2"])
            + month_sales["Product 3"]
            * (sales_price["Product 3"] - acquisition_costs["Product 3"])
            - month_storage_cost
            - month_breach_cost
        )

        net_income.append(month_net_income)

    average_service_level = service_level / simulation_duration
    average_net_income = sum(net_income) / simulation_duration

    context = {
        "simulation_duration": simulation_duration,
        "simulation_duration_range": range(1, simulation_duration + 1),
        "sales": sales,
        "demand": demand,
        "inventory": inventory,
        "average_service_level": average_service_level,
        "average_net_income": average_net_income,
    }

    return render(request, "simulation.html", context)
