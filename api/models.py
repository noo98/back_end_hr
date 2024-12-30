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
    nickname = models.CharField(max_length=50)  # Nicknam
    date_of_birth = models.DateField()  # ວັນເດືອນປີເກີດ (Date of birth)
    employment_date = models.DateField()  # ວັນເຂົ້າການ (Date of joining)
    percent_95 = models.DateField(null=True, blank=True)  # 95% status
    youth_reserve = models.DateField()  # ພັກສຳຮອງ
    youth_full = models.DateField()  # ພັກສົມບູນ
    labor_union = models.DateField()  # ກຳມະບານ
    phone = models.CharField(max_length=15)  # ເບີຕິດຕໍ່ (Phone number)
    home_address = models.CharField(max_length=255)  # ບ້ານເກີດ (Home address)
    current_address = models.CharField(max_length=255)  # ບ້ານປັດຈຸບັນ (Current address)
    field_of_study = models.CharField(max_length=100)  # ວິຊາສະເພາະ (Specialization
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



class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class EducationLevel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
class Status(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
class SalaryGrade(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    min_salary = models.DecimalField(max_digits=10, decimal_places=2)
    max_salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.min_salary} - {self.max_salary})"
    
class Position(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

# class Birthplace(models.Model):
#     id = models.AutoField(primary_key=True)
#     village = models.CharField(max_length=255)
#     city = models.CharField(max_length=255)
#     province = models.CharField(max_length=255)

#     def __str__(self):
#         return f"{self.village}, {self.city}, {self.province}"

class Province_LCIC(models.Model):
    Prov_ID = models.CharField(max_length=50, blank=True, null=True)
    Province_Name = models.CharField(max_length=255, blank=True, null=True)
    
class District(models.Model):
    ID = models.IntegerField(blank=True, null=True)
    Prov_ID = models.CharField(max_length=255, blank=True, null=True)
    Dstr_ID = models.CharField(max_length=255, blank=True, null=True)
    District_Name = models.CharField(max_length=2500, blank=True, null=True)
    
class Village(models.Model):
    ID = models.IntegerField(blank=True, null=True)
    Prov_ID = models.CharField(max_length=255, blank=True, null=True)
    Dstr_ID = models.CharField(max_length=255, blank=True, null=True)
    Vill_ID = models.CharField(max_length=255, blank=True, null=True)
    Village_Name = models.CharField(max_length=2500, blank=True, null=True)