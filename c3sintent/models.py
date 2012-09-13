import transaction

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Unicode

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True)
    value = Column(Integer)

    def __init__(self, name, value):  # pragma: no coverage: not using this atm
        self.name = name
        self.value = value


def populate():  # pragma: no coverage: not using this atm
#    session = DBSession()
#    model = MyModel(name=u'root', value=55)
#    try:
#        session.add(model)
#    except InvalidRequestError, e:
#    except OperationalError, ope:
#        pass
#    session.flush()
#    transaction.commit()
    pass


def initialize_sql(engine):
    pass
#    DBSession.configure(bind=engine)
#    Base.metadata.bind = engine
#    Base.metadata.create_all(engine)
#    try:
#        populate()
#    except IntegrityError:  # pragma: no cover
#        transaction.abort()
#        # if data is already present in database the transaction is aborted
