import numpy as np
import pandas as pd

x = 100
c_A, c_B = 20, 30
k_A, k_B = 10, 15
T_A, T_B = 6, 4
sim_days = 31

def distribution_A():
    return round(np.random.normal(50))

def distribution_B():
    return round(np.random.normal(35))

def expired(warehouse, current_day, max_age):
    expired = sum(qty for qty, day in warehouse if current_day - day >= max_age)
    warehouse = [(qty, day) for qty, day in warehouse if current_day - day < max_age]
    return expired, warehouse

def reduce(warehouse, sold):
    remaining = sold
    updated_warehouse = []
    for quantity, day in warehouse:
        if remaining > 0:
            if quantity <= remaining:
                remaining -= quantity
            else:
                updated_warehouse.append((quantity - remaining, day))
                remaining = 0
        else:
            updated_warehouse.append((quantity, day))
    return updated_warehouse

warehouse_A = []
warehouse_B = []
results = []
M_A_prev = 0
M_B_prev = 0

for N in range(sim_days):
    Q_A = int(x * 0.6)
    Q_B = x - Q_A
    warehouse_A.append((Q_A, N))
    warehouse_B.append((Q_B, N))

    P_A, warehouse_A = expired(warehouse_A, N, T_A)
    P_B, warehouse_B = expired(warehouse_B, N, T_B)

    Z_A = distribution_A()
    Z_B = distribution_B()

    S_A = Z_A if M_A_prev >= Z_A else M_A_prev
    S_B = Z_B if M_B_prev >= Z_B else M_B_prev

    warehouse_A = reduce(warehouse_A, S_A)
    warehouse_B = reduce(warehouse_B, S_B)

    M_A = M_A_prev - S_A - P_A + Q_A
    M_B = M_B_prev - S_B - P_B + Q_B
    p_N = S_A * c_A + S_B * c_B
    k_N = Q_A * k_A + Q_B * k_B
    d_N = p_N - k_N

    results.append({
        "pro_A": Q_A,
        "pro_B": Q_B,
        "sol_A": S_A,
        "sol_B": S_B,
        "exp_A": P_A,
        "exp_B": P_B,
        "rem_A": M_A,
        "rem_B": M_B,
        "reve": p_N,
        "cost": k_N,
        "prof": d_N
    })

    M_A_prev, M_B_prev = M_A, M_B

results_df = pd.DataFrame(results)
pd.set_option('display.max_columns', None)
print("Wyniki symulacji:")
print(results_df)

summary = {
    "Całkowity przychód": results_df["reve"].sum(),
    "Całkowity koszt": results_df["cost"].sum(),
    "Całkoiwty zysk": results_df["prof"].sum(),
    "Przeterminowane produkty A": results_df["exp_A"].sum(),
    "Przeterminowane produkty B": results_df["exp_B"].sum()
}

print("\nPodsumowanie symulacji:")
for key, value in summary.items():
    print(f"{key}: {value}")
