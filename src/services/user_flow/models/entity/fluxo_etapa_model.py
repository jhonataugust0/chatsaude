from typing import Any, Dict

from sqlalchemy import Column, ForeignKey, Integer

from models.configs.base import Base


class FluxoEtapa(Base):
    __tablename__ = "fluxo_etapa"
    id = Column(Integer, primary_key=True)
    id_usuario = Column(ForeignKey("usuario.id"))

    fluxo_registro = Column(Integer)
    etapa_registro = Column(Integer)

    fluxo_agendamento_consulta = Column(Integer)
    etapa_agendamento_consulta = Column(Integer)

    fluxo_agendamento_exame = Column(Integer)
    etapa_agendamento_exame = Column(Integer)

    lista_unidades = Column(Integer)

    fluxo_denuncia = Column(Integer)

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        data = {
            "id": int(self.id),
            "id_usuario": int(self.id_usuario),
            "fluxo_registro": int(self.fluxo_registro),
            "etapa_registro": int(self.etapa_registro),
            "fluxo_agendamento_consulta": int(self.fluxo_agendamento_consulta),
            "etapa_agendamento_consulta": int(self.etapa_agendamento_consulta),
            "fluxo_agendamento_exame": int(self.fluxo_agendamento_exame),
            "etapa_agendamento_exame": int(self.etapa_agendamento_exame),
            "lista_unidades": int(self.lista_unidades),
            "fluxo_denuncia": int(self.fluxo_denuncia),
        }
        return data

    def __str__(self):
        return f"""id = {int(self.id)}, id_usuario= {int(self.id_usuario)}, fluxo_registro= {int(self.fluxo_registro)}, etapa_registro= {int(self.etapa_registro)}, fluxo_agendamento_consulta= {int(self.fluxo_agendamento_consulta)}, etapa_agendamento_consulta= {int(self.etapa_agendamento_consulta)}, fluxo_agendamento_exame= {int(self.fluxo_agendamento_exame)}, etapa_agendamento_exame={int(self.etapa_agendamento_exame)}, lista_unidades= {int(self.lista_unidades)}, fluxo_denuncia= {int(self.fluxo_denuncia)}"""

    @classmethod
    def as_dict(cls, row) -> Dict[str, Any]:
        return {c.name: getattr(row, c.name) for c in row.__table__.columns}
