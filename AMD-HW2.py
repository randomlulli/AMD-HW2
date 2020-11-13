''' insert the assignamnet introduction '''

''' the importation of library and the reading of document '''
from collections import OrderedDict
import pandas as pd
import pandasql as ps
import matplotlib.pyplot as plt
from operator import itemgetter

ds_Oct = pd.read_csv('D:/Storage file PC/Documenti/Università/Data Science/Anno 1/Semestre 1/Algorthmic\
     Methods of Data Mining/Homeworks/HW2/2019-Oct.csv', parse_dates=['event_time'], date_parser=pd.to_datetime)
ds_Nov = pd.read_csv('D:/Storage file PC/Documenti/Università/Data Science/Anno 1/Semestre 1/Algorthmic \
    Methods of Data Mining/Homeworks/HW2/2019-Oct.csv', parse_dates=['event_time'], date_parser=pd.to_datetime)

ds = pd.concat([ds_Oct, ds_Nov])

'''[RQ1]
    A marketing funnel describes your customer’s journey with your e-commerce.\
    It may involve different stages, beginning when someone learns about your business,\
    when he/she visits your website for the first time, to the purchasing stage,\
    marketing funnels map routes to conversion and beyond. \
    Suppose your funnel involves just three simple steps: 1) view, 2) cart, 3) purchase. \
    Which is the rate of complete funnels?'''


ds_count_view = pd.DataFrame({'count_view' : ds[ds.event_type == 'view']\
                .groupby(['user_id', 'user_session'])['event_type']\
                .value_counts().sort_values(ascending=False)}).reset_index()

ds_count_cart = pd.DataFrame({'count_cart' : ds[ds.event_type == 'cart']\
                .groupby(['user_id', 'user_session'])['event_type']\
                .value_counts().sort_values(ascending=False)}).reset_index()

ds_count_purchase = pd.DataFrame({'count_purchase' : ds[ds.event_type == 'purchase']\
                    .groupby(['user_id', 'user_session'])['event_type']\
                    .value_counts().sort_values(ascending=False)}).reset_index()

'''merge view and cart'''
ds_count_event = ds_count_view[['user_id', 'user_session', 'count_view']]\
                .merge(ds_count_cart[['user_id', 'user_session', 'count_cart']],\
                 how = 'inner', on=['user_id', 'user_session'])

'''merge view, cart and purchase'''
ds_count_event = ds_count_event[['user_id', 'user_session', 'count_view', 'count_cart']]\
                .merge(ds_count_purchase[['user_id', 'user_session', 'count_purchase']],\
                 how = 'inner', on=['user_id', 'user_session'])

'''The number of complete funnels is rappresented by the number of tatal purchases on the number of total views.'''

complete_funnels_rate = ds_count_purchase['count_purchase'].sum()*100/len(ds_count_view)
print('The complete funnel rate is: ' + str(round(complete_funnels_rate, 2)) + "%")

'''What’s the operation users repeat more on average within a session?\
 Produce a plot that shows the average number of times users perform\
 each operation (view/removefromchart etc etc).'''

'''The dataframe create can also used to print the plot for this question.\
    In this case there is an operation that is not defined in the principal dataframe. \
    This is the "remove from cart" operation. That can be calculated with the difference between purchase and cart.'''

values = ds_count_event.mean().to_list()[1:]
values.append(values[-2]-values[-1])
values = [ round(x) for x in values ]

labels = ['view', 'cart', 'purchase', 'remove']
explode = (0.05, 0, 0, 0)

fig1, ax1 = plt.subplots()
plt.rcParams['figure.figsize'] = (10, 10)
ax1.pie(values,
        explode=explode,
        labels=labels,
        autopct='%1.0f%%',
        shadow=True,
        startangle=180)
ax1.axis('equal')

plt.show()



'''How many times, on average, a user views a product before adding it to the cart?'''

