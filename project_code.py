# -- coding: utf-8 --
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Initializations
order = []
rating_gen = []
delivery_gen = []
no_of_cust = []
order_value = []
ret_num = []
retention_choice = []
reten_choice_sum = []
del_choice = []
rrr_rr = []
num_of_customers_ini = 30
time = 200

# Calculate number of customers in each time unit
def num_of_customers(num_of_customers_initial):
    change_in_customers = change_cust
    number_of_customers = num_of_customers_initial + change_in_customers
    num_of_customers_initial = number_of_customers
    return number_of_customers

# Generate ratings from the customers
def generate_rating_data(number_of_customers):
    rating_gen = np.random.randint(1,5,number_of_customers)
    return rating_gen

# Generate number of delivery days for the customers    
def generate_delivery_data(number_of_customers):
    delivery_gen = np.random.randint(1,9,number_of_customers)
    return delivery_gen

# Generate order values from the customers
def generate_order_value(number_of_customers):
    orders = np.random.randint(20,200,number_of_customers)
    return orders

# Defining Antecedants and Consequents for the Fuzzification
rating = ctrl.Antecedent(np.arange(1, 6, 1), 'rat')
delivery = ctrl.Antecedent(np.arange(1, 10, 1), 'deli')
retention_rate = ctrl.Consequent(np.arange(0, 12, 1), 'reten')

# Membership function for the Rating
rating['poor'] = fuzz.trapmf(rating.universe, [1, 1, 2, 3])
rating['average'] = fuzz.trimf(rating.universe, [2, 3, 4])
rating['good'] = fuzz.trapmf(rating.universe, [3, 4, 5, 5])

# Membership function for the number of Delivery days
delivery['good'] = fuzz.trapmf(delivery.universe, [1, 1, 3, 5])
delivery['average'] = fuzz.trimf(delivery.universe, [3, 5, 7])
delivery['poor'] = fuzz.trapmf(delivery.universe, [5, 7, 9, 9])

# Membership function for the Retention Rate
retention_rate['poor'] = fuzz.trapmf(retention_rate.universe, [0, 0, 1, 2])
retention_rate['poor_average'] = fuzz.trimf(retention_rate.universe, [2, 4, 6])
retention_rate['average'] = fuzz.trimf(retention_rate.universe, [4, 6, 8])
retention_rate['good_average'] = fuzz.trimf(retention_rate.universe, [6, 8, 10])
retention_rate['good'] = fuzz.trapmf(retention_rate.universe, [8, 10, 11, 11])

# Define the rules
rule1 = ctrl.Rule(rating['poor'], retention_rate['poor'])
rule2 = ctrl.Rule(rating['average'] & delivery['poor'], retention_rate['poor_average'])
rule3 = ctrl.Rule(rating['average'] & delivery['average'], retention_rate['average'])
rule4 = ctrl.Rule(rating['average'] & delivery['good'], retention_rate['good_average'])
rule5 = ctrl.Rule(rating['good'] & delivery['poor'], retention_rate['average'])
rule6 = ctrl.Rule(rating['good'] & delivery['average'], retention_rate['good_average'])
rule7 = ctrl.Rule(rating['good'] & delivery['good'], retention_rate['good'])

customer_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7])
retention_rate_customers = ctrl.ControlSystemSimulation(customer_ctrl)

# Compute Retention Rate
def retention_compute(rating_gen, delivery_gen):
    retention_rate_customers.input['rat'] = rating_gen
    retention_rate_customers.input['deli'] = delivery_gen
    retention_rate_customers.compute()
    global rrr_rr
    rrr = retention_rate_customers.output['reten']
    rrr_rr.append(rrr)
    return retention_rate_customers.output['reten']

# Main function call
def main_loop(num_of_customers_ini):
    global no_of_cust_atm
    no_of_cust_atm = num_of_customers(num_of_customers_ini)
    no_of_cust.append(no_of_cust_atm)
    
    rat_gen = generate_rating_data(no_of_cust_atm)
    del_gen = generate_delivery_data(no_of_cust_atm)
    order_value_atm = generate_order_value(no_of_cust_atm)
    order_value.append(sum(order_value_atm))
    
    for i in range(1,no_of_cust_atm):
        ret_num_atm = retention_compute(rat_gen[i],del_gen[i])
        ret_num.append(round(ret_num_atm))
    return ret_num

global change_cust
change_cust = 0
global ret_n
ret_n = []

# Main loop
for ind_i in range(1,time):
    retention_choice = main_loop(num_of_customers_ini)
    cust_loss_choice = round(no_of_cust_atm*0.1)
    temp_value = round(sum(retention_choice)/100)
    value = round(np.sqrt(temp_value)) - np.random.randint(1,3)
    change_cust = value-cust_loss_choice
    ret_n.append(value)
    reten_choice_sum.append(change_cust)

# Plots
#plt.plot(reten_choice_sum)
#plt.plot(ret_n)
plt.plot(order_value)
plt.title("Order Value over time(After Improvement)")
plt.xlabel("Time")
plt.ylabel("Order Value")