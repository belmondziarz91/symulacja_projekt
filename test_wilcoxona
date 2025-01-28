import scipy.stats as stats
import pandas as pd

data = {
    "Strategia": [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    "Średni zysk": [
        33476.94, 33706.44, 35291.26, 35411.47, 36661.02, 36905.03,
        34945.88, 35112.61, 36366.28, 36565.97, 37178.98, 37315.19,
        35954.58, 36169.96, 36833.04, 36943.94, 37333.10, 37364.09
    ]
}

df = pd.DataFrame(data)

strategia_0 = df[df["Strategia"] == 0]["Średni zysk"]
strategia_1 = df[df["Strategia"] == 1]["Średni zysk"]

wilcoxon = stats.wilcoxon(strategia_0, strategia_1)
wilcoxon
