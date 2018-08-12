from mongoengine import *

# connect('ultrabear_homework',host='127.0.0.1',port=27017)
connect('mongodb://jamie:jamie199469@localhost:27676/ultrabear_homework', serverSelectionTimeoutMS=3)


class Student(Document):
    """
    报名信息
    """
    sexChoice = ((0, '女'),
                   (1, '男'))
    gradeChoice = (1,2,3,4,5,6)

    name = StringField(required=True)
    fname = StringField(required=True)
    grade = IntField(required=True, max_length=3, choice=gradeChoice)
    phone = StringField(required=True,unique=True)
    equipments = ListField(StringField(max_length=50),required=True)
    sex = IntField(required=True, choice=sexChoice)
    city = StringField(required=True)


class File(Document):
    """
    文件
    """
    filename = StringField()
    size = IntField()
    content = BinaryField()
    md5 = StringField()
    time = DateTimeField()
    mime = StringField()


class Day(Document):
    """
    优秀作品
    """
    name = StringField()
    homeWork = StringField()
    imgfile = StringField()
    text = StringField()
    comments = StringField()
    kadaUrl = StringField()
    title = StringField()
    videofile = StringField()

