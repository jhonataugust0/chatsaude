from typing import Any, Dict

from sqlalchemy import (VARCHAR, BigInteger, Column, Date, ForeignKey, Integer,
                        Text, Time)
from src.models.configs.base import Base
from src.services.health_unit.models.entity.unidade_model import Unidade


class AgendamentoExame(Base):
    __tablename__ = "agendamento_exame"

    id = Column(Integer, primary_key=True)
    id_usuario = Column(ForeignKey("usuario.id"))
    id_unidade = Column(ForeignKey("unidade.id"))
    id_especialidade = Column(ForeignKey("especialidade.id"))
    data_agendamento = Column(Date)
    data_criado = Column(Date)
    horario_inicio_agendamento = Column(Time)
    horario_termino_agendamento = Column(Time)
    descricao_necessidade = Column(Text)
    ativo = Column(Integer)

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        data = {
            "id": int(self.id),
            "id_usuario": int(self.id_usuario),
            "id_unidade": int(self.id_unidade),
            "id_especialidade": int(self.id_especialidade),
            "data_agendamento": str(self.data_agendamento),
            "horario_inicio_agendamento": str(self.horario_inicio_agendamento),
            "horario_termino_agendamento": str(self.horario_termino_agendamento),
            "descricao_necessidade": str(self.descricao_necessidade),
            "ativo": int(self.ativo),
        }
        return data

    def __str__(self):
        return f"""id = {self.id}, id_usuario = {self.id_usuario}, id_unidade = {self.id_unidade}, id_especialidade = {self.id_especialidade}, data_agendamento = {self.data_agendamento}, horario_inicio_agendamento = {self.horario_inicio_agendamento}, horario_termino_agendamento = {self.horario_termino_agendamento}, descricao_necessidade = {self.descricao_necessidade}, ativo= {self.ativo}"""

    @classmethod
    def as_dict(cls, row) -> Dict[str, Any]:
        return {c.name: getattr(row, c.name) for c in row.__table__.columns}
