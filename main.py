import numpy as np
import pandas as pd


class Factory:
    x = 100
    c_A, c_B = 20, 30 # cena sprzedarzy produktow
    k_A, k_B = 10, 15 # koszt wytworzenia produktow
    T_A, T_B = 6, 4 # czas warznosci
    sim_days = 31 # ilosc symulowanych dni

    a_proportion = None
    distribution_A = None
    distribution_B = None

    @staticmethod
    def expired(warehouse, current_day, max_age):
        expired = sum(qty for qty, day in warehouse if current_day - day >= max_age)
        warehouse = [(qty, day) for qty, day in warehouse if current_day - day < max_age]
        return expired, warehouse

    @staticmethod
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

    def simulate(self):
        # listy z prduktami i dniem w którym zostały wytworzone
        warehouse_A = []
        warehouse_B = []

        # ilosc nieprzeterminowanych produktow na koncu ZESZŁEGO dnia / poczatku TEGO dnia
        M_A_prev = 0
        M_B_prev = 0

        results = []

        for N in range(self.sim_days):
            # ilość wytworzonych produktów
            Q_A = int(self.x * self.a_proportion(M_A_prev, M_B_prev, self.x))
            Q_B = self.x - Q_A

            warehouse_A.append((Q_A, N))
            warehouse_B.append((Q_B, N))

            # ilość przeterminowanych produktów tego dani
            P_A, warehouse_A = self.expired(warehouse_A, N, self.T_A)
            P_B, warehouse_B = self.expired(warehouse_B, N, self.T_B)

            # ilość produktów którą chcą kupić klienci
            Z_A = self.distribution_A()
            Z_B = self.distribution_B()

            # ilość produktów którą sprzedaliśmy
            S_A = Z_A if M_A_prev >= Z_A else M_A_prev
            S_B = Z_B if M_B_prev >= Z_B else M_B_prev

            warehouse_A = self.reduce(warehouse_A, S_A)
            warehouse_B = self.reduce(warehouse_B, S_B)

            # stan magazynu na KOŃCU tego dnia
            M_A = M_A_prev - S_A - P_A + Q_A
            M_B = M_B_prev - S_B - P_B + Q_B

            
            p_N = S_A * self.c_A + S_B * self.c_B # przychud tego dnia
            k_N = Q_A * self.k_A + Q_B * self.k_B # koszty tego dnia
            d_N = p_N - k_N # dochud tego dnia

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

        return results


def summarize(results_df):
    return {
        "Całkowity przychód": results_df["reve"].sum(),
        "Całkowity koszt": results_df["cost"].sum(),
        "Całkoiwty zysk": results_df["prof"].sum(),
        "Przeterminowane produkty A": results_df["exp_A"].sum(),
        "Przeterminowane produkty B": results_df["exp_B"].sum()
    }


# jakaś przykładowa funkcja
# oblicza w jakiej proporcji produkować, aby warehouse_A/warehouse_B = expected_proportion.
# amount - max liczba produkcji
def a_const_warehouse_prop(war_a, war_b, exp_prop, amount):
    xa = min(max(round((exp_prop * (war_b + amount) - war_a) / (1 + exp_prop)), 0), amount)
    return xa/amount


# wartości do uruchomienia symulacji (każdy z każdym)
a_buy_dist = [37.5, 40, 42.5]
b_buy_dist = [57.5, 60, 62.5] 
a_prod_prop = [
    lambda a_dist, b_dist: lambda a_amo, b_amo, total_prod : a_dist/(a_dist+b_dist),
    lambda a_dist, b_dist: lambda a_amo, b_amo, total_prod: a_const_warehouse_prop(a_amo, b_amo, a_dist/b_dist, total_prod)
    ]

sim_count = 500 # ile razy uruchamiać każdy przypadek
simulation_output = [] # wyniki symulacja (śr przychód) dla każdego przypadku

print("Simulation is running...")

for ad in a_buy_dist:
    for bd in b_buy_dist:
        for ap_i in range(len(a_prod_prop)):
            f = Factory()

            f.distribution_A = lambda: np.random.poisson(ad)
            f.distribution_B = lambda: np.random.poisson(bd)
            f.a_proportion = a_prod_prop[ap_i](ad, bd)

            results = []    
            for i in range(sim_count):
                results.append(pd.DataFrame(f.simulate()))

            avg = sum(map(lambda df: df["prof"].sum(), results)) / sim_count

            simulation_output.append(
                {
                    "a_prod_prop": ap_i, # indeks sposobu doboru prokorcji
                    "a_buy_dist": ad,
                    "b_buy_dist": bd,
                    "avg": avg
                }
            )


print("Finished!")
print(pd.DataFrame(simulation_output))
              

# ---------------------------------------------------------------
# OLD CODE
# ---------------------------------------------------------------
# różne przypadki do sprawdzenia
# cases = [
#     {
#         "prop": lambda a, b, amount: 4/6,
#         "a_buy_dis": lambda: np.random.binomial(40, 0.8),
#         "b_buy_dis": lambda: np.random.binomial(60, 0.8)
#     },
#     {
#         "prop": lambda a, b, amount: 6/4,
#         "a_buy_dis": lambda: np.random.binomial(40, 0.8),
#         "b_buy_dis": lambda: np.random.binomial(60, 0.8)
#     },
#     {
#         "prop": lambda a, b, amount: 0.4,
#         "a_buy_dis": lambda: np.random.binomial(40, 0.8),
#         "b_buy_dis": lambda: np.random.binomial(60, 0.8)
#     },
#     {
#         "prop": lambda a, b, amount: 0.6,
#         "a_buy_dis": lambda: np.random.binomial(40, 0.8),
#         "b_buy_dis": lambda: np.random.binomial(60, 0.8)
#     },
#     {
#         "prop": lambda a, b, amount: a_const_warehouse_prop(a, b, 4/6, amount),
#         "a_buy_dis": lambda: np.random.binomial(40, 0.8),
#         "b_buy_dis": lambda: np.random.binomial(60, 0.8)
#     },
#     {
#         "prop": lambda a, b, amount: a_const_warehouse_prop(a, b, 6/4, amount),
#         "a_buy_dis": lambda: np.random.binomial(40, 0.8),
#         "b_buy_dis": lambda: np.random.binomial(60, 0.8)
#     }
# ]
# sim_output = [] # lista, która składa się z list data frame'ów z wynikami danej symulacji. sim_output[nr_przypadku][nr_data_frame]

# for i in range(len(cases)):
#     f = Factory()
#     f.a_proportion = cases[i]["prop"]
#     f.distribution_A = cases[i]["a_buy_dis"]
#     f.distribution_B = cases[i]["b_buy_dis"]

#     results = []
#     for j in range(sim_count):
#         results.append(pd.DataFrame(f.simulate()))

#     sim_output.append(results)

#     # średni zysk dla danego przypadku
#     avg = sum(map(lambda df: df["prof"].sum(), results)) / sim_count
#     print(f"{i}: {avg}")


# results_df = pd.DataFrame(f.simulate())
# pd.set_option('display.max_columns', None)
# print("Wyniki symulacji:")
# print(results_df)

# summary = summarize(results_df)

# print("\nPodsumowanie symulacji:")
# for key, value in summary.items():
#     print(f"{key}: {value}")
