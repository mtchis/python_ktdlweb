import os
import re
from bs4 import BeautifulSoup
import nltk

nltk.download('stopwords')
nltk.download('punkt')
from nltk.tokenize import word_tokenize, sent_tokenize
from string import punctuation
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
my_stopwords = set(stopwords.words('english') + list(punctuation))
ps = PorterStemmer()

# Hàm duyệt danh sách file từ thư mục
pattern = 'json'
def browseFiles(path):
    list_path = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if not re.search(pattern, file):
                list_path.append(root + '/' + file)
    return list_path

# Hàm đọc file, xử lý
def readFile(list_path):
    read_files = []
    i = 0
    for i in range(len(list_path)):
        read_file = open(list_path[i], "r", encoding="utf8")
        a = read_file.readlines()
        a = ' '.join(a)
        read_files.append(a)
    return read_files

# Hàm xử lý HTML
def clean_html(text):
    soup = BeautifulSoup(text, 'html.parser')
    return soup.get_text()

# Hàm loại bỏ các ký tự đạc biệt và chuẩn hóa khoảng trắng
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
        words = '\n'.join(words)
        # Loại bỏ từ duplicate
        # words = '\n'.join(remove_duplicate(words.split()))
        res.append(words)
    return res

# Ghi ra file txt
def writeVectorFite(txtAfter, outputName, o_path):
    f = open(o_path + "/" + outputName + "_word.txt", 'w', encoding='utf-8-sig')
    f.write(str(txtAfter))
    f.close()

# main
def main():
    path = input('Nhập thư mục <TenWebsite>/<Topic>: ')
    path = 'Out_Data/' + path
    list_path = browseFiles(path)
    o_path = path
    for i in range(len(list_path)):
        filename = os.path.basename(list_path[i])
        slipt_filename = os.path.splitext(filename)
        name_file = slipt_filename[0]

        read_files = readFile(list_path)
        files_filted = filterTexts(read_files)
        writeVectorFite(files_filted[i], str(name_file), o_path)
    print('Đã xuất file tới: ', o_path)
if __name__ == "__main__":
    main()


