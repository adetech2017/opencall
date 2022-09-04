from pickle import FALSE
from pyexpat import model
from django.contrib import admin
from .models import Application, AssessmentCriteria

admin.site.disable_action('delete_selected')

# Register your models here.


class AssessmentInline(admin.TabularInline):
    model = AssessmentCriteria
    extra = 1
    max_num = 1
    can_delete = FALSE
    actions = []
    
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
    
    def __init__(self, *args, **kwargs):
        super(AssessmentInline, self).__init__(*args, **kwargs)
        self.can_delete = False
    

    

    # Permission to disable add button
    # def has_add_permission(self, request, obj=None):
    #     return False


    # def has_delete_permission(self, request, obj=None):
    #     return False
    
    
    

class ApplicationAdmin(admin.ModelAdmin):
    inlines = [AssessmentInline]
    # model = Application
    list_display = ("last_name", "first_name", "matric_number", "phone_number", "email", "school_name")
    search_fields = ['last_name']
    can_delete = FALSE
    
    def has_delete_permission(self, request, obj=None):
        return False
    #class Meta:
        #search_fields = ("last_name__startswith", )
        #readonly_fields = ["total_score"]



admin.site.register(Application, ApplicationAdmin)

#admin.site.register(AssessmentCriteria)
@admin.register(AssessmentCriteria)
class CriteriaAdmin(admin.ModelAdmin):
    model = AssessmentCriteria
    extra = 1
    list_display = ("applicant_name", "project_objective", "project_desc", "project_ingenuity", "project_source", "expected_benefit")
    editable_fields = ['project_objective', 'project_desc', 'project_ingenuity', 'project_source',
        'expected_benefit', 'presentation_skills', 'project_viability', 'sustainability', 'applicant_name']
    readonly_fields = []
    exclude = ['created_at', 'updated_at', 'id']
    
    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
            [field.name for field in self.model._meta.fields
            if field.name not in self.editable_fields and
                field.name not in self.exclude]
            
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    
    