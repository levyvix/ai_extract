from typing import Any, Dict
from docling_core.types.doc.document import DoclingDocument
from pydantic_ai import Agent
from pydantic import BaseModel, Field
from docling.datamodel.accelerator_options import AcceleratorDevice, AcceleratorOptions
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    TableFormerMode,
)

import pdfplumber

import fitz  # PyMuPDF
from docling.document_converter import DocumentConverter, PdfFormatOption


class Document(BaseModel):
    NomeDeclarante: list[str] = Field(
        ..., description="Nome do declarante do documento"
    )
    CPFDeclarante: str = Field(..., description="CPF do declarante do documento")
    EnderecoCompleto: str = Field(..., description="Endereco do documento")
    CEP: str = Field(..., description="CEP do documento")
    Municipio: str = Field(..., description="Municipio do documento")
    UF: str = Field(..., description="UF do documento")
    TotalRendimentoTributavel: str = Field(
        ..., description="Total de rendimento tributavel do documento"
    )
    ImpostoDevido: str = Field(..., description="Imposto devido do documento")
    NumeroDoRecibo: str = Field(..., description="Numero do recibo do documento")
    DataDoRecibo: str = Field(..., description="Data do recibo do documento")


agent = Agent("groq:llama-3.3-70b-versatile", output_type=Document)


def extract_pdf_text(pdf_path: str) -> str | None:
    """Extract text from a PDF file using docling library with fallback to OCR if needed.

    Args:
        pdf_path: Path to the PDF file

    Raises:
        FileNotFoundError: If the PDF file doesn't exist
        Exception: For other PDF processing errors
    """
    # pipeline_options = PdfPipelineOptions()
    # pipeline_options.do_table_structure = True
    # pipeline_options.table_structure_options.do_cell_matching = False
    # pipeline_options.table_structure_options.mode = TableFormerMode.FAST
    # doc_converter = DocumentConverter(
    #     format_options={
    #         InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    #     }
    # )

    # doc: DoclingDocument = doc_converter.convert(pdf_path).document
    # text: Dict[str, Any] = doc.export_to_markdown()

    # return text

    doc = pdfplumber.open(pdf_path)
    text = []
    for page in doc.pages:
        text.append(page.extract_text())
    return "\n".join(text)


if __name__ == "__main__":
    doc_path: str = "/home/levi/llms/16921508714-IRPF-2025-2024-origi-imagem-recibo.pdf"

    content: str | None = extract_pdf_text(doc_path)
    if content is None:
        raise Exception("Failed to extract text from PDF")
    print(content)
    result = agent.run_sync(
        f"""
        Extraia as informações do documento de IRPF:
        {content}
        """,
    )

    print(result.output)
