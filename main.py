import os
from dotenv import load_dotenv
load_dotenv()

import smtplib
from datetime import datetime, timedelta, date
from email.message import EmailMessage
from typing import List, Optional
import json
import redis
import cloudinary
import cloudinary.uploader
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import EmailStr
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session, relationship
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from starlette.requests import Request
from database import SessionLocal, engine, Base
from models import Contact, User, ContactResponse, ContactCreate, UserRole

# Redis configuration
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
    decode_responses=True
)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

app = FastAPI()

# Create tables only when running the app
@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def get_db():
    """
    Dependency to get a database session.
    
    Yields:
        Session: A SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT access token.
    
    Args:
        data (dict): Data to encode in the token
        expires_delta (Optional[timedelta]): Token expiration time
        
    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user(db: Session, email: str):
    """
    Get a user by email from the database.
    
    Args:
        db (Session): The database session.
        email (str): The user's email.
    
    Returns:
        User: The user object if found, None otherwise.
    """
    return db.query(User).filter(User.email == email).first()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    
    Args:
        plain_password (str): Plain text password to verify
        hashed_password (str): Hashed password to verify against
        
    Returns:
        bool: True if passwords match, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password.
    
    Args:
        password (str): Plain text password to hash
        
    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)


def authenticate_user(db: Session, email: str, password: str):
    """
    Authenticate a user with email and password.
    
    Args:
        db (Session): The database session.
        email (str): The user's email.
        password (str): The user's password.
    
    Returns:
        User: The authenticated user object if successful, None otherwise.
    """
    user = get_user(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Get the current authenticated user from the JWT token.
    First tries to get the user from Redis cache, if not found, gets from database.
    
    Args:
        token (str): JWT token from Authorization header
        db (Session): Database session
        
    Returns:
        User: Current authenticated user
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        
        # Try to get user from Redis cache
        cached_user = redis_client.get(f"user:{email}")
        if cached_user:
            user_dict = json.loads(cached_user)
            user = User(
                id=user_dict["id"],
                email=user_dict["email"],
                hashed_password=user_dict["hashed_password"],
                is_verified=user_dict["is_verified"]
            )
            return user
        
        # If not in cache, get from database
        user = get_user(db, email)
        if not user:
            raise credentials_exception
        
        # Cache user in Redis for 30 minutes
        user_dict = {
            "id": user.id,
            "email": user.email,
            "hashed_password": user.hashed_password,
            "is_verified": user.is_verified
        }
        redis_client.setex(
            f"user:{email}",
            timedelta(minutes=30),
            json.dumps(user_dict)
        )
        
        return user
    except JWTError:
        raise credentials_exception


def send_verification_email(email: str, token: str):
    """
    Send a verification email to the user.
    
    Args:
        email (str): User's email address
        token (str): Verification token
    """
    verification_url = f"http://localhost:8000/verify/{token}"
    msg = EmailMessage()
    msg["Subject"] = "Verify your email"
    msg["From"] = os.getenv("SMTP_EMAIL")
    msg["To"] = email
    msg.set_content(f"Please verify your email by clicking the link: {verification_url}")

    with smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT"))) as server:
        server.starttls()
        server.login(os.getenv("SMTP_EMAIL"), os.getenv("SMTP_PASSWORD"))
        server.send_message(msg)


@app.post("/contacts/", response_model=ContactResponse)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    """
    Create a new contact for the current user.
    
    Args:
        contact (ContactCreate): The contact data.
        db (Session): The database session.
        current_user (User): The authenticated user.
    
    Returns:
        ContactResponse: The created contact.
    """
    db_contact = Contact(**contact.dict(), owner_id=current_user.id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


@app.get("/contacts/", response_model=List[ContactResponse])
def read_contacts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get all contacts for the current user.
    
    Args:
        db (Session): The database session.
        current_user (User): The authenticated user.
    
    Returns:
        List[ContactResponse]: List of user's contacts.
    """
    return db.query(Contact).filter(Contact.owner_id == current_user.id).all()


