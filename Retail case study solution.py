#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import seaborn as sns
import re
get_ipython().run_line_magic('matplotlib', 'inline')
sns.set(style="ticks")


# ###### 1. Merge the datasets Customers, Product Hierarchy and Transactions as Customer_Final. Ensure to keep all customers who have done transactions with us and select the join type accordingly

# In[2]:


Customer= pd.read_csv("E:\Data analysis 360\Assignments\python\Retail case study\Python Foundation Case Study 1 - Retail Case Study\Customer.csv")
Transactions= pd.read_csv("E:\Data analysis 360\Assignments\python\Retail case study\Python Foundation Case Study 1 - Retail Case Study\Transactions.csv")
Product= pd.read_csv("E:\Data analysis 360\Assignments\python\Retail case study\Python Foundation Case Study 1 - Retail Case Study\prod_cat_info.csv")


# In[3]:


Customer.head(2)


# In[4]:


Transactions.head(2)


# In[5]:


Product.head(2)


# In[6]:


merge_1= Transactions.merge(Product, left_on= ['prod_cat_code','prod_subcat_code'], right_on= ['prod_cat_code', 'prod_sub_cat_code'],how= 'left')
merge_1.head(5)


# In[7]:


merge_1.rename(columns={"cust_id" : "customer_Id"}, inplace=True)


# In[8]:


Customer_Final= merge_1.merge(Customer, left_on=["customer_Id"], right_on=["customer_Id"], how= "left")
Customer_Final.head()


# ###### 2. Prepare a summary report for the merged data set.

# In[9]:


#a. Get the column names and their corresponding data types


# In[10]:


Customer_Final.dtypes


# In[11]:


#b.Top/Bottom 10 observations


# In[12]:


Customer_Final.head(10)


# In[13]:


# c. “Five-number summary” for continuous variables (min, Q1, median, Q3 and max)


# In[14]:


Continous_variables= pd.DataFrame()


# In[15]:


Continous_variables= Customer_Final[["Qty", "Rate", "Tax", "total_amt"]]


# In[16]:


Continous_variables.describe()


# In[17]:


#d. Frequency tables for all the categorical variables


# In[18]:


Customer_Final.columns


# In[19]:


categorical_columns= Customer_Final[['prod_subcat_code','prod_cat_code','Store_type','prod_cat', 'prod_subcat','Gender','city_code']]
categorical_columns.head()


# In[20]:


for c in categorical_columns:
    df = pd.DataFrame(Customer_Final.loc[:,str(c)].value_counts().reset_index())
    print(df)


# ###### 3. Generate histograms for all continuous variables and frequency bars for categorical variables

# In[21]:


#Rate

Continous_variables.Rate.hist()


# In[22]:


#total_amt
Continous_variables.total_amt.hist()


# In[23]:


#Tax
Continous_variables.Tax.hist()


# In[24]:


#Qty
Continous_variables.Qty.hist()


# In[25]:


categorical_columns.columns


# In[26]:


#prod_cat_code
categorical_columns.prod_cat_code.value_counts().plot.bar()


# In[27]:


#prod_cat
categorical_columns.prod_cat.value_counts().plot.bar()


# In[28]:


#prod_subcat_code
categorical_columns.prod_subcat_code.value_counts().plot.bar()


# In[29]:


#prod_subcat
categorical_columns.prod_subcat.value_counts().plot.bar()


# In[30]:


#Gender
categorical_columns.Gender.value_counts().plot.bar()


# In[31]:


categorical_columns.city_code.value_counts().plot.bar()


# ##### 4. Calculate the following information using the merged dataset :

# In[32]:


#a. Time period of the available transaction data


# In[33]:


trans = pd.Series(Customer_Final.tran_date.apply(lambda x: x.replace("/", "-")))


# In[34]:


trans= pd.to_datetime(trans, format="%d-%m-%Y")


# In[35]:


trans.sort_values(inplace = True)


# In[36]:


first = trans[trans.size-1]
last = trans[0]
last-first


# In[37]:


#b. Count of transactions where the total amount of transaction was negative


# In[38]:


negative_trans = len(Customer_Final[Customer_Final.total_amt<0].total_amt)
negative_trans


# ##### 5. Analyze which product categories are more popular among females vs male customers.
# 

# In[39]:


