from django.db import models
#ຂໍ້ມູນບຸກຄົນ
class PersonalInformation(models.Model):
    per_id = models.AutoField(primary_key=True)  # ລະຫັດຂໍ້ມູນບຸກຄົນ
    full_name = models.CharField(max_length=255)  # ຊື່ເຕັມ
    dob = models.DateField()  # ວັນເກີດ
    eth = models.CharField(max_length=100)  # ຊົນເຜົ່າ
    rel = models.CharField(max_length=100)  # ສາສະໜາ
    b_vill = models.CharField(max_length=100)  # ບ້ານເກີດ
    b_dist = models.CharField(max_length=100)  # ເມືອງເກີດ
    b_prov = models.CharField(max_length=100)  # ແຂວງເກີດ
    c_vill = models.CharField(max_length=100)  # ບ້ານປັດຈຸບັນ
    c_dist = models.CharField(max_length=100)  # ເມືອງປັດຈຸບັນ
    c_prov = models.CharField(max_length=100)  # ແຂວງປັດຈຸບັນ
    gov_entry = models.DateField()  # ວັນເຂົ້າສັງກັດລັດ(ພະນັກງານສົມບູນ)
    youth_date = models.DateField(null=True, blank=True)  # ວັນເຂົ້າເປັນສະມາຊິກຊາວໝຸ່ມ
    women_date = models.DateField(null=True, blank=True)  # ວັນເຂົ້າເປັນສະມາຊິກແມ່ຍິງ
    union_date = models.DateField(null=True, blank=True)  # ວັນເຂົ້າເປັນສະມາຊິກກຳມະບານ
    party_cand_date = models.DateField(null=True, blank=True)  # ວັນເຂົ້າເປັນສະມາຊິກພັັກສຳຮອງ
    full_party_date = models.DateField(null=True, blank=True)  # ວັນເຂົ້າເປັນສະມາຊິກພັກສົມບູນ
    curr_party_pos = models.CharField(max_length=255, null=True, blank=True)  # ຕຳແໜ່ງຂອງພັກປັດຈຸບັນ
    party_apt_date = models.DateField(null=True, blank=True)  # ວັນທີເດືອນປີແຕ່ງຕັ້ງຄຕຳແໜ່ງຂອງພັກ
    curr_gov_pos = models.CharField(max_length=255, null=True, blank=True)  # ຕຳແໜ່ງເບື່ອງລັດປັດຈຸບັນ
    gov_apt_date = models.DateField(null=True, blank=True)  # ວັນທີເດືອນປີແຕ່ງຕັ້ງຕຳແໜ່ງຂອງລັດ
#ປະວັດການສຶກສາ
class Education(models.Model):
    per_id = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE)  # ບຸກຄົນ
    level = models.CharField(max_length=255)  # ຂັ້ນ
    school = models.CharField(max_length=255)  # ຊື່ໂຮງຮຽນ
    year = models.IntegerField()  # ປີ
    dom_abrd = models.CharField(max_length=50)  # ພາຍໃນ/ຕ່າງປະເທດ
#ປະວັດການສຶກສາພາສາສາລາວ
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
    prof = models.CharField(max_length=50, choices=[("Excellent", "ດີ"), ("Good", "ກາງ"), ("Fair", "ອ່ອນ")])  # ຄວາມຊໍານານ

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
    


    #get all data


from rest_framework import viewsets, serializers
from .models import PersonalInformation, Education, SpecializedEducation, PoliticalTheoryEducation, ForeignLanguage, WorkExperience, TrainingCourse, Award, DisciplinaryAction, FamilyMember, Evaluation

