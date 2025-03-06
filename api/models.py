from django.db import models
# from django.contrib.auth.models import User

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class SystemUser(models.Model):
    us_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)  # Store hashed passwords
    Department = models.ForeignKey('Department', on_delete=models.CASCADE)
    Employee =  models.ForeignKey('Employee_lcic', on_delete=models.CASCADE) # ພະແນກ
    status = models.IntegerField()

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
    position = models.CharField(max_length=100)  # ຕຳແໜ່ງ
    year_entry = models.CharField(null=True)  # ປີເຂົ້າເຮັດວຽກ
    salary_level = models.CharField(max_length=100)# ຂັ້ນເງິນເດືອນ
    phone = models.CharField(max_length=20)  # ເບີໂທ
    pic = models.ImageField(blank=True, null=True)  # ຮູບໂປຣຟາຍ (ທາງເລືອກ)

    def __str__(self):
        return f"{self.emp_id} - {self.name_E} ({self.nickname})"
      
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
    name = models.CharField(unique=True, max_length=250)

class document_lcic(models.Model):
    doc_id = models.AutoField(primary_key=True) # ລະຫັດເອກະສານ
    insert_date = models.CharField(max_length=100, blank=True, null=True) # ວັນທີ່ເພີ່ມ
    doc_number = models.CharField(max_length=100, blank=True, null=True) # ເລກທີເອກະສານ
    subject = models.CharField(max_length=255, blank=True, null=True) # ເລື່ອງ
    format = models.ForeignKey(Document_format, on_delete=models.CASCADE) # ຮູບແບບ
    doc_type = models.CharField(max_length=255, blank=True, null=True) # ປະເພດເອກະສານ(ຂາເຂົ້າ, ຂາອອກ, ອື່ນໆ)
    doc_type_info = models.CharField(max_length=255, blank=True, null=True) # ປະເພດເອກະສານ ທີສົ່ງໃຫ້ພະແນກອື່ນ (ຂາເຂົ້າ, ຂາອອກ,)
    file = models.FileField(upload_to='documents/',null=True) # ໄຟລແທນ
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='document_lcic_department')
    document_detail = models.CharField(max_length=255, blank=True, null=True) # ລາຍລະອຽດ
    name = models.CharField(max_length=255, blank=True, null=True) # ຜູ້ສ້າງ
    department_into = models.ManyToManyField('Department', related_name='document_lcic_department_into', blank=True)  # ພະແນກທີ່ສົ່ງໃຫ້
    status = models.ManyToManyField('SystemUser', through='Document_Status', blank=True) # ສະຖານະເອກະສານ
    status2 = models.CharField(max_length=10, default='new')

class document_general(models.Model):
    docg_id = models.AutoField(primary_key=True) # ລະຫັດເອກະສານ
    insert_date = models.CharField(max_length=100, blank=True, null=True) # ວັນທີ່ເພີ່ມ
    doc_number = models.CharField(max_length=100, blank=True, null=True) # ເລກທີເອກະສານ
    subject = models.CharField(max_length=255, blank=True, null=True) # ເລື່ອງ
    format = models.ForeignKey(Document_format, on_delete=models.CASCADE) # ຮູບແບບ
    file = models.FileField(upload_to='documents_general/',null=True) # ໄຟລແທນ
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='document_lcic_general') # ພະແນກ
    document_detail = models.CharField(max_length=255, blank=True, null=True) # ລາຍລະອຽດ
    name = models.CharField(max_length=255, blank=True, null=True) # ຜູ້ສ້າງ

class PersonalInformation(models.Model):
    per_id = models.AutoField(primary_key=True)  # ລະຫັດຂໍ້ມູນບຸກຄົນ
    full_name = models.CharField(max_length=255)  # ຊື່ເຕັມ
    dob = models.CharField(max_length=100)  # ວັນເກີດ
    eth = models.CharField(max_length=100)  # ຊົນເຜົ່າ
    rel = models.CharField(max_length=100)  # ສາສະໜາ
    b_vill = models.CharField(max_length=100)  # ບ້ານເກີດ
    b_dist = models.CharField(max_length=100)  # ເມືອງເກີດ
    b_prov = models.CharField(max_length=100)  # ແຂວງເກີດ
    c_vill = models.CharField(max_length=100)  # ບ້ານປັດຈຸບັນ
    c_dist = models.CharField(max_length=100)  # ເມືອງປັດຈຸບັນ
    c_prov = models.CharField(max_length=100)  # ແຂວງປັດຈຸບັນ
    gov_entry = models.CharField(max_length=100)  # ວັນເຂົ້າສັງກັດລັດ(ພະນັກງານສົມບູນ)
    youth_date = models.DateField(null=True, blank=True)  # ວັນເຂົ້າເປັນສະມາຊິກຊາວໝຸ່ມ
    women_date = models.DateField(null=True, blank=True)  # ວັນເຂົ້າເປັນສະມາຊິກແມ່ຍິງ
    union_date = models.DateField(null=True, blank=True)  # ວັນເຂົ້າເປັນສະມາຊິກກຳມະບານ
    party_cand_date = models.DateField(null=True, blank=True)  # ວັນເຂົ້າເປັນສະມາຊິກພັັກສຳຮອງ
    full_party_date = models.DateField(null=True, blank=True)  # ວັນເຂົ້າເປັນສະມາຊິກພັກສົມບູນ
    curr_party_pos = models.CharField(max_length=255, null=True, blank=True)  # ຕຳແໜ່ງຂອງພັກປັດຈຸບັນ
    party_apt_date = models.DateField(null=True, blank=True)  # ວັນທີເດືອນປີແຕ່ງຕັ້ງຄຕຳແໜ່ງຂອງພັກ
    curr_gov_pos = models.CharField(max_length=255, null=True, blank=True)  # ຕຳແໜ່ງເບື່ອງລັດປັດຈຸບັນ
    gov_apt_date = models.DateField(null=True, blank=True)  # ວັນທີເດືອນປີແຕ່ງຕັ້ງຕຳແໜ່ງຂອງລັດ

