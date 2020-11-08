''' insert the assignamnet introduction '''

''' the importation of library and the reading of document '''

import pandas as pd
import pandasql as ps
import matplotlib.pyplot as plt

ds_Oct = pd.read_csv('D:/Storage file PC/Documenti/Università/Data Science/Anno 1/Semestre 1/Algorthmic Methods of Data Mining/Homeworks/HW2/2019-Oct.csv')
ds_Nov = pd.read_csv('D:/Storage file PC/Documenti/Università/Data Science/Anno 1/Semestre 1/Algorthmic Methods of Data Mining/Homeworks/HW2/2019-Oct.csv')

ds = pd.concat([ds_Oct, ds_Nov])

'''[RQ1]
    A marketing funnel describes your customer’s journey with your e-commerce.\
    It may involve different stages, beginning when someone learns about your business,\
    when he/she visits your website for the first time, to the purchasing stage,\
    marketing funnels map routes to conversion and beyond. \
    Suppose your funnel involves just three simple steps: 1) view, 2) cart, 3) purchase. \
    Which is the rate of complete funnels?'''

q_count_view = '''select distinct user_id, user_session, count(event_type) as count_view
                from ds
                where event_type = 'view'
                group by user_id,  user_session
                order by count_view desc;
                '''
q_count_cart = '''select distinct user_id, user_session, count(event_type) as count_cart
                from ds
                where event_type = 'cart'
                group by user_id, user_session
                order by count_cart desc;
                '''
q_count_purchase = '''select distinct user_id, user_session, count(event_type) as count_purchase
                    from ds
                    where event_type = 'purchase'
                    group by user_id,  user_session
                    order by count_purchase desc;
                    '''

ds_count_view = ps.sqldf(q_count_view, locals())
ds_count_cart = ps.sqldf(q_count_cart, locals())
ds_count_purchase = ps.sqldf(q_count_purchase, locals())

q_count_event = '''select distinct v.user_id, v.user_session, v.count_view, c.count_cart, p.count_purchase
                from ds_count_view as v
                inner join ds_count_cart as c
                inner join ds_count_purchase as p
                where v.user_session = c.user_session
                and v.user_id = c.user_id
                and v.user_id = p.user_id
                and v.user_session = p.user_session;
                '''

ds_count_event = ps.sqldf(q_count_event, locals())

'''The number of complete funnels is rappresented by the number of rows in ds_count_event.
To calculate rate we can use the number of rows of ds_count_view. They rapresent\
    the number of totally view session.'''

complete_funnels_rate = len(ds_count_event)*100/len(ds_count_view)
print('The funnel rate is: ' + complete_funnels_rate + "%")

'''What’s the operation users repeat more on average within a session?\
 Produce a plot that shows the average number of times users perform\
 each operation (view/removefromchart etc etc).'''

# if the remove from cart is escluded remove this part

'''The dataframe create can also used to print the plot for this question.\
    In this case thre is an operation that is not defined in the principal dataframe. \
    This is the "remove from cart" operation. That can be calculated from the number \
    of cart minus the number of purchase.
    Assume that the number of non-purchase for each session is a remove operation.'''

ds_product_cart = ds[['user_id', 'user_session', 'product_id']].loc[ds['event_type'] == 'cart']
ds_product_purchase = ds[['user_id', 'user_session', 'product_id']].loc[ds['event_type'] == 'purchase']

# define the difference
# ---> https://datascience.stackexchange.com/questions/37227/how-to-remove-rows-from-a-data-frame-that-are-identical-to-other-df
# for now the plot donn't have the remove operation

avg_view = ds_count_view['count_view'].mean()
avg_cart = ds_count_cart['count_cart'].mean()
avg_purchase = ds_count_purchase['count_purchase'].mean()

# use correct plot function

'''How many times, on average, a user views a product before adding it to the cart?'''
# To Do this 

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

q_trending_category_oct = '''select distinct category_id, category_code, count(product_id) as count_product_sold
                        from ds_Oct
                        where event_type = 'purchase'
                        group by category_id, category_code
                        order by count_product_sold desc;'''

ds_trending_category_oct = ps.sqldf(q_trending_category_oct, locals())
ds_trending_category_oct = ds_trending_category_oct.dropna().head(10)

labels_prod_cat = [e.split('.')[-1] for e in list(ds_trending_category_oct['category_code'])]

plt.figure(figsize=(20, 10))
plt.bar(labels_prod_cat, ds_trending_category_oct['count_product_sold'])
plt.xlabel('category')
plt.ylabel('number of sold product')
plt.title('Top 10 trending category of october', fontsize=20)
plt.show()


'''The top 10 of category with the highest number of views'''

q_most_viewed_category_oct = '''select distinct category_id, category_code, count(event_type) as count_view
                        from ds_Oct
                        where event_type = 'view'
                        group by category_id, category_code
                        order by count_view desc;'''

