from django.db import models
from django.db import models
import os
import os
from django.utils import timezone
from decimal import Decimal
from datetime import date, datetime
import datetime
import os
from unidecode import unidecode
from django.utils.timezone import now
import re
def department_directory_path(instance, filename):
    # return os.path.join('documents', str(instance.department.id), filename)
    name, ext = os.path.splitext(filename)
    if ext.lower() == '.docx':
        ascii_name = unidecode(name)
        ascii_name = re.sub(r'[^a-zA-Z0-9]+', '_', ascii_name)
        name = ascii_name
    return f'documents/{str(instance.department.id)}/{name}{ext}'

def general_document_directory_path(instance, filename):
    # return os.path.join('documents_general', str(instance.department.id), filename)
    name, ext = os.path.splitext(filename)
    if ext.lower() == '.docx':
        ascii_name = unidecode(name)
        ascii_name = re.sub(r'[^a-zA-Z0-9]+', '_', ascii_name)
        name = ascii_name
    return f'documents_general/{str(instance.department.id)}/{name}{ext}'

class SystemUser(models.Model):
    us_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)  # Store hashed passwords
    Department = models.ForeignKey('Department', on_delete=models.CASCADE)
    Employee =  models.ForeignKey('Employee_lcic', on_delete=models.CASCADE) # ພະແນກ
    status = models.IntegerField()
    pic = models.ImageField(upload_to='user_img/',null=True,blank=True)  # ຮູບໂປຣຟາຍ (ທາງເລືອກ)

    def __str__(self):
        return self.username

class Sidebar(models.Model):
    sid_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Employee_lcic(models.Model):
    emp_id = models.AutoField(primary_key=True)  # ລະຫັດພະນັກງານ
    lao_name = models.CharField(max_length=100)  # ຊື່ພາສາລາວ
    eng_name = models.CharField(max_length=100)  # ຊື່ພາສາອັງກິດ
    nickname = models.CharField(max_length=50, blank=True, null=True)  # ຊື່ຫຼິ້ນ
    Gender = models.CharField(max_length=100)  #ເພດ
    birth_date = models.CharField(max_length=100, blank=True, null=True) # ວັນເດືອນປີເກີດ
    status = models.CharField(max_length=20)  # ສະຖານະພາບ (ເຊັ່ນ ໂສດ, ແຕ່ງງານ)
    Department = models.ForeignKey('Department', on_delete=models.CASCADE)
    pos_id = models.ForeignKey('Position', on_delete=models.CASCADE,null=True,blank=True) # ຕຳແໜ່ງ
    year_entry = models.CharField(null=True)  # ປີເຂົ້າເຮັດວຽກ
    age_entry = models.CharField(null=True,default=0)
    salary_level = models.CharField(max_length=100)# ຂັ້ນເງິນເດືອນ
    phone = models.CharField(max_length=20)  # ເບີໂທ
    pic = models.ImageField(upload_to='emp_img/',null=True)  # ຮູບໂປຣຟາຍ (ທາງເລືອກ)

    def __str__(self):
        return f"{self.emp_id} - {self.eng_name} ({self.nickname})"

    def save(self, *args, **kwargs):
        if self.year_entry:
            try:
                entry_date = datetime.datetime.strptime(self.year_entry, "%Y-%m-%d").date()
                today = datetime.date.today()
                delta = today - entry_date
                years = delta.days // 365
                # months = (delta.days % 365) // 30
                # day = (delta.days % 365) % 30
                self.age_entry = f"{years}"
            except ValueError:
                # ກໍລະນີວັນທີບໍ່ຖືກຮູບແບບ
                self.age_entry = None
        super().save(*args, **kwargs)

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
    name = models.CharField(max_length=255, unique=True,null=True)
    name_e = models.CharField(max_length=255, unique=True,null=True)

    def __str__(self):
            return self.name


class EducationLevel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
class Status(models.Model):
    sta_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    icon = models.CharField(max_length=255)
    Sidebar = models.ManyToManyField('Sidebar', related_name='status_roles', blank=True)
    def __str__(self):
        return self.name
    
