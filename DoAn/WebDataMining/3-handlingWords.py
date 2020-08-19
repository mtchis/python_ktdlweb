import os
from bs4 import BeautifulSoup
import nltk
from scipy import spatial
import re
import requests
import io
nltk.download('stopwords')
nltk.download('punkt')
from nltk.tokenize import word_tokenize, sent_tokenize
from string import punctuation
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
my_stopwords = set(stopwords.words('english') + list(punctuation))
ps = PorterStemmer()
# Thư viện triển khai BoW & TF IDF
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from pip._vendor.distlib.compat import raw_input
from gensim.summarization.bm25 import get_bm25_weights

# Hàm duyệt danh sách file từ thư mục
pattern = 'json|word|BoW|BoW.CosSim|BoW_OkapiBM25|TF-IDF|TF-IDF_CosSim|TF-IDF_OkapiBM25'
def browseFiles(path):
    list_path = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if not re.search(pattern, file):
                list_path.append(root + '/' + file)
    return list_path

# Hàm duyệt danh sách URL đưa vào mảng
def browseURL(urls):
    list_path = []
    list_path = urls.split(' ')
    return list_path

# Hàm đọc file, xử lý
def readFile(list_path):
    read_files = []
    i = 0
    for i in range(len(list_path)):
        read_file = open(list_path[i], 'r', encoding="utf8")
        a = read_file.readlines()
        a = ' '.join(a)
        read_files.append(a)
    return read_files

# Hàm đọc URLs và đưa vào mảng
def readURL(list_path):
    read_sources = []
    for url in list_path:
        r = requests.get(url)
        source = r.text
        read_source = io.StringIO(source)
        a = read_source.readlines()
        a = ' '.join(a)
        read_sources.append(a)
    return read_sources

# Hàm xử lý html
def clean_html(text):
    soup = BeautifulSoup(text, 'html.parser')
    return soup.get_text()

# Hàm loại bỏ các ký tự đạc biệt và khoảng trắng
def remove_special_character(text):
    # Thay thế các ký tự đặc biệt bằng ''
    string = re.sub('[^\w\s]', '', text)
    # Xử lí các khoảng trắng thừa ở giữa chuỗi
    string = re.sub('\s', ' ', string)
    # Xử lý khoảng trắng thừa ở đầu và cuối câu
    string = string.strip()
    return string

