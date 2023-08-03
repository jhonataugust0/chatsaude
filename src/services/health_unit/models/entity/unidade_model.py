from sqlalchemy import VARCHAR, BigInteger, Column, ForeignKey, Integer, Text

from src.models.configs.base import Base


class Unidade(Base):
    __tablename__ = "unidade"
    id = Column(Integer, primary_key=True)
    nome = Column(VARCHAR(150))
    endereco = Column(Text)
    bairro = Column(VARCHAR(100))
    cidade = Column(VARCHAR(80))
    estado = Column(VARCHAR(80))
    horario_funcionamento = Column(VARCHAR(20))
    contato = Column(BigInteger)
    cep = Column(BigInteger)

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        data = {
            "id": int(self.id),
            "nome": str(self.nome),
            "endereco": str(self.endereco),
            "bairro": str(self.bairro),
            "cidade": str(self.cidade),
            "estado": str(self.estado),
            "horario_funcionamento": str(self.horario_funcionamento),
            "contato": str(self.contato),
            "cep": int(self.cep),
        }
        return data

    def __str__(self):
        return f"""id = {int(self.id)}, nome = {str(self.nome)}, endereco = {str(self.endereco)}, bairro = {str(self.bairro)}, cidade = {str(self.cidade)}, estado = {str(self.estado)}, horario_funcionamento = {str(self.horario_funcionamento)}, contato = {str(self.contato)}, cep = {int(self.cep)}"""

    @classmethod
    def as_dict(cls, row):
        return {c.name: getattr(row, c.name) for c in row.__table__.columns}
