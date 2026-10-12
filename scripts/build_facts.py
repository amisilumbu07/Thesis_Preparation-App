import json, re
S = json.load(open('thesis/sections.json'))
norm = lambda t: re.sub(r'\s+', ' ', t).strip()
F = []
def f(cat, label, value, sec, quote):
    F.append(dict(id=f'f{len(F)+1:03d}', category=cat, label=label, value=value, section=sec, sentence=quote))

# hardware / setup
f('hardware','GPU / laptop','ASUS ROG Zephyrus G14 (GA401IV), NVIDIA GeForce RTX 2060 (Max-Q), 6GB VRAM','3.1','All experiments reported in this thesis were executed on a single ASUS ROG Zephyrus G14 (GA401IV) laptop equipped with an NVIDIA GeForce RTX 2060 (Max-Q, 6GB')
f('hardware','VRAM budget','6GB','1.5','All experiments are conducted on a single NVIDIA RTX 2060 GPU with 6GB of VRAM')
f('hardware','Framework','PyTorch','3.7','using PyTorch as the underlying deep learning framework')
# datasets
f('dataset','Dataset list','WTH, ETTh1, STEEL, Smart Meters (London)','3.2','This study utilises four publicly available datasets')
f('dataset','WTH size','35,064 records, hourly, 12 variables','3.2.1','35,064 total entries across 12 variables')
f('dataset','ETTh1 size','17,420 hourly samples','3.2.2','This study uses ETTh1, containing 17,420 hourly samples in its canonical form')
f('dataset','ETTh1 features','7 native columns -> 33 engineered input features','3.2.2','this study\'s feature-engineering pipeline expands the native seven-column structure to 33 input features per timestep')
f('dataset','STEEL size','35,040 records, 15-minute, 11 variables (7 retained)','3.2.3','The dataset comprises 35,040 records at 15-minute resolution across 11 variables')
f('dataset','STEEL retained variables','7 continuous variables','3.2.3','of these, seven continuous variables were retained for modelling after feature selection')
f('dataset','STEEL scale span','roughly six to seven orders of magnitude','3.2.3','a span of roughly six to seven orders of magnitude across the seven variables retained after feature selection')
f('dataset','STEEL Usage_kWh range','0 to 157.18 kWh (mean 27.39, std 33.44)','3.2.3','energy usage ranges from 0 to 157.18 kWh (mean 27.39, std 33.44)')
f('dataset','STEEL NSM range','0 to 85,500 (mean 42,750, std 24,940.53)','3.2.3','the seconds-since-midnight (NSM) feature ranges from 0 to 85,500 (mean 42,750, std 24,940.53)')
f('dataset','Smart Meters size','>3.4 million half-hourly readings, 26 input features','3.2.4','At over 3.4 million raw readings prior to windowing')
f('dataset','Smart Meters features','26 input features','3.2.4','yielding 26 input features')
f('dataset','Smart Meters period','Nov 2011 - Feb 2014','3.2.4','collected between November 2011 and February 2014')
# preprocessing
f('preprocessing','Split','70% / 20% / 10% chronological','3.3','in a ratio of 70% / 20% / 10%')
f('preprocessing','ETTh1 window counts','12,177 train / 3,479 val / 1,740 test (17,396 usable windows)','3.3','ETTh1 yields 12,177 training, 3,479 validation, and 1,740 test sequences, an exact 70/20/10 split of the dataset\'s 17,396 usable windows')
f('preprocessing','Lookback / Label / Horizon','96 / 48 / 24','3.3','using a Lookback of 96 timesteps, a Label length of 48 timesteps, and a prediction Horizon of 24 timesteps')
f('preprocessing','Lags','1, 6, 12, 24-hour','3.3','lagged values (at 1, 6, 12, and 24-hour intervals)')
f('preprocessing','Rolling windows','mean and std over 3-, 12-, 24-hour windows','3.3','rolling-window statistics (mean and standard deviation over 3-, 12-, and 24-hour windows)')
f('preprocessing','Scaling','Z-score StandardScaler, fitted on training partition only','3.3','computed on the training partition only')
f('preprocessing','Missing values','linear interpolation; <0.5% of data','4.2','missing values—constituting less than 0.5% of the total data—were handled via linear interpolation')
# training
f('training','Optimiser and learning rates','Adam; 1e-4 Transformers, 1e-3 recurrent','3.5.2','learning rate of 1×10⁻⁴ for the three Transformer models and 1×10⁻³ for the four recurrent models')
f('training','Early-stopping patience','5 epochs recurrent, 7 epochs Transformer','3.5.2','with a patience of 5 epochs for the recurrent models and 7 epochs for the Transformer models')
f('training','Batch size (recurrent)','32','3.5.2','Batch size was set to 32 for all four recurrent models across every dataset')
f('training','Batch size (Transformers)','8 on WTH/ETTh1/STEEL; 16 on Smart Meters','3.5.2','a batch size of 8 was used for the Transformer models on WTH, ETTh1, and STEEL, while a batch size of 16 was used')
f('training','Epoch budget','10 epochs (after 5 vs 10 calibration on WTH)','3.5.1','This motivated the adoption of a 10-epoch training budget')
f('training','Smart Meters epoch cap','3 epochs','4.5','all seven models were capped at 3 completed epochs')
f('training','Smart Meters Transformer epoch time','55-70 minutes per epoch','4.5','each Transformer epoch took 55–70 minutes')
f('training','LSTM-16 hidden size','16 units','3.4.2','with a hidden dimension of 16 units')
f('training','Recurrent hidden dims','16-64 units','3.5.3','with hidden dimensions of 16–64 units sufficient in every case')
f('training','PatchTST patch settings (3.4.1 example)','patch 16, stride 8','3.4.1','grouping 16 consecutive time steps into a single patch with a stride of 8')
f('training','PatchTST patch settings (4.2.1 example)','patch 16, stride 4','4.2.1','by grouping 16 time steps into a single patch with a stride of 4')
f('training','PatchTST effective patches','approximately 11 patches from 96 timesteps','4.3','reducing the effective sequence length from 96 raw timesteps to approximately 11 patches')
f('training','PatchTST calibration times','180 s (WTH), 156 s (ETTh1)','4.3','On WTH, PatchTST converged in 180 seconds during early calibration testing, and on ETTh1 in 156 seconds')
f('training','Informer params by dataset','~2.90M (WTH, ETTh1); 87,623 (STEEL); 27,610 (Smart Meters)','3.4.1','ranging from approximately 2.90 million parameters on WTH and ETTh1 down to 87,623 parameters')
f('training','Autoformer training time (3.4.1 claim)','exceeding 68,000 seconds, longest of all models','3.4.1','exceeding 68,000 seconds')
f('training','PatchTST MSE (3.4.1 claim)','18.38','3.4.1','producing an MSE of 18.38')
f('training','Smart Meters Transformer 3-epoch times','Informer 11,119.1 s, Autoformer 10,694.7 s; recurrent 1,189.7-1,592.2 s','3.5.3','Informer and Autoformer required 11,119.1 and 10,694.7 seconds respectively to complete three epochs')
f('training','Smart Meters run length (3.7 claim)','Transformer training on Smart Meters required over three hours per model','3.7','required over three hours per model')
# metrics
f('metrics','Accuracy metrics','MAE, MSE, RMSE (MAPE excluded on Smart Meters)','3.6.1','the following three metrics are computed')
f('metrics','Operational metrics','Training time, parameter count, GPU memory (VRAM)','3.6.2','Training Time: total wall-clock time in seconds')
f('metrics','MAPE on Smart Meters','infinite/undefined for every model (zeros in target)','3.6.1','MAPE returned an infinite or undefined value for every model tested')
# results tables
T = {
 '4.4.1': [('Informer','2,901,542','0.4802','0.4046','0.6361','1,100.9'),('Autoformer','2,729,766','0.5988','0.6097','0.7808','1,252.3'),('PatchTST','399,744','0.5084','0.4871','0.6979','1,452.7')],
 '4.4.2': [('Informer','2,892,577','0.5560','0.5652','0.7518','525.6'),('Autoformer','2,716,961','0.5299','0.4452','0.6673','884.5'),('PatchTST','399,744','0.4689','0.3742','0.6117','726.4')],
 '4.5':   [('LSTM','18,816','5.2733','81.4314','9.0239','1,279.4'),('BiLSTM','38,097','7.1175','98.8821','9.9439','1,592.2'),('GRU','16,896','5.2432','75.3838','8.6824','1,283.3'),('LSTM-16','13,424','8.5613','110.1040','10.4930','1,189.7'),('Informer','27,610','6.0268','99.1785','9.9588','11,119.1'),('Autoformer','29,786','4.2817','38.6661','6.2182','10,694.7'),('PatchTST','9,120','2.5819','20.1874','4.4930','3,905.5')],
}
tab = {'4.4.1':'Table 4.1 WTH','4.4.2':'Table 4.2 ETTh1','4.5':'Table 4.4 Smart Meters'}
for sec, rows in T.items():
    for r in rows:
        f('results', f'{tab[sec]} {r[0]}', dict(params=r[1],MAE=r[2],MSE=r[3],RMSE=r[4],train_s=r[5]), sec, ' '.join(r))
