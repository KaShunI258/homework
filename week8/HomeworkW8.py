import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

ct = pd.read_csv("archive\shopping_trends.csv")
# print(ct.shape) the matrix sized (3900,19)
# print(ct.columns)
"""
#Index(['Customer ID', 'Age', 'Gender', 'Item Purchased', 'Category',
       'Purchase Amount (USD)', 'Location', 'Size', 'Color', 'Season',
       'Review Rating', 'Subscription Status', 'Payment Method',
       'Shipping Type', 'Discount Applied', 'Promo Code Used',
       'Previous Purchases', 'Preferred Payment Method',
       'Frequency of Purchases'],
      dtype='object')
"""
# print(ct.info())
"""
RangeIndex: 3900 entries, 0 to 3899
Data columns (total 19 columns):
 #   Column                    Non-Null Count  Dtype  
---  ------                    --------------  -----  
 0   Customer ID               3900 non-null   int64  
 1   Age                       3900 non-null   int64  
 2   Gender                    3900 non-null   object 
 3   Item Purchased            3900 non-null   object 
 4   Category                  3900 non-null   object 
 5   Purchase Amount (USD)     3900 non-null   int64  
 6   Location                  3900 non-null   object 
 7   Size                      3900 non-null   object 
 8   Color                     3900 non-null   object 
 9   Season                    3900 non-null   object 
 10  Review Rating             3900 non-null   float64
 11  Subscription Status       3900 non-null   object 
 12  Payment Method            3900 non-null   object 
 13  Shipping Type             3900 non-null   object 
 14  Discount Applied          3900 non-null   object 
 15  Promo Code Used           3900 non-null   object 
 16  Previous Purchases        3900 non-null   int64  
 17  Preferred Payment Method  3900 non-null   object 
 18  Frequency of Purchases    3900 non-null   object 
dtypes: float64(1), int64(4), object(14)
memory usage: 579.0+ KB
None
"""
men = 0; women = 0
for i in ct['Gender']:
    if i == "Male":
        men += 1
    elif i == "Female":
        women += 1
genderNum = [men, women]
# print(genderNum) [2652, 1248]
# plt.bar(["Male", "Female"], genderNum, color='r')
# plt.title("the portion of gender")
# plt.xlabel("gender")
# plt.ylabel("amount")

# plt.pie(genderNum, labels=['men', 'women'] ,colors=['green', 'blue'])
# plt.show()

# fig, ax = plt.subplots(figsize = (20, 5))
#
# ax.hist(ct['Age'], bins = 25, edgecolor = 'black', alpha = 0.7, color = 'skyblue', density = True)
# ct['Age'].plot(kind = 'kde', color = 'red', ax = ax)
#
# ax.set_xlabel('Age')
# ax.set_ylabel('Count / Density')
# ax.set_title('Age Distribution Histogram with Density Curve')
# ax.legend(['Density Curve', 'Histogram'])
# plt.show()

# sns.stripplot(x = 'Gender', y = 'Purchase Amount (USD)', data = ct)
# plt.show() # 说明消费水平差不多

# sns.scatterplot(x = 'Age', y = 'Purchase Amount (USD)',data = ct, size = 0.2)
# plt.show()

# sns.histplot(x = 'Age', kde=True, data=ct)
# plt.show()
