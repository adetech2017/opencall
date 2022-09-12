from email.mime import application
from django.db import models
from django.db.models import Sum
from django.core.validators import FileExtensionValidator

# Create your models here.

CRITERIA = [
    # (5,'Excellent'),
    # (4,'Good'),
    # (3, 'Average'),
    # (2,'Poor'),
    # (1, 'Very poor')
    (i) for i in range(101)
]


class Application(models.Model):
    matric_number = models.CharField(max_length=15)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=11)
    date_of_birth = models.DateField()
    email = models.CharField(max_length=50)
    aim_objective = models.CharField(max_length=100)
    school_name = models.CharField(max_length=150)
    school_address = models.TextField()
    school_id = models.ImageField(upload_to='media/schoolIds')
    video_file = models.FileField(upload_to='media/applications', validators=[FileExtensionValidator(['mp4'])])
    photo = models.ImageField(upload_to='media/photos')
    project_source = models.CharField(max_length=10)
    desc = models.TextField()
    project_desc = models.TextField()
    project_benefit = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "students_applications"
        ordering = ("last_name", "first_name")
        
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    
    
class AssessmentCriteria(models.Model):
    applicant_name = models.ForeignKey(Application, on_delete=models.CASCADE)
    project_objective = models.IntegerField(choices = CRITERIA)
    project_desc = models.IntegerField(choices = CRITERIA)
    project_ingenuity = models.IntegerField(choices = CRITERIA)
    project_source = models.IntegerField(choices = CRITERIA)
    expected_benefit = models.IntegerField(choices = CRITERIA)
    presentation_skills = models.IntegerField(choices = CRITERIA)
    project_viability = models.IntegerField(choices = CRITERIA)
    sustainability = models.IntegerField(choices = CRITERIA) 
    total_score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "assessment_criteria"
        
    def save(self, *args, **kwargs):
        self.total_score = self.project_objective + self.project_desc + self.project_ingenuity + self.project_source + self.expected_benefit + self.presentation_skills + self.project_viability + self.sustainability
        super(AssessmentCriteria, self).save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.applicant_name}"
        
    # def __init__(self, *args, **kwargs):
    #     super(AssessmentCriteria).__init__(*args, **kwargs)
    #     self.total_score['total_score'].disabled = True

    
