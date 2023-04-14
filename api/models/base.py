# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.ext.asyncio import create_async_engine
# from sqlalchemy.orm import sessionmaker, declarative_base
# from sqlalchemy import Column,  Date, Time,  ForeignKey,  func,  Integer,  String, BigInteger, VARCHAR, Text 
# import yaml

# with open('env.yaml', 'r') as file:
#   db_config = yaml.safe_load(file)


# engine = create_async_engine(db_config['CONNECTION_URL'], echo=True)
# Base = declarative_base()

# async_session = sessionmaker(
#   engine, class_=AsyncSession, expire_on_commit=False
# )

# async def init_models():
#   async with engine.begin() as conn:
#       await conn.run_sync(Base.metadata.drop_all)
#       await conn.run_sync(Base.metadata.create_all)


# async def get_session() -> AsyncSession:
#   async with async_session() as session:
#     yield session

# class Especialidade(Base):
#   __tablename__ = "especialidade"
#   id = Column(Integer, primary_key=True)
#   nome = Column(VARCHAR(50))

#   __mapper_args__ = {"eager_defaults": True}  

# class FluxoEtapa(Base):
#   __tablename__ = "fluxo_etapa"
#   id = Column(Integer, primary_key=True)
#   id_usuario = Column(ForeignKey("usuario.id"))
#   fluxo_registro = Column(Integer)
#   fluxo_agendamento_consulta = Column(Integer)
#   fluxo_agendamento_exame = Column(Integer)
#   lista_unidades = Column(Integer)
  
#   __mapper_args__ = {"eager_defaults": True}

# class Unidade(Base):
#   __tablename__ = "unidade"
#   id = Column(Integer, primary_key=True)
#   nome = Column(VARCHAR(150))
#   endereco = Column(Text)
#   bairro = Column(VARCHAR(100))
#   cidade = Column(VARCHAR(80))
#   estado = Column(VARCHAR(80))
#   horario_funcionamento = Column(VARCHAR(20))
#   contato = Column(BigInteger)
#   cep = Column(BigInteger)
#   __mapper_args__ = {"eager_defaults": True}


# class Usuario(Base):
#   __tablename__ = "usuario"

#   id = Column(Integer, primary_key=True)
#   nome = Column(VARCHAR(100))
#   telefone = Column(BigInteger)
#   email = Column(VARCHAR(100))
#   data_nascimento = Column(Date)
#   cep = Column(BigInteger)
#   cpf = Column(BigInteger)
#   rg = Column(BigInteger)
#   c_sus =Column(BigInteger)  

# class Agendamentos(Base):
#   __tablename__ = "consulta_agendameno"
#   id = Column(Integer, primary_key=True)
#   id_usuario = Column(ForeignKey("usuario.id"))
#   id_unidade = Column(ForeignKey("unidade.id"))
#   id_especialidade = Column(ForeignKey("especialidade.id"))
#   data_agendamento = Column(Date)
#   horario_inicio_agendamento = Column(Time)
#   horario_termino_agendamento  = Column(Time)
#   descricao_necessidade = Column(Text)

#   __mapper_args__ = {"eager_defaults": True}
  
