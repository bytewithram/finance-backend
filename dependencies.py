from fastapi import Depends, HTTPException, status
from auth import get_current_user
import models

# Only allow ADMIN users
def require_admin(current_user: models.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can perform this action"
        )
    return current_user

# Allow ADMIN and ANALYST users
def require_analyst(current_user: models.User = Depends(get_current_user)):
    if current_user.role not in ["admin", "analyst"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins and analysts can perform this action"
        )
    return current_user

# Allow ALL logged in users (admin, analyst, viewer)
def require_viewer(current_user: models.User = Depends(get_current_user)):
    if current_user.role not in ["admin", "analyst", "viewer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    return current_user