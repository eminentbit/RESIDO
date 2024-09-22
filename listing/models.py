from django.db import models
from django.utils.timezone import now

class Listing(models.Model):
    class SaleType(models.TextChoices):
        FOR_SALE = 'For Sale'
        FOR_RENT = 'For Rent'
        HOTEL = 'hotel'
        GUEST_HOUSE = 'guest_house'

    class HomeType(models.TextChoices):
        HOUSE = 'House'
        APARTMENT = 'apartment'
        TOWNHOUSE = 'Townhouse'

    realtor = models.EmailField(max_length=255000)
    title = models.CharField(max_length=255000)
    slug = models.SlugField(unique=True)
    address = models.CharField(max_length=255000)
    city = models.CharField(max_length=255000)
    state = models.CharField(max_length=255000)
    zipcode = models.CharField(max_length=20000)
    description = models.TextField()
    price = models.IntegerField()
    bedrooms = models.IntegerField()
    parking_space = models.IntegerField(null = True , blank = True)
    bathrooms = models.DecimalField(max_digits=20, decimal_places=1)
    sale_type = models.CharField(max_length=1000, choices=SaleType.choices, default=SaleType.FOR_SALE)
    home_type = models.CharField(max_length=1000, choices=HomeType.choices, default=HomeType.HOUSE)
    main_photo = models.ImageField(upload_to='listings/', null=True, blank= True)
    photo_1 = models.ImageField(upload_to='listings/', null=True, blank= True)
    photo_2 = models.ImageField(upload_to='listings/', null=True, blank= True)
    photo_3 = models.ImageField(upload_to='listings/', null=True, blank= True)
    photo_4 = models.ImageField(upload_to='listings/', null=True, blank= True)
    photo_5 = models.ImageField(upload_to='listings/', null=True, blank= True)
    photo_6 = models.ImageField(upload_to='listings/', null=True, blank= True)
    photo_7 = models.ImageField(upload_to='listings/', null=True, blank= True)
    photo_8 = models.ImageField(upload_to='listings/', null=True, blank= True)
    photo_9 = models.ImageField(upload_to='listings/', null=True, blank= True)
    photo_10 = models.ImageField(upload_to='listings/', null=True, blank= True)
    video_files = models.FileField(upload_to='listing/', null=True, blank= True) 
    is_published = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=now)

    def delete(self):
        self.main_photo.storage.delete(self.main_photo.name)
        self.photo_1.storage.delete(self.photo_1.name)
        self.photo_2.storage.delete(self.photo_2.name)
        self.photo_3.storage.delete(self.photo_3.name)
        self.photo_4.storage.delete(self.photo_4.name)
        self.photo_5.storage.delete(self.photo_5.name)
        self.photo_6.storage.delete(self.photo_6.name)
        self.photo_7.storage.delete(self.photo_7.name)
        self.photo_8.storage.delete(self.photo_8.name)
        self.photo_9.storage.delete(self.photo_9.name)
        self.photo_10.storage.delete(self.photo_10.name)
        self.video_files.storage.delete(self.video_files.name)
        


        super().delete()

    def __str__(self):
        return self.title
