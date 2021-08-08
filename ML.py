from sklearn import tree
from sklearn.preprocessing import LabelEncoder
import bama_backend
import re
from pyfiglet import figlet_format
from termcolor import colored

# get data from database
data = bama_backend.select_date()

car = []
model = []
func = []
city = []
price = []

for d in data:
    if 'کارکرد' in d[2] or d[2] == '-' or 'حواله' in d[2] or 'کارتکس' in d[2]:
        continue
    else:
        car.append(d[0])
        model.append(d[1])
        f = re.sub(',', '', d[2])
        func.append(f)
        city.append(d[3])
        p = re.sub(',', '', d[4])
        price.append(p)

# encode data
le = LabelEncoder()
car = le.fit_transform(car)
model = le.fit_transform(model)
city = le.fit_transform(city)


ListOfData = []
for info in zip(car, model, func, city):
    ListOfData.append([info[0], info[1], info[2], info[3]])

clf = tree.DecisionTreeClassifier()
clf = clf.fit(ListOfData, price)

# print maktabkhooneh
maktabkhooneh = figlet_format('''MAKTAB
KHOONEH''')
print(maktabkhooneh)

# help
text = '''Hi guys, welcome to bama, please input data like below of format:
name of car (enter) brand (enter) function (enter) city (enter)
thanks, happy new year !!!!'''
print(colored(text, 'blue'))
print()

text2 = '''<< حتما ورودی ها را کامل و درست بنویسید >> 
به طور مثال عبارات صحبح مثل : هیوندای، آزرا
عبارت نادرست مثل : هیوندا، ازرا
این موضوع باعث میمشه قیمت دقیق تری دریافت کنید'''
print(colored(text2,'green'))
print()

# get data from user
new_data = []
name_user = input('Enter name of car: ').split()
model_user = input('Enter name of model: ').split()
func_user = input('how many is mileage your car: ').split()
city_user = input('what\'s your city\'s name: ').split()

name_user = le.fit_transform(name_user)

if model_user[0].isalpha():
    model_user = le.fit_transform(model_user)

city_user = le.fit_transform(city_user)

for i in zip(name_user,model_user,func_user,city_user):
    new_data.append([i[0],i[1],i[2],i[3]])


predict = clf.predict(new_data)
print(predict[0])
