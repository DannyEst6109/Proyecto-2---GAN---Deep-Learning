"""Carga recursiva, huella del dataset y encuadre sin recortar alas."""

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageOps
from torch.utils.data import Dataset
from torchvision.transforms.functional import to_tensor


class DragonDataset(Dataset):
    def __init__(self, folder, image_size=64):
        self.root = Path(folder).resolve()
        if not self.root.is_dir():
            raise FileNotFoundError(f'Dataset inexistente: {self.root}')
        self.files = sorted(p for p in self.root.rglob('*')
                            if p.is_file() and p.suffix.lower() in {'.png', '.jpg', '.jpeg', '.webp'})
        if len(self.files) < 2:
            raise ValueError('Se necesitan al menos dos imágenes legibles.')
        self.image_size = image_size

    def __len__(self):
        return len(self.files)

    def __getitem__(self, index):
        path = self.files[index]
        try:
            with Image.open(path) as image:
                image = ImageOps.exif_transpose(image).convert('RGBA')
                background = Image.new('RGBA', image.size, 'white')
                image = Image.alpha_composite(background, image).convert('RGB')
                image = ImageOps.pad(image, (self.image_size, self.image_size),
                                     method=Image.Resampling.LANCZOS, color='white')
                return to_tensor(image).mul(2).sub(1)
        except (OSError, ValueError) as error:
            raise ValueError(f'Imagen no legible: {path}') from error

    def manifest(self):
        rows = []
        for path in self.files:
            digest = hashlib.sha256()
            with path.open('rb') as source:
                for chunk in iter(lambda: source.read(1024 * 1024), b''):
                    digest.update(chunk)
            rows.append({'path': path.relative_to(self.root).as_posix(), 'sha256': digest.hexdigest()})
        encoded = json.dumps(rows, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
        return rows, hashlib.sha256(encoded).hexdigest()
