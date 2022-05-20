from django.db import models
from django.db.models import Model, ForeignKey
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime
from django.utils import timezone
import uuid
from application.validators import validate_file_extension

classification = (
    ('1', 'administrator',),
    ('2', 'staff',),
)

class User_Type(models.Model):
    user                    = models.OneToOneField(User, on_delete = models.CASCADE)
    is_active               = models.BooleanField(default=True)
    classification          = models.CharField(default="2",choices=classification,max_length = 200)
    date_updated            = models.DateTimeField(auto_now = True)
    date_created            = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(self.user.last_name) + ", " + str(self.user.first_name)

class Author(models.Model):
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lastname                = models.CharField(max_length = 200)
    firstname               = models.CharField(max_length = 200)
    middlename              = models.CharField(max_length = 200,blank=True)
    ext_name                = models.CharField(max_length = 200,blank=True)
    user                    = models.ForeignKey(User, on_delete = models.CASCADE)
    date_updated            = models.DateTimeField(auto_now = True)
    date_created            = models.DateTimeField(auto_now_add = True)


    @property
    def fullname(self):
        return str(self.lastname) + ', ' + str(self.firstname) + ' ' + str(self.middlename) + ' ' + str(self.ext_name)

    def __str__(self):
        return str(self.lastname) + ', ' + str(self.firstname) + ' ' + str(self.middlename) + ' ' + str(self.ext_name)

    class Meta:
        ordering = ['lastname','firstname','middlename','ext_name']

class Position(models.Model):
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    position                = models.CharField(max_length = 1000)
    date_updated            = models.DateTimeField(auto_now = True)
    date_created            = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(self.position)

    class Meta:
        ordering = ['date_created']

class Member(models.Model):
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    position                = models.OneToOneField(Position, on_delete = models.CASCADE)
    author                  = models.OneToOneField(Author, on_delete = models.CASCADE)
    user                    = models.ForeignKey(User, on_delete = models.CASCADE)
    date_updated            = models.DateTimeField(auto_now = True)
    date_created            = models.DateTimeField(auto_now_add = True)

class Category(models.Model):
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category                = models.CharField(max_length = 1000)
    user                    = models.ForeignKey(User, on_delete = models.CASCADE)
    date_updated            = models.DateTimeField(auto_now = True)
    date_created            = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(self.category)

    class Meta:
        ordering = ['category']


class Terms(models.Model):
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description             = models.CharField(max_length = 200)
    date_from               = models.DateField(default=timezone.now)
    date_to                 = models.DateField(default=timezone.now)
    user                    = models.ForeignKey(User, on_delete = models.CASCADE)
    date_updated            = models.DateTimeField(auto_now = True)
    date_created            = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(self.description)

    class Meta:
        ordering = ['date_from']

class Terms_Author(models.Model):
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author                  = models.ForeignKey(Author, on_delete = models.CASCADE)
    user                    = models.ForeignKey(User, on_delete = models.CASCADE)
    date_updated            = models.DateTimeField(auto_now = True)
    date_created            = models.DateTimeField(auto_now_add = True)

class Terms_Author_Abstract(models.Model):
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    terms                   = models.ForeignKey(Terms, on_delete = models.CASCADE)
    author                  = models.ForeignKey(Author, on_delete = models.CASCADE)
    user                    = models.ForeignKey(User, on_delete = models.CASCADE)
    date_updated            = models.DateTimeField(auto_now = True)
    date_created            = models.DateTimeField(auto_now_add = True)

class Year_Term(models.Model):
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    year_term               = models.CharField(max_length = 200)
    user                    = models.ForeignKey(User, on_delete = models.CASCADE)
    date_updated            = models.DateTimeField(auto_now = True)
    date_created            = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(self.year_term)

    class Meta:
        ordering = ['year_term']

class Document_Type(models.Model):
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document_type           = models.CharField(max_length = 200)
    user                    = models.ForeignKey(User, on_delete = models.CASCADE)
    date_updated            = models.DateTimeField(auto_now = True)
    date_created            = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(self.document_type)

    class Meta:
        ordering = ['document_type']



class Document(models.Model):
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    series_no               = models.CharField(max_length = 5000)
    description             = models.CharField(max_length = 5000)
    remarks                 = models.CharField(max_length = 5000,blank=True)
    category                = models.ForeignKey(Category, on_delete = models.CASCADE)
    document_type           = models.ForeignKey(Document_Type, on_delete = models.CASCADE)
    date_enacted            = models.DateField(default=timezone.now)
    date_approved           = models.DateField(default=timezone.now)
    file                    = models.FileField(upload_to='upload_document/', validators=[validate_file_extension])
    user                    = models.ForeignKey(User, on_delete = models.CASCADE)
    date_updated            = models.DateTimeField(auto_now = True)
    date_created            = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(self.description)

    class Meta:
        ordering = ['description']

class Document_Author(models.Model):
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author                  = models.ForeignKey(Author, on_delete = models.CASCADE)
    user                    = models.ForeignKey(User, on_delete = models.CASCADE)
    date_updated            = models.DateTimeField(auto_now = True)
    date_created            = models.DateTimeField(auto_now_add = True)

class Document_Author_Abstract(models.Model):
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document                = models.ForeignKey(Document, on_delete = models.CASCADE)
    author                  = models.ForeignKey(Author, on_delete = models.CASCADE)
    user                    = models.ForeignKey(User, on_delete = models.CASCADE)
    date_updated            = models.DateTimeField(auto_now = True)
    date_created            = models.DateTimeField(auto_now_add = True)
