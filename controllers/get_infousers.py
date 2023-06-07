from fastapi import HTTPException
from sqlalchemy import cast, Numeric, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload
from starlette.responses import RedirectResponse
import re
from models import models as _models


def get_user_info(db: Session, id_account):
    session = db
    general_info = session.query(_models.GeneralInformation).filter_by(account_id=id_account).first()
    result = {}
    if general_info is None:
        result["surname"] = "Введите фамилию"
        result["name"] = "Введите имя"
        result["patronymic"] = "Введите отчество"
        result["mail"] = "Введите почту"
    else:
        if general_info.surname is None:
            result["surname"] = "Введите фамилию"
        else:
            result["surname"] = general_info.surname

        if general_info.name is None:
            result["name"] = "Введите имя"
        else:
            result["name"] = general_info.name

        if general_info.patronymic is None:
            result["patronymic"] = "Введите отчество"
        else:
            result["patronymic"] = general_info.patronymic

        if general_info.mail is None:
            result["mail"] = "Введите почту"
        else:
            result["mail"] = general_info.mail

    session.close()
    return result


def update_user_info(db, id_account, data):
    general_info = db.query(_models.GeneralInformation).filter_by(account_id=id_account).first()
    if general_info is None:
        raise HTTPException(status_code=404, detail="Информация о пользователе не найдена")
    if 'surname' in data:
        general_info.surname = data['surname']
    if 'name' in data:
        general_info.name = data['name']
    if 'patronymic' in data:
        general_info.patronymic = data['patronymic']
    if 'mail' in data:
        general_info.mail = data['mail']

    db.commit()

    return {"message": "Информация о пользователе успешно обновлена"}


def update_status_records(db, data, id_account):
    try:
        match = re.search(r"(Одобренно|Отклоненно) (\d+)", data)
        new_status = match.group(1)
        postinfo_id = int(match.group(2))
        postinfo = db.query(_models.PostInfo).filter_by(id_postinfo=postinfo_id).first()
        postinfo.status = new_status

        geninfo_id = db.query(_models.GeneralInformation.id_general_information).filter_by(account_id=id_account).first()

        db_post_processing = _models.PostProcessing(
            post_id=postinfo_id,
            geninfo_id=geninfo_id[0],
        )
        db.add(db_post_processing)
        db.commit()
        db.refresh(db_post_processing)

        redirect_url = '/profile_moder'
        response = RedirectResponse(url=redirect_url, status_code=302)
        response.headers["Location"] = redirect_url

        return response
    except SQLAlchemyError as e:
        return None


def get_all_user_info(db):
    try:
        query = db.query(
            _models.GeneralInformation.name,
            _models.GeneralInformation.surname,
            _models.GeneralInformation.patronymic,
            _models.GeneralInformation.mail,
            _models.Account.login,
            _models.Account.post
        ).join(_models.Account, _models.GeneralInformation.account_id == _models.Account.id_account).all()

        users_info = [
            {
                "name": user[0],
                "surname": user[1],
                "patronymic": user[2],
                "mail": user[3],
                "login": user[4],
                "post": user[5]
            }
            for user in query
        ]
        return users_info
    except SQLAlchemyError as e:
        return None


def get_moderators_work_info(db):
    try:
        query = db.query(
            _models.GeneralInformation.name,
            _models.GeneralInformation.surname,
            _models.Account.login,
            _models.ModeratorsWork.number_of_warnings,
            _models.ModeratorsWork.number_of_processed_posts
        ).join(_models.Account, _models.GeneralInformation.account_id == _models.Account.id_account).join(
            _models.ModeratorsWork, _models.GeneralInformation.id_general_information == _models.ModeratorsWork.geninfo_id
        ).all()

        moderators_info = [
            {
                'name': user[0],
                'surname': user[1],
                'login': user[2],
                'number_of_warnings': user[3],
                'number_of_processed_posts': user[4]
            }
            for user in query
        ]

        return moderators_info
    except SQLAlchemyError as e:
        return None


def get_employee(db: Session):
    try:
        query = db.query(_models.EmployeeInfo.work_experience,
                         _models.EmployeeInfo.start_date,
                         cast(_models.EmployeeInfo.salary, Numeric),
                         _models.GeneralInformation.surname,
                         _models.GeneralInformation.name,
                         _models.GeneralInformation.mail,
                         _models.JobTitle.name_job
                         ).join(_models.GeneralInformation).join(_models.JobTitle).all()

        employee_info = [
            {
                'start_date': int(user[0]),
                'work_experience': str(user[1]),
                'salary': float(user[2]),
                'surname': user[3],
                'name': user[4],
                'mail': user[5],
                'name_job': user[6],
            }
            for user in query
        ]

        return employee_info
    except SQLAlchemyError as e:
        return None