# Serializer
class PersonalInformationSerializer(serializers.ModelSerializer):
    education = serializers.SerializerMethodField()
    specialized_education = serializers.SerializerMethodField()
    political_education = serializers.SerializerMethodField()
    languages = serializers.SerializerMethodField()
    work_experience = serializers.SerializerMethodField()
    training_courses = serializers.SerializerMethodField()
    awards = serializers.SerializerMethodField()
    disciplinary_actions = serializers.SerializerMethodField()
    family_members = serializers.SerializerMethodField()
    evaluations = serializers.SerializerMethodField()

    class Meta:
        model = PersonalInformation
        fields = '__all__'
    
    def get_education(self, obj):
        return Education.objects.filter(person=obj).values()
    
    def get_specialized_education(self, obj):
        return SpecializedEducation.objects.filter(person=obj).values()
    
    def get_political_education(self, obj):
        return PoliticalTheoryEducation.objects.filter(person=obj).values()
    
    def get_languages(self, obj):
        return ForeignLanguage.objects.filter(person=obj).values()
    
    def get_work_experience(self, obj):
        return WorkExperience.objects.filter(person=obj).values()
    
    def get_training_courses(self, obj):
        return TrainingCourse.objects.filter(person=obj).values()
    
    def get_awards(self, obj):
        return Award.objects.filter(person=obj).values()
    
    def get_disciplinary_actions(self, obj):
        return DisciplinaryAction.objects.filter(person=obj).values()
    
    def get_family_members(self, obj):
        return FamilyMember.objects.filter(person=obj).values()
    
    def get_evaluations(self, obj):
        return Evaluation.objects.filter(person=obj).values()

# ViewSet
class PersonalInformationViewSet(viewsets.ModelViewSet):
    queryset = PersonalInformation.objects.all()
    serializer_class = PersonalInformationSerializer



from django.db import models

class EmployeeLCIC(models.Model):
    emp_id = models.AutoField(primary_key=True)  # ລະຫັດພະນັກງານ (Primary Key, ອັດຕະໂນມັດ)
    gender = models.CharField(max_length=10)  # ເພດຂອງພະນັກງານ
    name_l = models.CharField(max_length=100)  # ຊື່ແລະນາມສະກຸນ (ພາສາລາວ)
    name_e = models.CharField(max_length=100)  # ຊື່ແລະນາມສະກຸນ (ພາສາອັງກິດ)
    nickname = models.CharField(max_length=50, blank=True, null=True)  # ຊື່ຫຼີ້ນ (ທາງເລືອກ)
    birth_date = models.CharField()  # ວັນເກີດ
    status = models.CharField(max_length=20)  # ສະຖານະພາບ (ເຊັ່ນ ໂສດ, ແຕ່ງງານ)
    dept = models.CharField(max_length=100)  # ພະແນກ
    position = models.CharField(max_length=100)  # ຕຳແໜ່ງ
    years_of_service = models.IntegerField()  # ປີການເຮັດວຽກ
    salary_level = models.CharField(max_length=100)# ຂັ້ນເງິນເດືອນ
    phone = models.CharField(max_length=20)  # ເບີໂທ
    pic = models.ImageField(blank=True, null=True)  # ຮູບໂປຣຟາຍ (ທາງເລືອກ)
    
    def __str__(self):
        return f"{self.name_e} ({self.emp_id})"  # ສະແດງຊື່ພະນັກງານໃນຮູບແບບ string


department_into = models.ManyToManyField('Department', related_name='document_lcic_department_into', blank=True)  # ພະແນກທີ່ສົ່ງໃຫ້


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
    status = models.CharField(max_length=10, choices=[('new', 'ໃໝ່'), ('viewed', 'ເບີ່ງແລ້ວ')], default='new')# ສະຖານະຂອງເອກະສານ



class document_general(models.Model):
    docg_id = models.AutoField(primary_key=True) # ລະຫັດເອກະສານ
    insert_date = models.CharField(max_length=100, blank=True, null=True) # ວັນທີ່ເພີ່ມ
    doc_number = models.CharField(max_length=100, blank=True, null=True) # ເລກທີເອກະສານ
    subject = models.CharField(max_length=255, blank=True, null=True) # ເລື່ອງ
    format = models.ForeignKey(Document_format, on_delete=models.CASCADE) # ຮູບແບບ
    file = models.FileField(upload_to='documents_general/',null=True) # ໄຟລແທນ
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='document_lcic_g')
    document_detail = models.CharField(max_length=255, blank=True, null=True) # ລາຍລະອຽດ
    name = models.CharField(max_length=255, blank=True, null=True) # ຜູ້ສ້າງ