# Hàm loại bỏ words trùng lặp
def remove_duplicate(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist

# Tách câu tách từ, loại bỏ hư từ, chuẩn hóa từ
def filterTexts(txtArr):
    res = []
    for i in range(len(txtArr)):
        # Loại bỏ html
        text_cleaned = clean_html(txtArr[i])
        # Tách câu
        sents = sent_tokenize(text_cleaned)
        # Loại bỏ ký tự đặc biệt
        sents_cleaned = [remove_special_character(s) for s in sents]
        # Nối các câu lại thành text
        text_sents_join = ''.join(sents_cleaned)
        # Tách từ
        words = word_tokenize(text_sents_join)
        # Đưa về dạng chữ thường
        words = [word.lower() for word in words]
        # Loại bỏ hư từ
        words = [word for word in words if word not in my_stopwords]
        # Chuẩn hóa từ
        words = [ps.stem(word) for word in words]
        words = ' '.join(words)
        # Loại bỏ từ duplicate
        # words = '\n'.join(remove_duplicate(words.split()))
        res.append(words)
    return res

# Hàm Bag Of Word return matrix vector
def bagOfWords(txtArr):
    res = CountVectorizer()
    res.fit_transform(txtArr)
    print('(!) Tạo thứ tự từ điển BoW:')
    print (res.vocabulary_)
    return res.fit_transform(txtArr).todense()

# Hàm TFIDF
def tF_IDF(txtArr):
    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
    tf_idf_matrix = tf.fit_transform(txtArr)
    print('(!) Feature Names TF_IDF:')
    print('\n'.join(tf.get_feature_names()))
    print('(!) TF_IDF Matrix:')
    print(tf_idf_matrix)
    dense = tf_idf_matrix.todense()
    return dense

def chk_URL(_url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, _url) is not None

# Ghi Vector ra txt
def writeVectorFite(txtArrAfter, outputName, list_path, path):
    f = open(path + '/' + outputName + '.txt', 'w')
    if chk_URL(list_path[0]):
        stt = 1
        for i in range(len(txtArrAfter)):
            txtName = list_path[i].split('/')[2]
            stt = stt + 1
            f.write(txtName)
            f.write('\n')
            for j in range(len(txtArrAfter[i])):
                f.write(str(txtArrAfter[i][j]))
            f.write('\n')
    else:
        stt = 1
        for i in range(len(txtArrAfter)):
            strPath = list_path[i].split('/')
            txtFileName = strPath[len(strPath) - 1]
            stt_txtFileName = str(stt) + " " + txtFileName
            stt = stt + 1
            f.write(stt_txtFileName)
            f.write('\n')
            for j in range(len(txtArrAfter[i])):
                f.write(str(txtArrAfter[i][j]))
            f.write('\n')
    f.close()

# Hàm ghi độ tương đồng Cossim txt file
def writeCossimFile(txtArrAfter, outputName, path):
    f = open(path + '/' + outputName + '.txt', 'w')
    for i in range(len(txtArrAfter)):
        for j in range(len(txtArrAfter)):
            cossim = round(1 - spatial.distance.cosine(txtArrAfter[i], txtArrAfter[j]), 3)
            res = cossim
            # write float to file
            if len(str(res)) == 3:
                res = str(res) + "   "
            elif len(str(res)) == 4:
                res = str(res) + "  "
            else:
                res = str(res) + " "
            f.write(res)
        f.write("\n")
    f.close()

# Hàm ghi độ tương đồng okapi txt file
def writeOkapiFile(txtArrAfter, outputName, path):
    f = open(path + '/' + outputName + '.txt', 'w')
    arr = []
    for i in range(len(txtArrAfter)):
        item = txtArrAfter[i].split(" ")
        arr.append(item)
    result = get_bm25_weights(arr, n_jobs=-1)
    for i in range(len(result)):
        strItem = ""
        for j in range(len(result[i])):
            okapi = str(round(result[i][j], 3))
            if len(okapi) == 3:
                strItem = strItem + okapi + "    "
            elif len(okapi) == 4:
                strItem = strItem + okapi + "   "
            elif len(okapi) == 5:
                strItem = strItem + okapi + "  "
            else:
                strItem = strItem + okapi + " "
        f.write(strItem + "\n")
    f.close()

# main
def main():
    # Bước 1
    # path = raw_input('Nhập đường dẫn thư mục: ')
    print('Đang xử lý! Vui lòng chờ...')
    path = 'Out_Data/'
    list_path = browseFiles(path)
    read_files = readFile(list_path)
    files_filted = filterTexts(read_files)
    out_path = path

    # Bước 2
    while True:
        keyStep2 = raw_input('Chọn phương pháp Bow hoặc TF-IDF (0/1): ')
        keyStep2 = str(keyStep2)
        if keyStep2 == '0':
            BagOfWord = bagOfWords(files_filted)
            writeVectorFite(BagOfWord, 'BoW', list_path, out_path)
            break
        if keyStep2 == '1':
            TF_IDF = tF_IDF(files_filted)
            writeVectorFite(TF_IDF, 'TF-IDF', list_path, out_path)
            break

    # Bước 3
    while True:
        keyStep3 = raw_input('Chọn độ đo tương đồng Cossim hoặc Okapi (0/1): ')
        keyStep3 = str(keyStep3)
        if keyStep3 == '0':
            if keyStep2 == '0':
                writeCossimFile(BagOfWord, "BoW_CosSim", out_path)
            else:
                writeCossimFile(TF_IDF, "TF-IDF_CosSim", out_path)
            break
        if keyStep3 == '1':
            if keyStep2 == '0':
                writeOkapiFile(files_filted, "BoW_OkapiBM25", out_path)
            else:
                writeOkapiFile(files_filted, "TF-IDF_OkapiBM25", out_path)
            break

    print('=> Đã xuất file tới: ', out_path)

if __name__ == '__main__':
    main()