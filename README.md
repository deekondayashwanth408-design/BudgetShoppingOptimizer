# 🛒 Budget Shopping Optimizer

A Streamlit app that helps you choose a set of products within a budget while maximizing their combined utility. It compares a fast Greedy approach with the 0/1 Knapsack dynamic programming algorithm.

## Features

- Set minimum, maximum, and current budgets in rupees.
- Add products with a name, price, and utility score.
- View each product’s utility-to-price ratio.
- Remove products from the catalog.
- Compare product selections from the Greedy and 0/1 Knapsack algorithms.
- Review the recommended shopping list, total cost, total utility, and remaining budget.
- View budget utilization and algorithm comparison charts.

The app starts with a sample catalog of six products. Products you add or remove are kept in Streamlit session state for the current session.

## Algorithms

### Greedy

Sorts products by utility-to-price ratio, from highest to lowest, then adds each product if it fits within the remaining budget. It is quick, but may not find the combination with the highest total utility.

### 0/1 Knapsack

Uses dynamic programming to find the combination with the highest total utility without exceeding the budget. Each product can be selected at most once.

Its time and memory complexity are **O(n × B)**, where `n` is the number of products and `B` is the budget in rupees. Runtime and memory use can grow significantly with large budgets.

## Requirements

- Python 3.9 or later
- Streamlit

## Run locally

1. Clone the repository and open its folder:

   ```bash
   git clone https://github.com/YOUR-USERNAME/Budget-Shopping-Optimizer.git
   cd Budget-Shopping-Optimizer