import base64
from typing import Any, Union

import requests

from core.tools.entities.tool_entities import ToolInvokeMessage
from core.tools.tool.builtin_tool import BuiltinTool


class URLToBase64Tool(BuiltinTool):
    def _invoke(
        self,
        user_id: str,
        tool_parameters: dict[str, Any],
    ) -> Union[ToolInvokeMessage, list[ToolInvokeMessage]]:
        """
        Конвертирует файл из URL в base64 строку
        """
        url = tool_parameters.get("url", "")
        if not url:
            return self.create_text_message("Пожалуйста, укажите URL")

        try:
            # Загружаем файл по URL
            response = requests.get(url)
            response.raise_for_status()  # Проверяем на ошибки

            # Конвертируем содержимое в base64
            base64_content = base64.b64encode(response.content).decode("utf-8")

            # Возвращаем результат
            return self.create_text_message(base64_content)

        except Exception as e:
            return self.create_text_message(f"Ошибка при обработке файла: {str(e)}")

    def get_runtime_parameters(self) -> list[dict]:
        """
        Определяем параметры инструмента
        """
        return [
            {
                "name": "url",
                "type": "string",
                "required": True,
                "label": "URL файла",
                "description": "URL файла, который нужно конвертировать в base64",
            }
        ]
