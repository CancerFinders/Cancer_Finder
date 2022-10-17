from pymongo import MongoClient

def insert_file_info(filename, img_type, is_cancer, cancer_type, comment):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['cancer']

    cancer = db.cancer
    cancer_one = {
        "filename": str(filename),
        "img_type": str(img_type),
        "is_cancer": str(is_cancer),
        "cancer_type": str(cancer_type),
        "comment": str(comment)}

    find = cancer.find_one(cancer_one)

    print(find)
    if ( find == None):
        cancer_id = cancer.insert_one(cancer_one).inserted_id