class Document_Status(models.Model):
    docstat_id = models.AutoField(primary_key=True)
    doc_id = models.ForeignKey('document_lcic', on_delete=models.CASCADE, related_name='statuses')
    us_id = models.ForeignKey('SystemUser', on_delete=models.CASCADE, related_name='document_statuses')
    Doc_status = models.CharField(max_length=10, default='viewed')
    timestamp = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('doc_id', 'us_id')

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


class Document_type(models.Model):
    dmt_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)

class Document_format(models.Model):
    dmf_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    Department = models.ForeignKey("Department", on_delete=models.CASCADE, null=True)
    us_id = models.ForeignKey("SystemUser", on_delete=models.CASCADE, null=True)
    insert_date = models.CharField(max_length=255, null=True)
    update_date = models.DateField(auto_now=True, null=True)

class document_lcic(models.Model):
    doc_id = models.AutoField(primary_key=True) # ລະຫັດເອກະສານ
    insert_date = models.CharField(max_length=100, blank=True, null=True) # ວັນທີ່ເພີ່ມ
    date_add = models.DateTimeField(default=timezone.now, blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True, null=True)
    doc_number = models.CharField(max_length=100, blank=True, null=True, unique=True) # ເລກທີເອກະສານ
    subject = models.CharField(max_length=500, blank=True, null=True) # ເລື່ອງ
    format = models.ForeignKey(Document_format, on_delete=models.SET_NULL, null=True, blank=True)
    doc_type = models.CharField(max_length=255, blank=True, null=True) # ປະເພດເອກະສານ(ຂາເຂົ້າ, ຂາອອກ, ອື່ນໆ)
    doc_type_info = models.CharField(max_length=255, blank=True, null=True) # ປະເພດເອກະສານ ທີສົ່ງໃຫ້ພະແນກອື່ນ (ຂາເຂົ້າ, ຂາອອກ,)
    file = models.FileField(upload_to=department_directory_path, null=True,max_length=500) # ກຳນົດເສັ້ນທາງໄຟລ໌
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='document_lcic_department')
    document_detail = models.CharField(max_length=500, blank=True, null=True) # ລາຍລະອຽດ
    name = models.CharField(max_length=255, blank=True, null=True) # ຜູ້ສ້າງ
    department_into = models.ManyToManyField('Department', related_name='document_lcic_department_into', blank=True)  # ພະແນກທີ່ສົ່ງໃຫ້
    status = models.ManyToManyField('SystemUser', through='Document_Status', blank=True) # ສະຖານະເອກະສານ
    status2 = models.CharField(max_length=10, default='new')

class document_general(models.Model):
    docg_id = models.AutoField(primary_key=True) # ລະຫັດເອກະສານ
    insert_date = models.CharField(max_length=15, blank=True, null=True) # ວັນທີ່ເພີ່ມ
    update_date = models.DateField(auto_now=True, null=True)
    en_date = models.DateField(null=True, blank=True) # ວັນທີ່ເອກະສານສີນສຸດ
    status_doc = models.CharField(max_length=20, default="0") # ສະຖານະເອກະສານ ເຜີຍແຜ່, ບໍ່ເຜີຍແຜ່
    doc_number = models.CharField(max_length=100, blank=True, null=True, unique=True) # ເລກທີເອກະສານ
    subject = models.CharField(max_length=500, blank=True, null=True) # ເລື່ອງ
    format = models.ForeignKey(Document_format, on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(upload_to=general_document_directory_path, null=True,max_length=500) # ກຳນົດເສັ້ນທາງໄຟລ໌
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='document_lcic_general') # ພະແນກ
    document_detail = models.CharField(max_length=255, blank=True, null=True) # ລາຍລະອຽດ
    name = models.CharField(max_length=255, blank=True, null=True) # ຜູ້ສ້າງ