#ds.groupby(['user_id', 'product_id']).agg([ds[ds.event_type=='view'].count(), ds[ds.event_type=='cart'].count()])


'''What’s the probability that products added once to the cart are effectively bought?'''
# To Do this 


'''What’s the average time an item stays in the cart before being removed?'''
# To Do this 

'''How much time passes on average between the first view time and a purchase/addition to cart?'''



'''[RQ2]
    What are the categories of the most trending products overall? \
    For each month visualize this information through a plot showing the number of sold products per category.\
        - Plot the most visited subcategories. \n
        - What are the 10 most sold products per category?'''


'''In this request we have considered a subcaegory like a category. A product can be in a category\
     or subcategory (category of category) or can not have a category. \
    Assume that the trending category is the subcategory with the highest number of products sold.
    In the output are escluded all nan category.'''

''' Computating October month'''

'''The top 10 of category with the most popular products'''

ds_trending_category_oct = pd.DataFrame({'count_product_sold' : ds_Oct[ds_Oct.event_type == 'purchase']\
                                                    .groupby(['category_id', 'category_code'])\
                                                    ['event_type'].value_counts()\
                                                    .sort_values(ascending=False)}).reset_index()

ds_trending_category_oct = ds_trending_category_oct.dropna().head(10)

labels_prod_cat = [e.split('.')[-1] for e in list(ds_trending_category_oct['category_code'])]

plt.figure(figsize=(20, 10))
plt.bar(labels_prod_cat, ds_trending_category_oct['count_product_sold'])
plt.xlabel('Category', fontsize=15)
plt.ylabel('Number of sold product', fontsize=15)
plt.title('Top 10 trending category of october', fontsize=20)
plt.show()


'''The top 10 of category with the highest number of views'''

ds_most_viewed_category_oct = pd.DataFrame({'count_view' : ds_Oct[ds_Oct.event_type == 'view']\
                                                    .groupby(['category_id', 'category_code'])\
                                                    ['event_type'].value_counts()\
                                                    .sort_values(ascending=False)}).reset_index()

ds_most_viewed_category_oct = ds_most_viewed_category_oct.dropna().head(10)

labels_most_viewed = [e.split('.')[-1].replace('_', ' ') for e in list(ds_most_viewed_category_oct['category_code'])]

plt.figure(figsize=(20, 10))
plt.bar(labels_most_viewed, ds_most_viewed_category_oct['count_view'])
plt.xlabel('Category', fontsize=15)
plt.ylabel('Number of views', fontsize=15)
plt.title('Top 10 of most viewed category', fontsize=20)
plt.show()

'''The 10 (or less) most sold products for category.'''

categories = set(ds_Oct[ds_Oct.event_type == 'purchase']['category_code'].dropna())

for c in categories:
    x = ds_Oct[(ds_Oct.category_code == c) & (ds_Oct.event_type=='purchase')].loc[:, 'product_id'].value_counts().head(10).to_string()
    print('''The 10 (or less) most sold product for ''' + c.split('.')[-1].replace('_', ' '))
    print(x)


''' Computating November month'''

'''The top 10 of category with the most popular products'''

ds_trending_category_nov = pd.DataFrame({'count_product_sold' : ds_Nov[ds_Nov.event_type == 'purchase']\
                                                    .groupby(['category_id', 'category_code'])\
                                                    ['event_type'].value_counts()\
                                                    .sort_values(ascending=False)}).reset_index()

ds_trending_category_nov = ds_trending_category_nov.dropna().head(10)

labels_prod_cat = [e.split('.')[-1] for e in list(ds_trending_category_nov['category_code'])]

plt.figure(figsize=(20, 10))
plt.bar(labels_prod_cat, ds_trending_category_nov['count_product_sold'])
plt.xlabel('Category', fontsize=15)
plt.ylabel('Number of sold product', fontsize=15)
plt.title('Top 10 trending category of october', fontsize=20)
plt.show()


'''The top 10 of category with the highest number of views'''

