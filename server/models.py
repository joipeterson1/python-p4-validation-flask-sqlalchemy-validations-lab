from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, name):
    # Check if the name already exists in the database
        existing_author = db.session.query(Author).filter(Author.name == name).first()
        if existing_author:
            raise ValueError("Name must be unique")
        if len(name) == 0:
            raise ValueError("Name cannot be empty")
        return name

    @validates("phone_number")
    def validate_number(self, key, phone_number):
    # Check if the phone number is exactly 10 digits and all characters are digits
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise ValueError("Phone number must be exactly 10 digits and contain only numbers")
        return phone_number 
        
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates("content")
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Content must be at least 250 characters long")
        return content
    
    @validates("summary")
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Summary must be a max of 250 characters long")
        return summary
    
    @validates("category")
    def validate_category(self, key, category):
        if category not in ["Fiction" ,"Non-Fiction"]:
            raise ValueError("Catergory must be fiction or non-fiction")
        return category
    
    @validates("title")
    def validate_title(self, key, title):
        post_title = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in title for phrase in post_title):
            raise ValueError("Invalid title")
        return title


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
