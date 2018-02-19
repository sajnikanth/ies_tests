import random
from random import randint

# Test congigurations
hostnames = {
    'production': 'https://image-editor.ebt.infra.photos/api/',
    'acceptance': 'https://image-editor.nonprod.ebt.infra.photos/api/',
    'test': 'https://image-editor.nonprod.ebt.infra.photos/api/',
}

sample_image_urls = ['https://i.imgur.com/XT4BQIy.jpg', 'https://preview.ibb.co/iCtf1S/sample.jpg']

all_flips = ['None', 'FLIP_HORIZONTAL', 'FLIP_VERTICAL', 'FLIP_BOTH']
all_effects = ['None', 'Sephia', 'BlackWhite', 'Enhance']
all_border_colors = ['White', 'Black', 'Yellow', 'Green', 'Blue', 'Red']

"""
Adjust Brightness needs to be a float between 1 and -1
Adjust Contrast needs to be a float between 1 and -1
Crop x/y/width/height must be in percent between 0-100
Rotate Angle needs to be between 0 and 360
Resize  Width and Height must be > 0
"""
operations_template = {
    'crop': {
        'x': random.uniform(0.0, 50.0),
        'y': random.uniform(0.0, 50.0),
        'w': random.uniform(0.1, 10.0),
        'h': random.uniform(0.1, 10.0)
    },
    'rotate': {
        'angle': randint(0, 360),
        'flip': random.choice(all_flips)
    },
    'adjust': {
        'brightness': random.uniform(-1.0, 1.0),
        'contrast': random.uniform(-1.0, 1.0)
    },
    'resize': {
        'h': randint(1, 1000),
        'w': randint(1, 1000)
    },
    'effect': {
        'type': random.choice(all_effects),
        'strength': randint(0, 100)
    },
    'effects': [
        {
            'type': random.choice(all_effects),
            'strength': randint(0, 100)
        }
    ],
    'prep': {
        'h': randint(1, 100),
        'w': randint(1, 100),
        'imageBorder': {
            'shouldApply': random.choice([True, False]),
            'w': randint(0, 10),
            'color': random.choice(all_border_colors)
        }

    },
}