steel = [('LSTM','8,632','0.0827','0.0419','0.2047','38.3','Success'),('BiLSTM','18,185','0.0746','0.0358','0.1893','48.7','Success'),('GRU','7,320','0.0709','0.0384','0.1960','38.4','Success'),('LSTM-16','4,456','0.0718','0.0420','0.2049','34.2','Success'),('Informer','87,623','NaN','NaN','NaN','502.0','Failed (ep. 1)'),('Autoformer','88,327','NaN','NaN','NaN','662.7','Failed (ep. 1)'),('PatchTST','34,368','0.0766','0.0100','0.1000','173.7','Success')]
for r in steel:
    f('results', f'Table 4.3 STEEL {r[0]}', dict(params=r[1],MAE=r[2],MSE=r[3],RMSE=r[4],train_s=r[5],outcome=r[6]), '4.4.3', ' '.join(r))
f('results','STEEL first run PatchTST','MAE 0.3407, MSE 0.2985, RMSE 0.5464','4.4.3','achieving MAE 0.3407, MSE 0.2985, and RMSE 0.5464')
f('results','STEEL comparison capacity range','4,456 to 88,327 parameters','4.4.3','at comparably small capacity (4,456 to 88,327 parameters)')
f('results','STEEL failure epoch','NaN from epoch 1, all ten epochs attempted','4.4.3','remaining so for all ten epochs attempted')
f('results','WTH 5-epoch calibration','Informer MAE 0.51 / RMSE 0.69; Autoformer MAE 0.56 / RMSE 0.74','4.4.1','Informer achieved an MAE of 0.51 and RMSE of 0.69, appearing statistically superior to Autoformer\'s MAE of 0.56 and RMSE of 0.74')
f('results','ETTh1 PatchTST gains over Informer','13.6% MAE, 25.9% MSE, 13.8% RMSE','4.4.2','a 13.6% improvement in MAE and a 25.9% improvement in MSE over Informer, and a 13.8% improvement in RMSE')
f('results','Smart Meters PatchTST gain vs mean of other six','MAE 57.6%, MSE 76.0%, RMSE 50.4%','4.5','improving on the average of the other six models by 57.6%, 76.0%, and 50.4%')
f('results','Smart Meters PatchTST vs Transformer time','3,905.5 s vs 10,694.7-11,119.1 s (about a third)','4.5','trained in roughly a third of the time of Informer or Autoformer (3,905.5s vs. 10,694.7–11,119.1s)')
f('results','Recurrent speed vs PatchTST (Smart Meters)','two to three times slower than any recurrent model','4.5','it remained two to three times slower than any recurrent model')
f('results','Recurrent vs Transformer speed factor','three to twenty-five times faster','4.6.3','training three to twenty-five times faster than any Transformer depending on dataset scale')
f('results','Informer speed claim','fastest of three Transformers on every dataset examined','4.6.1','Informer is the fastest of the three Transformers to train on every dataset examined in this chapter')
f('results','External validation','within approximately 2% of the published Informer figure','5.1','found this study\'s result within approximately 2% of the published figure')
# models
f('models','Model list','Informer, Autoformer, PatchTST (Transformers); LSTM, BiLSTM, GRU, LSTM-16 (recurrent)','1.5','three Transformer-based models (Informer, Autoformer, PatchTST) against four recurrent baselines (LSTM, BiLSTM, GRU, and a minimal single-layer LSTM configuration)')
f('models','Complexity','Informer ProbSparse O(L log L); Autoformer auto-correlation O(L log L)','3.4.1','reduces the computational burden to O(L log L)[7]')
f('models','Experimental runs','3-model on WTH and ETTh1; 7-model on STEEL and Smart Meters','3.7','Four experimental runs are reported in this thesis')

bad = [x for x in F if norm(x['sentence']) not in norm(S[x['section']]['text'])]
for x in bad: print('QUOTE NOT FOUND', x['id'], x['section'], x['sentence'][:80])
json.dump(F, open('thesis/facts.json','w'), ensure_ascii=False, indent=1)
print(len(F), 'facts,', len(bad), 'bad')
