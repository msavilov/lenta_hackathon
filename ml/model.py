import numpy as np
import pandas as pd

from model import forecast
from prophet import Prophet
from sklearn.ensemble import RandomForestRegressor

# Load the model
model = RandomForestRegressor()
model.load_model('models/trained_model.joblib')
model_pr = Prophet()
model_pr.load_model('models/trained_model_pr.joblib')

"""
train - данные за прошедший период
test - данные, которые необходимо предсказать на 2 недели
"""


def train(train, test):
    """
    Здесь мы формируем дополнительные признаки и добавляем колонки,
    по которым отделим трейн и тест,
    чтобы подать в модель только тест из запроса
    """
    train['num'] = range(len(train))
    test['num'] = range(len(test))
    train['type_df'] = 'train'
    test['type_df'] = 'test'
    test['pr_sales_type_id'] = 0
    test[['pr_sales_in_rub', 'pr_sales_in_units']] = 0
    rub = train[train['pr_sales_type_id'] == 0].pivot_table(
        index='pr_sku_id', values='pr_sales_in_rub_id', aggfunc='last')

    test = test.merge(rub, on='pr_sku_id', how='left').set_index(test.index)

    train = train.append(test)
    train = train[train['st_is_active'] == 1]
    train['pr_sales_in_rub_id'] = round(train['pr_sales_in_rub']
                                        / train['pr_sales_in_units'], 1)
    train = train.fillna(0)
    return train


def make_features(df_mf, max_lag, rolling_mean_size):
    """
    Создаем объекты временных рядов на основе индекса временных рядов.
    """
    df_mf_full_list = []
    for s in df_mf['pr_sales_type_id'].unique():
        df_mf_temp = df_mf.loc[df_mf['pr_sales_type_id'] == s].copy()

        df_mf_temp['day'] = df_mf_temp.index.day
        df_mf_temp['dayofweek'] = df_mf_temp.index.dayofweek
        df_mf_temp['month'] = df_mf_temp.index.month
        df_mf_temp['sin_dayofweek'] = np.sin(df_mf_temp['dayofweek']
                                             * np.pi * 2
                                             / np.max(df_mf_temp['dayofweek']))
        df_mf_temp['sin_month'] = np.sin(df_mf_temp['month'] * np.pi * 2
                                         / np.max(df_mf_temp['month']))
        df_mf_temp['sin_day'] = np.sin(df_mf_temp['day'] * np.pi * 2
                                       / np.max(df_mf_temp['day']))
        df_mf_temp['cos_dayofweek'] = np.cos(df_mf_temp['dayofweek']
                                             * np.pi * 2
                                             / np.max(df_mf_temp['dayofweek']))
        df_mf_temp['cos_month'] = np.cos(df_mf_temp['month'] * np.pi * 2
                                         / np.max(df_mf_temp['month']))
        df_mf_temp['cos_day'] = np.cos(df_mf_temp['day'] * np.pi * 2
                                       / np.max(df_mf_temp['day']))

        lags = list(range(14, max_lag + 1))
        for lag in lags:
            df_mf_temp['sales_lag_' + str(lag)] = df_mf_temp.groupby(
                ["st_id", "pr_sku_id"])['pr_sales_in_units'].transform(
                lambda x: x.shift(lag))

        df_mf_temp['rolling_mean_units'] = df_mf_temp.groupby(
            ["st_id", "pr_sku_id"])['pr_sales_in_units'].transform(
            lambda x: x.shift(14).rolling(rolling_mean_size).mean())

        df_mf_full_list.append(df_mf_temp)
    df_mf_full = pd.concat(df_mf_full_list)
    df_mf_full = df_mf_full.drop(columns=['day', 'dayofweek', 'month'])
    return df_mf_full


