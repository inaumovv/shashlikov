import json
from collections import defaultdict

import aiofiles
from openai import AsyncOpenAI

from src.products import products


class OpenAIWorker:
    products: list[dict] = products

    def __init__(self, model: str, history_file: str, api_key: str, organization: str, project: str):
        self.model = model
        self.history_file = history_file
        self.api_key = api_key
        self.organization = organization
        self.project = project

    async def get_client(self):
        return AsyncOpenAI(
            api_key=self.api_key,
            organization=self.organization,
            project=self.project
        )

    async def load_histories(self):
        try:
            async with aiofiles.open(self.history_file, 'r', encoding='UTF-8') as file:
                content = await file.read()
                return json.loads(content)
        except FileNotFoundError:
            return defaultdict(list)

    async def save_histories(self, histories):
        async with aiofiles.open(self.history_file, 'w', encoding='UTF-8') as file:
            await file.write(json.dumps(histories, ensure_ascii=False, indent=4))

    async def get_product_info(self, query: str, user: int, prompt: str):
        client = await self.get_client()
        user_histories: dict = await self.load_histories()

        # Получение истории сообщений пользователя
        messages = user_histories.get(str(user), [])

        # Если история пуста, добавляем системное сообщение
        if len(messages) == 0:
            messages.append(
                {
                    "role": "system",
                    "content": prompt

                }
            )

        # Добавляем информацию о товарах в сообщения, если это первое сообщение
            for product in self.products:
                product_info = (
                    f"Name: {product['name']}\n"
                    f"Price: {product['price']}\n"
                    f"Category: {product['category']}\n"
                    f"Description: {product['description']}\n"
                    f"Weight: {product['weight']}\n"
                    f"Composition: {product['composition']}\n"
                )
                messages.append({"role": "system", "content": product_info})
                print(product_info)

        messages.append({"role": "user", "content": query})

        # Делаем запрос к OpenAI API
        response = await client.chat.completions.create(
            model=self.model,
            user=str(user),
            messages=messages
        )

        msg = response.choices[0].message.content

        # Добавляем ответ ассистента в историю сообщений
        messages.append({"role": "assistant", "content": msg})

        # Обновляем историю сообщений пользователя
        user_histories[str(user)] = messages

        # Сохранение истории сообщений в файл
        await self.save_histories(user_histories)

        return msg
