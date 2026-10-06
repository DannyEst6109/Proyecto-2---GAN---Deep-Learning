"""Comprobar el entorno local sin iniciar entrenamientos ni modificar archivos."""

import json
import platform
import sys

try:
    import torch
    import torchvision
except ImportError:
    raise SystemExit(
        "Falta PyTorch o torchvision. Instala las dependencias en el entorno .venv."
    ) from None


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # Comprobar cómputo y retropropagación en el dispositivo seleccionado.
    x = torch.ones((4, 4), device=device, requires_grad=True)
    (x @ x).sum().backward()
    if x.grad is None or not torch.isfinite(x.grad).all():
        raise RuntimeError("Falló la comprobación de retropropagación.")
    report = {
        "python": sys.version.split()[0],
        "system": platform.system(),
        "torch": torch.__version__,
        "torchvision": torchvision.__version__,
        "device": str(device),
        "cuda_build": torch.version.cuda,
        "gpu": torch.cuda.get_device_name(0) if device.type == "cuda" else None,
        "backpropagation": "ok",
    }
    print(json.dumps(report, indent=2))
    if device.type == "cpu":
        print("CPU seleccionada. Medir tiempo de entrenamiento antes de fijar el presupuesto.")


if __name__ == "__main__":
    main()
