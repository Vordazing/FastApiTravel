from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload
from starlette.responses import RedirectResponse
import re
from models import models as _models


def get_Country(db):
    try:
        query = db.query(_models.Country, func.count(_models.PostInfo.id_postinfo)). \
            join(_models.Territory, _models.Country.id_country == _models.Territory.country_id). \
            join(_models.Locality, _models.Territory.id_territory == _models.Locality.territory_id). \
            join(_models.PostInfo, _models.Locality.id_locality == _models.PostInfo.country_id). \
            group_by(_models.Country). \
            order_by(func.count(_models.PostInfo.id_postinfo).desc())

        results = query.all()
        json_results = []
        for result in results:
            country, count = result
            json_results.append({
                'country_name': country.name,
                'count': count
            })

        return json_results
    except SQLAlchemyError as e:
        return None


def get_Territory(db):
    try:
        query = db.query(_models.Territory, func.count(_models.PostInfo.id_postinfo)). \
            join(_models.Locality, _models.Territory.id_territory == _models.Locality.territory_id). \
            join(_models.PostInfo, _models.Locality.id_locality == _models.PostInfo.country_id). \
            group_by(_models.Territory). \
            order_by(func.count(_models.PostInfo.id_postinfo).desc())

        results = query.all()
        json_results = []
        for result in results:
            territory, count = result
            json_results.append({
                'territory_name': territory.name,
                'count': count
            })

        return json_results
    except SQLAlchemyError as e:
        return None


def get_Locality(db):
    try:
        query = db.query(_models.Locality, func.count(_models.PostInfo.id_postinfo)). \
            join(_models.PostInfo, _models.Locality.id_locality == _models.PostInfo.country_id). \
            group_by(_models.Locality). \
            having(func.count(_models.PostInfo.id_postinfo) > 0)

        results = query.all()
        json_results = []
        for result in results:
            locality, count = result
            json_results.append({
                'locality_name': locality.name,
                'count': count
            })

        return json_results
    except SQLAlchemyError as e:
        return None
