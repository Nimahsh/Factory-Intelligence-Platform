import streamlit as st

st.write("1 - Streamlit OK")

import pandas as pd
st.write("2 - Pandas OK", pd.__version__)

import numpy as np
st.write("3 - NumPy OK", np.__version__)

import plotly.express as px
import plotly.graph_objects as go
st.write("4 - Plotly OK")

import jdatetime
st.write("5 - jdatetime OK")

st.success("All imports loaded successfully.")