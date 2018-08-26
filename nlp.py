import pandas as pd, numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import time
t1=time.time()
train = pd.read_csv('input/train_set.csv')[:100]
test = pd.read_csv('input/test_set.csv')[:10]
test_id = pd.read_csv('input/test_set.csv')[["id"]][:10].copy()

column="word_seg"
# 用来查找数据的维度

n = train.shape
# 将原始文档集合转换为TF-IDF特征矩阵
vec = TfidfVectorizer(ngram_range=(1,2),min_df=3, max_df=0.9,use_idf=1,smooth_idf=1, sublinear_tf=1)
# 这一步的变换是比较耗时的。
trn_term_doc = vec.fit_transform(train[column])
test_term_doc = vec.transform(test[column])

# 把
y=(train["class"]-1).astype(int)
# 创建逻辑回归分类器
clf = LogisticRegression(C=4, dual=True)
clf.fit(trn_term_doc, y)
preds=clf.predict_proba(test_term_doc)

#保存概率文件
test_prob=pd.DataFrame(preds)
test_prob.columns=["class_prob_%s"%i for i in range(1,preds.shape[1]+1)]
test_prob["id"]=list(test_id["id"])
test_prob.to_csv('input/prob_lr_baseline.csv',index=None)

#生成提交结果
preds=np.argmax(preds,axis=1)
test_pred=pd.DataFrame(preds)
test_pred.columns=["class"]
test_pred["class"]=(test_pred["class"]+1).astype(int)
print(test_pred.shape)
print(test_id.shape)
test_pred["id"]=list(test_id["id"])
test_pred[["id","class"]].to_csv('input/sub_lr_baseline.csv',index=None)
t2=time.time()
print("time use:",t2-t1)