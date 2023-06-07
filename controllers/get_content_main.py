from sqlalchemy.orm import Session, joinedload, query
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from models.models import PostInfo, Locality, Territory, Country, Categories
from models import models as _models


def get_postinfo(db: Session):
    try:
        my_query = db.query(
            PostInfo.id_postinfo,
            PostInfo.image,
            PostInfo.name,
            Locality.name,
            Country.name,
            Categories.category
        ) \
        .join(Locality, PostInfo.country_id == Locality.id_locality) \
        .join(Territory, Locality.territory_id == Territory.id_territory) \
        .join(Country, Territory.country_id == Country.id_country) \
        .join(Categories, PostInfo.categories_id == Categories.id_categories).filter(_models.PostInfo.status == 'Одобренно') \
        .all()

        return my_query
    except SQLAlchemyError as e:
        print(e)
        return None




def get_users(db: Session):
    return db.query(_models.Account).all()


def get_users_member(db: Session):
    return db.query(_models.Account).filter(_models.Account.post == "member").all()


def get_users_by_username(db: Session, username: str):
    return (
        db.query(_models.Account).filter(_models.Account.login == username).first()
    )


def get_profile_user(db: Session, id_user: int):
    session = db
    res = session.query(_models.Account.login) \
        .filter(_models.Account.id_account == id_user) \
        .first()

    res_achievement = (
        session.query(_models.Achievement)
        .join(_models.UserInfo)
        .filter(_models.UserInfo.account_id == id_user)
        .first()
    )

    if res_achievement:
        achievement_id = res_achievement.achievement
    else:
        achievement_id = 'у вас нету уровня'

    res_user = (
        session.query(_models.GeneralInformation)
        .filter(_models.GeneralInformation.account_id == id_user)
        .first()
    )
    session.close()

    account_info = {
        "login": res.login,
        "level": achievement_id,
        "name": res_user.name,
        'rating': res_user.rating
    }
    return account_info


