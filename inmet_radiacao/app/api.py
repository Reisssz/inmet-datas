from fastapi import APIRouter
from core.process_files import save_file

router = APIRouter()

@router.post("/coletar")
def coletar_dados():
    """
    Dispara a coleta e processamento dos dados do INMET.
    """
    try:
        save_file()
        return {"status": "sucesso", "mensagem": "Coleta e processamento concluídos."}
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}
