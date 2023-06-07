import uuid
from fastapi import Request, APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates
from auth.auth import pwd_context
from controllers.get_analysis import get_Country, get_Territory, get_Locality
from controllers.get_content_main import get_postinfo, get_users, get_users_by_username, get_profile_user
from controllers.get_my_record import get_record, get_record_check, get_postinfo_id, get_categories, get_location, add_new_post
from controllers.get_infousers import get_user_info, update_user_info, update_status_records, get_all_user_info, \
    get_moderators_work_info, get_employee
from fastapi import Depends
from models.database import get_db, SessionLocal
from auth import auth as _auth
from asyncio import CancelledError
from models import models as _models


templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/")
async def main_page(request: Request, db: Session = Depends(get_db)):
    try:
        posts = get_postinfo(db)
        user_token = request.cookies.get("session_id")
        prof = 'no'
        if user_token:
            result = _auth.verify_token(user_token)
            role = result.get('role')
            if role == 'moderator':
                prof = 'moder'
            elif role == 'administrator':
                prof = 'admin'
            else:
                prof = 'yes'
        context = {"request": request, "posts": posts, "prof": prof}
        return templates.TemplateResponse("index.html", context)
    except CancelledError:
        pass


@router.get("/home")
async def main_page(request: Request, db: Session = Depends(get_db)):
    posts = get_postinfo(db)
    prof = 'no'
    try:
        user_token = request.cookies.get("session_id")
        if user_token:
            result = _auth.verify_token(user_token)
            role = result.get('role')
            if role == 'moderator':
                prof = 'moder'
            elif role == 'administrator':
                prof = 'admin'
            else:
                prof = 'yes'

        context = {"request": request, "posts": posts, "prof": prof}
        return templates.TemplateResponse("index.html", context)
    except CancelledError:
        context = {"request": request, "posts": posts, "prof": prof}
        return templates.TemplateResponse("index.html", context)


