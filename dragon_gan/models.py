"""DCGAN para imágenes RGB de 64×64; D devuelve logits sin sigmoid."""

from torch import nn
from torch.nn.utils import parametrize
from torch.nn.utils.parametrizations import spectral_norm


class Generator(nn.Module):
    def __init__(self, latent_dim=100, channels=3, features=64):
        super().__init__()
        layers = []
        previous = latent_dim
        for index, multiple in enumerate((8, 4, 2, 1)):
            current = features * multiple
            layers.extend([
                nn.ConvTranspose2d(previous, current, 4, 1 if index == 0 else 2,
                                   0 if index == 0 else 1, bias=False),
                nn.BatchNorm2d(current), nn.ReLU(inplace=True),
            ])
            previous = current
        layers.extend([nn.ConvTranspose2d(features, channels, 4, 2, 1, bias=False), nn.Tanh()])
        self.network = nn.Sequential(*layers)

    def forward(self, noise):
        return self.network(noise)


class Discriminator(nn.Module):
    """Con spectral=True cada convolución usa normalización espectral (Miyato et al., 2018)
    y BatchNorm se sustituye por identidad, como en la formulación original de SN-GAN."""

    def __init__(self, channels=3, features=64, spectral=False):
        super().__init__()
        wrap = spectral_norm if spectral else (lambda layer: layer)
        layers = [wrap(nn.Conv2d(channels, features, 4, 2, 1, bias=False)), nn.LeakyReLU(0.2, inplace=True)]
        previous = features
        for multiple in (2, 4, 8):
            current = features * multiple
            layers.extend([
                wrap(nn.Conv2d(previous, current, 4, 2, 1, bias=False)),
                nn.Identity() if spectral else nn.BatchNorm2d(current), nn.LeakyReLU(0.2, inplace=True),
            ])
            previous = current
        layers.append(wrap(nn.Conv2d(previous, 1, 4, 1, 0, bias=False)))
        self.network = nn.Sequential(*layers)

    def forward(self, images):
        return self.network(images).flatten()


def initialize_weights(module):
    if isinstance(module, (nn.Conv2d, nn.ConvTranspose2d)):
        # Con normalización espectral, inicializar el peso original y no el normalizado.
        weight = (module.parametrizations.weight.original
                  if parametrize.is_parametrized(module, 'weight') else module.weight)
        nn.init.normal_(weight, 0.0, 0.02)
    elif isinstance(module, nn.BatchNorm2d):
        nn.init.normal_(module.weight, 1.0, 0.02)
        nn.init.zeros_(module.bias)


def build_models(config, device):
    generator = Generator(config['latent_dim'], config['channels'], config['features']).to(device)
    if config.get('isolate_init_rng', False):
        # Inicializar G antes de construir D: así G parte idéntico aunque D cambie (p. ej. SN).
        generator.apply(initialize_weights)
    discriminator = Discriminator(config['channels'], config['features'],
                                  config.get('discriminator_spectral_norm', False)).to(device)
    if not config.get('isolate_init_rng', False):
        generator.apply(initialize_weights)  # Orden original de v2, conservado por reproducibilidad.
    discriminator.apply(initialize_weights)
    return generator, discriminator
