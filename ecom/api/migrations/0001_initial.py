from django.db import migrations
from api.user.models import CustomUser

class Migration(migrations.Migration):
    def seed_data(apps, schema_editor):
        user = CustomUser(name="atul", email="atullsharma2000@gmail.com", is_staff=True, is_superuser=True, phone="8825454545", gender="Male")

        user.set_password("atul") 
        user.save()
    
    dependencies = [            # this user is not dependent on anyone , so we leave this field blank
    
    ]

    operations = [
        migrations.RunPython(seed_data),                # this will run the seed_data we created
    ]