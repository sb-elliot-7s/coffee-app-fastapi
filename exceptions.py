from fastapi import HTTPException, status


def raise_obj_not_found(element: str):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'{element} not found'
    )


def raise_user_exists():
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='User with this username exists'
    )


def raise_incorrect_username_or_password():
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Incorrect username or password'
    )
