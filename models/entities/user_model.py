from sqlalchemy import Column,  Date, Integer,  BigInteger, VARCHAR 
from ..configs.base import Base


class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True)
    nome = Column(VARCHAR(100))
    telefone = Column(BigInteger)
    email = Column(VARCHAR(100))
    data_nascimento = Column(Date)
    cep = Column(BigInteger)
    bairro = Column(VARCHAR(80))
    cpf = Column(BigInteger)
    rg = Column(BigInteger)
    c_sus =Column(BigInteger)

    # __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
      return {'id': self.id, 'nome': self.nome, 'telefone': self.telefone, 'email': self.email, 'data_nascimento': self.data_nascimento, 'cep': self.cep, 'bairro': self.bairro, 'cpf':self.cpf, 'rg': self.rg, 'c_sus': self.c_sus}

    def __str__(self):
      return f"""id={self.id}, nome={self.nome}, telefone={self.telefone}, email={self.email}, data_nascimento={self.data_nascimento}, cep={self.cep}, bairro={self.bairro}, cpf={self.cpf}, rg={self.rg}, c_sus={self.c_sus}"""



#     async def connect_db(self):
#         try:
#             engine = create_async_engine(db_config['CONNECTION_URL'],echo=True)
#             Session = sessionmaker(bind=engine)
#             session = Session()
            
#         except Exception as error:
#             message = 'Erro ao conectar no banco de dados'
#             # log = Logging(message)
#             # log.warning('connect_db', None, str(error), 500, {'params': None})
#             raise HTTPException(status_code=500, detail=str(error))
        
#         return session

#     async def get_user_data(self, cellphone: int = None):
#         session = await self.connect_db()
#         # users = session.query(Usuario.nome).all
#         users = await session.get(Usuario, 'Jhonata')
#         # Logging(f'users: {users}').info()
#         print(f'users: {users}')
#         return users 


# asyncio.run(Usuario().get_user_data())

