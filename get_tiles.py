from PIL import Image


def remove_background(input_path, output_path):
    original_image = Image.open(input_path)

    # Конвертируем изображение в формат RGBA
    original_image = original_image.convert("RGBA")

    # Получаем данные о пикселях
    data = original_image.getdata()

    # Создаем новый список данных без фона (белого цвета)
    new_data = [(255, 255, 255, 0) if item[:3] == (255, 255, 255) else item for item in data]

    # Помещаем новые данные в изображение
    original_image.putdata(new_data)

    # Сохраняем изображение
    original_image.save(output_path, format="PNG")


# Пример использования:
input_image_path = "graphics/fileball/1.png"
output_image_path = "graphics/fileball/1.png"
remove_background(input_image_path, output_image_path)
