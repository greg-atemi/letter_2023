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
            data = pd.read_excel(file_path, dtype={'PO Box No': str, 'PO Box Code': str,'Mobile 1': str,'Mobile 2': str})
            for index, row in data.iterrows():
                username = row['Email']
                email = row['Email']
                password = row['Index']
                encrypted_password = make_password(password)
                index_number = row['Index']
                f_name = row['First Name']
                middle_name = row['Middle Name']
                surname = row['Surname']
                box_no = row['PO Box No']
                box_code = row['PO Box Code']
                town = row['Town']
                country = row['Country']
                mobile1 = row['Mobile 1']
                mobile2 = row['Mobile 2']
                mode = row['Mode']
                course = row['Course']
                fee_boarder = row['Fee Boarder']
                fee_day = row['Fee Day']

                Student.objects.create(email=email, username=username, password=encrypted_password,
                                       index_number=index_number, first_name=f_name, middle_name=middle_name,
                                       surname=surname, box_no=box_no, box_code=box_code, town=town,
                                       country=country, course=course, phone_number=mobile1, phone_number2=mobile2,
                                       mode=mode, fee_boarder=fee_boarder, fee_day=fee_day, email_address=email)

                self.stdout.write(self.style.SUCCESS(f'Successfully created student: '
                                                     f'{f_name + " " + middle_name + " " + surname}'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating user: {str(e)}'))
