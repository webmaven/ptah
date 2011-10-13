import ptah
import sqlalchemy as sqla
import pyramid_sqla as psa

Base = psa.get_base()
Session = psa.get_session()


class CrowdProvider(object):

    def authenticate(self, creds):
        login, password = creds['login'], creds['password']

        user = CrowdUser.get_bylogin(login)

        if user is not None:
            if ptah.passwordTool.checkPassword(user.password, password):
                return user

    def get_principal_bylogin(self, login):
        return CrowdUser.get_bylogin(login)


URI_gen = ptah.UriGenerator('user+crowd')


class CrowdUser(Base):

    __tablename__ = 'ptah_crowd'

    pid = sqla.Column(sqla.Integer, primary_key=True)
    uri = sqla.Column(sqla.Unicode(45), unique=True)
    name = sqla.Column(sqla.Unicode(255))
    login = sqla.Column(sqla.Unicode(255), unique=True)
    email = sqla.Column(sqla.Unicode(255), unique=True)
    password = sqla.Column(sqla.Unicode(255))

    def __init__(self, name, login, email, password=u''):
        super(Base, self).__init__()

        self.name = name
        self.uri = URI_gen()
        self.login = login
        self.email = email
        self.password = password

    _sql_get = ptah.QueryFreezer(
        lambda: Session.query(CrowdUser)\
           .filter(CrowdUser.pid==sqla.sql.bindparam('pid')))

    _sql_get_uri = ptah.QueryFreezer(
        lambda: Session.query(CrowdUser)\
           .filter(CrowdUser.uri==sqla.sql.bindparam('uri')))

    _sql_get_login = ptah.QueryFreezer(
        lambda: Session.query(CrowdUser)\
           .filter(CrowdUser.login==sqla.sql.bindparam('login')))

    @classmethod
    def get(cls, id):
        return cls._sql_get.first(pid=id)

    @classmethod
    def get_byuri(cls, uri):
        return cls._sql_get_uri.first(uri=uri)

    @classmethod
    def get_bylogin(cls, login):
        return cls._sql_get_login.first(login=login)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '%s <%s>'%(self.name, self.uri)


_sql_search = ptah.QueryFreezer(
    lambda: Session.query(CrowdUser) \
    .filter(
        sqla.sql.or_(CrowdUser.email.contains(sqla.sql.bindparam('term')),
                     CrowdUser.name.contains(sqla.sql.bindparam('term'))))\
    .order_by(sqla.sql.asc('name')))

def search(term):
    for user in _sql_search.all(term = '%%%s%%'%term):
        yield user


def change_pwd(principal, password):
    principal.password = password


ptah.register_principal_searcher('user+crowd', search)
ptah.register_auth_provider('user+crowd', CrowdProvider())
ptah.passwordTool.registerPasswordChanger('user+crowd', change_pwd)
ptah.registerResolver('user+crowd', CrowdUser.get_byuri,
                      'Crowd principal resolver')
