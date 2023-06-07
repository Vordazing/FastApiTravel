import bcrypt
import passlib.hash as _hash
from sqlalchemy import Column, ForeignKey, Integer, Text, Date, Numeric, String
from sqlalchemy.orm import relationship
import datetime


from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Achievement(Base):
    __tablename__ = "achievement"
    id_achievement = Column(Integer, primary_key=True)
    achievement = Column(Text)
    condition = Column(Integer)


class Categories(Base):
    __tablename__ = "categories"
    id_categories = Column(Integer, primary_key=True)
    category = Column(Text)
    postinfo = relationship("PostInfo", back_populates="category")


class Country(Base):
    __tablename__ = "country"
    id_country = Column(Integer, primary_key=True)
    name = Column(Text)
    territories = relationship("Territory", back_populates="country")


class Territory(Base):
    __tablename__ = "territory"
    id_territory = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey("country.id_country"))
    name = Column(Text)

    country = relationship("Country", back_populates="territories")
    localities = relationship("Locality", back_populates="territory")


class Locality(Base):
    __tablename__ = "locality"
    id_locality = Column(Integer, primary_key=True)
    name = Column(Text)
    territory_id = Column(Integer, ForeignKey("territory.id_territory"))
    territory = relationship("Territory", back_populates="localities")


class GeneralInformation(Base):
    __tablename__ = "general_information"
    id_general_information = Column(Integer, primary_key=True)
    surname = Column(Text, nullable=False)
    name = Column(Text, nullable=False)
    patronymic = Column(Text, nullable=False)
    mail = Column(Text, nullable=False)
    rating = Column(Numeric(10, 2), default=0.00, nullable=False)
    account_id = Column(Integer, ForeignKey("account.id_account"))


class EmployeeInfo(Base):
    __tablename__ = "employee_info"
    id_infoemp = Column(Integer, primary_key=True)
    geninfo_id = Column(Integer, ForeignKey("general_information.id_general_information"))
    start_date = Column(Date)
    work_experience = Column(Numeric)
    salary = Column(Numeric)
    job_id = Column(Integer, ForeignKey("job_title.id_job"))


class JobTitle(Base):
    __tablename__ = "job_title"
    id_job = Column(Integer, primary_key=True)
    name_job = Column(String)


class Report(Base):
    __tablename__ = "report"
    id_report = Column(Integer, primary_key=True)
    admin_id = Column(Integer, ForeignKey("general_information.id_general_information"))
    moder_id = Column(Integer, ForeignKey("general_information.id_general_information"))
    reason = Column(Text)


class ModeratorsWork(Base):
    __tablename__ = "moderators_work"
    id_modwork = Column(Integer, primary_key=True)
    geninfo_id = Column(Integer, ForeignKey("general_information.id_general_information"), unique=True)
    number_of_warnings = Column(Integer)
    number_of_processed_posts = Column(Integer)


class AdminsWork(Base):
    __tablename__ = "admins_work"
    id_admin = Column(Integer, primary_key=True)
    geninfo_id = Column(Integer, ForeignKey("general_information.id_general_information"), unique=True)
    number_of_moderators_processed = Column(Integer)


class Account(Base):
    __tablename__ = "account"
    id_account = Column(Integer, primary_key=True)
    login = Column(String, unique=True)
    hashed_password = Column(String)
    status = Column(Text, default="work")
    post = Column(Text, default="member")

    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.hash_password)


class UserInfo(Base):
    __tablename__ = "user_info"
    id_userinfo = Column(Integer, primary_key=True)
    post_count = Column(Integer)
    account_id = Column(Integer, ForeignKey("account.id_account"))
    achievement_id = Column(Integer, ForeignKey("achievement.id_achievement"))


class PostInfo(Base):
    __tablename__ = "postinfo"
    id_postinfo = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey("locality.id_locality"))
    data = Column(Date, default=datetime.datetime.utcnow)
    description = Column(Text)
    name = Column(Text)
    categories_id = Column(Integer, ForeignKey("categories.id_categories"))
    status = Column(Text, default="На проверке")
    account_id = Column(Integer, ForeignKey("account.id_account"))

    category = relationship("Categories", foreign_keys=[categories_id], back_populates="postinfo",
                            overlaps="category_name")
    image = Column(String)


class Rating(Base):
    __tablename__ = "rating"
    id_rating = Column(Integer, primary_key=True)
    record_id = Column(Integer, ForeignKey("postinfo.id_postinfo"), nullable=False)
    account_id = Column(Integer, ForeignKey("account.id_account"), nullable=False)
    estimation = Column(Text)
    comments = Column(Text)


class PostProcessing(Base):
    __tablename__ = "post_processing"
    id_postpr = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("postinfo.id_postinfo"), nullable=False)
    geninfo_id = Column(Integer, ForeignKey("general_information.id_general_information"))
    comment = Column(Text)
    general_information = relationship("GeneralInformation", backref="post_processing")


