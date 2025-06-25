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




from .models import (PersonalInformation, Education,SpecializedEducation, PoliticalTheoryEducation, ForeignLanguage, WorkExperience, 
                     TrainingCourse, Award, DisciplinaryAction, FamilyMember, Evaluation)
from .serializers import (PersonalInformationSerializer, EducationSerializer, SpecializedEducationSerializer, AwardSerializer,
                          PoliticalTheoryEducationSerializer, ForeignLanguageSerializer, WorkExperienceSerializer, TrainingCourseSerializer,DisciplinaryActionSerializer,
                          FamilyMemberSerializer, EvaluationSerializer)
import logging
from django.db import transaction
from rest_framework.generics import get_object_or_404
from typing import Optional
from django.db import transaction
logger = logging.getLogger(__name__)
class PersonalEducationCreateView(APIView):
    def get(self, request, per_id: Optional[int] = None):
        if per_id:
            personal_instances = PersonalInformation.objects.filter(per_id=per_id)
        else:
            personal_instances = PersonalInformation.objects.all()
        response_data = []
        for personal_instance in personal_instances:
            per_id = personal_instance.per_id
            education_instances = Education.objects.filter(per_id=per_id)
            specialized_instances = SpecializedEducation.objects.filter(per_id=per_id)
            political_instances = PoliticalTheoryEducation.objects.filter(per_id=per_id)
            language_instances = ForeignLanguage.objects.filter(per_id=per_id)
            work_instances = WorkExperience.objects.filter(per_id=per_id)
            training_instances = TrainingCourse.objects.filter(per_id=per_id)
            award_instances = Award.objects.filter(per_id=per_id)
            disciplinary_instances = DisciplinaryAction.objects.filter(per_id=per_id)
            family_instances = FamilyMember.objects.filter(per_id=per_id)
            evaluation_instance = Evaluation.objects.filter(per_id=per_id).first()
            response_data.append({
                "personal_information": PersonalInformationSerializer(personal_instance).data,
                "education": EducationSerializer(education_instances, many=True).data,
                "specialized_education": SpecializedEducationSerializer(specialized_instances, many=True).data,
                "political_theory_education": PoliticalTheoryEducationSerializer(political_instances, many=True).data,
                "foreign_languages": ForeignLanguageSerializer(language_instances, many=True).data,
                "work_experiences": WorkExperienceSerializer(work_instances, many=True).data,
                "training_courses": TrainingCourseSerializer(training_instances, many=True).data,
                "awards": AwardSerializer(award_instances, many=True).data,
                "disciplinary_actions": DisciplinaryActionSerializer(disciplinary_instances, many=True).data,
                "family_members": FamilyMemberSerializer(family_instances, many=True).data,
                "evaluation": EvaluationSerializer(evaluation_instance).data if evaluation_instance else None
            })

        return Response(response_data, status=status.HTTP_200_OK)
    
    def save_related_data(self, serializer_class, dataset, per_id):
        try:
            for item in dataset:
                item["per_id"] = per_id
            serializer = serializer_class(data=dataset, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception as e:
            logger.error(f"Error saving {serializer_class.__name__}: {e}")
            raise e

    def post(self, request):
        data = request.data or {}

        personal_data_list = data.get('PersonalInformation', [])
        if not personal_data_list:
            return Response({"error": "ຂໍ້ມູນບໍ່ຖືກຮູບແບບ"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                personal_data = personal_data_list[0]
                personal_serializer = PersonalInformationSerializer(data=personal_data)
                personal_serializer.is_valid(raise_exception=True)
                personal_instance = personal_serializer.save()

                related_data_map = {
                    FamilyMemberSerializer: data.get('FamilyMember', []),
                    EducationSerializer: data.get('Education', []),
                    SpecializedEducationSerializer: data.get('SpecializedEducation', []),
                    PoliticalTheoryEducationSerializer: data.get('PoliticalTheoryEducation', []),
                    ForeignLanguageSerializer: data.get('ForeignLanguage', []),
                    WorkExperienceSerializer: data.get('WorkExperience', []),
                    TrainingCourseSerializer: data.get('TrainingCourse', []),
                    AwardSerializer: data.get('Award', []),
                    DisciplinaryActionSerializer: data.get('DisciplinaryAction', [])
                }

                for serializer_class, dataset in related_data_map.items():
                    self.save_related_data(serializer_class, dataset, personal_instance.per_id)

                evaluation_list = data.get('Evaluation', [])
                if evaluation_list:
                    evaluation_data = evaluation_list[0]
                    evaluation_data["per_id"] = personal_instance.per_id
                    evaluation_serializer = EvaluationSerializer(data=evaluation_data)
                    evaluation_serializer.is_valid(raise_exception=True)
                    evaluation_serializer.save()

            return Response({
                "message": "ບັນທຶກສຳເລັດ",
                "per_id": personal_instance.per_id,
                "name": personal_instance.full_name
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error in post method: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, per_id: int):
        data = request.data
        personal_data = data.get('personal_information', {})
        family_data = data.get('family_members', [])
        evaluation_data = data.get('evaluation', {})
        education_data = data.get('education', [])
        specialized_data = data.get('specialized_education', [])
        political_data = data.get('political_theory_education', [])
        language_data = data.get('foreign_languages', [])
        work_data = data.get('work_experiences', [])
        training_data = data.get('training_courses', [])
        award_data = data.get('awards', [])
        disciplinary_data = data.get('disciplinary_actions', [])
        # ຄົ້ນຫາ PersonalInformation ທີ່ຈະອັບເດດ
        personal_instance = get_object_or_404(PersonalInformation, per_id=per_id)
        try:
            with transaction.atomic():
                # 1. ອັບເດດ Personal Information
                personal_serializer = PersonalInformationSerializer(personal_instance, data=personal_data, partial=True)
                personal_serializer.is_valid(raise_exception=True)
                personal_serializer.save()
                # 2. ລົບຂໍ້ມູນເກົ່າ ແລະ Insert ໃໝ່ (ສໍາລັບຂໍ້ມູນທີ່ເປັນ Many-to-Many)
                def update_related_data(model_class, serializer_class, dataset):
                    model_class.objects.filter(per_id=per_id).delete()
                    for item in dataset:
                        item["per_id"] = per_id
                    serializer = serializer_class(data=dataset, many=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                update_related_data(FamilyMember, FamilyMemberSerializer, family_data)
                update_related_data(Education, EducationSerializer, education_data)
                update_related_data(SpecializedEducation, SpecializedEducationSerializer, specialized_data)
                update_related_data(PoliticalTheoryEducation, PoliticalTheoryEducationSerializer, political_data)
                update_related_data(ForeignLanguage, ForeignLanguageSerializer, language_data)
                update_related_data(WorkExperience, WorkExperienceSerializer, work_data)
                update_related_data(TrainingCourse, TrainingCourseSerializer, training_data)
                update_related_data(Award, AwardSerializer, award_data)
                update_related_data(DisciplinaryAction, DisciplinaryActionSerializer, disciplinary_data)
                # 3. ອັບເດດ Evaluation (ຖ້າມີ)
                if evaluation_data:
                    Evaluation.objects.filter(per_id=per_id).delete()
                    evaluation_data["per_id"] = per_id
                    evaluation_serializer = EvaluationSerializer(data=evaluation_data)
                    evaluation_serializer.is_valid(raise_exception=True)
                    evaluation_serializer.save()
            return Response({
                "message": "ອັບເດດສຳເລັດ",
                "per_id": per_id,
                "name": personal_instance.full_name
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, per_id: int):
        personal_instance = get_object_or_404(PersonalInformation, per_id=per_id)
        try:
            with transaction.atomic():
                # ລຶບຂໍ້ມູນທີ່ມີຄວາມສຳພັນກັນ
                FamilyMember.objects.filter(per_id=per_id).delete()
                Education.objects.filter(per_id=per_id).delete()
                SpecializedEducation.objects.filter(per_id=per_id).delete()
                PoliticalTheoryEducation.objects.filter(per_id=per_id).delete()
                ForeignLanguage.objects.filter(per_id=per_id).delete()
                WorkExperience.objects.filter(per_id=per_id).delete()
                TrainingCourse.objects.filter(per_id=per_id).delete()
                Award.objects.filter(per_id=per_id).delete()
                DisciplinaryAction.objects.filter(per_id=per_id).delete()
                Evaluation.objects.filter(per_id=per_id).delete()

                # ລຶບຂໍ້ມູນຫຼັກ
                personal_instance.delete()

            return Response({"message": "ລຶບສຳເລັດ"}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # def delete(self, request):
    #     try:
    #         with transaction.atomic():
    #             # ລຶບທຸກຕາຕະລາງທີ່ກ່ຽວຂ້ອງ
    #             FamilyMember.objects.all().delete()
    #             Education.objects.all().delete()
    #             SpecializedEducation.objects.all().delete()
    #             PoliticalTheoryEducation.objects.all().delete()
    #             ForeignLanguage.objects.all().delete()
    #             WorkExperience.objects.all().delete()
    #             TrainingCourse.objects.all().delete()
    #             Award.objects.all().delete()
    #             DisciplinaryAction.objects.all().delete()
    #             Evaluation.objects.all().delete()
    #             PersonalInformation.objects.all().delete()

    #         return Response({"message": "ລຶບຂໍ້ມູນທັງໝົດສຳເລັດ"}, status=status.HTTP_204_NO_CONTENT)

    #     except Exception as e:
    #         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



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
    year_entry = models.CharField()  # ປີເຂົ້າເຮັດວຽກ
    salary_level = models.CharField(max_length=100)# ຂັ້ນເງິນເດືອນ
    phone = models.CharField(max_length=20)  # ເບີໂທ
    pic = models.ImageField(blank=True, null=True)  # ຮູບໂປຣຟາຍ (ທາງເລືອກ)

    def __str__(self):
        return f"{self.emp_id} - {self.name_E} ({self.nickname})"
    

    emp_id = models.ForeignKey(Employee_lcic, on_delete=models.CASCADE)  # ບຸກຄົນ


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
    pic = models.ImageField(upload_to='emp_img/',null=True)  # ຮູບໂປຣຟາຍ (ທາງເລືອກ)

    def __str__(self):
        return f"{self.emp_id} - {self.name_E} ({self.nickname})"
    
class PersonalInformation(models.Model):
    emp_id = models.ForeignKey(Employee_lcic, on_delete=models.CASCADE,null=True) # ຮູບແບບ
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
    emp_id = models.ForeignKey(Employee_lcic, on_delete=models.CASCADE,null=True) # ຮູບແບບ
    level = models.CharField(max_length=255)  # ຂັ້ນ
    school = models.CharField(max_length=255)  # ຊື່ໂຮງຮຽນ
    year = models.IntegerField()  # ປີ
    dom_abrd = models.CharField(max_length=50)  # ພາຍໃນ/ຕ່າງປະເທດ

class SpecializedEducation(models.Model):
    emp_id = models.ForeignKey(Employee_lcic, on_delete=models.CASCADE,null=True) # ຮູບແບບ
    field = models.CharField(max_length=255)  # ຂະແໜງສຶກສາ
    inst = models.CharField(max_length=255)  # ສະຖາບັນ
    level = models.CharField(max_length=100)  # ຂັ້ນ
    year = models.IntegerField()  # ປີ
    dom_abrd = models.CharField(max_length=50)  # ພາຍໃນ/ຕ່າງປະເທດ

class PoliticalTheoryEducation(models.Model):
    emp_id = models.ForeignKey(Employee_lcic, on_delete=models.CASCADE,null=True) # ຮູບແບບ
    inst = models.CharField(max_length=255)  # ສະຖາບັນ
    level = models.CharField(max_length=100)  # ຂັ້ນ
    year = models.IntegerField()  # ປີ
    dom_abrd = models.CharField(max_length=50)  # ພາຍໃນ/ຕ່າງປະເທດ

class ForeignLanguage(models.Model):
    emp_id = models.ForeignKey(Employee_lcic, on_delete=models.CASCADE,null=True) # ຮູບແບບ
    lang = models.CharField(max_length=100)  # ພາສາ
    prof = models.CharField(max_length=50)  # ຄວາມຊໍານານ

class WorkExperience(models.Model):
    emp_id = models.ForeignKey(Employee_lcic, on_delete=models.CASCADE,null=True) # ຮູບແບບ
    work = models.CharField(max_length=255)  # ສະຖານທີ່ເຮັດວຽກ
    start = models.DateField()  # ວັນເລີ່ມຕົ້ນ
    end = models.DateField()  # ວັນຈົບ
    gov_pos = models.CharField(max_length=255)  # ຕໍາແຫນໃນລັດຕະການ
    party_pos = models.CharField(max_length=255, null=True, blank=True)  # ຕໍາແຫນຂອງພັກ

class TrainingCourse(models.Model):
    emp_id = models.ForeignKey(Employee_lcic, on_delete=models.CASCADE,null=True) # ຮູບແບບ
    start = models.DateField()  # ວັນເລີ່ມຕົ້ນ
    end = models.DateField()  # ວັນຈົບ
    subj = models.CharField(max_length=255)  # ວິຊາ
    inst = models.CharField(max_length=255)  # ສະຖາບັນ
    country = models.CharField(max_length=100)  # ປະເທດ
    
class Award(models.Model):
    emp_id = models.ForeignKey(Employee_lcic, on_delete=models.CASCADE,null=True) # ຮູບແບບ
    dec_num = models.CharField(max_length=100)  # ເລກທີ່ການຕັດສິນໃຈ
    date = models.DateField()  # ວັນທີ
    award_type = models.CharField(max_length=255)  # ປະເພດລາງວັນ
    reason = models.TextField()  # ເຫດຜົນ

class DisciplinaryAction(models.Model):
    emp_id = models.ForeignKey(Employee_lcic, on_delete=models.CASCADE,null=True) # ຮູບແບບ
    dec_num = models.CharField(max_length=100)  # ເລກທີ່ການຕັດສິນໃຈ
    date = models.DateField()  # ວັນທີ
    action_type = models.CharField(max_length=255)  # ປະເພດມາດຕະການ
    reason = models.TextField()  # ເຫດຜົນ

class FamilyMember(models.Model):
    emp_id = models.ForeignKey(Employee_lcic, on_delete=models.CASCADE,null=True) # ຮູບແບບ
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
    emp_id = models.ForeignKey(Employee_lcic, on_delete=models.CASCADE,null=True) # ຮູບແບບ
    strengths = models.TextField()  # ຈຸດແຂງແຮງ
    weaknesses = models.TextField()  # ຈຸດອ່ອນ

    def __str__(self):
        return self.emp_id
    

class Account(models.Model):
    id = models.AutoField(primary_key=True)  # ID
    number = models.CharField(max_length=100, unique=True)  # ເລກທີ່ບັນຊີ
    asset_type = models.CharField(max_length=100)  # ປະເພດຊັບສິນ

class Asset(models.Model):
    id = models.AutoField(primary_key=True)  # ID
    code = models.CharField(max_length=100,unique=True)  # ລະຫັດຊັບສິນ
    ac_num = models.ForeignKey(Account, on_delete=models.CASCADE,unique=True)  # ເລກທີ່ບັນຊີ
    ac_name = models.CharField(max_length=500)  # ເນື້ອໃນລາຍການ
    dep_status = models.CharField(max_length=100)  # ສະຖານະຫຼຸ້ຍຫ້ຽນ
    value = models.DecimalField(max_digits=20, decimal_places=2)  # ມູນຄ່າເດີມ (ກີບ)
    date_use = models.DateField()  # ວ/ດ/ປ ນໍາໃຊ້
    date_exp = models.DateField()  # ວ/ດ/ປ ໝົດອາຍຸນໍາໃຊ້
    life_left = models.IntegerField()  # ອາຍຸຍັງເຫຼືອ (ເດືອນ)
    location = models.CharField(max_length=200)  # ທີ່ຕັ້ງຊັບສິນ
    emp_user = models.CharField(max_length=100)  # ຜູ້ນຳໃຊ້
    note = models.TextField(blank=True, null=True)  # ໝາຍເຫດ

    def __str__(self):
        return f"{self.code} - {self.desc}"


    def put(self, request, per_id: int):
        data = request.data
        personal_data = data.get('personal_information', {})
        family_data = data.get('family_members', [])
        evaluation_data = data.get('evaluation', {})
        education_data = data.get('education', [])
        specialized_data = data.get('specialized_education', [])
        political_data = data.get('political_theory_education', [])
        language_data = data.get('foreign_languages', [])
        work_data = data.get('work_experiences', [])
        training_data = data.get('training_courses', [])
        award_data = data.get('awards', [])
        disciplinary_data = data.get('disciplinary_actions', [])

        personal_instance = get_object_or_404(PersonalInformation, per_id=per_id)

        try:
            with transaction.atomic():
                # 1. Update Personal Information
                personal_serializer = PersonalInformationSerializer(personal_instance, data=personal_data, partial=True)
                personal_serializer.is_valid(raise_exception=True)
                personal_serializer.save()

                # 2. Update Related Many-to-Many Data (Using Bulk Operations)
                def update_related_data(model_class, serializer_class, dataset):
                    existing_items = {obj.id: obj for obj in model_class.objects.filter(per_id=per_id)}
                    new_items = []
                    for item in dataset:
                        item["per_id"] = per_id
                        if "id" in item and item["id"] in existing_items:
                            serializer = serializer_class(existing_items[item["id"]], data=item, partial=True)
                        else:
                            serializer = serializer_class(data=item)
                        serializer.is_valid(raise_exception=True)
                        new_items.append(serializer)
                    model_class.objects.bulk_create(
                        [serializer.save() for serializer in new_items], ignore_conflicts=True
                    )

                update_related_data(FamilyMember, FamilyMemberSerializer, family_data)
                update_related_data(Education, EducationSerializer, education_data)
                update_related_data(SpecializedEducation, SpecializedEducationSerializer, specialized_data)
                update_related_data(PoliticalTheoryEducation, PoliticalTheoryEducationSerializer, political_data)
                update_related_data(ForeignLanguage, ForeignLanguageSerializer, language_data)
                update_related_data(WorkExperience, WorkExperienceSerializer, work_data)
                update_related_data(TrainingCourse, TrainingCourseSerializer, training_data)
                update_related_data(Award, AwardSerializer, award_data)
                update_related_data(DisciplinaryAction, DisciplinaryActionSerializer, disciplinary_data)

                # 3. Update Evaluation (If exists)
                if evaluation_data:
                    evaluation_instance, _ = Evaluation.objects.update_or_create(per_id=per_id, defaults=evaluation_data)

            return Response({
                "message": "ອັບເດດສຳເລັດ",
                "per_id": per_id,
                "name": personal_instance.full_name
            }, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

def put(self, request, emp_id: int):
    # Parse incoming data directly from request.data
    data = request.data
    employee_data = data.get('employee', {})
    personal_data = data.get('personal_information', {})
    family_data = data.get('family_members', [])
    evaluation_data = data.get('evaluation', {})
    education_data = data.get('education', [])
    specialized_data = data.get('specialized_education', [])
    political_data = data.get('political_theory_education', [])
    language_data = data.get('foreign_languages', [])
    work_data = data.get('work_experiences', [])
    training_data = data.get('training_courses', [])
    award_data = data.get('awards', [])
    disciplinary_data = data.get('disciplinary_actions', [])

    # Get existing employee instance or 404
    employee_instance = get_object_or_404(Employee_lcic, emp_id=emp_id)

    try:
        with transaction.atomic():
            # 1. Update Employee_lcic
            if employee_data:
                employee_serializer = EmployeeSerializer(employee_instance, data=employee_data, partial=True)
                employee_serializer.is_valid(raise_exception=True)
                employee_serializer.save()

            # 3. Update Related Many-to-Many Data
            def update_related_data(model_class, serializer_class, dataset):
                existing_items = {obj.id: obj for obj in model_class.objects.filter(emp_id=emp_id)}
                new_items = []
                for item in dataset:
                    item["emp_id"] = emp_id
                    if "id" in item and item["id"] in existing_items:
                        serializer = serializer_class(existing_items[item["id"]], data=item, partial=True)
                    else:
                        serializer = serializer_class(data=item)
                    serializer.is_valid(raise_exception=True)
                    new_items.append(serializer)
                model_class.objects.bulk_create(
                    [serializer.save() for serializer in new_items], ignore_conflicts=True
                )
            update_related_data(PersonalInformation, PersonalInformationSerializer, personal_data)
            update_related_data(FamilyMember, FamilyMemberSerializer, family_data)
            update_related_data(Education, EducationSerializer, education_data)
            update_related_data(SpecializedEducation, SpecializedEducationSerializer, specialized_data)
            update_related_data(PoliticalTheoryEducation, PoliticalTheoryEducationSerializer, political_data)
            update_related_data(ForeignLanguage, ForeignLanguageSerializer, language_data)
            update_related_data(WorkExperience, WorkExperienceSerializer, work_data)
            update_related_data(TrainingCourse, TrainingCourseSerializer, training_data)
            update_related_data(Award, AwardSerializer, award_data)
            update_related_data(DisciplinaryAction, DisciplinaryActionSerializer, disciplinary_data)

            # 4. Update Evaluation (If exists)
            if evaluation_data:
                evaluation_instance, _ = Evaluation.objects.update_or_create(
                    emp_id=emp_id, 
                    defaults=evaluation_data
                )

            return Response({
                "message": "ອັບເດດສຳເລັດ",
                "emp_id": emp_id,
                "name": employee_instance.lao_name
            }, status=status.HTTP_200_OK)

    except ValidationError as e:
        logger.error(f"Validation error updating emp_id {emp_id}: {str(e)}")
        return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Error updating emp_id {emp_id}: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    


class Asset_Transfer(models.Model):
    ast_id = models.ForeignKey(Asset, on_delete=models.CASCADE)  # ລະຫັດຊັບສິນ
    emp_id = models.ForeignKey(Employee_lcic, on_delete=models.CASCADE)  # ລະຫັດເພະນັກງານ
    date = models.DateField()  # ວ/ດ/ປ ຍ່າຍ
    location = models.CharField(max_length=200)  # ສະຖານທີ່ໃໝ່ 
    note = models.TextField(blank=True, null=True)  # ໝາຍເຫດ
    status = models.CharField(max_length=100, blank=True)  # ສະຖານະການຍ່າຍ
    def __str__(self):
        return f"{self.ast_id} - {self.emp_id} - {self.date} - {self.location}"
    


class Position(models.Model):
    pos_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    sal_id = models.ForeignKey('Salary', on_delete=models.CASCADE, null=True, blank=True)  # ເງິນເດືອນ
    sp_id = models.ForeignKey('SubsidyPosition', on_delete=models.CASCADE, null=True, blank=True)  # ສະໜັບສະໜູນຕຳແໜ່ງ
    fs_id = models.ForeignKey('FuelSubsidy', on_delete=models.CASCADE, null=True, blank=True)  # ສະໜັບສະໜູນນ້ຳມັນ
    ot_id = models.ForeignKey('OvertimeWork', on_delete=models.CASCADE, null=True, blank=True)  # ງານເວລາເພີ່ມ
    mb = models.ForeignKey('MobilePhoneSubsidy', on_delete=models.CASCADE, null=True, blank=True)  # ສະໜັບສະໜູນໂທລະສັບ



class Overtime_history(models.Model):
    id = models.AutoField(primary_key=True)  # ID as AutoField
    date = models.CharField(max_length=20,null=True, blank=True)
    ot_id = models.BigIntegerField()
    emp_id = models.BigIntegerField()
    pos_id = models.BigIntegerField()
    csd_evening = models.CharField(max_length=20,null=True, blank=True)
    csd_night = models.CharField(max_length=20,null=True, blank=True)
    hd_mor_after = models.CharField(max_length=20,null=True, blank=True)
    hd_evening = models.CharField(max_length=20,null=True, blank=True)
    hd_night = models.CharField(max_length=20,null=True, blank=True) 
    salary = models.CharField(max_length=50,null=True, blank=True)
    value_150 = models.CharField(max_length=20,null=True, blank=True)
    value_200 = models.CharField(max_length=20,null=True, blank=True)
    value_250 = models.CharField(max_length=20,null=True, blank=True)
    value_300 = models.CharField(max_length=20,null=True, blank=True)
    value_350 = models.CharField(max_length=20,null=True, blank=True)
    total_ot = models.CharField(max_length=20,null=True, blank=True)

class colpolicy_history(models.Model):
    id = models.AutoField(primary_key=True)  # ID as AutoField
    date = models.CharField(max_length=20)
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
    fp_id = models.BigIntegerField()
    update_date = models.CharField(max_length=20, null=True, blank=True)
    emp_id = models.BigIntegerField()
    emp_name = models.CharField(max_length=255, null=True, blank=True)
    emp_id = models.BigIntegerField()
    position = models.CharField(max_length=255, null=True, blank=True)
    fuel_subsidy = models.CharField(max_length=50, null=True, blank=True)
    fuel_price = models.CharField(max_length=50, null=True, blank=True)
    total_fuel = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    # # amount_per_day = serializers.SerializerMethodField()
    # # jm_policy = serializers.SerializerMethodField()
    # # total_amount = serializers.SerializerMethodField()



class monthly_paymentSerializer1(serializers.ModelSerializer):
    lao_name = serializers.CharField(source='emp_id.lao_name', read_only=True)
    pos_id = serializers.IntegerField(source='emp_id.pos_id.pos_id', read_only=True)
    position = serializers.CharField(source='emp_id.pos_id.name', read_only=True)
    salary = serializers.SerializerMethodField()

    class Meta:
        model = monthly_payment
        fields = ["id",
                  "date",
                  "emp_id",
                  "lao_name",
                  "pos_id",
                  "position",
                  "salary",
                  ]
        

    def get_y_subsidy(self, obj):
        age_entry = self.get_age_entry(obj)
        try:
            age_entry = int(age_entry) if age_entry is not None else None
        except ValueError:
            age_entry = None
        if age_entry is not None and age_entry == 0:
            return 0
        if age_entry is not None and age_entry < 6:
            default_subsidy = SubsidyYear.objects.filter(sy_id=1).first()
            return default_subsidy.y_subsidy if default_subsidy else 0
        if age_entry is not None and age_entry > 5 and age_entry < 16:
            default_subsidy = SubsidyYear.objects.filter(sy_id=2).first()
            return default_subsidy.y_subsidy if default_subsidy else 0
        if age_entry is not None and age_entry > 15 and age_entry < 26:
            default_subsidy = SubsidyYear.objects.filter(sy_id=2).first()
            return default_subsidy.y_subsidy if default_subsidy else 0
        if age_entry is not None and age_entry > 26:
            default_subsidy = SubsidyYear.objects.filter(sy_id=3).first()
            return default_subsidy.y_subsidy if default_subsidy else 0       

        subsidy_year = SubsidyYear.objects.filter(sy_id=obj.sy_id).first()
        return subsidy_year.y_subsidy if subsidy_year else 0
    













class monthly_paymentSerializer1(serializers.ModelSerializer):
    lao_name = serializers.CharField(source='emp_id.lao_name', read_only=True)
    pos_id = serializers.IntegerField(source='emp_id.pos_id.pos_id', read_only=True)
    position = serializers.CharField(source='emp_id.pos_id.name', read_only=True)
    salary = serializers.SerializerMethodField()
    total_ot = serializers.SerializerMethodField()
    salary_payment = serializers.SerializerMethodField()
    fuel_payment = serializers.SerializerMethodField()
    # totol_payment = serializers.SerializerMethodField()
    age_entry = serializers.SerializerMethodField()
    y_subsidy = serializers.SerializerMethodField()
    total_subsidy_y = serializers.SerializerMethodField()
    subsidyPosition = serializers.SerializerMethodField()
    total_basic_income = serializers.SerializerMethodField()
    Deduct_into_the_welfare_fund_8 = serializers.SerializerMethodField()
    Deduct_into_the_welfare_fund_5_5 = serializers.SerializerMethodField()
    Deduct_into_the_welfare_fund_8_5 = serializers.SerializerMethodField()
    Deduct_into_the_welfare_fund_6 = serializers.SerializerMethodField()
    total_regular_income = serializers.SerializerMethodField()
    other_non_regular = serializers.SerializerMethodField()
    total_income_before_tax = serializers.SerializerMethodField()
    tax_exempt = serializers.SerializerMethodField()
    calculate_taxes_0 = serializers.SerializerMethodField()
    calculate_taxes_5 = serializers.SerializerMethodField()
    calculate_taxes_10 = serializers.SerializerMethodField()
    calculate_taxes_15 = serializers.SerializerMethodField()
    calculate_taxes_20 = serializers.SerializerMethodField()
    calculate_taxes_25 = serializers.SerializerMethodField()
    tortal_tax = serializers.SerializerMethodField()
    # tariff = serializers.SerializerMethodField()

    def get_subsidyPosition(self, obj):
        employee = obj.emp_id
        if not employee or not employee.pos_id:
            return None
        sp_id = SubsidyPosition.objects.filter(pos_id=employee.pos_id).first()
        return sp_id.grant if sp_id else None
 
    def get_age_entry(self, obj):
        if not obj.emp_id:
            return None
        age_entry = Employee_lcic.objects.filter(emp_id=obj.emp_id.emp_id).first()
        return age_entry.age_entry if age_entry else None
    
    def get_y_subsidy(self, obj):
        age_entry = self.get_age_entry(obj)
        try:
            age_entry = int(age_entry) if age_entry is not None else None
        except ValueError:
            age_entry = None
        if age_entry is not None and age_entry == 0:
            return 0
        if age_entry is not None and age_entry < 6:
            default_subsidy = SubsidyYear.objects.filter(sy_id=1).first()
            return default_subsidy.y_subsidy if default_subsidy else 0
        if age_entry is not None and age_entry > 5 and age_entry < 16:
            default_subsidy = SubsidyYear.objects.filter(sy_id=2).first()
            return default_subsidy.y_subsidy if default_subsidy else 0
        if age_entry is not None and age_entry > 15 and age_entry < 26:
            default_subsidy = SubsidyYear.objects.filter(sy_id=2).first()
            return default_subsidy.y_subsidy if default_subsidy else 0
        if age_entry is not None and age_entry > 26:
            default_subsidy = SubsidyYear.objects.filter(sy_id=3).first()
            return default_subsidy.y_subsidy if default_subsidy else 0       

        subsidy_year = SubsidyYear.objects.filter(sy_id=obj.sy_id).first()
        return subsidy_year.y_subsidy if subsidy_year else 0

    def get_total_subsidy_y(self, obj):
        age_entry = self.get_age_entry(obj)
        y_subsidy = self.get_y_subsidy(obj)
        try:
            age_entry = int(age_entry) if age_entry is not None else 0
        except ValueError:
            age_entry = 0
        try:
            y_subsidy = int(y_subsidy) if y_subsidy is not None else 0
        except ValueError:
            y_subsidy = 0
        return age_entry * y_subsidy

    def get_salary(self, obj):
        employee = obj.emp_id
        if not employee or not employee.pos_id:
            return None
        salary = Salary.objects.filter(pos_id=employee.pos_id).first()
        return salary.SalaryGrade if salary else None
    
    def get_total_ot(self, obj):
        overtime = OvertimeWork.objects.filter(emp_id=obj.emp_id).first()
        if not overtime:
            return None
        return overtime.total_ot if overtime.total_ot else 0

    def get_salary_payment(self, obj):
        subsidyPosition = self.get_subsidyPosition(obj) or 0
        salary = self.get_salary(obj)
        total_ot = self.get_total_ot(obj) 
        total_subsidy_y = self.get_total_subsidy_y(obj) or 0
        if salary is None:
            return 0
        if total_ot is None:
            total_ot = 0
        return math.ceil(float(salary) + float(total_ot)+ float(total_subsidy_y)+ float(subsidyPosition or 0))
    
    # def get_totol_payment(self, obj):
    #     total_fuel = self.get_fuel_payment(obj) or 0
    #     salary_payment = self.get_salary_payment(obj) or 0
    #     return math.ceil(float(total_fuel)+ float(salary_payment))

    def get_fuel_payment(self, obj):
        employee = obj.emp_id
        if not employee or not employee.pos_id:
            return 0
        fuel_payment = FuelSubsidy.objects.filter(pos_id=employee.pos_id).first()
        return fuel_payment.total_fuel if fuel_payment and fuel_payment.total_fuel else 0
    
    def get_total_basic_income(self, obj):
        salary = self.get_salary(obj) or 0
        subsidyPosition = self.get_subsidyPosition(obj) or 0
        total_subsidy_y = self.get_total_subsidy_y(obj) or 0
        total_ot = self.get_total_ot(obj) or 0
        return math.ceil(float(salary) + float(subsidyPosition) + float(total_subsidy_y)+ float(total_ot))
    
    def get_total_regular_income(self, obj):
        total_basic_income = self.get_total_basic_income(obj) or 0
        fuel_payment = self.get_fuel_payment(obj) or 0
        return math.ceil(float(total_basic_income) + float(fuel_payment))
    
    def get_other_non_regular(self, obj):
        col = col_policy.objects.filter(emp_id=obj.emp_id).order_by('-col_id').first()
        if not col:
            return 0.0
        # ดึง job_mobility ตามตำแหน่ง
        jm = job_mobility.objects.filter(pos_id=obj.emp_id.pos_id).order_by('-date').first()
        if not jm:
            return 0.0
        # คำนวณเหมือนใน col_policySerializer
        total_amount = (jm.number_of_days or 0) * (jm.amount_per_day or 0)
        total_payment = total_amount + (jm.jm_policy or 0)
        return total_payment
     
    def get_total_income_before_tax(self, obj):
        total_regular_income = self.get_total_regular_income(obj) or 0
        other_non_regular = self.get_other_non_regular(obj) or 0
        return math.ceil(float(total_regular_income) + float(other_non_regular))   
    
    def get_calculate_taxes_0(self, obj):
        income_before_tax = self.get_total_income_before_tax(obj)
        if income_before_tax <= Decimal('1300000.00'):
            return 0 
        tariff1 = income_tax.objects.filter(tax_id=1).first()
        return tariff1.tariff if tariff1 else 0
        
    def get_calculate_taxes_5(self, obj):
        income_before_tax = self.get_total_income_before_tax(obj) or Decimal('0')
        if income_before_tax > Decimal('1300000.00') and income_before_tax <= Decimal('5000000.00'):
            tariff1 = income_tax.objects.filter(tax_id=1).first()
            tariff2 = income_tax.objects.filter(tax_id=2).first()
            return (income_before_tax - tariff1.calculation_base) * tariff2.tariff  if tariff2 else Decimal('0')
        if Decimal('5000000.00') < income_before_tax :
            tariff2 = income_tax.objects.filter(tax_id=2).first()
            if tariff2:
                return (tariff2.calculation_base * tariff2.tariff)
            return Decimal('0')

    def get_calculate_taxes_10(self, obj):
        income_before_tax = self.get_total_income_before_tax(obj) or Decimal('0')
        if income_before_tax > Decimal('5000000.00') and income_before_tax <= Decimal('15000000.00'):
            tariff1 = income_tax.objects.filter(tax_id=1).first()
            tariff2 = income_tax.objects.filter(tax_id=2).first()
            tariff3 = income_tax.objects.filter(tax_id=3).first()
            return (income_before_tax - (tariff1.calculation_base + tariff2.calculation_base)) * tariff3.tariff if tariff3 else Decimal('0')
        if Decimal('10000000.00') < income_before_tax :
            tariff3 = income_tax.objects.filter(tax_id=3).first()
            if tariff3:
                return (tariff3.calculation_base * tariff3.tariff)
            return Decimal('0')

    def get_calculate_taxes_15(self, obj):
        income_before_tax = self.get_total_income_before_tax(obj) or Decimal('0')
        if income_before_tax > Decimal('15000000.00') and income_before_tax <= Decimal('25000000.00'):
            tariff1 = income_tax.objects.filter(tax_id=1).first()
            tariff2 = income_tax.objects.filter(tax_id=2).first()
            tariff3 = income_tax.objects.filter(tax_id=3).first()
            tariff4 = income_tax.objects.filter(tax_id=4).first()
            return (income_before_tax - (tariff1.calculation_base + tariff2.calculation_base + tariff3.calculation_base)) * tariff4.tariff  if tariff4 else Decimal('0')
        if Decimal('10000000.00') < income_before_tax :
            tariff4 = income_tax.objects.filter(tax_id=4).first()
            if tariff4 and tariff4:
                return (tariff4.calculation_base * tariff4.tariff)
            return Decimal('0')
        
    def get_calculate_taxes_20(self, obj):
        income_before_tax = self.get_total_income_before_tax(obj) or Decimal('0')
        if income_before_tax > Decimal('25000000.00') and income_before_tax <= Decimal('65000000.00'):
            tariff1 = income_tax.objects.filter(tax_id=1).first()
            tariff2 = income_tax.objects.filter(tax_id=2).first()
            tariff3 = income_tax.objects.filter(tax_id=3).first()
            tariff4 = income_tax.objects.filter(tax_id=4).first()
            tariff5 = income_tax.objects.filter(tax_id=5).first()
            return (income_before_tax - (tariff1.calculation_base + tariff2.calculation_base + tariff3.calculation_base + tariff4.calculation_base)) *tariff5.tariff  if tariff5 else Decimal('0')
        if Decimal('25000000.00') < income_before_tax :
            tariff5 = income_tax.objects.filter(tax_id=5).first()
            if tariff5:
                return (tariff5.calculation_base * tariff5.tariff)
            return Decimal('0')
    
    def get_calculate_taxes_25(self, obj):
        income_before_tax = self.get_total_income_before_tax(obj) or Decimal('0')
        if income_before_tax > Decimal('65000000.00'):
            tariff1 = income_tax.objects.filter(tax_id=1).first()
            tariff2 = income_tax.objects.filter(tax_id=2).first()
            tariff3 = income_tax.objects.filter(tax_id=3).first()
            tariff4 = income_tax.objects.filter(tax_id=4).first()
            tariff5 = income_tax.objects.filter(tax_id=5).first()
            tariff6 = income_tax.objects.filter(tax_id=6).first()
            return (income_before_tax - (tariff1.calculation_base + tariff2.calculation_base + tariff3.calculation_base + tariff4.calculation_base + tariff5.calculation_base)) * tariff6.tariff if tariff6 else Decimal('0')

    def get_tortal_tax(self, obj):
        tax_0 = self.get_calculate_taxes_0(obj) or Decimal('0')
        tax_5 = self.get_calculate_taxes_5(obj) or Decimal('0')
        tax_10 = self.get_calculate_taxes_10(obj) or Decimal('0')
        tax_15 = self.get_calculate_taxes_15(obj) or Decimal('0')
        tax_20 = self.get_calculate_taxes_20(obj) or Decimal('0')
        tax_25 = self.get_calculate_taxes_25(obj) or Decimal('0')
        return math.ceil(float(tax_0 + tax_5 + tax_10 + tax_15 + tax_20 + tax_25))

    def get_tax_exempt(self, obj):
        return 1300000
    def get_Deduct_into_the_welfare_fund_8(self, obj):
        return 0
    def get_Deduct_into_the_welfare_fund_5_5(self, obj):
        return 0
    def get_Deduct_into_the_welfare_fund_8_5(self, obj):
        return 0
    def get_Deduct_into_the_welfare_fund_6(self, obj):
        return 0
    class Meta:
        model = monthly_payment
        fields = ["id",
                  "date",
                  "emp_id",
                  "lao_name",
                  "pos_id",
                  "position",
                  "salary",
                  "Deduct_into_the_welfare_fund_8",
                    "Deduct_into_the_welfare_fund_5_5",
                    "Deduct_into_the_welfare_fund_8_5",
                    "Deduct_into_the_welfare_fund_6",
                  "subsidyPosition",
                  "age_entry",
                  "y_subsidy",
                  "total_subsidy_y",
                  "total_ot",
                  "total_basic_income",
                  "fuel_payment",
                    "total_regular_income",
                    "other_non_regular",
                    "total_income_before_tax",
                    "tax_exempt",
                    "calculate_taxes_0",
                    "calculate_taxes_5",
                    "calculate_taxes_10",
                    "calculate_taxes_15",
                    "calculate_taxes_20",
                    "calculate_taxes_25",
                    "tortal_tax",
                  "salary_payment"
                  
                  ]
        






from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import monthly_payment, Employee_lcic, SubsidyPosition, SubsidyYear, Salary, OvertimeWork, FuelSubsidy, Saving_cooperative, income_tax, job_mobility, col_policy
from .serializers import monthly_paymentSerializer1
import math
from decimal import Decimal

class MonthlyPaymentDetailView(APIView):

    def get_tax_amount(self, income, tax_id, prev_base):
        tier = income_tax.objects.filter(tax_id=tax_id).first()
        return (income - prev_base) * tier.tariff if tier else 0

    def compute_payment_data(self, obj):
        emp = obj.emp_id
        pos = emp.pos_id

        salary_obj = Salary.objects.filter(pos_id=pos).first()
        salary = salary_obj.SalaryGrade if salary_obj and salary_obj.SalaryGrade else 0

        subsidy_pos = SubsidyPosition.objects.filter(pos_id=pos).first()
        subsidy_position = subsidy_pos.grant if subsidy_pos and subsidy_pos.grant else 0

        emp_info = Employee_lcic.objects.filter(emp_id=emp.emp_id).first()
        age_entry = int(emp_info.age_entry) if emp_info and emp_info.age_entry else 0

        # y_subsidy
        if age_entry == 0:
            y_subsidy = 0
        elif age_entry < 6:
            y_subsidy = SubsidyYear.objects.filter(sy_id=1).first()
            y_subsidy = y_subsidy.y_subsidy if y_subsidy and y_subsidy.y_subsidy else 0
        elif age_entry < 26:
            y_subsidy = SubsidyYear.objects.filter(sy_id=2).first()
            y_subsidy = y_subsidy.y_subsidy if y_subsidy and y_subsidy.y_subsidy else 0
        else:
            y_subsidy = SubsidyYear.objects.filter(sy_id=3).first()
            y_subsidy = y_subsidy.y_subsidy if y_subsidy and y_subsidy.y_subsidy else 0

        total_subsidy_y = age_entry * y_subsidy

        overtime = OvertimeWork.objects.filter(emp_id=emp).first()
        total_ot = overtime.total_ot if overtime and overtime.total_ot else 0

        fuel_payment = FuelSubsidy.objects.filter(pos_id=pos).first()
        fuel = fuel_payment.total_fuel if fuel_payment and fuel_payment.total_fuel else 0

        # ✅ Convert all to Decimal safely
        salary = Decimal(salary)
        subsidy_position = Decimal(subsidy_position)
        total_subsidy_y = Decimal(total_subsidy_y)
        total_ot = Decimal(total_ot)
        fuel = Decimal(fuel)

        total_basic_income = salary + subsidy_position + total_subsidy_y + total_ot
        total_regular_income = total_basic_income + fuel

        # Other non regular
        col = col_policy.objects.filter(emp_id=emp).first()
        jm = job_mobility.objects.filter(pos_id=pos).order_by('-date').first()
        other_non_regular = Decimal('0')
        if col and jm:
            total_amount = Decimal(jm.number_of_days or 0) * Decimal(jm.amount_per_day or 0)
            other_non_regular = total_amount + Decimal(jm.jm_policy or 0)

        total_income_before_tax = total_regular_income + other_non_regular

        tax_total = Decimal('0')
        if total_income_before_tax > 1300000:
            if total_income_before_tax <= 5000000:
                tax_total += self.get_tax_amount(total_income_before_tax, 2, 1300000)
            elif total_income_before_tax <= 15000000:
                tax_total += self.get_tax_amount(5000000, 2, 1300000)
                tax_total += self.get_tax_amount(total_income_before_tax, 3, 5000000)
            elif total_income_before_tax <= 25000000:
                tax_total += self.get_tax_amount(5000000, 2, 1300000)
                tax_total += self.get_tax_amount(15000000, 3, 5000000)
                tax_total += self.get_tax_amount(total_income_before_tax, 4, 15000000)
            elif total_income_before_tax <= 65000000:
                tax_total += self.get_tax_amount(5000000, 2, 1300000)
                tax_total += self.get_tax_amount(15000000, 3, 5000000)
                tax_total += self.get_tax_amount(25000000, 4, 15000000)
                tax_total += self.get_tax_amount(total_income_before_tax, 5, 25000000)
            else:
                tax_total += self.get_tax_amount(5000000, 2, 1300000)
                tax_total += self.get_tax_amount(15000000, 3, 5000000)
                tax_total += self.get_tax_amount(25000000, 4, 15000000)
                tax_total += self.get_tax_amount(65000000, 5, 25000000)
                tax_total += self.get_tax_amount(total_income_before_tax, 6, 65000000)

        total_basic_income_after_tax = total_basic_income - tax_total
        total_income_after_tax = total_income_before_tax - tax_total

        child_subsidy = Decimal(obj.child or 0) * Decimal(obj.child_Subsidy or 0)

        saving = Saving_cooperative.objects.filter(emp_id=emp).first()
        loan = Decimal(saving.loan_amount or 0) if saving else Decimal('0')
        interest = Decimal(saving.interest or 0) if saving else Decimal('0')
        deposit = Decimal(saving.deposit or 0) if saving else Decimal('0')
        loan_deduct_194 = Decimal(saving.Loan_deduction_194 or 0) if saving else Decimal('0')
        total_saving = loan + interest + deposit

        computed = {
            "salary": float(salary),
            "subsidyPosition": float(subsidy_position),
            "age_entry": age_entry,
            "y_subsidy": float(y_subsidy),
            "total_subsidy_y": float(total_subsidy_y),
            "total_ot": float(total_ot),
            "fuel_payment": float(fuel),
            "total_basic_income": float(total_basic_income),
            "total_regular_income": float(total_regular_income),
            "other_non_regular": float(other_non_regular),
            "total_income_before_tax": float(total_income_before_tax),
            "tortal_tax": math.ceil(tax_total),
            "total_basic_income_after_tax": math.ceil(total_basic_income_after_tax),
            "total_income_after_tax": math.ceil(total_income_after_tax),
            "total_child_Subsidy": math.ceil(child_subsidy),
            "loan": float(loan),
            "interest": float(interest),
            "deposit": float(deposit),
            "Loan_deduction_194": float(loan_deduct_194),
            "total_Saving_cooperative": float(total_saving),
            "salary_payment": math.ceil(total_basic_income_after_tax),
        }

        base = monthly_paymentSerializer1(obj).data
        return {**base, **computed}

    def get(self, request, pk=None):
        if pk:
            try:
                obj = monthly_payment.objects.select_related('emp_id__pos_id').get(pk=pk)
            except monthly_payment.DoesNotExist:
                return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

            return Response(self.compute_payment_data(obj))
        else:
            queryset = monthly_payment.objects.select_related('emp_id__pos_id').all()
            results = [self.compute_payment_data(obj) for obj in queryset]
            return Response(results)

    path('monthly-payment/', MonthlyPaymentDetailView.as_view()),
    path('monthly-payment/<int:pk>/', MonthlyPaymentDetailView.as_view()),

class monthly_paymentSerializer1(serializers.ModelSerializer):
    class Meta:
        model = monthly_payment
        fields = [
            "id", "date", "emp_id", "child", "child_Subsidy", "health_Subsidy"
        ]