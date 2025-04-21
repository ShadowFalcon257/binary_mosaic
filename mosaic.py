from PIL import Image

# Load and resize images to 100px width (maintaining aspect ratio)
def load_and_resize_image(filename):
    img = Image.open(filename)
    width, height = img.size
    new_height = int((100 / width) * height)  # Maintain aspect ratio
    return img.resize((100, new_height), Image.LANCZOS)

zero_img = load_and_resize_image("zero.png")
one_img = load_and_resize_image("one.png")
separator_img = load_and_resize_image("separator.png")

def text_to_binary(text):
    return ' '.join(format(ord(c), '08b') for c in text)

def create_binary_image(binary_text):
    octets = binary_text.split(' ')  # Split into individual 8-bit segments
    rows = [octets[i:i+4] for i in range(0, len(octets), 4)]  # Group into rows of 4 octets

    row_images = []  # Store each row as an image
    for row in rows:
        images = []
        for octet in row:
            for bit in octet:
                images.append(one_img if bit == '1' else zero_img)
            images.append(separator_img)  # Add separator after each octet
        
        images.pop()  # Remove the last separator in each row
        
        # Create a row image
        row_width = sum(img.width for img in images)
        row_height = max(img.height for img in images)
        row_img = Image.new("RGB", (row_width, row_height), (255, 255, 255))
        
        x_offset = 0
        for img in images:
            row_img.paste(img, (x_offset, 0))
            x_offset += img.width
        
        row_images.append(row_img)

    # Stack all rows vertically
    final_width = max(row.width for row in row_images)
    final_height = sum(row.height for row in row_images)
    
    final_image = Image.new("RGB", (final_width, final_height), (255, 255, 255))
    
    y_offset = 0
    for row in row_images:
        final_image.paste(row, (0, y_offset))
        y_offset += row.height

    return final_image

# Example usage
text = "EnterTextToEncodeHere"
binary_text = text_to_binary(text)
binary_image = create_binary_image(binary_text)

# Display the final binary image
binary_image.show()

# Optionally save it
binary_image.save("output.png")