def prophet(df):
    test_p_f = df[df['type_df'] == 'test']
    train_p_f = df[df['type_df'] == 'train']

    train_p_f = train_p_f.sort_values(by='num', ascending=True)
    test_p_f = test_p_f.sort_values(by='num', ascending=True)

    pr_train = train_p_f.reset_index().sort_values(by=['st_id',
                                                       'pr_sku_id',
                                                       'date'])
    pr_train['st_pr_sku'] = pr_train['st_id'] + ' ' + pr_train['pr_sku_id']
    pr_train = pr_train.rename(columns={'date': 'ds',
                                        'pr_sales_in_units': 'y'})

    pr_test = test_p_f.reset_index().sort_values(
        by=['st_id', 'pr_sku_id', 'date'])
    pr_test['st_pr_sku'] = (pr_test['st_id']
                            + ' ' + pr_test['pr_sku_id'])
    pr_test = pr_test.rename(columns={'date': 'ds'})
    pr_df_mf = df.reset_index().sort_values(by=['st_id', 'pr_sku_id', 'date'])
    pr_df_mf['st_pr_sku'] = df['st_id'] + ' ' + df['pr_sku_id']

    p = list()
    short_time_series = 0
    for id in pr_train['st_pr_sku'].unique():
        # профет не предсказывает для рядов с менее чем 2-мя измерениями
        if len(pr_train.loc[pr_train['st_pr_sku'] == id]) > 2:
            train_ = pr_train.loc[pr_train['st_pr_sku'] == id]
            test_ = pr_test.loc[pr_test['st_pr_sku'] == id]
            model_pr.fit(train_)
            future = model_pr.make_future_dataframe(periods=14)
            future = future.merge(test_[['ds']], on='ds', how='left')
            forecast = model_pr.predict(future)
            forecast['st_pr_sku'] = id
            p.append(forecast[['ds', 'st_pr_sku', 'trend', 'yearly',
                               'weekly', 'yhat']])
        else:
            short_time_series += len(pr_train.loc[pr_train['st_pr_sku'] == id])

    p = pd.concat(p, ignore_index=True)
    p['yhat'] = p['yhat'].clip(lower=0)
    p = p.rename(columns={'ds': 'date'})
    p.drop_duplicates(inplace=True)

    df_mf_full = pr_df_mf.merge(p, on=['date', 'st_pr_sku'], how='left')
    df_mf_full.drop(columns='st_pr_sku', inplace=True)

    prophet_features = ['trend', 'yearly', 'weekly', 'yhat']
    for feature in prophet_features:
        df_mf_full[feature] = df_mf_full[feature].fillna(0)
    return df_mf_full


def holydays(df, holydays_df):

    holydays_df['date'] = holydays_df['calday'].astype(str).apply(
        lambda x: x[:4] + '-' + x[4:6] + '-' + x[6:8])
    holydays_df['date'] = pd.to_datetime(holydays_df['date'])
    holydays_df = holydays_df[holydays_df['year'] >= 2022]
    holydays_df = holydays_df[['date', 'holiday']]

    holydays_df['new_year'] = 0
    holydays_df.loc[((holydays_df['date'] >= '2022-12-30')
                     & (holydays_df['date'] <= '2023-01-01')), 'new_year'] = 1
    holydays_df['easter'] = 0
    holydays_df.loc[((holydays_df['date'] >= '2023-04-14')
                     & (holydays_df['date'] <= '2023-04-16')), 'easter'] = 1
    df = df.merge(holydays_df, on='date', how='left')
    return df


def mean(train_m):
    """ Здесь мы кодируем данные средней"""
    features_cat = ['st_id', 'st_city_id', 'st_division_code', 'pr_sku_id',
                    'pr_group_id', 'pr_cat_id', 'pr_subcat_id', 'type_df']

    """
    Создаем словарь для хранения средних значений по
    каждой категории в каждом признаке.
    """
    mean_encoding_dict = {}

    # Значение по умолчанию для новых категорий
    default_value = 0  # Думаю логично использовать 0

    # Проходимся по каждому категориальному признаку
    for feature in features_cat:
        # Вычисляем средние продажи для каждой категории в текущем признаке
        mean_encoding_dict[feature] = train_m.groupby(
            feature)['pr_sales_in_units'].mean()
        # Добавляем значение по умолчанию для новых категорий
        mean_encoding_dict[feature].fillna(default_value, inplace=True)
    # Применяем Mean Encoding к обучающему набору данных
    for feature in features_cat:
        train_m[feature + '_mean_encoded'] = train_m[feature].map(
            mean_encoding_dict[feature])

    """
    Удаляем исходные категориальные признаки, так как мы
    их заменили закодированными значениями
    """
    train_m.drop(features_cat, axis=1, inplace=True)
    # Теперь features содержит закодированные признаки для обучения
    return train_m


def predict(train_m):
    """
    Здесь данные мы уже конечные отбираем
    удаляем лишнее и загоняем в модель.
    """
    train_m = train_m.fillna(0)
    test_final = train_m[train_m['type_df'] == 'test']
    test_final = test_final.sort_values(by='num', ascending=True)
    test_final = test_final.drop([
        'pr_sales_in_rub',
        'pr_sales_in_units',
        'num',
        'type_df'], axis=1)
    predict = model.predict(test_final)
    return predict

def forecast(sales, item_info, store):
    """
    Обобщающая функция
    """
    """Необходимо написать реализацию для перевода
    sales, item_info, store в df_train, df_test
    """

    train = train(df_train, df_test)
    train_mf = make_features(train, 28, 14)
    train_p = prophet(train_mf)
    train_h = holydays(train_p, holydays)
    train_fin = mean(train_h)
    predict = predict(train_fin)
    return predict
