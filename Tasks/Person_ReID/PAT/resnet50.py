import torch
from torch import nn

class Bottleneck(nn.Module):
    def __init__(self, in_channels, out_channels, stride, expansion, downsample=None):
        super().__init__()
        self.proj_conv = nn.Conv2d(in_channels, out_channels, kernel_size=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv3x3 = nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)
        self.expand_conv = nn.Conv2d(out_channels, out_channels * expansion, kernel_size=1, bias=False)
        self.bn3 = nn.BatchNorm2d(out_channels * expansion)
        self.relu = nn.ReLU(inplace=True)
        self.downsample = downsample

    def forward(self, x):
    
        h = self.proj_conv(x)
        h = self.bn1(h)
        h = self.relu(h)

        h = self.conv3x3(h)
        h = self.bn2(h)
        h = self.relu(h)

        h = self.expand_conv(h)
        h = self.bn3(h)

        if self.downsample is not None:
            identity = self.downsample(x)
        else:
            identity = x

        h += identity

        out = self.relu(h)

        return out


class ResNet50(nn.Module):
    def __init__(self, inplanes, num_classes=1000, expansion=4, is_top=False):
        super(ResNet50, self).__init__()
        self.is_top = is_top
        self.expansion = expansion
        self.inplanes = 64
        self.dilation = 1

        self.conv1 = nn.Conv2d(inplanes, self.inplanes, kernel_size=7, stride=2, padding=3, bias=False)
        self.bn1 = nn.BatchNorm2d(self.inplanes)
        self.relu = nn.ReLU(inplace=True)

        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)

        self.block1 = self._make_block(Bottleneck, 64, 3)
        self.block2 = self._make_block(Bottleneck, 128, 4, stride=2)
        self.block3 = self._make_block(Bottleneck, 256, 6, stride=2)
        self.block4 = self._make_block(Bottleneck, 512, 3, stride=1)

        if is_top:
            self.avgpool = nn.AdaptiveAvgPool2d(output_size=(1, 1))
            self.fc = nn.Linear(512*Bottleneck.expansion, num_classes)

    def forward(self, x):
        h = self.conv1(x)
        h = self.bn1(h)
        c1 = self.relu(h)
        h = self.maxpool(c1)

        c2 = self.block1(h)
        c3 = self.block2(c2)
        c4 = self.block3(c3)
        c5 = self.block4(c4)

        if self.is_top:
            h = self.avgpool(c5)
            h = torch.flatten(h, 1)
            out = self.fc(h)
            return out
        return c2, c3, c4, c5

    def _make_block(self, block, out_channels, num_layer, stride=1, dilate=False):
        downsample = None
        if stride != 1 or (self.inplanes != out_channels * self.expansion):
            downsample = nn.Sequential(
                nn.Conv2d(self.inplanes, out_channels * self.expansion, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels * self.expansion)
            )
        else:
            downsample = nn.Identity()

        block_layers = list()

        block_layers.append(block(self.inplanes, out_channels, stride, self.expansion, downsample))
        self.inplanes = out_channels * self.expansion

        for _ in range(1, num_layer):
            # block_layers.append(block(self.inplanes, out_channels, 1, downsample, self.expansion))
            block_layers.append(block(self.inplanes, out_channels, 1, self.expansion))

        return nn.Sequential(*block_layers)

if __name__=='__main__':
    from torchsummary import summary as summary
    resnet50 = ResNet50(3).cuda()
    model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet50', pretrained=True).cuda()

    # for current_params, ma_params in zip(resnet18.parameters(), model.parameters()):
    #     current_params.data = ma_params.data
    #     old_weight, up_weight = ma_params.data, current_params.data

    # print(resnet18.named_children())

    summary(resnet50, (3,256,128), batch_size=1)
    # summary(model, (3,256,192), batch_size=1)