ds_most_viewed_category_nov = pd.DataFrame({'count_view' : ds_Nov[ds_Nov.event_type == 'view']\
                                                    .groupby(['category_id', 'category_code'])\
                                                    ['event_type'].value_counts()\
                                                    .sort_values(ascending=False)}).reset_index()

ds_most_viewed_category_nov = ds_most_viewed_category_nov.dropna().head(10)

labels_most_viewed = [e.split('.')[-1].replace('_', ' ') for e in list(ds_most_viewed_category_nov['category_code'])]

plt.figure(figsize=(20, 10))
plt.bar(labels_most_viewed, ds_most_viewed_category_nov['count_view'])
plt.xlabel('Category', fontsize=15)
plt.ylabel('Number of views', fontsize=15)
plt.title('Top 10 of most viewed category', fontsize=20)
plt.show()

'''The 10 (or less) most sold products for category.'''

categories = set(ds_Nov[ds_Nov.event_type == 'purchase']['category_code'].dropna())

for c in categories:
    x = ds_Nov[(ds_Nov.category_code == c) & (ds_Nov.event_type=='purchase')]\
        .loc[:, 'product_id'].value_counts().head(10).to_string()
    print('''The 10 (or less) most sold product for ''' + c.split('.')[-1].replace('_', ' '))
    print(x)

'''[RQ3]
    For each category, what’s the brand whose prices are higher on average?'''

ds_expensive_brand = pd.DataFrame({'avg_price' : ds.groupby(['category_id', 'category_code', 'brand'])\
                                                    ['price'].mean()\
                                                    .sort_values(ascending=False)}\
                                    ).reset_index()

all_cat = list()
for c in ds_expensive_brand.category_code:
    if c not in all_cat:
        all_cat.append(c)

for c in all_cat:
    b = ds_expensive_brand[(ds_expensive_brand.category_code == c)]['brand']\
        .dropna().head(1).to_string(index=False).strip()
    print(c.split('.')[-1].replace('_', ' ') + ': ' + b)


'''Write a function that asks the user a category in input and returns a plot\
     indicating the average price of the products sold by the brand.'''

def brand_status():
    c = input().strip()

    d = pd.DataFrame({'avg_price' : ds[(ds.category_code == c) & (ds.event_type == 'purchase')].groupby('brand')['price'].mean()}).reset_index()

    plt.figure(figsize=(20, 10))
    plt.bar(d.brand, d.avg_price)
    plt.xticks(rotation='vertical')
    plt.xlabel('Brand', fontsize=15)
    plt.ylabel('Average price of products', fontsize = 15)
    plt.title('Average price  of products for ' + c.split('.')[-1].replace('_',' '), fontsize=20)
    plt.show()

brand_status()

'''Find, for each category, the brand with the highest average price.\
     Return all the results in ascending order by price.'''


l = []
for c in all_cat:
    l += [(c, ds_expensive_brand[ds_expensive_brand.category_code == c]['brand'].head(1).to_string(index=False).strip())]
for e in sorted(l, key=lambda tup: tup[1]):
    print(e[0].split('.')[-1].replace('_', ' ') + ': ' + e[1])


'''[RQ4]
    How much does each brand earn per month?\
     Write a function that given the name of a brand in input returns, for each month, its profit.'''

'''An economic profit or loss is the difference between the revenue received \
    from the sale of an output and the costs of all inputs used.
    We don't have sufficient information to do that. For that reason we\
        mean the profit has a sum of money received by purchasing products.'''

def brand_profit(brand):
    o = ds_Oct.loc[ds_Oct['event_type']=='purchase'].groupby(ds_Oct.brand)['price'].sum()[brand]
    n = ds_Nov.loc[ds_Nov['event_type']=='purchase'].groupby(ds_Nov.brand)['price'].sum()[brand]
    return o, n

'''This function below can be used to print the result of the previous function\
    with a good presentation'''

