import pandas as pd
import numpy as np


class CarPrice:

    def __init__(self):
        self.df = pd.read_csv("data/data.csv")
        print(f'${len(self.df)} lines loaded')
        print(self.df)

        self.df.columns = self.df.columns.str.lower().str.replace(' ', '_')

        self.string_columns = list(self.df.dtypes[self.df.dtypes == 'object'].index)

        for col in self.string_columns:
            self.df[col] = self.df[col].str.lower().str.replace(' ', '_')

        np.random.seed(2)

        self.n = len(self.df)

        self.n_val = int(0.2 * self.n)
        self.n_test = int(0.2 * self.n)
        self.n_train = self.n - (self.n_val + self.n_test)

        self.idx = np.arange(self.n)
        np.random.shuffle(self.idx)

        self.df_shuffled = self.df.iloc[self.idx]

        self.df_train = self.df_shuffled.iloc[:self.n_train].copy()
        self.df_val = self.df_shuffled.iloc[self.n_train:self.n_train + self.n_val].copy()
        self.df_test = self.df_shuffled.iloc[self.n_train + self.n_val:].copy()

        self.y_train_orig = self.df_train["msrp"].values
        self.y_val_orig = self.df_val["msrp"].values
        self.y_test_orig = self.df_test["msrp"].values

        self.y_train = np.log1p(self.df_train["msrp"].values)
        self.y_val = np.log1p(self.df_val["msrp"].values)
        self.y_test = np.log1p(self.df_test["msrp"].values)

        del self.df_train["msrp"]
        del self.df_val["msrp"]
        del self.df_test["msrp"]

    def trim(self):
        self.df.columns = self.df.columns.str.lower().str.replace(' ', '_')
        string_columns = list(self.df.dtypes[self.df.dtypes == 'object'].index)
        for col in string_columns:
            self.df[col] = self.df[col].str.lower().str.replace(' ', '_')

    def linear_regression(self, X, y):
        ones = np.ones(X.shape[0])
        X = np.column_stack([ones, X])
        xtx = X.T.dot(X)
        xtx_inv = np.linalg.inv(xtx)
        w = xtx_inv.dot(X.T).dot(y)
        return w[0], w[1:]

    def validate(self):
        base = ['engine_cylinders', 'highway_mpg', 'city_mpg', 'popularity']
        base2 = ['transmission_type', 'driven_wheels', 'number_of_doors',
                 'market_category', 'vehicle_size', 'vehicle_style']
        base2_data = self.df_train[base2]
        self.remain = self.df_train[base]
        self.df_train = self.df_train[base]
        self.df_train = self.df_train.fillna(0)
        self.p = self.df_train.values
        w_0, w = self.linear_regression(self.p, self.y_train)
        y_pred = w_0 + self.p.dot(w)
        suggestion = np.expm1(y_pred)
        self.df_train['msrp_pred'] = np.expm1(y_pred)
        self.df_train['msrp'] = np.expm1(self.y_train)

        self.df_train.append(base2_data)

        self.df_train['transmission_type'] = base2_data['transmission_type']
        self.df_train['driven_wheels'] = base2_data['driven_wheels']
        self.df_train['number_of_doors'] = base2_data['number_of_doors']
        self.df_train['market_category'] = base2_data['market_category']
        self.df_train['vehicle_size'] = base2_data['vehicle_size']
        self.df_train['vehicle_style'] = base2_data['vehicle_style']

        print(self.df_train)


c = CarPrice()
c.validate()