class PersonalInformation(models.Model):
    emp_id = models.ForeignKey(Employee_lcic, on_delete=models.CASCADE, null=True)  # ຮູບແບບ
    full_name = models.CharField(max_length=255, null=True, blank=True)  # ຊື່ເຕັມ
    dob = models.CharField(max_length=100, null=True, blank=True)  # ວັນເກີດ
    eth = models.CharField(max_length=100, null=True, blank=True)  # ຊົນເຜົ່າ
    rel = models.CharField(max_length=100, null=True, blank=True)  # ສາສະໜາ
    b_vill = models.CharField(max_length=100, null=True, blank=True)  # ບ້ານເກີດ
    b_dist = models.CharField(max_length=100, null=True, blank=True)  # ເມືອງເກີດ
    b_prov = models.CharField(max_length=100, null=True, blank=True)  # ແຂວງເກີດ
    c_vill = models.CharField(max_length=100, null=True, blank=True)  # ບ້ານປັດຈຸບັນ
    c_dist = models.CharField(max_length=100, null=True, blank=True)  # ເມືອງປັດຈຸບັນ
    c_prov = models.CharField(max_length=100, null=True, blank=True)  # ແຂວງປັດຈຸບັນ
    gov_entry = models.CharField(max_length=100, null=True, blank=True, default=None)  # ວັນເຂົ້າສັງກັດລັດ(ພະນັກງານສົມບູນ)
    youth_date = models.CharField(max_length=100, null=True, blank=True, default=None)  # ວັນເຂົ້າເປັນສະມາຊິກຊາວໝຸ່ມ
    women_date = models.CharField(max_length=100, null=True, blank=True, default=None)  # ວັນເຂົ້າເປັນສະມາຊິກແມ່ຍິງ
    union_date = models.CharField(max_length=100, null=True, blank=True, default=None)  # ວັນເຂົ້າເປັນສະມາຊິກກຳມະບານ
    party_cand_date = models.CharField(max_length=100, null=True, blank=True, default=None)  # ວັນເຂົ້າເປັນສະມາຊິກພັັກສຳຮອງ
    full_party_date = models.CharField(max_length=100, null=True, blank=True, default=None)  # ວັນເຂົ້າເປັນສະມາຊິກພັກສົມບູນ
    curr_party_pos = models.CharField(max_length=100, null=True, blank=True, default=None)  # ຕຳແໜ່ງຂອງພັກປັດຈຸບັນ
    party_apt_date = models.CharField(max_length=100, null=True, blank=True, default=None)  # ວັນທີເດືອນປີແຕ່ງຕັ້ງຄຕຳແໜ່ງຂອງພັກ
    curr_gov_pos = models.CharField(max_length=255, null=True, blank=True, default=None)  # ຕຳແໜ່ງເບື່ອງລັດປັດຈຸບັນ
    gov_apt_date = models.CharField(max_length=100, null=True, blank=True, default=None)  # ວັນທີເດືອນປີແຕ່ງຕັ້ງຕຳແໜ່ງຂອງລັດ


class Education(models.Model):
    emp_id = models.ForeignKey(Employee_lcic, on_delete=models.CASCADE,null=True) # ຮູບແບບ
    level = models.CharField(max_length=255, null=True, blank=True)  # ຂັ້ນ
    school = models.CharField(max_length=255, null=True, blank=True)  # ຊື່ໂຮງຮຽນ
    year = models.CharField(max_length=10, null=True, blank=True)  # ປີ
    dom_abrd = models.CharField(max_length=50, null=True, blank=True)  # ພາຍໃນ/ຕ່າງປະເທດ

class SpecializedEducation(models.Model):
    emp_id = models.ForeignKey(Employee_lcic, on_delete=models.CASCADE,null=True) # ຮູບແບບ
    field = models.CharField(max_length=255, null=True, blank=True)  # ຂະແໜງສຶກສາ
    inst = models.CharField(max_length=255, null=True, blank=True)  # ສະຖາບັນ
    level = models.CharField(max_length=100, null=True, blank=True)  # ຂັ້ນ
    year = models.CharField(max_length=100, null=True, blank=True)  # ປີ
    dom_abrd = models.CharField(max_length=50, null=True, blank=True)  # ພາຍໃນ/ຕ່າງປະເທດ

class PoliticalTheoryEducation(models.Model):
    emp_id = models.ForeignKey(Employee_lcic, on_delete=models.CASCADE,null=True) # ຮູບແບບ
    inst = models.CharField(max_length=255, null=True, blank=True)  # ສະຖາບັນ
    level = models.CharField(max_length=100, null=True, blank=True)  # ຂັ້ນ
    year = models.CharField(max_length=100, null=True, blank=True)  # ປີ
    dom_abrd = models.CharField(max_length=50, null=True, blank=True)  # ພາຍໃນ/ຕ່າງປະເທດ

