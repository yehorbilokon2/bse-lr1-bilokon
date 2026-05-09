class Document:
    #Клас, що репрезентує завантажений документ (з діаграми класів).
    def __init__(self, doc_id: int, file_name: str, size_mb: float):
        self.id = doc_id
        self.file_name = file_name
        self.size_mb = size_mb
        self.is_public = False
        self.tags = []
        self.report = None

    def add_tag(self, tag: str):
        #Додає тег до файлу (FR-05).
        if not isinstance(tag, str) or not tag.strip():
            raise ValueError("Тег має бути непорожнім рядком")
        tag_lower = tag.strip().lower()
        if tag_lower not in self.tags:
            self.tags.append(tag_lower)


class AIService:
    #Сервіс обробки документів штучним інтелектом (FR-03).
    def analyze(self, doc: Document) -> dict:
        if doc.size_mb == 0:
            raise ValueError("Неможливо проаналізувати порожній файл")
        
        # Імітація генерації звіту ШІ
        confidence = max(0.1, 1.0 - (doc.size_mb / 100))
        return {
            "summary": f"Звіт для файлу {doc.file_name}",
            "confidence_score": round(confidence, 2)
        }


class DocumentManager:
    #Головний контролер системи управління документами.
    def __init__(self):
        self.documents = {}
        self.ai_service = AIService()

    # МЕТОД 1: Складна валідація (умови + винятки) на основі Sequence Diagram
    def upload_document(self, file_name: str, size_mb: float) -> Document:
        #Завантажує документ, перевіряючи розмір та формат.#
        if size_mb <= 0:
            raise ValueError("Розмір файлу має бути більшим за нуль")
        
        # Обмеження з діаграми послідовності: [file size < 20MB]
        if size_mb > 20.0:
            raise ValueError("Файл занадто великий. Максимум 20 МБ")
            
        if not file_name.endswith(('.txt', '.pdf', '.docx')):
            raise ValueError("Непідтримуваний формат файлу")

        doc_id = len(self.documents) + 1
        doc = Document(doc_id, file_name, size_mb)
        self.documents[doc_id] = doc
        return doc

    # МЕТОД 2: Взаємодія сервісів
    def process_document(self, doc_id: int) -> dict:
        #Відправляє документ на обробку ШІ (FR-03).
        if doc_id not in self.documents:
            raise KeyError("Документ не знайдено")
        
        doc = self.documents[doc_id]
        report = self.ai_service.analyze(doc)
        doc.report = report
        return report

    # МЕТОД 3: Вкладені цикли та умови (FR-04: Пошук за тегами)
    def search_by_tags(self, query_tags: list) -> list:
        #Шукає документи, які містять хоча б один із вказаних тегів.
        if not query_tags:
            return []
            
        search_tags = [t.strip().lower() for t in query_tags]
        result = []
        
        for doc in self.documents.values():
            match = False
            for tag in search_tags:
                if tag in doc.tags:
                    match = True
                    break  # Знайшли збіг, перевіряти інші теги для цього файлу не треба
            if match:
                result.append(doc)
                
        return result