@router.post("/register")
async def register_user(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    username = form_data.get("login")
    password = form_data.get("hashed_password")
    hashed_password = pwd_context.hash(password)
    db_user = _models.Account(login=username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    redirect_url = '/home'
    response = RedirectResponse(url=redirect_url, status_code=302)
    response.headers["Location"] = redirect_url

    return response


@router.get("/register")
async def main_pagereg(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("register.html", context)


@router.post("/login")
async def login_user(
    response: RedirectResponse, request: Request, db: Session = Depends(get_db),
):
    form_data = await request.form()
    username = form_data.get("username")
    password = form_data.get("password")

    db_user = get_users_by_username(db=db, username=username)
    if not db_user:
        raise HTTPException(
            status_code=401, detail="Anmeldeinformationen nicht korrekt"
        )

    if _auth.verify_password(password, db_user.hashed_password):
        token = _auth.create_access_token(db_user)
        session_id = str(uuid.uuid4())
        if db_user.post == 'moderator':
            url = '/profile_moder'
        elif db_user.post == 'administrator':
            url = '/profile_admin'
        else:
            url = '/profile'

        response = RedirectResponse(url)
        response.set_cookie(key="session_id", value=f"{token}", max_age=3600, domain="127.0.0.1", httponly=True)
        return response

    raise HTTPException(status_code=401, detail="Anmeldeinformationen nicht korrekt")


@router.get("/get_cookie")
def get_cookie(request: Request):
    session_id = request.cookies.get("session_id")
    decode_session_id = _auth.verify_token(session_id)
    if session_id:
        return {"session_id": decode_session_id}
    else:
        return {"message": "Cookie not found"}


@router.get("/logout")
def logout():
    redirect_url = '/home'
    response = RedirectResponse(redirect_url)
    response.delete_cookie(key="session_id")
    return response


@router.route("/profile", methods=["GET", "POST"])
async def profile(request: Request):
    try:
        db = SessionLocal()
        user_token = request.cookies.get("session_id")
        if not user_token:
            redirect_url = '/home'
            response = RedirectResponse(redirect_url)
            return response
        result = _auth.verify_token(user_token)
        id_user = result.get('id_account')
        res_new = get_profile_user(db=db, id_user=id_user)
        record = get_record(db=db, id_user=id_user)

        context = {"request": request, "account_info": res_new, "record": record}
        return templates.TemplateResponse("profile.html", context)
    except CancelledError:
        pass


@router.route("/profile_moder", methods=["GET", "POST"])
async def profile_moder(request: Request):
    try:
        db = SessionLocal()
        user_token = request.cookies.get("session_id")
        if not user_token:
            redirect_url = '/home'
            response = RedirectResponse(redirect_url)
            return response
        result = _auth.verify_token(user_token)
        role = result.get('role')
        id_user = result.get('id_account')
        if role == 'moderator':
            post_info = get_profile_user(db=db, id_user=id_user)

            context = {"request": request, "acc_info": post_info, "record_checks": get_record_check(db)}
            return templates.TemplateResponse("moder.html", context)
        else:
            redirect_url = '/home'
            response = RedirectResponse(redirect_url)
            return response
    except CancelledError:
        pass


@router.route('/profile_admin', methods=["GET", "POST"])
async def profile_moder(request: Request):
    try:
        db = SessionLocal()
        user_token = request.cookies.get("session_id")
        if not user_token:
            redirect_url = '/home'
            response = RedirectResponse(redirect_url)
            return response
        result = _auth.verify_token(user_token)
        role = result.get('role')
        id_user = result.get('id_account')
        if role == 'administrator':
            post_info = get_profile_user(db=db, id_user=id_user)
            users_info = get_all_user_info(db)
            moderators_work = get_moderators_work_info(db)
            employee = get_employee(db)
            anl_count = get_Country(db)
            anl_terr = get_Territory(db)
            anl_loc = get_Locality(db)

            context = {"request": request, "acc_info": post_info, 'users_info': users_info,
                       'moderators_work': moderators_work, "employee": employee,
                       'country': anl_count, 'territory': anl_terr, 'locality': anl_loc}
            return templates.TemplateResponse("admins.html", context)
        else:
            redirect_url = '/home'
            response = RedirectResponse(redirect_url)
            return response
    except CancelledError:
        pass


@router.post('/myupdate')
async def myupdate(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    user_token = request.cookies.get("session_id")

    if user_token is None:
        raise HTTPException(status_code=401, detail="Доступ запрещен")

    result = _auth.verify_token(user_token)
    id_account = result.get('id_account')
    name = form_data.get("name")
    surname = form_data.get("surname")
    patronymic = form_data.get("patronymic")
    mail = form_data.get("mail")

    data = {
        "name": name,
        "surname": surname,
        "patronymic": patronymic,
        "mail": mail
    }

    update_user_info(db=db, id_account=id_account, data=data)

    redirect_url = '/myinfo'
    response = RedirectResponse(url=redirect_url, status_code=302)
    response.headers["Location"] = redirect_url

    return response


@router.get('/myinfo')
async def myinfo_user(request: Request, db: Session = Depends(get_db)):
    user_token = request.cookies.get("session_id")

    if user_token is None:
        raise HTTPException(status_code=401, detail="Доступ запрещен")

    result = _auth.verify_token(user_token)
    id_account = result.get('id_account')
    role = result.get('role')
    if role == 'moderator':
        url = '/profile_moder'
    elif role == 'administrator':
        url = '/profile_admin'
    else:
        url = 'profile'
    result_front = get_user_info(db=db, id_account=id_account)
    context = {"request": request, 'info': result_front, 'url': url}
    return templates.TemplateResponse("myinfo.html", context)


@router.post('/addtravelcards')
async def addtravelcards(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    user_token = request.cookies.get("session_id")
    if user_token is None:
        raise HTTPException(status_code=401, detail="Доступ запрещен")
    result = _auth.verify_token(user_token)
    id_account = result.get('id_account')
    name = form_data.get("name")
    categories_id = form_data.get("categories_id")
    country_id = form_data.get("country_id")
    description = form_data.get("description")

    data = {
        "name": name,
        "categories_id": categories_id,
        "country_id": country_id,
        "description": description,
        "id_account": id_account
    }

    return add_new_post(db=db, id_account=id_account, data=data)


@router.post("/statusupdate")
async def statusupdate(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    user_token = request.cookies.get("session_id")
    if user_token is None:
        raise HTTPException(status_code=401, detail="Доступ запрещен")

    result = _auth.verify_token(user_token)

    id_account = result.get('id_account')

    information = form_data.get("status")
    result = update_status_records(db=db, data=information, id_account=id_account)

    return result


@router.post('/{post_id}')
async def post_details(post_id, db: Session = Depends(get_db)):
    return get_postinfo_id(db=db, post_id=post_id)


@router.get('/my_card/{post_id}')
async def my_card(request: Request, post_id, db: Session = Depends(get_db)):
    user_token = request.cookies.get("session_id")
    if user_token is None:
        raise HTTPException(status_code=401, detail="Доступ запрещен")

    result = _auth.verify_token(user_token)
    role = result.get('role')
    result = get_postinfo_id(db=db, post_id=post_id)
    context = {"request": request, 'info_cards': result, 'user_status': role}
    return templates.TemplateResponse("cards_chek.html", context)


@router.get('/travelcards')
async def travelcards(request: Request, db: Session = Depends(get_db)):
    user_token = request.cookies.get("session_id")
    if user_token is None:
        raise HTTPException(status_code=401, detail="Доступ запрещен")

    result = _auth.verify_token(user_token)
    role = result.get('role')
    result_categories = get_categories(db)
    result_location = get_location(db)
    context = {"request": request, "info_cat": result_categories, "info_location": result_location, 'user_status': role}
    return templates.TemplateResponse("cards_add.html", context)

