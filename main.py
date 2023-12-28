import cv2
import numpy as np

# Read vertex data from the .obj file
def load_vertices(filename):
    vertices = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith('v '):
                parts = line.strip().split()
                vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
    return np.array(vertices)

# Normalize the vertex data
def normalize_vertices(vertices):
    min_vals = vertices.min(axis=0)
    max_vals = vertices.max(axis=0)
    norm_vertices = (vertices - min_vals) / (max_vals - min_vals)
    return norm_vertices, min_vals, max_vals

# Encode vertex data into an image
def encode_vertices_to_image(vertices, image_size):
    img = np.zeros((image_size, image_size, 3), dtype=np.uint8)
    step = max(vertices.shape[0] // (image_size * image_size), 1)
    for i in range(0, vertices.shape[0], step):
        x, y, z = vertices[i]
        xi, yi = int(x * (image_size - 1)), int(y * (image_size - 1))
        img[yi, xi] = np.uint8(z * 255)
    return img

# Main process
filename = 'idol.obj'
vertices = load_vertices(filename)
norm_vertices, min_vals, max_vals = normalize_vertices(vertices)
image_size = 200

print(f'min_vals: {min_vals}')
print(f'max_vals: {max_vals}')

# Encoding
img = encode_vertices_to_image(norm_vertices, image_size)
cv2.imwrite('encoded_vertices.png', img)
