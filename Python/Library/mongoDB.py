import pymongo

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient["myDB"]


class DataBase:
    @staticmethod
    def bases_list():
        print(myclient.list_database_names())

    @staticmethod
    def is_db_exist(name):
        dblist = myclient.list_database_names()
        if name in dblist:
            print("The database exists.")
        else:
            print("The database is not exists.")

    @staticmethod
    def add(collection_name, value):  # добавлять нужно по типу: { "name": "John", "address": "Highway 37" }
        x = mydb[collection_name].insert_one(value)
        print(x)

    @staticmethod
    def add_many(collection_name, values):
        x = mydb[collection_name].insert_many(values)
        print(x)

    @staticmethod
    def delete_one(collection_name, value):  # удалять нужно по типу: {"address": "Mountain 21"}
        mydb[collection_name].delete_one(value)

    @staticmethod
    def delete_all(collection_name):
        mydb[collection_name].drop()

    @staticmethod
    def find(collection_name, any_value):  # искать нужно по типу: { "address": "Park Lane 38" }
        return mydb[collection_name].find(any_value)

    @staticmethod
    def update_one(collection_name, value_to_change, new_value):
        mydb[collection_name].update_one(value_to_change, new_value)  # В ЗАМЕНЕ ВСЕГДА ИСКАТЬ ТОЛЬКО ПО ID!!!!!!!

    '''
    выводить по типу:
    for y in x:
        print(y) #x - переменная, которой присваивается значение функции
    '''

    @staticmethod
    def show(collection_name):
        for i in mydb[collection_name].find():
            print(i)

    @staticmethod
    def pop(collection_name):
        return mydb[collection_name].find()  # для извлечения определенных полей

    @staticmethod
    def show_some_element(collection_name, items_not_to_show):  # {"_id": 0, "name": 1, "address": 1} не выведет, где 0
        for x in mydb[collection_name].find({}, items_not_to_show):
            print(x)


'''
books: _id, name, author, price
users: _id, name, password, email, books, coins, image
statistics: _id, downloads, users, money
'''

if __name__ == "__main__":
    # DataBase.delete_all("statistics")

    # DataBase.add("books", {'_id': 11,'name': 'a', 'author': 'b', 'price':3})
    # DataBase.add("statistics", {'_id': 1, 'downloads': 0, 'users': 2, 'money': 0})

    # DataBase.add_many("books", list_of_books)
    # DataBase.bases_list()
    # DataBase.delete_one("users", {'name': 'Tester'})
    # DataBase.update_one('statistics', {'_id': 1}, {"$set": dict(users=2)})
    DataBase.show("users")
    print('')
    DataBase.show("statistics")
