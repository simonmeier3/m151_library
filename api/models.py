from django.db import models


class Author(models.Model):
    """
    Author-Model
    Basic-Model to store authors with image.
    """
    first_name = models.CharField(null=False, max_length=150)
    last_name = models.CharField(null=False, max_length=150)
    image = models.ImageField(null=False, upload_to='authors', default='noimage.png')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Book(models.Model):
    """
    Book-Model
    Basic-Model to store books.
    Linked to authors with many-to-many.
    """
    isbn = models.CharField(null=False, max_length=150)
    title = models.CharField(null=False, max_length=150)
    pages = models.IntegerField(null=False)
    is_borrowed = models.BooleanField(null=False, default=False)
    authors = models.ManyToManyField(Author, related_name='book_list', blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}' .format(self.title)


class Place(models.Model):
    """
    Place-Model
    Basic-Model to store places.
    """
    postcode = models.IntegerField(null=False)
    place = models.CharField(null=False, max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {}' .format(self.postcode, self.place)


class Customer(models.Model):
    """
    Customer-Model
    Basic-Model to store customers.
    Linked to place with foreign-key.
    """
    first_name = models.CharField(null=False, max_length=150)
    last_name = models.CharField(null=False, max_length=150)
    email = models.EmailField(null=False)
    street = models.CharField(null=False, max_length=150)
    phone = models.CharField(null=False, max_length=100)
    place = models.ForeignKey(Place, null=False, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Rent(models.Model):
    """
    Rent-Model
    Basic-Model to store rents.
    Linked to customer with foreign-key.
    Linked to boos with many-to-many.
    """
    begin = models.DateField(null=False)
    end = models.DateField(null=False)
    is_picked_up = models.BooleanField(default=False, null=False)
    is_returned = models.BooleanField(default=False, null=False)
    books = models.ManyToManyField(Book, related_name='book_list', blank=False)
    customers = models.ForeignKey(Customer, null=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} to {}, rented by {} {}'.format(self.begin, self.end, self.customer.first_name,
                                                  self.customer.last_name)
