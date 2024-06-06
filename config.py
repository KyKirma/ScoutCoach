SECRET_KEY = 'segredo'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql',
        usuario = 'root',
        senha = '',
        servidor = 'localhost',
        database = 'iadatabase'
    )