@app.get("/contacts/{contact_id}", response_model=ContactResponse)
def read_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get a specific contact by ID.
    
    Args:
        contact_id (int): The contact's ID.
        db (Session): The database session.
        current_user (User): The authenticated user.
    
    Returns:
        ContactResponse: The requested contact.
    
    Raises:
        HTTPException: If the contact is not found.
    """
    contact = db.query(Contact).filter(Contact.id == contact_id, Contact.owner_id == current_user.id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@app.put("/contacts/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, contact_data: ContactCreate, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    """
    Update a contact by ID.
    
    Args:
        contact_id (int): The contact's ID.
        contact_data (ContactCreate): The updated contact data.
        db (Session): The database session.
        current_user (User): The authenticated user.
    
    Returns:
        ContactResponse: The updated contact.
    
    Raises:
        HTTPException: If the contact is not found.
    """
    contact = db.query(Contact).filter(Contact.id == contact_id, Contact.owner_id == current_user.id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    for key, value in contact_data.dict().items():
        setattr(contact, key, value)
    db.commit()
    db.refresh(contact)
    return contact


@app.delete("/contacts/{contact_id}", response_model=ContactResponse)
def delete_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Delete a contact by ID.
    
    Args:
        contact_id (int): The contact's ID.
        db (Session): The database session.
        current_user (User): The authenticated user.
    
    Returns:
        ContactResponse: The deleted contact.
    
    Raises:
        HTTPException: If the contact is not found.
    """
    contact = db.query(Contact).filter(Contact.id == contact_id, Contact.owner_id == current_user.id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
    return contact


limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.get("/me/")
@limiter.limit("5/minute")
async def read_users_me(request: Request, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Get the current user's information.
    
    Args:
        request (Request): The FastAPI request object.
        token (str): The JWT token.
        db (Session): The database session.
    
    Returns:
        User: The current user's information.
    
    Raises:
        HTTPException: If the token is invalid or the user is not found.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        user = get_user(db, email)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_admin(current_user: User = Security(get_current_user)):
    """
    Dependency to get the current user and verify they are an admin.
    
    Args:
        current_user (User): The current authenticated user.
    
    Returns:
        User: The current admin user.
    
    Raises:
        HTTPException: If the user is not an admin.
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user

@app.post("/register/")
def register_user(email: EmailStr, password: str, is_admin: bool = False, db: Session = Depends(get_db)):
    """
    Register a new user.
    
    Args:
        email (EmailStr): The user's email.
        password (str): The user's password.
        is_admin (bool): Whether to create an admin user.
        db (Session): The database session.
    
    Returns:
        dict: A message indicating successful registration.
    
    Raises:
        HTTPException: If a user with the given email already exists.
    """
    db_user = db.query(User).filter(User.email == email).first()
    if db_user:
        raise HTTPException(status_code=409, detail="User already exists")
    
    hashed_password = get_password_hash(password)
    user = User(
        email=email,
        hashed_password=hashed_password,
        is_verified=False,
        role=UserRole.ADMIN if is_admin else UserRole.USER
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    verification_token = create_access_token({"sub": email})
    send_verification_email(email, verification_token)
    
    return {"message": "User registered successfully. Please check your email to verify your account."}


@app.get("/verify/{token}")
def verify_email(token: str, db: Session = Depends(get_db)):
    """
    Verify a user's email address.
    
    Args:
        token (str): The verification token.
        db (Session): The database session.
    
    Returns:
        dict: A message indicating successful verification.
    
    Raises:
        HTTPException: If the token is invalid or the user is not found.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=400, detail="Invalid token")
        user.is_verified = True
        db.commit()
        return {"message": "Email verified successfully"}
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")


@app.put("/users/avatar/")
def update_avatar(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Update the current user's avatar.
    Only admin users can change their avatar.
    
    Args:
        file (UploadFile): The avatar image file.
        db (Session): The database session.
        current_user (User): The authenticated user.
    
    Returns:
        dict: A message indicating successful update and the new avatar URL.
    
    Raises:
        HTTPException: If there's an error uploading the avatar or if the user doesn't have permission.
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only admin users can change their avatar")
    
    try:
        upload_result = cloudinary.uploader.upload(file.file)
        current_user.avatar_url = upload_result["secure_url"]
        db.commit()
        db.refresh(current_user)
        
        # Update user in Redis cache
        user_dict = {
            "id": current_user.id,
            "email": current_user.email,
            "hashed_password": current_user.hashed_password,
            "is_verified": current_user.is_verified,
            "role": current_user.role.value,
            "avatar_url": current_user.avatar_url
        }
        redis_client.setex(
            f"user:{current_user.email}",
            timedelta(minutes=30),
            json.dumps(user_dict)
        )
        
        return {"message": "Avatar updated successfully", "avatar_url": current_user.avatar_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading avatar: {str(e)}")


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticate a user and return an access token.
    Also caches the user in Redis upon successful login.
    
    Args:
        form_data (OAuth2PasswordRequestForm): The login form data.
        db (Session): The database session.
    
    Returns:
        dict: The access token and token type.
    
    Raises:
        HTTPException: If the credentials are invalid or the email is not verified.
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not user.is_verified:
        raise HTTPException(status_code=401, detail="Email not verified")

    # Cache user in Redis
    user_dict = {
        "id": user.id,
        "email": user.email,
        "hashed_password": user.hashed_password,
        "is_verified": user.is_verified
    }
    redis_client.setex(
        f"user:{user.email}",
        timedelta(minutes=30),
        json.dumps(user_dict)
    )

    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

def send_password_reset_email(email: str, token: str):
    """
    Send a password reset email to the user.
    
    Args:
        email (str): The recipient's email address.
        token (str): The password reset token.
    """
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT"))
    smtp_email = os.getenv("SMTP_EMAIL")
    smtp_password = os.getenv("SMTP_PASSWORD")

    msg = EmailMessage()
    msg["Subject"] = "Reset your password"
    msg["From"] = smtp_email
    msg["To"] = email
    msg.set_content(f"Click the link to reset your password: http://127.0.0.1:8000/reset-password/{token}")

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_email, smtp_password)
        server.send_message(msg)

@app.post("/forgot-password/")
def forgot_password(email: EmailStr, db: Session = Depends(get_db)):
    """
    Initiate the password reset process.
    
    Args:
        email (EmailStr): The user's email address.
        db (Session): The database session.
    
    Returns:
        dict: A message indicating that the reset email was sent.
    
    Raises:
        HTTPException: If the user is not found.
    """
    user = get_user(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Create a password reset token
    reset_token = create_access_token(
        {"sub": email, "type": "password_reset"},
        expires_delta=timedelta(minutes=15)
    )
    
    # Send the reset email
    send_password_reset_email(email, reset_token)
    
    return {"message": "Password reset email sent. Please check your email."}

@app.post("/reset-password/{token}")
def reset_password(token: str, new_password: str, db: Session = Depends(get_db)):
    """
    Reset a user's password using a reset token.
    
    Args:
        token (str): The password reset token.
        new_password (str): The new password.
        db (Session): The database session.
    
    Returns:
        dict: A message indicating successful password reset.
    
    Raises:
        HTTPException: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        token_type = payload.get("type")
        
        if token_type != "password_reset":
            raise HTTPException(status_code=400, detail="Invalid token type")
        
        user = get_user(db, email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Update the password
        user.hashed_password = get_password_hash(new_password)
        db.commit()
        
        # Update user in Redis cache
        user_dict = {
            "id": user.id,
            "email": user.email,
            "hashed_password": user.hashed_password,
            "is_verified": user.is_verified
        }
        redis_client.setex(
            f"user:{email}",
            timedelta(minutes=30),
            json.dumps(user_dict)
        )
        
        return {"message": "Password has been reset successfully"}
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")