import pandas as pd
import numpy as np
from fbprophet import Prophet

df = pd.read_csv('outdoor-temperature-hourly.csv')
df = df[df.temperature != 'DIFF']