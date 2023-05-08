from typing import Any, Dict

from sqlalchemy import VARCHAR, Column, ForeignKey, Integer

from ..configs.base import Base


class Especialidade(Base):
    __tablename__ = "especialidade"

    id = Column(Integer, primary_key=True)
    nome = Column(VARCHAR(50))
    ativo = Column(Integer)
    id_unidade = Column(ForeignKey("unidade.id"))

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        data = {
            "id": int(self.id),
            "nome": str(self.nome),
            "ativo": int(self.ativo),
            "id_unidade": int(self.id_unidade),
        }
        return data

    def __str__(self):
        return f"""id = {int(self.id)}, nome = {str(self.nome)}, ativo = {int(self.ativo)}, id_unidade = {int(self.id_unidade)}"""

    @classmethod
    def as_dict(cls, row) -> Dict[str, Any]:
        return {c.name: getattr(row, c.name) for c in row.__table__.columns}