class ForeignLanguage(models.Model):
    emp_id = models.ForeignKey(Employee_lcic, on_delete=models.CASCADE,null=True) # ຮູບແບບ
    lang = models.CharField(max_length=100, null=True, blank=True)  # ພາສາ
    prof = models.CharField(max_length=50, null=True, blank=True)  # ຄວາມຊໍານານ

class WorkExperience(models.Model):
    emp_id = models.ForeignKey(Employee_lcic, on_delete=models.CASCADE,null=True) # ຮູບແບບ
    work = models.CharField(max_length=255, null=True, blank=True)  # ສະຖານທີ່ເຮັດວຽກ
    start = models.CharField(max_length=100, null=True, blank=True)  # ວັນເລີ່ມຕົ້ນ
    end = models.CharField(max_length=100, null=True, blank=True)  # ວັນຈົບ
    gov_pos = models.CharField(max_length=255, null=True, blank=True)  # ຕໍາແຫນໃນລັດຕະການ
    party_pos = models.CharField(max_length=255, null=True, blank=True)  # ຕໍາແຫນຂອງພັກ

class TrainingCourse(models.Model):
    emp_id = models.ForeignKey(Employee_lcic, on_delete=models.CASCADE,null=True) # ຮູບແບບ
    start = models.CharField(max_length=255, null=True, blank=True)  # ວັນເລີ່ມຕົ້ນ
    end = models.CharField(max_length=255, null=True, blank=True)  # ວັນຈົບ
    subj = models.CharField(max_length=255, null=True, blank=True)  # ວິຊາ
    inst = models.CharField(max_length=255, null=True, blank=True)  # ສະຖາບັນ
    country = models.CharField(max_length=100, null=True, blank=True)  # ປະເທດ
    
class Award(models.Model):
    emp_id = models.ForeignKey(Employee_lcic, on_delete=models.CASCADE,null=True) # ຮູບແບບ
    dec_num = models.CharField(max_length=100, null=True, blank=True)  # ເລກທີ່ການຕັດສິນໃຈ
    date = models.CharField(max_length=255, null=True, blank=True)  # ວັນທີ
    award_type = models.CharField(max_length=255, null=True, blank=True)  # ປະເພດລາງວັນ
    reason = models.TextField(null=True, blank=True)  # ເຫດຜົນ

class DisciplinaryAction(models.Model):
    emp_id = models.ForeignKey(Employee_lcic, on_delete=models.CASCADE,null=True) # ຮູບແບບ
    dec_num = models.CharField(max_length=100, null=True, blank=True)  # ເລກທີ່ການຕັດສິນໃຈ
    date = models.CharField(max_length=255, null=True, blank=True)  # ວັນທີ
    action_type = models.CharField(max_length=255, null=True, blank=True)  # ປະເພດມາດຕະການ
    reason = models.TextField(null=True, blank=True)  # ເຫດຜົນ

class FamilyMember(models.Model):
    emp_id = models.ForeignKey(Employee_lcic, on_delete=models.CASCADE,null=True) # ຮູບແບບ
    relation = models.CharField(max_length=50, null=True, blank=True)  # ຄວາມສຳພັນ (ເມຍ, ພໍ່, ແມ່, ເຫຼົ້າ)
    full_name = models.CharField(max_length=255, null=True, blank=True)  # ຊື່ເຕັມ
    dob = models.CharField(max_length=255, null=True, blank=True)  # ວັນເກີດ
    eth = models.CharField(max_length=100, null=True, blank=True)  # ຊົນເຜົ່າ
    rel = models.CharField(max_length=100, null=True, blank=True)  # ສາສະໜາ
    occ = models.CharField(max_length=255, null=True, blank=True)  # ອາຊີບ
    work = models.CharField(max_length=255, null=True, blank=True)  # ສະຖານທີ່ເຮັດວຽກ
    vill = models.CharField(max_length=100, null=True, blank=True)  # ບ້ານ
    dist = models.CharField(max_length=100, null=True, blank=True)  # ເມືອງ
    prov = models.CharField(max_length=100, null=True, blank=True)  # ແຂວງ

class Evaluation(models.Model):
    emp_id = models.ForeignKey(Employee_lcic, on_delete=models.CASCADE,null=True) # ຮູບແບບ
    strengths = models.TextField(null=True, blank=True)  # ຈຸດແຂງແຮງ
    weaknesses = models.TextField(null=True, blank=True)  # ຈຸດອ່ອນ

    def __str__(self):
        return self.emp_id
    
