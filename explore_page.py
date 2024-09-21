import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map


def clean_experience(x):
    if x ==  'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)

def clean_education(x):
    if 'Bachelor' in x:
        return 'Bachelor\'s degree'
    if 'Master' in x:
        return 'Master\'s degree'
    if 'Professional' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'

@st.cache
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    g_df = df[['Country', 'Employment', 'ConvertedCompYearly', 'YearsCodePro', 'EdLevel']]
    g_df = g_df.rename({'ConvertedCompYearly' : 'SalaryByYearly'}, axis=1)
    g_df= g_df[g_df['SalaryByYearly'].notnull()]
    gf = g_df
    gf= gf.dropna()
    gf = gf[gf['Employment'] == 'Employed, full-time']
    gf = gf.drop('Employment', axis=1)
    country_map = shorten_categories(gf['Country'].value_counts(), 400)
    gf['Country'] = gf['Country'].map(country_map)
    gf['Salary'] = gf['SalaryByYearly']/12
    gf = gf[gf["Salary"] <= 80000]
    gf = gf[gf["Salary"] >= 5000 ]
    gf = gf[gf['Country'] != 'Other']
    gf['YearsCodePro'] = gf['YearsCodePro'].apply(clean_experience)
    gf['EdLevel'] = gf['EdLevel'].apply(clean_education)
    return gf

df = load_data()

def show_explore_page():
    st.title("Explore Software Engineer Salaries")
    st.write(
        """
    ### Stack Overflow Developer Survey 2024
    """
    )
    data = df['Country'].value_counts()
    fig1, ax1 = plt.subplots(figsize=(8, 8))
    # Création du diagramme circulaire avec une police plus grande
    wedges, texts, autotexts = ax1.pie(data, labels=data.index, autopct='%1.1f%%', shadow=True, startangle=90,
                                   pctdistance=0.85, labeldistance=1.1, textprops=dict(color="w"))
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # Personnaliser la taille de la police des labels et des pourcentages
    plt.setp(texts, size=14, weight="bold")
    plt.setp(autotexts, size=12, weight="bold")
    # Ajouter un léger espacement entre les tranches
    plt.tight_layout()
    # Afficher la légende
    ax1.legend(wedges, data.index, title="Labels", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    st.write(fig1)
    st.write(
        """
    #### Mean salary by country
    """
    )
    data = df[['Country', 'Salary']].groupby(['Country']).mean().sort_values('Salary')
    st.bar_chart(data)
    st.write(
        """
    #### Mean salary by experience
    """
    )
    data = df[['YearsCodePro', 'Salary']].groupby(['YearsCodePro']).mean().sort_values('Salary')
    st.line_chart(data)