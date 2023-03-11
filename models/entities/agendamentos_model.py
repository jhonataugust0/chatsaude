from sqlalchemy.orm import relationship, selectinload, sessionmaker
from sqlalchemy import Column,  Date, Time,  ForeignKey, Integer,  BigInteger, Text, VARCHAR 
from .unidade_model import Unidade
from ..configs.base import Base


class Agendamentos(Base):
    __tablename__ = "agendamentos"
    id = Column(Integer, primary_key=True)
    id_usuario = Column(ForeignKey("usuario.id"))
    id_unidade = Column(ForeignKey("unidade.id"))
    id_especialidade = Column(ForeignKey("especialidade.id"))
    tipo_agendamento = Column(VARCHAR(150))
    data_agendamento = Column(Date)
    horario_inicio_agendamento = Column(Time)
    horario_termino_agendamento  = Column(Time)
    descricao_necessidade = Column(Text)
    ativo = Column(Integer)
    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
      return {'id': int(self.id), 'id_usuario': int(self.id_usuario), 'id_unidade': int(self.id_unidade), 'id_especialidade': int(self.id_especialidade), 'tipo_agendamento': str(self.tipo_agendamento), 'data_agendamento': str(self.data_agendamento), 'horario_inicio_agendamento': str(self.horario_inicio_agendamento), 'horario_termino_agendamento': str(self.horario_termino_agendamento), 'descricao_necessidade': str(self.descricao_necessidade), 'ativo': int(self.ativo)}

    def __str__(self):
      return f"""id = {self.id}, id_usuario = {self.id_usuario}, id_unidade = {self.id_unidade}, id_especialidade = {self.id_especialidade}, tipo_agendamento = {self.tipo_agendamento}, data_agendamento = {self.data_agendamento}, horario_inicio_agendamento = {self.horario_inicio_agendamento}, horario_termino_agendamento = {self.horario_termino_agendamento}, descricao_necessidade = {self.descricao_necessidade}, ativo= {self.ativo}"""


        