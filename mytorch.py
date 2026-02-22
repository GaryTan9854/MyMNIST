import time
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
import os  # 用來檢查檔案是否存在

# --- 1. 設定與設備 ---
if torch.backends.mps.is_available():
    device = torch.device("mps")
else:
    device = torch.device("cpu")
print(f" usando {device} 進行運算")

# --- 2. 定義大腦結構 (必須跟存檔時一致) ---
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

# --- 3. 準備數據 ---
transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])
train_loader = torch.utils.data.DataLoader(
    datasets.MNIST('./data', train=True, download=True, transform=transform), 
    batch_size=64, shuffle=True)

model = Net().to(device)
MODEL_PATH = "my_mnist_model.pth"

# --- 4. 核心邏輯：讀取或訓練 ---
choice = "n" # 預設重新訓練
if os.path.exists(MODEL_PATH):
    choice = input(f"偵測到已存在的模型檔案 '{MODEL_PATH}'，是否直接載入？ (y/n): ").lower()

if choice == 'y':
    # 載入現有大腦
    print("⏳ 正在載入已學習的資料...")
    state_dict = torch.load(MODEL_PATH, map_location=device, weights_only=True)
    model.load_state_dict(state_dict)
    print("✅ 載入成功！跳過訓練階段。")
else:
    # 重新修煉
    print("\n🚀 開始重新修煉 AI (預計 3 輪)...")
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    for epoch in range(1, 4):
        model.train()
        start_time = time.time()
        for batch_idx, (data, target) in enumerate(train_loader):
            data, target = data.to(device), target.to(device)
            optimizer.zero_grad()
            output = model(data)
            loss = F.nll_loss(output, target)
            loss.backward()
            optimizer.step()
        
        duration = time.time() - start_time
        print(f"第 {epoch} 輪完成，耗時: {duration:.2f} 秒")
    
    # 存檔供下次使用
    torch.save(model.state_dict(), MODEL_PATH)
    print(f"💾 修煉完成，大腦已存檔至 {MODEL_PATH}")

# --- 5. 考試階段 ---
print("\n--- AI 隨堂測驗 ---")
model.eval()
test_data, test_target = next(iter(train_loader))
img = test_data[0].unsqueeze(0).to(device)

with torch.no_grad():
    output = model(img)
    prediction = output.argmax(dim=1, keepdim=True).item()

print(f"AI 猜這張圖是: {prediction} | 實際答案是: {test_target[0].item()}")

plt.imshow(test_data[0].squeeze().cpu().numpy(), cmap='gray')
plt.title(f"Prediction: {prediction}")
plt.show()y