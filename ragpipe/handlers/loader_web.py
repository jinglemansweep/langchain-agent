import logging
from dynaconf import Dynaconf
from langchain_community.document_loaders import WebBaseLoader

# from pydantic import Field
from .utils import MessageBody, validate_payload, clean_text_body
from typing import Optional

logger = logging.getLogger(__name__)


class InputModel(MessageBody):
    pass


def loader_web_handler(
    _payload: MessageBody, settings: Dynaconf
) -> Optional[MessageBody]:
    payload = validate_payload(InputModel, _payload)
    if not payload:
        return None
    logger.info(f"loader.web.handler: payload={payload}")

    try:
        loader = WebBaseLoader(payload.data)
        docs = loader.load()
        body = ""

        for doc in docs:
            fields = doc.model_dump()
            content = clean_text_body(fields["page_content"])
            body += f"{fields["metadata"]["title"]}: {content}\n\n"

        logger.info(f"loader.web.data: docs={len(docs)}")
        return MessageBody(data=body, metadata=payload.metadata)
    except Exception as e:
        logger.error(f"loader.web.handler: error={e}")
        return None