class Position(models.Model):
    pos_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)


class Salary(models.Model):
    sal_id = models.AutoField(primary_key=True)
    pos_id = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True)
    SalaryGrade = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True)  # ເງິນເດືອນ


class SubsidyPosition(models.Model):
    sp_id = models.AutoField(primary_key=True)
    pos_id = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True)
    grant = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True)

class SubsidyYear(models.Model):
    sy_id = models.AutoField(primary_key=True)
    year_range = models.CharField(max_length=50,null=True, blank=True)  # e.g. "1-5", "6-15"
    y_subsidy = models.BigIntegerField(null=True, blank=True)

class SystemSetting(models.Model):
    key = models.CharField(max_length=50, unique=True)
    date = models.DateField(auto_now=True, null=True, blank=True)
    value = models.CharField(max_length=100)

class FuelSubsidy(models.Model):
    fs_id = models.AutoField(primary_key=True)
    pos_id = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now=True, null=True)
    fuel_subsidy = models.DecimalField(max_digits=12, decimal_places=2,null=True, blank=True)
    fuel_price = models.ForeignKey(SystemSetting, on_delete=models.CASCADE,null=True, blank=True)
    total_fuel = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
class Fuel_payment(models.Model):
    fp_id = models.AutoField(primary_key=True)
    emp_id = models.ForeignKey(Employee_lcic, on_delete=models.CASCADE, null=True, blank=True)

class AnnualPerformanceGrant(models.Model):
    APG_id = models.AutoField(primary_key=True)
    level = models.CharField(max_length=50, null=True, blank=True)  # ລະດັບ
    calculate = models.FloatField()

class SpecialDayGrant(models.Model):
    sdg_id = models.AutoField(primary_key=True)
    occasion_name = models.CharField(max_length=255)
class SpecialDay_Position(models.Model):
    special_day = models.ForeignKey(SpecialDayGrant, on_delete=models.CASCADE)
    pos_id = models.ForeignKey(Position, on_delete=models.CASCADE)
    grant = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  # ຈຳນວນເງິນທີ່ເພີ່ມໃນວັນສຳຄັນ

class MobilePhoneSubsidy(models.Model):
    mb_id = models.AutoField(primary_key=True)
    pos_id = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True)
    grant = models.BigIntegerField()

class OvertimeWork(models.Model):
    ot_id = models.AutoField(primary_key=True)
    emp_id = models.ForeignKey(Employee_lcic, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    csd_evening = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  # ວັນລັດຖະການເງິນເພີ່ມໃນຄແລງ 17:00-22:00
    csd_night = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  # ວັນລັດຖະການເງິນເພີ່ມໃນຕອນກາງຄືນ 22:00-6:00
    hd_mor_after= models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  # ວັນພັກເງິນເພີ່ມໃນເວັນ 8:00-16:00
    hd_evening = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  # ວັນພັກເງິນເພີ່ມໃນຕອນແລງ 16:00-22:00
    hd_night = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  # ວັນພັກເງິນເພີ່ມໃນຕອນກາງຄືນ 22:00-6:00
    total_ot = models.BigIntegerField(null=True, blank=True)  # ຍອມໃຫ້ປ່ຽນແປງໄດ້ ແລະໃສ່ຄ່າວ່າງໄດ້

class Saving_cooperative(models.Model):
    sc_id = models.AutoField(primary_key=True)
    emp_id = models.ForeignKey(Employee_lcic, on_delete=models.CASCADE) # ລະຫັດພະນັກງານ
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True) # ຈຳນວນເງິນກູ້
    interest = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True) # ອັດຕາດອກເບີກ
    deposit = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True) # ຈຳນວນເງິນຝາກ
    Loan_deduction_194 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True) # ຈຳນວນເງິນຫຼຸດການກູ້ 194
    date = models.DateField(auto_now=True) # ວັນທີ່ບັນທຶກ


