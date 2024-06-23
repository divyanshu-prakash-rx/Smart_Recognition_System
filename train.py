from ultralytics import YOLO

# Load a model
model = YOLO()  # load a pretrained model (recommended for training)

# Train the model
model.train(data='/home/divyanshu/Desktop/Model2/data.yaml',epochs=30, device='cuda')
