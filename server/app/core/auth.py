from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Subcontractor

# ---------------------------
# JWT Settings
# ---------------------------
SECRET_KEY = "supersecretkey123"  # move to .env for production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hour

# ---------------------------
# Password hashing
# ---------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_password_hash(password: str) -> str:
    """
    Hash password safely with SHA256 pre-hash + bcrypt (prevents >72 bytes error)
    """
    import hashlib
    sha256_pw = hashlib.sha256(password.encode()).hexdigest()
    sha256_pw_trunc = sha256_pw[:72]
    return pwd_context.hash(sha256_pw_trunc)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    import hashlib
    sha256_pw = hashlib.sha256(plain_password.encode()).hexdigest()
    sha256_pw_trunc = sha256_pw[:72]
    return pwd_context.verify(sha256_pw_trunc, hashed_password)

# ---------------------------
# JWT Token Functions
# ---------------------------
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

# ---------------------------
# Get current subcontractor
# ---------------------------
def get_current_subcontractor(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        sub_id: int = payload.get("sub_id")
        if sub_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    subcontractor = db.query(Subcontractor).filter(Subcontractor.id == sub_id).first()
    if subcontractor is None:
        raise credentials_exception
    return subcontractor
