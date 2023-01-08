from pickle import FALSE
from pyexpat import model
from django.contrib import admin
from .models import Application, AssessmentCriteria, StudentAssessment
from django.contrib.auth.models import User
from import_export.fields import Field, widgets
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ExportMixin, ExportActionMixin
from import_export.widgets import ManyToManyWidget,ForeignKeyWidget
from django.db.models import Avg
from django.utils.html import format_html



admin.site.disable_action('delete_selected')

# Register your models here.


class AssessmentInline(admin.TabularInline):
    model = AssessmentCriteria
    extra = 1
    max_num = 1
    can_delete = FALSE
    #actions = []
    
    editable_fields = ['project_objective', 'project_desc', 'project_ingenuity', 'project_source',
        'expected_benefit', 'presentation_skills', 'project_viability', 'sustainability']
    readonly_fields = []
    exclude = ['created_at', 'updated_at']
    
    
    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
            [field.name for field in self.model._meta.fields
            if field.name not in self.editable_fields and
                field.name not in self.exclude]
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(assessor=request.user)
    
    
    def __init__(self, *args, **kwargs):
        super(AssessmentInline, self).__init__(*args, **kwargs)
        self.can_delete = False
    
    # Permission to disable add button
    # def has_add_permission(self, request, obj=None):
    #     return False

    # def has_delete_permission(self, request, obj=None):
    #     return False
    
class ApplicantResource(resources.ModelResource):
    
    class Meta:
        model = Application

    
class ApplicationAdmin(ExportActionMixin, admin.ModelAdmin):
    pass
    inlines = [AssessmentInline]
    resource_class = ApplicantResource
    show_average = Field(column_name='show_average')
    exclude = ('created_at', 'updated_at', 'photo', 'video_file', 'school_id')
    # model = Application
    list_display = ("last_name", "first_name", "matric_number", "phone_number", "email", "school_name", "show_average")
    search_fields = ['last_name']
    can_delete = FALSE
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def show_average(self, obj):
        result = AssessmentCriteria.objects.filter(applicant_name=obj).aggregate(Avg("total_score"))
        return format_html("<b><i>{}</i></b>", result["total_score__avg"])
    show_average.short_description = "Average Grade"
    #class Meta:
        #search_fields = ("last_name__startswith", )
        #readonly_fields = ["total_score"]



admin.site.register(Application, ApplicationAdmin)

class AssessmentResource(resources.ModelResource):
    # applicant_name = Field(
    #     column_name = "Last Name",
    #     attribute = "applicant_name",
    #     widget = ForeignKeyWidget(Application, 'last_name')
    # )
    # assessor = Field(
    #     column_name = "Assessor",
    #     attribute = "assessor",
    #     widget = ForeignKeyWidget(User, 'username')
    # )
    
    class Meta:
        model = AssessmentCriteria
        fields = ('id', 'applicant_name__first_name', 'project_objective', 'project_desc', 'total_score', 'assessor__first_name',)
        #export_order = ('id', 'applicant_name', 'assessor__username', 'project_objective', 'project_desc', 'total_score',)
        exclude = ('created_at', 'updated_at', )
        published = Field(attribute='published', column_name='applicant_name__first_name')
        
        

#admin.site.register(AssessmentCriteria)
@admin.register(AssessmentCriteria)
class CriteriaAdmin(ImportExportModelAdmin):
    model = AssessmentCriteria
    resource_class = AssessmentResource
    extra = 1
    list_display = ("applicant_name", "project_objective", "project_desc", "project_ingenuity", "project_source", "expected_benefit", "total_score", "assessor")
    editable_fields = ['project_objective', 'project_desc', 'project_ingenuity', 'project_source',
        'expected_benefit', 'presentation_skills', 'project_viability', 'sustainability', 'applicant_name']
    readonly_fields = []
    exclude = ['created_at', 'updated_at', 'id']
    search_fields = ("applicant_name__startswith", "assessor__startswith",)
    
    
    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
            [field.name for field in self.model._meta.fields
            if field.name not in self.editable_fields and
                field.name not in self.exclude]
            
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(assessor=request.user)
    
    
    
    # def __init__(self, *args, **kwargs):
    #     super (AssessmentCriteria, self ).__init__(*args,**kwargs)
    #     self.fields['assessor'].queryset = User.objects.filter(groups__name='assessor')
    
    
class StudentAssessmentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass
    list_display = ("Fullname", "Institution", "PresentationSkills", "ExpectedBenefits", "ProjectDesc", "ProjectIngenuity", "ProjectViability",
                    "Sustainability", "ProjectSource", "ProjectObjective", "TotalScore", "AverageScore")
    readonly_fields = ["Fullname", "Institution", "PresentationSkills", "ExpectedBenefits", "ProjectDesc", "ProjectIngenuity", "ProjectViability",
                    "Sustainability", "ProjectSource", "ProjectObjective", "TotalScore", "AverageScore"]
    exclude = ['unique_id']
    search_fields = ("Fullname", "Institution",)
    ordering = ('-AverageScore',)
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request, obj=None):
        return False
    
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': False,
            'show_save_and_continue': False,
            'show_delete': False
        })
        return super().render_change_form(request, context, add, change, form_url, obj)
admin.site.register(StudentAssessment, StudentAssessmentAdmin)
    