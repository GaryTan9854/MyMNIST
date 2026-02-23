import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image, ImageOps
from torchvision import transforms
import matplotlib.pyplot as plt

# 1. 必須定義跟訓練時一模一樣的構造
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = torch.flatten(x, 1)
        x = F.relu(self.fc1(x))
        return F.log_softmax(self.fc2(x), dim=1)

def predict(image_path):
    # 設定設備 (M3 晶片用 mps)
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    
    # 2. 載入訓練好的大腦
    model = Net().to(device)
    try:
        model.load_state_dict(torch.load("my_mnist_model.pth", map_location=device, weights_only=True))
        model.eval()
    except FileNotFoundError:
        print("❌ 找不到 my_mnist_model.pth，請先執行 mytorch.py 進行訓練！")
        return

    # 3. 處理你的手寫照片
    # MNIST 原始數據是「黑底白字」，但一般拍照是「白底黑字」
    raw_img = Image.open(image_path).convert('L') # 轉成灰階
    inv_img = ImageOps.invert(raw_img)           # 負片處理：把白底黑字轉成黑底白字

    # 影像轉換：縮放、轉張量、標準化
    transform = transforms.Compose([
        transforms.Resize((28, 28)),
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])

    img_tensor = transform(inv_img).unsqueeze(0).to(device)

    # 4. 讓 AI 猜猜看
    with torch.no_grad():
        output = model(img_tensor)
        prediction = output.argmax(dim=1).item()
        confidence = torch.exp(output.max()).item() * 100

    print(f"\n🔮 AI 預測結果: 【{prediction}】")
    print(f"📈 信心度: {confidence:.2f}%")

    # 顯示 AI 看到的樣子 (28x28 的小圖)
    plt.imshow(inv_img, cmap='gray')
    plt.title(f"AI sees this as: {prediction}")
    plt.show()

if __name__ == "__main__":
    # 在這裡輸入你的檔名
    user_img = "test.jpg" 
    predict(user_img)