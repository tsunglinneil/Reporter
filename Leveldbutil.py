# coding=utf-8
import leveldb
import array


# converting functions
# �ݭnconverting functions���z�ѡG(�x����y�z)
# Links : https://github.com/google/leveldb/blob/master/doc/index.md
# Reason: The leveldb library provides a persistent key value store. Keys and values are arbitrary byte arrays.
def cvt_to_bytes(string):
    # leave type check for system exceptions
    # return string.encode('ascii')  # ���夣�b��i�s�X�d��
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


# �@���ʧ�s�μg�J�Ҧ�����
# 1.����WriteBatch
def init_batch():
    return leveldb.WriteBatch()


# 2.������s�ηs�W���
def write_batch(batch, key, value):
    key_b, name_b = cvt_b(key, value)
    batch.Put(key_b, name_b)


# 3.�R���S�w���
def delete_batch(batch, key):
    key_b = cvt_to_bytes(key)
    batch.Delete(key_b)

# 3.�T�{��s�μg�J
def commit_batch(db, batch):
    db.Write(batch, sync=True)
