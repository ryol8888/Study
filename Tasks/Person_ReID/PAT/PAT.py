import torch
from torch import nn
from torch.nn import Functional as F
from resnet50 import ResNet50
import math


class PAT(nn.Module):
    def __init__(self, cfg):
        super(PAT, self).__init__()
        self.out_channels = cfg.out_channels
        self.k_parts = cfg.k_parts
        self.d_model = cfg.d_model
        self.num_head = cfg.num_head
        self.dropout = cfg.dropout
        self.layer_norm_eps = cfg.layer_norm_eps
        self.device = cfg.device

        self.backbone = ResNet50(3, is_top=False)
        self.encoder = Encoder(self.out_channels, self.d_model, 
                               self.num_head, self.dropout, self.layer_norm_eps)
        self.decoder = Decoder(self.k_parts, self.d_model, 
                               self.num_head, self.dropout, self.layer_norm_eps, self.device)

    def forward(self, x):
        f = self.backbone(x)
        f, gap = self.encoder(f) # gap = (n_batch, d_model, 1, 1)
        parts_features = self.decoder(f) # parts_features = (n_batch, d_model, k_parts)
        return gap, parts_features


class Encoder(nn.Module):
    '''
    Encoder : input -> Conv -> MultiHeadAttention -> FeedForwardNetwork -> GAP
    input : feature map is extraed by backbone (B, 2048, 16, 8)
    output : FFN output(decoder's weight pooling), GAP output(with object function)
    '''
    def __init__(self, out_channels, d_model, num_head, dropout, layer_norm_eps):
        super(Encoder, self).__init__()
        # cfg
        self.d_model = d_model
        self.num_head = num_head
        self.dropout = dropout
        self.layer_norm_eps = layer_norm_eps
        # Conv
        self.conv_1 = nn.Conv2d(out_channels, d_model, kernel_size=1, stride=1, bias=False)
        # MultiHeadAttention
        self.mha = MHA(self.d_model, self.num_head)
        # FeedForwardNetwork
        self.ffn = FFN(self.d_model,self.dropout)
        self.residual1 = ResidualConnection(self.d_model, self.layer_norm_eps, self.dropout)
        self.residual2 = ResidualConnection(self.d_model, self.layer_norm_eps, self.dropout)
        self.gap = nn.AdaptiveAvgPool2d(1)

    def forward(self, f):
        f = self.conv_1(f)
        B, C, H, W = f.size()
        input = f.contiguous().view(B, C, H*W).transpose(1,2)
        f = self.residual1(input, self.mha(input, input, input))
        f = self.residual2(f, self.ffn(f))
        f_reshape = f.contiguous().view(B, -1, H, W)
        gap = self.gap(f_reshape)
        return f, gap


class MHA(nn.Module):
    def __init__(self, d_model, num_head):
        super(MHA, self).__init__()
        self.d_model = d_model
        self.num_head = num_head
        self.d_k = self.d_v = self.d_model // self.num_head

        self.w_q = nn.Linear(d_model, self.d_k)
        self.w_k = nn.Linear(d_model, self.d_k)
        self.w_v = nn.Linear(d_model, self.d_v)
        self.w_o = nn.Linear(self.d_v, d_model)

    def scale_dot(self, query, key, value):
        qk = query @ key.transpose(-2, -1)
        attention_score = qk / math.sqrt(self.d_model)
        attention_softmax = F.softmax(attention_score, dim=-1)
        return attention_softmax @ value

    def forward(self, query, key, value): # (n_batch, d_model, hw)
        n_batch = query.size(0)
        if len(query.shape) <= 3:
          query_t = self.w_q(query)
          key_t = self.w_q(key)
          value_t = self.w_q(value)
          f = self.scale_dot(query_t, key_t, value_t)
        else:
          query_t = self.w_q(query).view(n_batch, -1, self.num_head, self.d_k).transpose(1,2)
          key_t = self.w_k(key).view(n_batch, -1, self.num_head, self.d_k).transpose(1,2)
          value_t = self.w_v(value).view(n_batch, -1, self.num_head, self.d_v).transpose(1,2)
          f = self.scale_dot(query_t, key_t, value_t)
          f = f.contiguous().view(n_batch, -1 , self.d_k) # (n_batch, hw, d_model)
        return self.w_o(f)


class ResidualConnection(nn.Module):
    def __init__(self, size, eps, dropout):
        super(ResidualConnection, self).__init__()
        self.norm = nn.LayerNorm(size, eps=eps)
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x, f):
        return x + self.dropout(self.norm(f))


class FFN(nn.Module):
    def __init__(self, d_model, dropout):
        super(FFN, self).__init__()
        self.linear1 = nn.Linear(in_features=d_model, out_features=d_model)
        self.act = nn.ReLU(inplace=True)
        self.linear2 = nn.Linear(in_features=d_model, out_features=d_model)
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x):
        f = self.linear1(x)
        f = self.act(f)
        f = self.dropout(f)
        f = self.linear2(f)
        return f


class Decoder(nn.Module):
    def __init__(self, num_k_parts, d_model, num_head, dropout, layer_norm_eps, device):
        super(Decoder,self).__init__()
        self.d_model = d_model
        self.num_head = num_head
        self.dropout = dropout
        self.layer_norm_eps = layer_norm_eps
        self.device = device

        self.k_parts_tensor = torch.randn(num_k_parts, self.d_model, requires_grad=True, device=self.device)
        self.self_attention = MHA(self.d_model, self.num_head)
        self.residual1 = ResidualConnection(self.d_model, self.layer_norm_eps, self.dropout)
        self.cross_attention = MHA(self.d_model, self.num_head)
        self.residual2 = ResidualConnection(self.d_model, self.layer_norm_eps, self.dropout)
        self.ffn = FFN(self.d_model, self.dropout)
        self.residual3 = ResidualConnection(self.d_model, self.layer_norm_eps, self.dropout)

    def forward(self, encoder_f): # (n_batch, hw, d_model)
        f = self.residual1(self.k_parts_tensor, self.self_attention(self.k_parts_tensor, self.k_parts_tensor, self.k_parts_tensor))
        f = self.residual2(f, self.cross_attention(f, encoder_f, encoder_f))
        return self.residual3(f, self.ffn(f)).contiguous().transpose(1, 2)






