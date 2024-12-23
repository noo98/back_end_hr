from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class UserLogin(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'user_login'

class Employee_lcic(models.Model):
    emp_id = models.AutoField(primary_key=True)  # Employee ID (Auto-increment)
    gender = models.CharField(max_length=10)  # Gender (e.g., Male, Female)
    name_E = models.CharField(max_length=100)  # English name
    name_L = models.CharField(max_length=100)  # Lao name
    nickname = models.CharField(max_length=50)  # Nickname
    position = models.CharField(max_length=100)  # ຕຳແໜ່ງ (Position)
    date_of_birth = models.DateField()  # ວັນເດືອນປີເກີດ (Date of birth)
    employment_date = models.DateField()  # ວັນເຂົ້າການ (Date of joining)
    percent_95 = models.DateField()  # 95% status
    youth_reserve = models.DateField()  # ພັກສຳຮອງ
    youth_full = models.DateField()  # ພັກສົມບູນ
    labor_union = models.DateField()  # ກຳມະບານ
    phone = models.CharField(max_length=15)  # ເບີຕິດຕໍ່ (Phone number)
    home_address = models.CharField(max_length=255)  # ບ້ານເກີດ (Home address)
    current_address = models.CharField(max_length=255)  # ບ້ານປັດຈຸບັນ (Current address)
    education_level = models.CharField(max_length=100)  # ລະດັບການສຶກສາ (Education level)
    field_of_study = models.CharField(max_length=100)  # ວິຊາສະເພາະ (Specialization)
    status = models.CharField(max_length=50)  # ສະຖານະພາບ (Status)
    salary_grade = models.CharField(max_length=50)  # ຂັ້ນເງິນເດືອນ (Salary grade)
    employment_years = models.IntegerField()  # ປີການ (Years of employment)

    def __str__(self):
        return f"{self.emp_id} - {self.name_E} ({self.nickname})"
    
class DocumentEntry(models.Model):
    date = models.DateField()  # Date field for the document's date
    number = models.CharField(max_length=50)  # A field for the document number
    subject = models.CharField(max_length=255)  # Field for the subject of the document
    section = models.CharField(max_length=100)  # Field for the section related to the document
    file = models.CharField(max_length=255)  # Field to store the file, specifying the upload directory
    receiver = models.CharField(max_length=255)  # Receiver of the document
    document = models.CharField(max_length=100)  # Field for storing document details or description

    def __str__(self):
        return f"{self.number} - {self.subject}"


class Document_out(models.Model):
    date = models.DateField()  # Date field for the document's date
    number = models.CharField(max_length=50)  # A field for the document number
    subject = models.CharField(max_length=255)  # Field for the subject of the document
    section = models.CharField(max_length=100)  # Field for the section related to the document
    file = models.CharField(max_length=255)  # Field to store the file, specifying the upload directory
    Sender = models.CharField(max_length=255)  # Receiver of the document
    document = models.CharField(max_length=100)  # Field for storing document details or description

    def __str__(self):
        return f"{self.number} - {self.subject}"
    
class activity(models.Model):
    Tname = models.CharField(max_length=50)  
    Tdeteil = models.CharField(max_length=255)
    Tfrom = models.CharField(max_length=100) 
    Tplace = models.CharField(max_length=100)
    Command = models.CharField(max_length=150)
    Tdate = models.DateField()

    def __str__(self):
        return f"{self.number} - {self.subject}"
