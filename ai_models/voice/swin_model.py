import torch
import torch.nn as nn
import timm

class SwinTransformer(nn.Module):
    def __init__(self, num_classes=2, pretrained=True):
        super(SwinTransformer, self).__init__()
        # Load preprained Swin Transformer
        self.model = timm.create_model('swin_tiny_patch4_window7_224', pretrained=pretrained, num_classes=num_classes)
        
    def forward(self, x):
        return self.model(x)

if __name__ == "__main__":
    # Test model
    model = SwinTransformer()
    print(model)
    x = torch.randn(1, 3, 224, 224)
    y = model(x)
    print(f"Output shape: {y.shape}")
