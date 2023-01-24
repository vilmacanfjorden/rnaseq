#!/usr/bin/env python
# coding: utf-8

import plotly.express as px
from sklearn.decomposition import PCA
import pandas as pd

# Load dataset from R script
df = pd.read_csv("deseq_all.txt", sep="\t")

# Make 3D PCA plot
fig = px.scatter_3d(
    df, x="PC1", y="PC2", z="PC3",color=df['Treatment'],
    title='All cell lines',
    labels={'0': 'PC 1', '1': 'PC 2', '2': 'PC 3'}
)
fig.show()
fig.write_html("all_pca_3d.html")

