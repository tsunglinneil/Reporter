# coding=utf-8
import leveldb

# converting functions
# 需要converting functions的理由：(官方文件描述)
# Links : https://github.com/google/leveldb/blob/master/doc/index.md
# Reason: The leveldb library provides a persistent key value store. Keys and values are arbitrary byte arrays.
def cvt_to_bytes(string):
    # leave type check for system exceptions
    # return string.encode('ascii')  # 中文不在其可編碼範圍
    return string.encode()  # The default encoding for Python source code is UTF-8


def cvt_list_to_bytes(datas):
    return bytearray(datas, 'utf-8')


def cvt_to_string(bytestring):
    # leave type check for system exceptions
    return bytestring.decode()


def cvt_b(key, value):
    key_b = key
    value_b = value
    if isinstance(key, type('str')):
        key_b = cvt_to_bytes(key)
    if isinstance(value, type('str')):
        value_b = cvt_to_bytes(value)
    return key_b, value_b


def cvt_s(key, value):
    key_s = key
    value_s = value

    if isinstance(key, (bytes, bytearray)):
        key_s = cvt_to_string(key)
    if isinstance(value, (bytes, bytearray)):
        value_s = cvt_to_string(value)
    return key_s, value_s


# database functions
def init(filename):
    db = leveldb.LevelDB(filename)
    return db


def insert(db, key, value):
    key_b, name_b = cvt_b(key, value)
    db.Put(key_b, name_b)


def delete(db, key):
    key_b = cvt_to_bytes(key)
    db.Delete(key_b)


def update(db, key, value):
    key_b, name_b = cvt_b(key, value)
    db.Put(key_b, name_b)


def search(db, key):
    key_b = cvt_to_bytes(key)
    value = db.Get(key_b)
    value_str = cvt_to_string(value)
    return value_str


def dump(db):
    print("=========START DUMP ALL DATA RECORD==========")
    for key, value in db.RangeIter():
        key_s, value_s = cvt_s(key, value)
        print ("Key: {} \nValue: [\n{}\n]".format(key_s, value_s))
        print()
    print("=========END   DUMP ALL DATA RECORD==========")


# 一次性更新或寫入所有異動
# 1.產生WriteBatch
def init_batch():
    return leveldb.WriteBatch()


# 2.紀錄更新或新增資料
def write_batch(batch, key, value):
    key_b, name_b = cvt_b(key, value)
    batch.Put(key_b, name_b)


# 3.刪除特定資料
def delete_batch(batch, key):
    key_b = cvt_to_bytes(key)
    batch.Delete(key_b)


# 4.確認更新或寫入
def commit_batch(db, batch):
    db.Write(batch, sync=True)
