from rest_framework import serializers
from .models import Book, Author, Customer, Place, Rent
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError


class BookSerializer(serializers.ModelSerializer):
    author_pks = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), source='authors', write_only=True,
                                                    many=True, label='Authors')

    def __init__(self, *args, **kwargs):
        # Get additional parameters from constructor
        depth = kwargs.pop('depth', None)
        fields = kwargs.pop('fields', None)

        # Add author_pks to fields if field is not None from constructor
        fields.append('author_pks') if fields is not None else None

        # Set Meta-Tags
        self.Meta.depth = depth if depth is not None else 1
        self.Meta.fields = fields if fields is not None else '__all__'

        # Call super-constructor
        super(BookSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Book

    def validate_author_pks(self, authors):
        """
        Validate authors from book.
        Check if any authors are selected. No books without authors!
        """
        if len(authors) == 0:
            raise serializers.ValidationError('No authors selected. Please select some authors for this book. ')
        return authors


class AuthorSerializer(serializers.ModelSerializer):
    # Create field-list for nested-books
    book_fields = ['id', 'isbn', 'title', 'pages', 'is_borrowed']

    # Create book-list for nested books with options
    book_list = BookSerializer(many=True, read_only=True, depth=0, fields=book_fields)

    # Change image-options to allow post/put/patch without an image
    image = serializers.ImageField(allow_null=True, required=False)

    class Meta:
        model = Author
        fields = '__all__'
        depth = 1


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'


class RentSerializer(serializers.ModelSerializer):
    customer_pk = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), source='customer',
                                                     write_only=True, label='Customer')
    book_pk = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), source='books', write_only=True,
                                                 many=True, label='Books')

    class Meta:
        model = Rent
        fields = '__all__'
        depth = 1

    def validate_book_pk(self, books):
        """
        Validate books to rent.
        Check if any books are selected. No Rent without any book!
        Check if books to rent are already borrowed.
        If rent is update --> check if new books to rent are already borrowed.
        """
        if len(books) == 0:
            raise serializers.ValidationError('No books selected. Please select some books to rent.')
        old_list = [] if not self.instance else self.instance.books.all()
        for book in books:
            if book not in old_list and book.is_borrowed:
                raise serializers.ValidationError(
                    'The Book "{}" with the ID "{}" is already borrowed.'.format(book.title, book.id))
        return books


class CustomerSerializer(serializers.ModelSerializer):
    rent_list = RentSerializer(many=True, read_only=True)
    place_pk = serializers.PrimaryKeyRelatedField(queryset=Place.objects.all(), source='place', write_only=True,
                                                  label='Place')

    class Meta:
        model = Customer
        fields = '__all__'
        depth = 1


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}, 'id': {'read_only': True}, 'email': {'required': True},
                        'first_name': {'required': True}, 'last_name': {'required': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        try:
            if User.objects.filter(email=validated_data.get('email')).exists():
                raise serializers.ValidationError('Email already registered.')
            password_validation.validate_password(password)
        except ValidationError as ve:
            raise serializers.ValidationError({'Password-Errors': [i for i in ve.messages]})
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        if User.objects.filter(email=validated_data.get('email')).exists():
            raise serializers.ValidationError('Email already registered.')
        return super(UserSerializer, self).update(instance, validated_data)