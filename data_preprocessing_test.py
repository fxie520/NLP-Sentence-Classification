import pandas as pd

balanced = 0  # 0/1: generate imbalanced/balanced train set + imbalanced eval set
train_amount = 10000
eval_amount = 10000
RANDOM_SEED = 42
RANDOM_SEED_2 = 21
pd.set_option("display.max_rows", 100, "display.max_columns", None, "max_colwidth", 100)

# df = pd.read_csv("./Datasets/Test_orig.tsv", sep='\t', encoding='utf-8')
df = pd.read_csv("./Datasets/Test_processed.csv", encoding='utf-8')
df = df.sample(frac=1, random_state=RANDOM_SEED).reset_index(drop=True)  # Shuffle the DataFrame rows then reset indices
df = df.sample(frac=1, random_state=RANDOM_SEED_2).reset_index(drop=True)

df['IsTypeOne'] = 0
df.loc[df['类别'] == 0, 'IsTypeOne'] = 1
df['IsTypeTwo'] = 0
df.loc[df['类别'] == 1, 'IsTypeTwo'] = 1

df_eval = df[['2', 'IsTypeOne']][0:eval_amount]  # For validation and testing
df = df.drop(df_eval.index)  # Make sure the data used for eval are not seen during training
df_eval = df_eval.rename(columns={"IsTypeOne": "IsType"})
df_eval.to_csv('./Datasets/Eval_1.csv', index=False, quoting=2)

df_eval = df[['2', 'IsTypeTwo']][0:eval_amount]
df = df.drop(df_eval.index)
df_eval = df_eval.rename(columns={"IsTypeTwo": "IsType"})
df_eval.to_csv('./Datasets/Eval_2.csv', index=False, quoting=2)

if balanced:
    df_train_pos = df[df['IsTypeOne'] == 1][['2', 'IsTypeOne']][0:train_amount / 2]
    df_train_neg = df[df['IsTypeOne'] == 0][['2', 'IsTypeOne']][0:train_amount / 2]
    df_train = df_train_pos.append(df_train_neg, ignore_index=True)
    df_train = df_train.sample(frac=1, random_state=RANDOM_SEED)
    df_train = df_train.rename(columns={"IsTypeOne": "IsType"})
    df_train.to_csv('./Datasets/Train_1.csv', index=False, quoting=2)

    df_train_pos = df[df['IsTypeTwo'] == 1][['2', 'IsTypeTwo']][0:train_amount / 2]
    df_train_neg = df[df['IsTypeTwo'] == 0][['2', 'IsTypeTwo']][0:train_amount / 2]
    df_train = df_train_pos.append(df_train_neg, ignore_index=True)
    df_train = df_train.sample(frac=1, random_state=RANDOM_SEED)
    df_train = df_train.rename(columns={"IsTypeTwo": "IsType"})
    df_train.to_csv('./Datasets/Train_2.csv', index=False, quoting=2)
else:
    df_train = df[['2', 'IsTypeOne']][0:train_amount]
    df_train = df_train.rename(columns={"IsTypeOne": "IsType"})
    df_train.to_csv('./Datasets/Train_1.csv', index=False, quoting=2)

    df_train = df[['2', 'IsTypeTwo']][0:train_amount]
    df_train = df_train.rename(columns={"IsTypeTwo": "IsType"})
    df_train.to_csv('./Datasets/Train_2.csv', index=False, quoting=2)
