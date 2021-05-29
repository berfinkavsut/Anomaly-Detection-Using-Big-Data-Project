import torch as th
from torch.autograd import Variable as V
from torch import nn, optim
from tqdm import tqdm_notebook as tqdm
import numpy as np
import random
# from ip2vec.trainer import Skipgram


class Trainer:
    def __init__(self, w2v, v2w, freq, emb_dim, device):
        self.v2w = v2w
        self.w2v = w2v
        self.unigram_table = self.noise(w2v, freq)
        self.vocab_size = len(w2v)

        ### Model ###
        self.device = device
        self.model = Skipgram(self.vocab_size, emb_dim).to(self.device)
        self.optim = optim.Adam(self.model.parameters())
        
    def noise(self, w2v, freq):
        unigram_table = []
        total_word = sum([c for c in freq.values()])
        for w, v in w2v.items():
            unigram_table.extend([v]*int(((freq[w]/total_word)**0.75)/0.001))
        return unigram_table
    
    def negative_sampling(self, batch_size, neg_num, batch_target):
        neg = np.zeros(neg_num)
        for i in range(batch_size):
            sample = random.sample(self.unigram_table, neg_num)
            while batch_target[i] in sample:
                sample = random.sample(self.unigram_table, neg_num)
            neg = np.vstack([neg, sample])
        return neg[1:batch_size+1]
    
    def fit(self, data, max_epoch, batch_size, neg_num):
        run_losses = []
        for epoch in range(max_epoch):
            run_loss = 0
            
            for batch in tqdm(data):
                batch = np.array(batch)
                # print('batch:', batch)
                # print(batch.shape)

                context, target = batch[:, 1], batch[:, 0]

                # print('context:', context)
                # print('target:', target)

                self.optim.zero_grad()
                batch_size = 5  # changed
                batch_neg = self.negative_sampling(batch_size, neg_num, target)
                context = V(th.LongTensor(context)).to(self.device)
                target = V(th.LongTensor(target)).to(self.device)
                batch_neg = V(th.LongTensor(batch_neg.astype(int))).to(self.device)
                # print('batch neg:',batch_neg )
                loss = self.model(target, context, batch_neg)
                # loss = self.model(target, context) #changed
                loss.backward()
                self.optim.step()
#               run_loss += loss.cpu().item()
#           run_losses.append(run_loss/len(data))
            # print(epoch, run_loss)
        return run_losses

    def most_similar(self, word, top):
        W = self.model.state_dict()["u_embedding.weight"]
        idx = self.w2v[word]
        similar_score = {}
        for i, vec in enumerate(W):
            if i != idx:
                d = vec.dot(W[idx])
                similar_score[self.v2w[i]] = d
        similar_score = sorted(similar_score.items(), key=lambda x: -x[1])[:top]
        for k, v in similar_score:
            print(k, ":", round(v.item(), 2))


class Skipgram(nn.Module):
    def __init__(self, vocab_size, emb_dim):
        super().__init__()
        self.vocab_size = vocab_size
        self.emb_dim = emb_dim
        self.u_embedding = nn.Embedding(vocab_size, emb_dim)
        self.v_embedding = nn.Embedding(vocab_size, emb_dim)
        self.log_sigmoid = nn.LogSigmoid()

        init_range = 0.5 / emb_dim
        self.u_embedding.weight.data.uniform_(-init_range, init_range)
        self.v_embedding.weight.data.uniform_(-0, 0)

    def forward(self, target, context, neg):
        v_embedd = self.u_embedding(target)
        u_embedd = self.v_embedding(context)
        positive = self.log_sigmoid(th.sum(u_embedd * v_embedd, dim=1)).squeeze()

        u_hat = self.v_embedding(neg)
        # negative_ = th.bmm(u_hat, v_embedd.unsqueeze(2)).squeeze(2)
        negative_ = (v_embedd.unsqueeze(1) * u_hat).sum(2)
        negative = self.log_sigmoid(-th.sum(negative_, dim=1)).squeeze()

        loss = positive + negative
        return -loss.mean()



