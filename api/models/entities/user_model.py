from sqlalchemy import Column,  Date, Integer,  BigInteger, VARCHAR 
from ..configs.base import Base
from typing import Dict, Any

from typing import Any, Dict

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
       return f"""id={self.id}, nome={self.nome}, telefone={self.telefone}, email={self.email}, data_nascimento={self.data_nascimento}, cep={self.cep}, bairro={self.bairro}, cpf={self.cpf}, rg={self.rg}, c_sus={self.c_sus}"""
      # return {'id': self.id, 'nome': self.nome, 'telefone': self.telefone, 'email': self.email, 'data_nascimento': self.data_nascimento, 'cep': self.cep, 'bairro': self.bairro, 'cpf':self.cpf, 'rg': self.rg, 'c_sus': self.c_sus}
      
    def __str__(self):
      return f"""id={self.id}, nome={self.nome}, telefone={self.telefone}, email={self.email}, data_nascimento={self.data_nascimento}, cep={self.cep}, bairro={self.bairro}, cpf={self.cpf}, rg={self.rg}, c_sus={self.c_sus}"""

    @classmethod
    def as_dict(cls, row) -> Dict[str, Any]:
        return {c.name: getattr(row, c.name) for c in row.__table__.columns}

    