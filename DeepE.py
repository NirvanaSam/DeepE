from sklearn.metrics import roc_auc_score
import torch
import numpy as np
import os
import time
import datetime
from builddata_softplus import *
from collections import Counter
import random
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import copy
from common import *
from buildtrain import *
from scipy.stats import rankdata
from model import *


parser = ArgumentParser("DeepE", formatter_class=ArgumentDefaultsHelpFormatter, conflict_handler='resolve')
parser.add_argument("--data_path", default="./data/", help="Data sources.")
parser.add_argument("--run_folder", default="./", help="Data sources.")
parser.add_argument("--data_name", default="FB15k-237", help="Name of the dataset.")
parser.add_argument("--embedding_dim", default=300, type=int, help="Entity/Relation dimension")
parser.add_argument("--min_lr",default=5e-5,type=float,help='L2 regularization')
parser.add_argument("--batch_size",default=1000,type=int,help='Batch Size')
parser.add_argument("--log_epoch",default=2,type=int,help='how many batches to wait before logging training status')
parser.add_argument("--neg_ratio", default=1.0, help="Number of negative triples generated by positive (default: 1.0)")

parser.add_argument("--hidden_drop",default=0.4,type=float,help="Dropout on input layer and FC layers in DeepE building blocks")
parser.add_argument("--identity_drop",default=0.01,type=float,help="Dropout on the identity mapping in DeepE building blocks")
parser.add_argument("--target_drop",default=0.4,type=float,help='Dropout on the FC layers in ResNet building blocks')

parser.add_argument("--num_source_layers",default=40,type=int)
parser.add_argument("--num_target_layers",default=1,type=int)
parser.add_argument("--num_inner_layers",default=3,type=int)

parser.add_argument("--device",default='cuda:0',type=str)
parser.add_argument("--opt",default="Adam",type=str)
parser.add_argument("--learning_rate", default=0.003, type=float, help="Learning rate")
parser.add_argument("--weight_decay",default=5e-8,type=float)
parser.add_argument("--factor",default=0.8,type=float)
parser.add_argument("--verbose",default=1,type=int)
parser.add_argument("--patience",default=5,type=int)
parser.add_argument("--max_mrr",default=0.35,type=float)
parser.add_argument("--epoch",default=1000,type=int)
parser.add_argument("--momentum",default=0.9,type=float)
parser.add_argument("--save_name",default='wn18rr.pt')
args = parser.parse_args()
setup_seed(1234) if args.data_name == "WN18RR" else setup_seed(2022)
print("Loading data...")
cuda_num = int(args.device[-1])
torch.cuda.set_device(cuda_num)
train, valid, test, words_indexes, indexes_words, \
headTailSelector, entity2id, id2entity, relation2id, id2relation = build_data(path=args.data_path, name=args.data_name)
data_size = len(train)

train_doubles,valid_doubles,test_doubles = get_doubles(train,valid,test,words_indexes)
x_valid = np.array(valid_doubles).astype(np.int32)
x_test = np.array(test_doubles).astype(np.int32)
rel_set = get_rel_set(train,valid,test)
vocab_size = max(rel_set) + len(words_indexes) + 1
target_dict=get_target_dict(train_doubles,x_valid,x_test)

model = DeepE(vocab_size,embedding_dim=args.embedding_dim,hidden_drop=args.hidden_drop,num_source_layers=args.num_source_layers,num_target_layers=args.num_target_layers,input_drop = args.hidden_drop,inner_layers=args.num_inner_layers,target_drop=args.target_drop,identity_drop=args.identity_drop)
device = args.device
model.init()

if args.opt == 'Adam':
    opt = torch.optim.Adam(model.parameters(), lr=args.learning_rate, weight_decay=args.weight_decay)
elif args.opt == 'SGD':
    opt = torch.optim.SGD(model.parameters(),lr=args.learning_rate, momentum=args.momentum)
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(opt, 'min',factor=args.factor,verbose=args.verbose,min_lr=args.min_lr,patience=args.patience)

    
num_batches_per_epoch = len(train_doubles)//args.batch_size+1
model = train_epoch(train_doubles,num_batches_per_epoch,args.batch_size,model,opt,scheduler,x_valid,target_dict,args.log_epoch,args.device,max_mrr=args.max_mrr,epoch=args.epoch,x_test=x_test)
model.eval()
torch.save(model, f'{args.save_name}')
model = torch.load(args.save_name)
print(evaluate(model,x_test,args.batch_size,target_dict))