ds_most_viewed_category_oct = ps.sqldf(q_most_viewed_category_oct, locals())
ds_most_viewed_category_oct = ds_most_viewed_category_oct.dropna().head(10)

labels_most_viewed = [e.split('.')[-1] for e in list(ds_most_viewed_category_oct['category_code'])]

plt.figure(figsize=(20, 10))
plt.bar(labels_most_viewed, ds_most_viewed_category_oct['count_view'])
plt.xlabel('category')
plt.ylabel('number of views')
plt.title('Top 10 of most viewed category', fontsize=20)
plt.show()

'''The 10 most sold products for category.\n
    Is possibile that a category don't have any products in list.'''

categories = set(ds_Oct['category_code'].dropna())

for c in categories:
    x = ds_Oct[ds_Oct.category_code == c]
    print('The 10 most sold product for ' + c.split('.')[-1].replace('_', ' '))
    p = x[x.event_type=='purchase'].loc[:, 'product_id'].value_counts().head(10).to_string()[:]
    if p != 'Series([], )':
        print(p)


''' Computating November month'''

'''The top 10 of category with the most popular products'''

q_trending_category_nov = '''select distinct category_id, category_code, count(product_id) as count_product_sold
                        from ds_Nov
                        where event_type = 'purchase'
                        group by category_id, category_code
                        order by count_product_sold desc;'''

ds_trending_category_nov = ps.sqldf(q_trending_category_nov, locals())
ds_trending_category_nov = ds_trending_category_nov.dropna().head(10)

labels_prod_cat = [e.split('.')[-1] for e in list(ds_trending_category_nov['category_code'])]

plt.figure(figsize=(20, 10))
plt.bar(labels_prod_cat, ds_trending_category_nov['count_product_sold'])
plt.xlabel('category')
plt.ylabel('number of sold product')
plt.title('Top 10 trending category of november', fontsize=20)
plt.show()


'''The top 10 of category with the highest number of views'''

q_most_viewed_category_nov = '''select distinct category_id, category_code, count(event_type) as count_view
                        from ds_Nov
                        where event_type = 'view'
                        group by category_id, category_code
                        order by count_view desc;'''

ds_most_viewed_category_nov = ps.sqldf(q_most_viewed_category_nov, locals())
ds_most_viewed_category_nov = ds_most_viewed_category_nov.dropna().head(10)

labels_most_viewed = [e.split('.')[-1] for e in list(ds_most_viewed_category_nov['category_code'])]

plt.figure(figsize=(20, 10))
plt.bar(labels_most_viewed, ds_most_viewed_category_nov['count_view'])
plt.xlabel('category')
plt.ylabel('number of views')
plt.title('Top 10 of most viewed category', fontsize=20)
plt.show()

'''The 10 most sold products for category.\n
    Is possibile that a category don't have any products in list.'''

categories = set(ds_Nov['category_code'].dropna())

for c in categories:
    x = ds_Nov[ds_Nov.category_code == c]
    print('The 10 most sold product for ' + c.split('.')[-1].replace('_', ' '))
    p = x[x.event_type=='purchase'].loc[:, 'product_id'].value_counts().head(10).to_string()[:]
    if p != 'Series([], )':
        print(p)

'''[RQ3]
    For each category, what’s the brand whose prices are higher on average?'''

q_expensive_brand = '''select distinct category_id, category_code, brand, avg(price) as avg_price
                        from ds
                        group by category_id
                        order by avg_price desc'''

ds_expensive_brand = ps.sqldf(q_expensive_brand, locals()).dropna()

all_cat = set(ds['category_code'].dropna())

for c in all_cat:
    b = ds_expensive_brand['brand'].loc[ds_expensive_brand['category_code']==c].head(1).to_string().split()[1]
    if b.isalpha():
        print(c.split('.')[-1] + ': ' + b)


'''Write a function that asks the user a category in input and returns a plot\
     indicating the average price of the products sold by the brand.'''

'''Make a plot with an only item isn't a good practice.\
    For a best view plot the average for each category of brand.'''

def brand_status():
    b = input()
    d = ds_expensive_brand[ds_expensive_brand.brand==b].dropna()
    c = [i.split('.')[-1] for i in list(d['category_code'])]
    plt.figure(figsize=(20, 10))
    plt.bar(c, d['avg_price'])
    plt.xlabel('category')
    plt.ylabel('average price of products')
    plt.title('Average products price for ' + b, fontsize=20)
    plt.show()

brand_status()

'''Find, for each category, the brand with the highest average price.\
     Return all the results in ascending order by price.'''
    
'''In this case is necessary print the value of ds_expensive_brand in reserve order.'''

l = []
for c in all_cat:
    b = ds_expensive_brand['brand'].loc[ds_expensive_brand['category_code']==c].head(1).to_string().split()[1]
    if b.isalpha():
        l += [str(c.split('.')[-1] + ': ' + b)]
for b in sorted(l, reverse=True):
    print(b)