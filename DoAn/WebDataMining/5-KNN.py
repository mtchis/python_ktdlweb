import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import plot

CATEGORIES = {
    'kinh-doanh': 0,
    'giai-tri': 1,
    'the-thao': 2,
    'giao-duc':  3,
    'suc-khoe': 4,
    'doi-song': 5,
    'du-lich': 6,
    'khoa-hoc': 7,
    'so-hoa': 8,
    'oto-xe-may': 9
}

CLASSNAME = ['Kinh doanh','Giải trí' ,'Thể thao' ,'Giáo dục', 'Sức khỏe', 'Đời sống', 'Du lịch' ,'Khoa học' ,'Số hóa' ,'Xe']


def KNN_confusion_matrix(X,y,test_Size):
    name = "train/test : " + str(int(100-100*test_Size)) + "/"  + str(int(100*test_Size))

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0, test_size=test_Size)

    # Khai báo lớp KNN với k = 10
    knn = KNeighborsClassifier(n_neighbors=10)

    # Huấn luyện
    knn.fit(X_train, y_train)

    # Tính độ chính xác
    accuracy = knn.score(X_test, y_test)

    # Tạo ma trận nhầm lẫn (confusion matrix)
    y_pred = knn.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)

    # Tính toán độ do precision
    precision = precision_score(y_test, y_pred, average=None)
    precision = sum(precision) / len(precision)
    # Tính đoán độ đo recall
    recall = recall_score(y_test, y_pred, average=None)
    recall = sum(recall) / len(recall)
    # Tính toán độ đo F1
    f1 = f1_score(y_test, y_pred, average=None)
    f1 = sum(f1) / len(f1)
    plot.plot_confusion_matrix(y_test, y_pred, classes=CLASSNAME, title='Confusion matrix. ' + name)
    # plot.plot_confusion_matrix(y_test, y_pred, classes=CLASSNAME, normalize=True, title='Normalized confusion matrix'+name)
    plt.show()

    print("---")
    print(name)
    print('   accuracy  : ' + str(accuracy))
    print('   precision : ' + str(precision))
    print('   recall    : ' + str(recall))
    print('   f1        : ' + str(f1))


with open('out.json', encoding="utf-8") as jsonFile:

    data = json.load(jsonFile)
    content = []
    y = []

    for x in data:
        content.append(' '.join(x['words']))
        y.append(int(CATEGORIES[x['category']]))

    tf = TfidfVectorizer(min_df=0)
    tf_idf_matrix = tf.fit_transform(content)
    X = tf_idf_matrix.todense()

    KNN_confusion_matrix(X, y, 0.1)
    KNN_confusion_matrix(X, y, 0.2)
    KNN_confusion_matrix(X, y, 0.3)
    KNN_confusion_matrix(X, y, 0.4)
    KNN_confusion_matrix(X, y, 0.5)

#### KNN

