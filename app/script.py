import pandas as pd
#import numpy as np
#df = pd.DataFrame(np.random.randn(6, 4), columns=list("ABCD"))
#df.iloc[1][1]
#print(df)
#df.to_feather("data.feather")

def get_data(x):
  df = pd.read_csv(x)
  return df
