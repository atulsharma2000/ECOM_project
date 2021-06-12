from rest_framework import serializers
from django.contrib.auth.hashers import make_password
# this allows u to bring your password from clear text format and hash it out

from rest_framework.decorators import authentication_classes, permission_classes, permission_classes
# decorators allows u to write or add something to those pre-written things from remotly 
from .models import CustomUser


class UserSerializer(serializers.HyperlinkedModelSerializer):

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data) #its gonna interacting with model and we will be saving it based on that, (coming up from meta part)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':    #if attr says u want to update the password
                instance.set_password(value)  #then use this instance and set_pass
            else:
                setattr(instance, attr, value)  #if not passw then update others
        instance.save()
        return instance

    class Meta:
        model = CustomUser
        extra_kwargs = {'password': {'write_only': True}}  
        fields = ('name', 'email', 'password', 'phone', 'gender', 'is_active', 'is_staff', 'is_superuser')  #fields i want to serialize  
        
        # active staff superuser all are field in django admin pannel
        