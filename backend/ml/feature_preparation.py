# This script is designed to prepare the features 
from dataclasses import dataclass
# Preprocessing and feature engineering
import numpy as np
from sklearn import preprocessing
from sklearn.feature_extraction.text import TfidfVectorizer

import pandas as pd
import json
from ml.salary_prediction_submission import SalaryPredictionSubmission




class FeaturePreprocessor:
    # Attributes
    target_column = 'salary_in_usd'
    vectorizer = TfidfVectorizer()  
    matrix_vectors = None
    model_features = None

    def __init__(self):
        self.fit()

    def fit(self):
        print("Training categorical features...")
        # Load the dataset to prepare the categorizers
        salaries_dataset_url = './ds_salaries.csv'
        full_dataset = pd.read_csv(salaries_dataset_url)
        full_dataset.describe(include='all').T
        self.matrix_vectors = self.vectorizer.fit_transform(full_dataset['job_title'])
        print("   Loading model features...")
        # Load detail models
        with open('model/model_features.json', 'r') as file:
            self.model_features = json.load(file)
        print("Categorical features training done.")
        
    def transform_input(self, submission: SalaryPredictionSubmission):
        df = pd.DataFrame([vars(submission)])
        df['salary_currency_USD'] = 1
        transformed_df = self.feature_engineering(df)   

        all_columns = self.model_features['columns']         
        transformed_df = transformed_df.reindex(columns=all_columns, fill_value=0)
        return transformed_df


    def feature_engineering(self, df):
        #X.drop(X[X.company_location != "US"].index, inplace = True)
        # Encode labels in column 'species'. 
        text_df = self.vectorizer.transform(df['job_title'])
        count_vect_df = pd.DataFrame(text_df.todense(), columns=self.vectorizer.get_feature_names_out())
        df = pd.concat([df, count_vect_df], axis=1)
        df = df.drop('job_title', axis=1)

        # We convert the work year as a categorical feature
        df['work_year'] = df['work_year'].map(str)

        data_with_dummies = pd.get_dummies(df, drop_first=df.shape[0]> 1)
        data_preprocessed = data_with_dummies.replace({True:1, False:0})

        # We apply log on the salary feature
        if 'salary_in_usd' in  data_preprocessed.columns: 
            q_low = data_preprocessed["salary_in_usd"].quantile(0.01)
            q_hi  = data_preprocessed["salary_in_usd"].quantile(0.99)
            data_preprocessed = data_preprocessed[(data_preprocessed["salary_in_usd"] < q_hi) & (data_preprocessed["salary_in_usd"] > q_low)]
        return data_preprocessed
    
    # Import necessary libraries
    def transform_df(self, df):

        # Reorder the salary column and remove the salary and currency columns and ID
        ignored_cols =  ['salary']
        df = df.drop(ignored_cols, axis=1)

        #sns.boxplot(data_preprocessed[self.target_column])
        data_preprocessed = self.feature_engineering(df)
        X = data_preprocessed
        Y = np.log(X[self.target_column])
        X = X.drop(['salary_in_usd'], axis=1)


        return (X, Y)
