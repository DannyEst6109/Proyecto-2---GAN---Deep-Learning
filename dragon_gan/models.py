"""DCGAN para imágenes RGB de 64×64; D devuelve logits sin sigmoid."""

from torch import nn


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
    def __init__(self, channels=3, features=64):
        super().__init__()
        layers = [nn.Conv2d(channels, features, 4, 2, 1, bias=False), nn.LeakyReLU(0.2, inplace=True)]
        previous = features
        for multiple in (2, 4, 8):
            current = features * multiple
            layers.extend([
                nn.Conv2d(previous, current, 4, 2, 1, bias=False),
                nn.BatchNorm2d(current), nn.LeakyReLU(0.2, inplace=True),
            ])
            previous = current
        layers.append(nn.Conv2d(previous, 1, 4, 1, 0, bias=False))
        self.network = nn.Sequential(*layers)

    def forward(self, images):
        return self.network(images).flatten()


def initialize_weights(module):
    if isinstance(module, (nn.Conv2d, nn.ConvTranspose2d)):
        nn.init.normal_(module.weight, 0.0, 0.02)
    elif isinstance(module, nn.BatchNorm2d):
        nn.init.normal_(module.weight, 1.0, 0.02)
        nn.init.zeros_(module.bias)


def build_models(config, device):
    generator = Generator(config['latent_dim'], config['channels'], config['features']).to(device)
    discriminator = Discriminator(config['channels'], config['features']).to(device)
    generator.apply(initialize_weights)
    discriminator.apply(initialize_weights)
    return generator, discriminator
