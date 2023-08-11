import pandas as pd
from admission.models import Student
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    help = 'Create user accounts from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('admission/~$accounts.xlsx', type=str, help='Path to the Excel file')

    def handle(self, *args, **options):
        file_path = options['admission/~$accounts.xlsx']

        try:
            data = pd.read_excel(file_path,
                                 dtype={'PO Box No': str, 'PO Box Code': str, 'Mobile 1': str, 'Mobile 2': str})
            for index, row in data.iterrows():
                username = row['Index']
                email = row['Email']
                password = row['Index']
                encrypted_password = make_password(password)
                index_number = row['Index']
                full_name = row['Student Name']
                gender = row['Gender']
                serial_number = row['Serial Number']
                box_no = row['PO Box No']
                box_code = row['PO Box Code']
                town = row['Town']
                mobile1 = row['Phone Number 1']
                mobile2 = row['Phone Number 2']
                mode = row['Mode']
                course = row['Course']

                Student.objects.create(email=email, username=username, password=encrypted_password,
                                       index_number=index_number, full_name=full_name, gender=gender,
                                       box_no=box_no, box_code=box_code, town=town, email_address=email,
                                       course=course, phone_number=mobile1, phone_number2=mobile2,
                                       mode=mode, serial_number=serial_number)

                self.stdout.write(self.style.SUCCESS(f'Successfully created student: '
                                                     f'{full_name}'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating user: {str(e)}'))
