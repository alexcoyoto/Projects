from sklearn import tree
import mongoDB

'''
Некоторая информация о соотношении картинка-пол:
    0 -- картинка женского пола
    1 -- картинка мужского пола
Некоторая информация об итогах:
    0 -- девушка, любящая девешые книжки
    1 -- девушка, любящая дорогие книжки
    2 -- парень, любящий дешевые книжки
    3 -- парень, любящий дорогие книжки
'''


def prediction(books, image):
    # test_user = basics.User()
    # test_user.set(3, 'Sam', 321, 'sanya@mail.com', '1;4;', 10, 'girl.png')

    db = mongoDB.DataBase()

    ids = books.split(';')
    if ids == ['']:
        return

    average_value = 0
    for i in range(len(ids) - 1):
        for row in db.pop('books'):
            if row['_id'] == int(ids[i]):
                average_value += row['price']
    average_value /= len(ids) - 1

    if image == 'girl.png' or image == 'woman.png':
        image_to_int = 0
    else:
        image_to_int = 1

    if learning(image_to_int, average_value) == 0:
        result_str = 'девушка, любящая маленькие по объему книжки'
    elif learning(image_to_int, average_value) == 1:
        result_str = 'девушка, любящая большие по объему книжки'
    elif learning(image_to_int, average_value) == 2:
        result_str = 'парень, любящий маленькие по объему книжки'
    else:
        result_str = 'парень, любящий большие по объему книжки'
    # print(result_str)
    return result_str


def learning(image, value):
    features = [[0, 2.0], [0, 2.4], [0, 2.9], [0, 3.5], [1, 2.0], [1, 2.4], [1, 2.9], [1, 3.5]]
    labels = [0, 0, 1, 1, 2, 2, 3, 3]

    classif = tree.DecisionTreeClassifier()
    classif.fit(features, labels)
    # print(classif.predict([[image, value]]))
    return classif.predict([[image, value]])


'''
features = [[int.from_bytes('chicken'.encode(), 'big'), 0.6, 40], [int.from_bytes('chicken'.encode(), 'big'), 0.6, 41],
            [int.from_bytes('horse'.encode(), 'big'), 600, 37], [int.from_bytes('horse'.encode(), 'big'), 600, 38]]
# labels = [chicken, chicken, horse, horse]
labels = [0, 0, 1, 1]
classif = tree.DecisionTreeClassifier()
classif.fit(features, labels)

print(classif.predict([[int.from_bytes('chicken'.encode(), 'big'), 600, 40]]))
'''