Products_Gender = Customer_Final.groupby(['prod_cat', 'Gender'])['transaction_id'].count().reset_index()
Products_Gender.rename(columns = {'transaction_id':'count'}, inplace = True)
Products_Gender


# In[40]:


Gender_Products_max = Products_Gender.groupby('prod_cat')['count'].max()
Gender_Products_max = Products_Gender.merge(Gender_Products_max, on='count', how='right')
Gender_Products_max


# ##### 6. Which City code has the maximum customers and what was the percentage of customers from that city?

# In[41]:


city_count = Customer_Final.groupby('city_code')['transaction_id'].count().reset_index()
city_count


# In[42]:


city_count[city_count.transaction_id == city_count.transaction_id.max()]


# ##### 7. Which store type sells the maximum products by value and by quantity?

# In[43]:


By_Amt= Customer_Final.groupby(["Store_type"])["total_amt"].sum().reset_index()
By_Amt


# In[44]:


By_Amt[By_Amt.total_amt == By_Amt.total_amt.max()]


# In[45]:


By_Qty= Customer_Final.groupby(["Store_type"])["Qty"].sum().reset_index()
By_Qty


# In[46]:


By_Qty[By_Qty.Qty== By_Qty.Qty.max()]


# ##### 8. What was the total amount earned from the "Electronics" and "Clothing" categories from Flagship Stores?

# In[58]:


Value_Cat= Customer_Final.groupby(['Store_type', 'prod_cat'])['total_amt'].sum().reset_index()
Value_Cat


# In[59]:


Flagship= Value_Cat[Value_Cat.Store_type == 'Flagship store']


# In[61]:


Elec_Cloth= Flagship[(Flagship.prod_cat== "Electronics") |(Flagship.prod_cat== "Clothing") ]
Elec_Cloth


# ##### 9. What was the total amount earned from "Male" customers under the "Electronics" category?

# In[67]:


Gender_Prod= Customer_Final.groupby(["prod_cat", 'Gender'])["total_amt"].sum().reset_index()
Gender_Prod


# In[79]:


Male= Gender_Prod[(Gender_Prod.Gender== "M") & (Gender_Prod.prod_cat== "Electronics") ]
Male


# ##### 10. How many customers have more than 10 unique transactions, after removing all transactions which have any negative amounts?

# In[83]:


#positive
postive_trans = Customer_Final[Customer_Final.total_amt>0].reset_index(drop=True)
postive_trans


# In[86]:


#count
transaction_count = postive_trans.groupby('customer_Id')['transaction_id'].count().reset_index()
#more than 10
transaction_count[transaction_count.transaction_id>10]


# ##### 11. For all customers aged between 25 - 35, find out:

# In[87]:


#a. What was the total amount spent for “Electronics” and “Books” product categories?


# In[90]:


Customer_Final.DOB = pd.to_datetime(Customer_Final.DOB, format = "%d-%m-%Y")
DOB = Customer_Final.DOB


# In[92]:


#age
Customer_Final['age'] = DOB.apply(lambda x: pd.to_datetime('today').year-x.year)


# In[106]:


age_bar = Customer_Final[(Customer_Final.age>=25) & (Customer_Final.age<=35)].reset_index(drop=True)
age_bar.head()


# In[96]:


age_cat = age_bar.groupby('prod_cat')['total_amt'].sum().reset_index()
age_cat


# In[97]:


age_cat[(age_cat.prod_cat=='Electronics') | (age_cat.prod_cat=='Books')]


# In[108]:


#b.  What was the total amount spent by these customers between 1st Jan, 2014 to 1st Mar, 2014?


# In[109]:


age_bar.info()


# In[102]:


# common format for all in tran_date for conversion
age_bar.tran_date = age_bar.tran_date.apply(lambda x: x.replace('/', '-'))

#converting tran date to date time
age_bar.tran_date = pd.to_datetime(age_bar.tran_date, format='%d-%m-%Y')


# In[104]:


date_bar = age_bar[(age_bar.tran_date > pd.to_datetime('01-01-2014', format='%d-%m-%Y')) & (age_bar.tran_date<pd.to_datetime('01-03-2014', format='%d-%m-%Y'))].reset_index(drop=True)
date_bar


# In[110]:


date_bar.total_amt.sum()

