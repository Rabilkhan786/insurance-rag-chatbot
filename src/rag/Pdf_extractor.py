import os
import re
from typing import List

import camelot
from pypdf import PdfReader
from langchain_core.documents import Document



class PDFExtractor:
    """
    Extracts text and tables from PDFs and returns
    structured LangChain Document objects.
    """

    # TEXT EXTRACTION :
    def extract_text(self, pdf_folder_path: str) -> List[Document]:
        documents = []

        for file_name in os.listdir(pdf_folder_path):
            if not file_name.lower().endswith(".pdf"):
                continue

            file_path = os.path.join(pdf_folder_path, file_name)

            try:
                reader = PdfReader(file_path)
            except Exception as e:
                print(f"[PDF READ ERROR] {file_name}: {e}")
                continue

            for page_num, page in enumerate(reader.pages, start=1):
                try:
                    text = page.extract_text()
                except Exception:
                    text = None

                if text and text.strip():
                    documents.append(
                        Document(
                            page_content=text.strip(),
                            metadata={
                                "source": file_name,
                                "page": page_num,
                                "type": "text"
                            }
                        )
                    )

        return documents

    #  TABLE Text EXTRACTION :
    def extract_tables(self, pdf_folder_path: str) -> List[Document]:
        documents = []

        for file_name in os.listdir(pdf_folder_path):
            if not file_name.lower().endswith(".pdf"):
                continue

            file_path = os.path.join(pdf_folder_path, file_name)

            try:
                tables = camelot.read_pdf(
                    file_path,
                    pages="all",
                    flavor="lattice"   # best for bordered tables
                )
            except Exception as e:
                print(f"[CAMELOT ERROR] {file_name}: {e}")
                continue

            for idx, table in enumerate(tables):
                raw_text = table.df.to_string(index=False)
                cleaned_text = self.clean_table_text(raw_text)
                sentences = self.table_to_sentences(cleaned_text)

                if not sentences:
                    continue

                # Split table sentences into smaller chunks (better for RAG)
                for sentence in sentences.split("\n"):
                    documents.append(
                        Document(
                            page_content=sentence,
                            metadata={
                                "source": file_name,
                                "page": table.page,
                                "table_index": idx,
                                "type": "table"
                            }
                        )
                    )

        return documents

    # CLEAN TABLE TEXT :
    def clean_table_text(self, text: str) -> str:
        lines = []

        for line in text.splitlines():
            line = line.strip()
            if line and not line.isdigit():
                lines.append(line)

        return "\n".join(lines)

    # CONVERT TABLE TO SENTENCES :
    def table_to_sentences(self, table_text: str) -> str:
        sentences = []
        buffer = ""

        for line in table_text.splitlines():
            line = re.sub(r"\s{2,}", " ", line)

            buffer = f"{buffer} {line}".strip() if buffer else line

            if line.endswith(".") and len(buffer.split()) > 6:
                sentences.append(buffer)
                buffer = ""

        if buffer and len(buffer.split()) > 6:
            sentences.append(buffer)

        return "\n".join(sentences)

    # EXTRACT EVERYTHING :
    def extract_all(self, pdf_folder_path: str) -> List[Document]:
        return (
            self.extract_text(pdf_folder_path)
            + self.extract_tables(pdf_folder_path)
        )
