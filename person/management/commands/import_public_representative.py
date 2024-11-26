from django.core.management.base import BaseCommand
from django.core.files import File
import csv
from django.core.exceptions import ObjectDoesNotExist

from person.models import PublicRepresentative, Post

class Command(BaseCommand):
    help = 'Import public representatives from a CSV file'

    def handle(self, *args, **kwargs):
        csv_file_path = 'C:/Users/AnnapurnaIT/Downloads/jpb.csv'
        default_profile_image_path = "C:/Users/AnnapurnaIT/Pictures/logo.png"
        with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)

            for row in reader:
                print(row.keys())
                # Extract data from the CSV row
                first_name = row['first_name']
                last_name = row['last_name']
                gender = int(row['gender'])  # Assuming 1 for male, 2 for female (Choices.male_female_choices)
                mobile_number = row['mobile_number']
                email = row['email']
                ward = int(row['ward'])  # Assuming 'ward' is a valid integer choice in Choices.WardChoices
                cabinet_member = row['cabinet_member'] == 'TRUE'  # Convert to boolean
                post_name = row['post_name']  # Assume the column in CSV is called 'post_name'
                status = int(row['status'])  # Assuming status is an integer that maps to Choices.StatusChoices
                # profile_image = row['profile_image']
                weight = int(row['weight'])

                # Check if the Post object already exists; if not, create it
                post, created = Post.objects.get_or_create(name=post_name)
                if created:
                    print(f"Created new Post: {post_name}")
                else:
                    print(f"Post '{post_name}' already exists.")

                # Create the PublicRepresentative object directly
                public_representative = PublicRepresentative.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    gender=gender,
                    mobile_number=mobile_number,
                    email=email,
                    post=post,
                    status=status,
                    weight=weight,
                    ward=ward,
                    cabinet_member=cabinet_member,

                )

                # Handle profile_image if the file exists (assuming the image file path is provided)
                if default_profile_image_path:
                    try:
                        with open(default_profile_image_path, 'rb') as img_file:
                            public_representative.profile_image.save('default_profile.jpg', File(img_file))
                            print(f"Assigned default profile image to {public_representative.get_full_name()}")
                    except FileNotFoundError:
                        print(f"Profile image file '{default_profile_image_path}' not found.")
                        # Handle if image file is not found (e.g., log the error or assign a placeholder image)
                
                print(f"Created PublicRepresentative: {public_representative.get_full_name()}")