class monthly_payment(models.Model):
    id = models.AutoField(primary_key=True)
    emp_id = models.ForeignKey(Employee_lcic, on_delete=models.CASCADE, null=True, blank=True)  # ພະນັກງານ
    sy_id = models.ForeignKey(SubsidyYear, on_delete=models.CASCADE, null=True, blank=True)  # ປີທີ່ຈ່າຍເງິນ 
    date = models.DateField(auto_now_add=True)  # ວັນທີ່ຈ່າຍເງິນ     
    child = models.IntegerField(null=True, blank=True)  # ລູກ
    child_Subsidy = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  # ອຸດໜູນລູກ
    health_Subsidy = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  # ອຸດໜູນສຸຂະພາບ

class col_policy(models.Model):
    col_id = models.AutoField(primary_key=True)
    emp_id = models.ForeignKey(Employee_lcic, on_delete=models.CASCADE, null=True, blank=True)  # ພະນັກງານ

class job_mobility(models.Model):
    jm_id = models.AutoField(primary_key=True)
    date = models.DateField(auto_now=True)  # ວັນທີ່ການເຄື່ອນໄຫວ
    pos_id = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True)  # ຕຳແໜ່ງ
    amount_per_day = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  # ຈຳນວນເງິນຕໍ່ມື້
    jm_policy = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  # ນະໂຍບາຍການເຄື່ອນໄຫວງານ
    number_of_days = models.IntegerField(null=True, blank=True)  # ຈຳນວນມື້

class uniform_price(models.Model):
    key = models.CharField(max_length=50, unique=True)
    date = models.DateField(auto_now=True, null=True, blank=True)
    emp_uniform = models.CharField(max_length=100, null=True, blank=True)  # ປະເພດເສື້ອ
    formal_suit = models.CharField(max_length=50, null=True, blank=True)  # ສູດທາງການ
    amount_uni = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    amount_sui = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True) 
class uniform(models.Model):
    uni_id = models.AutoField(primary_key=True)  # ລະຫັດເສື້ອ
    emp_id = models.ForeignKey(Employee_lcic, on_delete=models.CASCADE, null=True, blank=True)  # ພະນັກງານ
    date = models.DateField( auto_now=True, null=True, blank=True)  
    uniform_price = models.ForeignKey(uniform_price, on_delete=models.CASCADE,null=True, blank=True)

class income_tax(models.Model):
    tax_id = models.AutoField(primary_key=True)  # ລະຫັດພາສີ
    lvl = models.PositiveIntegerField(unique=True)  # ຂັ້ນ
    incom_base = models.CharField(max_length=35)  # ພື້ນຖານລາຍໄດ້
    calculation_base = models.DecimalField(max_digits=12, decimal_places=2)  # ພື້ນຖານການຄິດໄລ່
    tariff = models.DecimalField(max_digits=12, decimal_places=2)  # ອັດຕາພາສີ
    each_level_tax = models.DecimalField(max_digits=12, decimal_places=2)  # ພາສີຕໍ່ຂັ້ນ
    all_tax = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  # ພາສີທັງໝົດ

class welfare(models.Model):
    wf_id = models.AutoField(primary_key=True)  # ລະຫັດສິນເສີມ
    date = models.DateField(null=True, blank=True)  # ວັນທີ່ເພີ່ມ
    emp_id = models.ForeignKey(Employee_lcic, on_delete=models.CASCADE, null=True, blank=True)  # ພະນັກງານ
    emp_type = models.CharField(max_length=50, null=True, blank=True)  # ປະເພດພະນັກງານ (ເກົ່າ, ໃໝ່)
    from_company = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # ລັດສະເພາະ
    from_emp = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # ລັດສະເພາະຈາກພະນັກງານ

class evaluation_score(models.Model):
    es_id = models.AutoField(primary_key=True)
    es_type = models.CharField(max_length=50, null=True, blank=True)  # ປະເພດຄະແນນ
    calclate = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  # ຄະແນນທີ່ຄິດໄລ່

class evaluation_score_emp(models.Model):
    ese_id = models.AutoField(primary_key=True)
    emp_id = models.ForeignKey(Employee_lcic, on_delete=models.CASCADE, null=True, blank=True)  # ພະນັກງານ
    es_id = models.ForeignKey(evaluation_score, on_delete=models.CASCADE, null=True, blank=True)  # ຄະແນນ

# history models

