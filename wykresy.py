import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = {
    "a_prod_prop": [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    "a_buy_dist": [37.5, 37.5, 37.5, 37.5, 37.5, 37.5, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 42.5, 42.5, 42.5, 42.5, 42.5, 42.5],
    "b_buy_dist": [57.5, 57.5, 60.0, 60.0, 62.5, 62.5, 57.5, 57.5, 60.0, 60.0, 62.5, 62.5, 57.5, 57.5, 60.0, 60.0, 62.5, 62.5],
    "avg": [33476.94, 33706.44, 35291.26, 35411.47, 36661.02, 36905.03, 34945.88, 35112.61, 36366.28, 36565.97, 37178.98, 37315.19, 35954.58, 36169.96, 36833.04, 36943.94, 37333.10, 37364.09]
}

df = pd.DataFrame(data)

sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(2, 2, figsize=(12, 6))

ax = sns.barplot(x="a_prod_prop", y="avg", data=df, errorbar=None, hue="a_prod_prop", palette="muted", legend=False, ax=axes[0, 0])
axes[0, 0].set_title("Średnie 'avg' w zależności od 'a_prod_prop'")
ax.bar_label(ax.containers[0], label_type="center")
ax.bar_label(ax.containers[1], label_type="center")

df = df.groupby(["a_buy_dist", "b_buy_dist"], as_index=False).mean()

sns.lineplot(x="a_buy_dist", y="avg", hue="a_prod_prop", data=data, ax=axes[0, 1], marker="o", palette="muted")
axes[0, 1].set_title("Średnie 'avg' w zależności od 'a_buy_dist'")

sns.lineplot(x="b_buy_dist", y="avg", hue="a_prod_prop", data=data, ax=axes[1, 0], marker="o", palette="muted")
axes[1, 0].set_title("Średnie 'avg' w zależności od 'b_buy_dist'")

pivot = df.pivot(index="a_buy_dist", columns="b_buy_dist", values="avg")
sns.heatmap(pivot, annot=True, fmt=".2f", cmap="YlGnBu", ax=axes[1, 1])
axes[1, 1].set_title("Heatmapa 'avg' dla 'a_buy_dist' i 'b_buy_dist'")

plt.tight_layout()
plt.show()
