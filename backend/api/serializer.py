from rest_framework import serializers
from users.models import Resume 

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['name', 'file', 'summary', 'MatchedSkills', 'MissingSkills','ExtractSkills', 'score' ]


class ResumeDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Resume
        fields = [
            'name',
            'jobtitle',
            'Instutut_name',
            'desired_role',
            'file',
            'summary'
        ]