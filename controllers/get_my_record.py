from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload
from starlette.responses import RedirectResponse
import re

from models import models as _models


def get_record(db: Session, id_user: int):
    session = db

    record = db.query(_models.PostInfo, _models.Locality.name, _models.Country.name) \
        .join(_models.Locality, _models.PostInfo.country_id == _models.Locality.id_locality) \
        .join(_models.Territory, _models.Locality.territory_id == _models.Territory.id_territory) \
        .join(_models.Country, _models.Territory.country_id == _models.Country.id_country) \
        .options(joinedload(_models.PostInfo.category)).filter(_models.PostInfo.account_id == id_user) \
        .all()

    session.close()

    return record


def get_record_check(db: Session):
    post_infos = db.query(_models.PostInfo, _models.GeneralInformation.name). \
        join(_models.Account, _models.Account.id_account == _models.PostInfo.account_id). \
        join(_models.GeneralInformation, _models.GeneralInformation.account_id == _models.Account.id_account). \
        filter(_models.PostInfo.status == "На проверке"). \
        all()

    return post_infos


def get_postinfo_id(db: Session, post_id: int):
    try:
        query_result = db.query(
            _models.PostInfo,
            _models.Locality.name,
            _models.Country.name,
            _models.Territory.name,
            _models.Categories.category
        ).join(
            _models.Locality, _models.PostInfo.country_id == _models.Locality.id_locality
        ).join(
            _models.Territory, _models.Locality.territory_id == _models.Territory.id_territory
        ).join(
            _models.Country, _models.Territory.country_id == _models.Country.id_country
        ).join(
            _models.Categories, _models.PostInfo.categories_id == _models.Categories.id_categories
        ).options(joinedload(_models.PostInfo.category)).filter(
            _models.PostInfo.id_postinfo == post_id
        ).first()

        if query_result:
            post_info, locality_name, country_name, territory_name, category_name = query_result

            data = {
                "description": post_info.description,
                "name": post_info.name,
                "data": post_info.data,
                "locality_name": locality_name,
                "country_name": country_name,
                "territory_name": territory_name,
                "category_name": category_name,
                "status": post_info.status,
                "id_postinfo": post_info.id_postinfo
            }
            return data
        else:
            return None
    except SQLAlchemyError as e:
        return None


def get_categories(db: Session):
    try:
        query_result = db.query(_models.Categories).all()
        return query_result
    except SQLAlchemyError as e:
        return None


def get_location(db: Session):
    try:
        locations = db.query(_models.Locality).all()
        response_data = [{
            "id_location": location.id_locality,
            "location": location.name,
            "country": location.territory.country.name,
            "territory": location.territory.name
        } for location in locations]
        return response_data
    except SQLAlchemyError as e:
        return None


def add_new_post(db, id_account, data):
    try:
        existing_post = db.query(_models.PostInfo).where(func.lower(_models.PostInfo.name) == func.lower(data['name'])).first()
        if existing_post:
            return {"message": "Имя уже используется"}

        postinfo = _models.PostInfo(
            name=data['name'],
            country_id=data['country_id'],
            categories_id=data['categories_id'],
            description=data['description'],
            account_id=id_account
        )

        db.add(postinfo)
        db.commit()

        redirect_url = '/profile'
        response = RedirectResponse(url=redirect_url, status_code=302)
        response.headers["Location"] = redirect_url

        return response
    except SQLAlchemyError as e:
        return None
