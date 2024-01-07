from PIL import Image

image_path = 'tileset2.png'
original_image = Image.open(image_path)
chunk_size = 32
width, height = original_image.size
counter = 0
for y in range(0, height, chunk_size):
    for x in range(0, width, chunk_size):
        left, top, right, bottom = x, y, x + chunk_size, y + chunk_size
        cropped_image = original_image.crop((left, top, right, bottom))
        cropped_image = cropped_image.convert("RGBA")
        data = cropped_image.getdata()
        new_data = []
        for item in data:
            if item[:3] == (0, 0, 0):
                new_data.append((0, 0, 0, 0))
            else:
                new_data.append(item)
        cropped_image.putdata(new_data)
        save_path = f'graphics/monstres/calmar/{counter}.png'
        cropped_image.save(save_path, format="PNG")
        counter += 1
