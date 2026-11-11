from sklearn.model_selection import train_test_split

def prepare_data(df):
    train, test = train_test_split(df, test_size=0.3, random_state=42)
    
    df_out = df.copy()
    df_out["split"] = "train"
    df_out.loc[test.index, "split"] = "test"
    
    return df_out