class Education(models.Model):
    per_id = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE)  # ບຸກຄົນ
    level = models.CharField(max_length=255)  # ຂັ້ນ
    school = models.CharField(max_length=255)  # ຊື່ໂຮງຮຽນ
    year = models.IntegerField()  # ປີ
    dom_abrd = models.CharField(max_length=50)  # ພາຍໃນ/ຕ່າງປະເທດ

class SpecializedEducation(models.Model):
    per_id = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE)  # ບຸກຄົນ
    field = models.CharField(max_length=255)  # ຂະແໜງສຶກສາ
    inst = models.CharField(max_length=255)  # ສະຖາບັນ
    level = models.CharField(max_length=100)  # ຂັ້ນ
    year = models.IntegerField()  # ປີ
    dom_abrd = models.CharField(max_length=50)  # ພາຍໃນ/ຕ່າງປະເທດ

class PoliticalTheoryEducation(models.Model):
    per_id = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE)  # ບຸກຄົນ
    inst = models.CharField(max_length=255)  # ສະຖາບັນ
    level = models.CharField(max_length=100)  # ຂັ້ນ
    year = models.IntegerField()  # ປີ
    dom_abrd = models.CharField(max_length=50)  # ພາຍໃນ/ຕ່າງປະເທດ

class ForeignLanguage(models.Model):
    per_id = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE)  # ບຸກຄົນ
    lang = models.CharField(max_length=100)  # ພາສາ
    prof = models.CharField(max_length=50)  # ຄວາມຊໍານານ

class WorkExperience(models.Model):
    per_id = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE)  # ບຸກຄົນ
    work = models.CharField(max_length=255)  # ສະຖານທີ່ເຮັດວຽກ
    start = models.DateField()  # ວັນເລີ່ມຕົ້ນ
    end = models.DateField()  # ວັນຈົບ
    gov_pos = models.CharField(max_length=255)  # ຕໍາແຫນໃນລັດຕະການ
    party_pos = models.CharField(max_length=255, null=True, blank=True)  # ຕໍາແຫນຂອງພັກ

class TrainingCourse(models.Model):
    per_id = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE)  # ບຸກຄົນ
    start = models.DateField()  # ວັນເລີ່ມຕົ້ນ
    end = models.DateField()  # ວັນຈົບ
    subj = models.CharField(max_length=255)  # ວິຊາ
    inst = models.CharField(max_length=255)  # ສະຖາບັນ
    country = models.CharField(max_length=100)  # ປະເທດ
    
class Award(models.Model):
    per_id = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE)  # ບຸກຄົນ
    dec_num = models.CharField(max_length=100)  # ເລກທີ່ການຕັດສິນໃຈ
    date = models.DateField()  # ວັນທີ
    award_type = models.CharField(max_length=255)  # ປະເພດລາງວັນ
    reason = models.TextField()  # ເຫດຜົນ

class DisciplinaryAction(models.Model):
    per_id = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE)  # ບຸກຄົນ
    dec_num = models.CharField(max_length=100)  # ເລກທີ່ການຕັດສິນໃຈ
    date = models.DateField()  # ວັນທີ
    action_type = models.CharField(max_length=255)  # ປະເພດມາດຕະການ
    reason = models.TextField()  # ເຫດຜົນ

class FamilyMember(models.Model):
    per_id = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE, related_name='family_members')  # ບຸກຄົນ
    relation = models.CharField(max_length=50)  # ຄວາມສຳພັນ (ເມຍ, ພໍ່, ແມ່, ເຫຼົ້າ)
    full_name = models.CharField(max_length=255)  # ຊື່ເຕັມ
    dob = models.DateField()  # ວັນເກີດ
    eth = models.CharField(max_length=100, null=True, blank=True)  # ຊົນເຜົ່າ
    rel = models.CharField(max_length=100, null=True, blank=True)  # ສາສະໜາ
    occ = models.CharField(max_length=255, null=True, blank=True)  # ອາຊີບ
    work = models.CharField(max_length=255, null=True, blank=True)  # ສະຖານທີ່ເຮັດວຽກ
    vill = models.CharField(max_length=100, null=True, blank=True)  # ບ້ານ
    dist = models.CharField(max_length=100, null=True, blank=True)  # ເມືອງ
    prov = models.CharField(max_length=100, null=True, blank=True)  # ແຂວງ

class Evaluation(models.Model):
    per_id = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE)  # ບຸກຄົນ
    strengths = models.TextField()  # ຈຸດແຂງແຮງ
    weaknesses = models.TextField()  # ຈຸດອ່ອນ

    def __str__(self):
        return self.person.full_name