class Overtime_history(models.Model):
    id = models.AutoField(primary_key=True)  # ID as AutoField
    date_insert = models.DateTimeField(auto_now_add=True)  # ວັນທີ່ເພີ່ມ
    date = models.DateField(null=True, blank=True)
    ot_id = models.BigIntegerField()
    emp_id = models.BigIntegerField()
    emp_name = models.CharField(max_length=255,null=True, blank=True)
    pos_id = models.BigIntegerField()
    position = models.CharField(max_length=255,null=True, blank=True)
    csd_evening = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    csd_night = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    hd_mor_after = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    hd_evening = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    hd_night = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True) 
    salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    value_150 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    value_200 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    value_250 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    value_300 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    value_350 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    total_ot = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

class colpolicy_history(models.Model):
    id = models.AutoField(primary_key=True)  # ID as AutoField
    date_insert = models.DateTimeField(auto_now_add=True)
    date = models.DateField(null=True, blank=True)
    col_id = models.BigIntegerField()
    emp_id = models.BigIntegerField()
    pos_id = models.BigIntegerField()
    number_of_days = models.CharField(max_length=10)
    amount_per_day = models.CharField(max_length=20)
    total_amount = models.CharField(max_length=20)
    jm_policy = models.CharField(max_length=20)
    total_payment = models.CharField(max_length=20)

class fuel_payment_history(models.Model):
    id = models.AutoField(primary_key=True)  # ID as AutoField
    date_insert = models.DateTimeField(auto_now_add=True)  # ວັນທີ່ເພີ່ມ
    date = models.DateField(null=True, blank=True)
    fp_id = models.BigIntegerField()
    emp_id = models.BigIntegerField()
    emp_name = models.CharField(max_length=255, null=True, blank=True)
    emp_id = models.BigIntegerField()
    position = models.CharField(max_length=255, null=True, blank=True)
    fuel_subsidy = models.CharField(max_length=50, null=True, blank=True)
    fuel_price = models.CharField(max_length=50, null=True, blank=True)
    total_fuel = models.CharField(max_length=50, null=True, blank=True)

class specialday_emp_history(models.Model):
    id = models.AutoField(primary_key=True)  # ID as AutoField
    date_insert = models.DateTimeField(auto_now_add=True)  # ວັນທີ່ເພີ່ມ
    date = models.DateField(null=True, blank=True)
    emp_id = models.IntegerField()
    emp_name = models.CharField(max_length=255)
    pos_id = models.IntegerField()
    pos_name = models.CharField(max_length=255)
    sdg_id = models.IntegerField()
    sdg_name = models.CharField(max_length=255)
    grant = models.DecimalField(max_digits=12, decimal_places=2)

class MobilePhoneSubsidy_emp_History(models.Model):
    date = models.DateField()  # ວັນທີ່ກ່ຽວຂ້ອງ (ຕົວຢ່າງ: ວັນທີ່ມອບເງິນ)
    date_insert = models.DateField(auto_now_add=True)  # ວັນທີ່ເພີ່ມເຂົ້າລະບົບ
    emp_id = models.IntegerField()  # ລະຫັດພະນັກງານ
    lao_name = models.CharField(max_length=100)  # ຊື່ພະນັກງານ
    pos_id = models.IntegerField()  # ລະຫັດຕຳແໜ່ງ
    pos_name = models.CharField(max_length=100)  # ຊື່ຕຳແໜ່ງ
    mb_id = models.IntegerField()  # ລະຫັດຂອງ MobilePhoneSubsidy
    grant = models.BigIntegerField()  # ຈໍານວນເງິນຊ່ວຍເຫຼືອ

class saving_cooperative_history(models.Model):
    id = models.AutoField(primary_key=True)  # ID as AutoField
    date_insert = models.DateTimeField(auto_now_add=True)  # ວັນທີ່ເພີ່ມ
    date = models.DateField()
    emp_id = models.IntegerField()
    emp_name = models.CharField(max_length=255)
    pos_id = models.IntegerField()
    pos_name = models.CharField(max_length=255)
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest = models.DecimalField(max_digits=12, decimal_places=2)
    deposit = models.DecimalField(max_digits=12, decimal_places=2)
    Loan_deduction_194 = models.DecimalField(max_digits=12, decimal_places=2)
    total_Saving = models.DecimalField(max_digits=15, decimal_places=2)

