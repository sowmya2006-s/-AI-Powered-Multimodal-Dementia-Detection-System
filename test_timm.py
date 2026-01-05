import timm
import torch
import sys

print("Python version:", sys.version)
print("Torch version:", torch.__version__)
print("Timm version:", timm.__version__)

print("Attempting to create generic model...")
try:
    model = timm.create_model('resnet18', pretrained=True)
    print("ResNet18 created successfully.")
except Exception as e:
    print(f"ResNet18 creation failed: {e}")

print("Attempting to create Swin Transformer...")
try:
    model = timm.create_model('swin_tiny_patch4_window7_224', pretrained=True)
    print("Swin Transformer created successfully.")
except Exception as e:
    print(f"Swin creation failed: {e}")
