import pytest
from document_manager import DocumentManager, Document, AIService

#Тести для методу upload_document (Валідація розміру та розширення)

def test_upload_valid_document(): # EP: позитивний клас
    # Arrange
    manager = DocumentManager()
    # Act
    doc = manager.upload_document("report.pdf", 15.0)
    # Assert
    assert doc.file_name == "report.pdf"
    assert doc.size_mb == 15.0

def test_upload_zero_size(): # BVA: межа = 0
    # Arrange
    manager = DocumentManager()
    # Act & Assert
    with pytest.raises(ValueError, match="більшим за нуль"):
        manager.upload_document("test.txt", 0.0)

def test_upload_exact_max_size(): # BVA: межа = 20.0 (Допустимо за Sequence Diagram)
    # Arrange
    manager = DocumentManager()
    # Act
    doc = manager.upload_document("large_file.docx", 20.0)
    # Assert
    assert doc.id == 1

def test_upload_over_max_size(): # BVA: межа = 20.1 (Негативний)
    # Arrange
    manager = DocumentManager()
    # Act & Assert
    with pytest.raises(ValueError, match="Файл занадто великий"):
        manager.upload_document("huge.pdf", 20.1)

def test_upload_invalid_extension(): # EP: негативний клас
    # Arrange
    manager = DocumentManager()
    # Act & Assert
    with pytest.raises(ValueError, match="Непідтримуваний формат"):
        manager.upload_document("script.exe", 5.0)

#Тести для методу process_document

def test_process_existing_document(): # EP: позитивний
    # Arrange
    manager = DocumentManager()
    manager.upload_document("test.txt", 10.0) # doc_id = 1
    # Act
    report = manager.process_document(1)
    # Assert
    assert "summary" in report
    assert report["confidence_score"] == 0.9

def test_process_non_existing_document(): # EP: негативний
    # Arrange
    manager = DocumentManager()
    # Act & Assert
    with pytest.raises(KeyError, match="Документ не знайдено"):
        manager.process_document(999)

#Тести для методу search_by_tags

def test_search_existing_tag(): # EP: позитивний
    # Arrange
    manager = DocumentManager()
    doc = manager.upload_document("notes.txt", 1.0)
    doc.add_tag("Work")
    # Act
    results = manager.search_by_tags(["work", "urgent"])
    # Assert
    assert len(results) == 1
    assert results[0].file_name == "notes.txt"

def test_search_non_existing_tag(): # EP: негативний
    # Arrange
    manager = DocumentManager()
    doc = manager.upload_document("notes.txt", 1.0)
    doc.add_tag("Personal")
    # Act
    results = manager.search_by_tags(["work"])
    # Assert
    assert len(results) == 0

def test_search_empty_tags_list(): # BVA: пустий список
    # Arrange
    manager = DocumentManager()
    # Act
    results = manager.search_by_tags([])
    # Assert
    assert results == []

#Тести класу Document 

def test_add_empty_tag(): # BVA: пустий рядок
    # Arrange
    doc = Document(1, "test.txt", 5.0)
    # Act & Assert
    with pytest.raises(ValueError, match="непорожнім рядком"):
        doc.add_tag("   ")