class uniform_history(models.Model):
    uh_id = models.AutoField(primary_key=True)  
    uni_id = models.IntegerField()  
    date_insert = models.DateTimeField(auto_now_add=True) 
    date = models.DateField(null=True, blank=True)
    emp_id = models.IntegerField()  
    emp_name = models.CharField(max_length=255) 
    pos_id = models.IntegerField()  
    pos_name = models.CharField(max_length=255)  
    formal_suit = models.DecimalField(max_digits=12, decimal_places=2)  
    amount_sui = models.IntegerField()
    emp_uniform = models.DecimalField(max_digits=12, decimal_places=2)  
    amount_uni = models.IntegerField()  
    total_amount = models.DecimalField(max_digits=15, decimal_places=2) 

class evaluation_score_emp_history(models.Model):
    eseh_id = models.AutoField(primary_key=True)  # ລະຫັດບັນທຶກ
    ese_id = models.IntegerField()  # ລະຫັດຄະແນນພະນັກງານ
    date_insert = models.DateTimeField(auto_now_add=True)  # ວັນທີ່ເພີ່ມ
    emp_id = models.IntegerField(null=True, blank=True)  # ລະຫັດພະນັກງານ
    date = models.DateField(null=True, blank=True)
    emp_name = models.CharField(max_length=255, null=True, blank=True)  # ຊື່ເຕັມ
    pos_id = models.IntegerField()
    pos_name = models.CharField(max_length=255)
    salary =models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    es_id = models.IntegerField(null=True, blank=True)  # ລະຫັດຄະແນນ
    es_type = models.CharField(max_length=50, null=True, blank=True)  # ປະເພດຄະແນນ
    calclate = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  # ຄະແນນ
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)  # ຈຳນວນເງິນທີ່ເພີ່ມ

class monthly_payment_history(models.Model):
    mph_id = models.AutoField(primary_key=True)
    date_insert = models.DateTimeField(auto_now_add=True)  # ວັນທີ່ເພີ່ມ
    date = models.DateField(null=True, blank=True)
    emp_id = models.IntegerField(null=True, blank=True)
    lao_name = models.CharField(max_length=255, null=True, blank=True)
    pos_id = models.IntegerField(null=True, blank=True)
    position = models.CharField(max_length=255, null=True, blank=True)
    salary = models.FloatField(null=True, blank=True)
    wf_emp = models.FloatField(null=True, blank=True)
    wf_cpn = models.FloatField(null=True, blank=True)
    position_subsidy = models.FloatField(null=True, blank=True)
    age = models.CharField(max_length=10, null=True, blank=True)
    get_1_5 = models.FloatField(null=True, blank=True)
    get_6_15 = models.FloatField(null=True, blank=True)
    get_16_25 = models.FloatField(null=True, blank=True)
    get_26 = models.FloatField(null=True, blank=True)
    year_subsidy_total = models.FloatField(null=True, blank=True)
    ot = models.FloatField(null=True, blank=True)
    basic_income = models.FloatField(null=True, blank=True)
    fuel = models.FloatField(null=True, blank=True)  
    regular_income = models.FloatField(null=True, blank=True)
    other_income = models.FloatField(null=True, blank=True)
    income_before_tax = models.FloatField(null=True, blank=True)
    exempt = models.FloatField(null=True, blank=True)
    tax_5 = models.FloatField(null=True, blank=True)
    tax_10 = models.FloatField(null=True, blank=True)
    tax_15 = models.FloatField(null=True, blank=True)
    tax_20 = models.FloatField(null=True, blank=True)
    tax_25 = models.FloatField(null=True, blank=True)
    total_tax = models.FloatField(null=True, blank=True)
    income_after_tax = models.FloatField(null=True, blank=True)
    child = models.IntegerField(null=True, blank=True)
    child_subsidy = models.FloatField(null=True, blank=True)
    child_subsidy_total = models.FloatField(null=True, blank=True)
    health_subsidy = models.FloatField(null=True, blank=True)
    loan = models.FloatField(null=True, blank=True)
    interest = models.FloatField(null=True, blank=True)
    deposit = models.FloatField(null=True, blank=True)
    loan_194 = models.FloatField(null=True, blank=True)
    saving_total = models.FloatField(null=True, blank=True)
    salary_payment = models.FloatField(null=True, blank=True)
    monthly_income = models.FloatField(null=True, blank=True)