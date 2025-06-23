#Import biliotek
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import scipy.stats as stats
from statsmodels.stats.stattools import durbin_watson
from statsmodels.stats.outliers_influence import variance_inflation_factor
import pandas as pd
import statsmodels.api as sm

# 1. Wczytaj dane
df = pd.read_csv("Cars_dataset.csv")

# 2. Wybierz kolumny do modelu
columns_to_use = [
    #'Brand',
    #'Model',
    'Fuel',
    'Mileage',
    'Year',
    'Transmission',
    'HP'
    ]
target_column = 'Price'

# 3. Podziel dane na X i y
X = df[columns_to_use]
y = df[target_column]

# 4. Zakoduj zmienne kategoryczne (One-Hot Encoding)
X = pd.get_dummies(X, drop_first=True)

# Dodaj kolumnę interceptu
X_const = sm.add_constant(X)

# Upewnij się, że dane są liczbowe
y = y.astype(float)
X_const = X_const.astype(float)

# Tworzymy model OLS
model_sm = sm.OLS(y, X_const).fit()

# Wyświetlamy pełne statystyki regresji
print(model_sm.summary())


# Zakładam, że X to Twoja macierz cech (przed dodaniem stałej):
# Dodaj kolumnę stałej (interceptu)
X_const = sm.add_constant(X)

# Upewnij się, że wszystko jest typu float
X_const = X_const.astype(float)

# Obliczamy VIF
vif_data = pd.DataFrame()
vif_data["Feature"] = X_const.columns
vif_data["VIF"] = [variance_inflation_factor(X_const.values, i) for i in range(X_const.shape[1])]

print(vif_data)

# Obliczamy reszty
residuals = model_sm.resid
fitted_vals = model_sm.fittedvalues

# 1. Wykres reszt vs wartości dopasowane
plt.figure(figsize=(8, 6))
sns.residplot(x=fitted_vals, y=residuals, lowess=True, line_kws={'color': 'red'})
plt.xlabel('Wartości dopasowane (fitted values)')
plt.ylabel('Reszty')
plt.title('Reszty vs wartości dopasowane')
plt.axhline(0, color='black', linestyle='--')
plt.show()

# 2. Histogram reszt + krzywa normalna
plt.figure(figsize=(8, 6))
sns.histplot(residuals, kde=True, stat="density", bins=30)
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = stats.norm.pdf(x, residuals.mean(), residuals.std())
plt.plot(x, p, 'k', linewidth=2, label='Rozkład normalny')
plt.title('Histogram reszt')
plt.xlabel('Reszty')
plt.ylabel('Gęstość')
plt.legend()
plt.show()

# 3. Q-Q plot reszt
plt.figure(figsize=(8, 6))
stats.probplot(residuals, dist="norm", plot=plt)
plt.title("Q-Q plot reszt")
plt.show()

# 4. Test Durbin-Watsona (autokorelacja reszt)
dw_stat = durbin_watson(residuals)
print(f"Statystyka Durbin-Watsona: {dw_stat:.4f}")

'''
# Kopia X do tworzenia interakcji
X_inter = X.copy()

# Tworzymy kolumny z interakcjami
#X_inter['Year_HP'] = X['Year'] * X['HP']
#X_inter['Mileage_HP'] = X['Mileage'] * X['HP']
#X_inter['Fuel_Electric_HP'] = X['Fuel_Electric'] * X['HP']
#X_inter['Fuel_LPG_Mileage'] = X['Fuel_LPG'] * X['Mileage']
#X_inter['Transmission_Manual_HP'] = X['Transmission_Manual'] * X['HP']

# Dodaj kolumnę stałej (intercept)
X_const_inter = sm.add_constant(X_inter)

# Konwersja na typ float
X_const_inter = X_const_inter.astype(float)
y = y.astype(float)

# Tworzenie i trenowanie modelu
model_inter = sm.OLS(y, X_const_inter).fit()

# Podsumowanie modelu
print(model_inter.summary())
'''

X_inter = X.copy()

# Dodajemy interakcje
X_inter['Year_HP'] = X_inter['Year'] * X_inter['HP']
X_inter['Mileage_HP'] = X_inter['Mileage'] * X_inter['HP']

# Dodaj kolumnę interceptu
X_inter_const = sm.add_constant(X_inter)

# Upewnij się, że wszystkie dane są float
X_inter_const = X_inter_const.astype(float)
y = y.astype(float)

# Budujemy model regresji liniowej z interakcjami
model_inter = sm.OLS(y, X_inter_const).fit()

# Wyświetlamy podsumowanie modelu
print(model_inter.summary())

def print_regression_equation(model):
    params = model.params
    equation = f"Y = {params['const']:.4f}"
    
    for feature, coef in params.items():
        if feature == 'const':
            continue
        sign = " + " if coef >= 0 else " - "
        coef_abs = abs(coef)
        equation += f"{sign}{coef_abs:.4f} * {feature}"
    
    print(equation)

# Przykład użycia:
print_regression_equation(model_sm)