def print_brand_profit():
    b = input().strip()
    o, n = brand_profit(b)
    print('Profit for october is ' + str(o))
    print('Profit for november is ' + str(n))

print_brand_profit()


'''Is the average price of products of different brands significantly different?'''

'''To respond to this question can we print for each category the average price of products from differents brands'''

for c in all_cat:
    x = ds_expensive_brand[['brand', 'avg_price']].loc[(ds_expensive_brand.category_code==c)]
    print(c.split('.')[1].replace('_', ' ') + ': \n' +  x.to_string(index=False, col_space=15))

'''Using the function you just created, find the top 3 brands that have suffered the biggest \
        losses in earnings between one month and the next, specifing bothe the loss percentage \
        and the 2 months (e.g., brand_1 lost 20% between march and april).'''

brands = set(ds['brand'].loc[ds['event_type']=='purchase'].dropna())

'''The function must print the 3 cases of brands wich they have a loss in the following month.
    (profit of november is less then october)\n
    If there is the same value for one position returns the last one.
    We assume that there are at least 3 brands at a loss.'''

v = [-1, -1, -1]
b = ['', '', '']

for brand in brands:
    o, n = brand_profit(brand)
    p = -1
    if n <= o : p = ((o-n)*100)/o
    for i in range(3):
        if p >= v[i]:
            b[i] = brand
            v[i] = p
            break

print(b[0] + ' lost ' + str(v[0]) + '%' + ' between october and november')
print(b[1] + ' lost ' + str(v[1]) + '%' + ' between october and november')
print(b[2] + ' lost ' + str(v[2]) + '%' + ' between october and november')



'''[RQ5] 
In what part of the day is your store most visited? \
    Knowing which days of the week or even which hours of the day shoppers are likely to visit your online \
    store and make a purchase may help you improve your strategies. Create a plot that for each day of the \
    week show the hourly average of visitors your store has.'''

'''The code below print a plot with the average of views for each days of week'''

mon = ds[(ds.event_type == 'view') & (ds.event_time.dt.day == 0)]\
        .loc[:, 'event_type'].value_counts().mean()

tue = ds[(ds.event_type == 'view') & (ds.event_time.dt.day == 1)]\
        .loc[:, 'event_type'].value_counts().mean()

wed = ds[(ds.event_type == 'view') & (ds.event_time.dt.day == 2)]\
        .loc[:, 'event_type'].value_counts().mean()

thu = ds[(ds.event_type == 'view') & (ds.event_time.dt.day == 3)]\
        .loc[:, 'event_type'].value_counts().mean()

fri = ds[(ds.event_type == 'view') & (ds.event_time.dt.day == 4)]\
        .loc[:, 'event_type'].value_counts().mean()

sat = ds[(ds.event_type == 'view') & (ds.event_time.dt.day == 5)]\
        .loc[:, 'event_type'].value_counts().mean()

sun = ds[(ds.event_type == 'view') & (ds.event_time.dt.day == 6)]\
        .loc[:, 'event_type'].value_counts().mean()

plt.figure(figsize=(20, 10))
plt.bar(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], [mon, tue, wed, thu, fri, sat, sun])
plt.xlabel('Days of week', fontsize=15)
plt.ylabel('Average number of views', fontsize=15)
plt.title('Week views', fontsize=20)
plt.show()



'''The code below print a plot with the average of views for each hour'''

hours_label = [str(i) for i in range(24)]
hours_values = []

for h in range(24):
    hours_values.append(ds[(ds.event_type=='view') & (ds.event_time.dt.hour == h)].loc[:, 'event_type'].value_counts().mean())

plt.figure(figsize=(30, 10))
plt.plot_date(hours_label, hours_values)
plt.plot(hours_label, hours_values)
plt.xlabel('Hours', fontsize=15)
plt.ylabel('Average number of views', fontsize=15)
plt.title('Hours views', fontsize=20)
plt.show()


'''In the function below an user can input a day of week (ex: 'monday') and receive\
    an "Hours view" plot for that day of week'''

