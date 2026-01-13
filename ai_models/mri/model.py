import timm
import torch.nn as nn

def get_model(num_classes=4):
    model = timm.create_model(
        "swin_tiny_patch4_window7_224",
        pretrained=True,
        num_classes=num_classes
    )

    # Freeze early layers
    # Consistent with voice model choice to keep some layers trainable
    for name, param in model.named_parameters():
        if "layers.2" not in name and "layers.3" not in name:
            param.requires_grad = False

    return model