def dayweek_hours_views():

    d = input().strip().lower().capitalize()
    
    hours_label = [str(i) for i in range(24)]
    hours_values = []

    for h in range(24):
        hours_values.append(ds[(ds.event_time.dt.day_name()==d) & (ds.event_type=='view') & (ds.event_time.dt.hour == h)]\
            .loc[:, 'event_type'].value_counts().mean())

    plt.figure(figsize=(20, 10))
    plt.plot(hours_label, hours_values)
    plt.plot_date(hours_label, hours_values)
    plt.xlabel('Hours', fontsize=15)
    plt.ylabel('Average number of views', fontsize=15)
    plt.title('Hours views of ' + d, fontsize=20)
    plt.show()

'''[RQ6]
The conversion rate of a product is given by the purchase rate over the number of times the product has been visited.\
     What's the conversion rate of your online store?'''

'''Find the overall conversion rate of your store.'''

'''The conversion rate represents that value, expressed as a percentage,\
     which summarizes the ability of your web pages to transform visitors into customers.'''

total_views = int(ds[ds.event_type == 'view'].loc[:, 'event_type'].value_counts())
total_purchase = int(ds[ds.event_type == 'purchase'].loc[:, 'event_type'].value_counts())

print('The conversion rate of the store is ' + str(total_purchase*100/total_views) + "%")


'''Plot the purchase rate of each category and show the conversion rate of each category in decreasing order.'''

ds_purchase = pd.DataFrame({'purchases' : ds[(ds.event_type=='purchase')]\
    .groupby(['category_code'])['event_type'].value_counts()}).reset_index()

ds_view = pd.DataFrame({'views' : ds[(ds.event_type=='view')]\
    .groupby(['category_code'])['event_type'].value_counts()}).reset_index()

cat_purchase = ds_purchase['category_code'].dropna().to_list()
cat_rate = OrderedDict()

for cat in cat_purchase:
    v = int(ds_view[ds_view.category_code == cat]['views'])
    p = int(ds_purchase[ds_purchase.category_code == cat]['purchases'])
    cat_rate[cat] = p*100/v

dict_rate= OrderedDict(sorted(cat_rate.items(), key=itemgetter(1), reverse = True))


plt.figure(figsize=(int(len(cat_purchase)//8), int(len(cat_purchase)//5)))
plt.barh([ e.split('.')[-1].replace('_', ' ') for e in dict_rate.keys() ], dict_rate.values())
plt.gca().invert_yaxis()
plt.xlabel('Percentage values of conversion rate', fontsize=int(len(cat_purchase)//8))
plt.ylabel('Categories', fontsize=int(len(cat_purchase)//8))
plt.title('Conversion rate of categories', fontsize=int((len(cat_purchase)//5)))
plt.show()


'''[RQ7]
The Pareto principle states that for many outcomes roughly 80% of consequences\
     come from 20% of the causes. Also known as 80/20 rule, in e-commerce simply means that most \
         of your business, around 80%, likely comes from about 20% of your customers.
Prove that the pareto principle applies to your store.'''

def truncate(n):
    n = str(n).replace('',' ').split()
    n.reverse()
    for i in range(1, len(n)):
        v = int(n[i])
        if int(n[i-1]) >= 5:
            n[i] = str(v+1)
    n.reverse()
    return int(n[0] + '0'*(len(n)-1))

ds_group_user = ds[ds.event_type == 'purchase']\
    .groupby(ds.user_id)['price'].sum().sort_values(ascending=False)

total_user = int(len(ds_group_user))
user20 = (int(total_user)//100)*20
total_business= round(int(ds_group_user.sum()))
business80 = (int(total_business)//100)*80
business_user20 = round(int(ds_group_user.head(user20).sum()))


if truncate(business80) == truncate(business_user20):
    print('The Pareto principle is proved')
else:
    print("The Pareto principle isn't proved")