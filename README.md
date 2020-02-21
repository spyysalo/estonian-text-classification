# Estonian text classification

Tools for Estonian text classification experiments

## Get original data

Download data from Pajupuu, H. (2016). Valentsikorpus
(https://doi.org/10.15155/3-00-0000-0000-0000-05BE6L).

```
mkdir original_data
wget http://peeter.eki.ee:5000/valence/exportparagraphs \
    -O original_data/data.csv
```

## Deduplicate and reformat as TSV

```
mkdir data
python3 scripts/reformat.py --dedup original_data/data.csv > data/data.tsv
```

## Stratified split into train/dev/test

```
python3 scripts/stratify.py --seed 1234 0.7 0.1 0.2 \
    data/{data,train,dev,test}.tsv
```

Check

```
md5sum data/{train,dev,test}.tsv
f3d17f9bf857ef1197694ebc5d3d8c2d  data/train.tsv
9ec62b8648d7d6aa93f2451b2e93f12d  data/dev.tsv
b09aec80145dcb9f9b3787c252885653  data/test.tsv
```

### Separate by task

```
mkdir sentiment
for s in train dev test; do cut -f 4,5 data/$s.tsv > sentiment/$s.tsv; done
```

```
mkdir topic
for s in train dev test; do cut -f 4,5 data/$s.tsv > topic/$s.tsv; done
```

### FastText experiments

Reformat for fasttext

```
for f in sentiment/*.tsv topic/*.tsv;
    do perl -pe 's/^(\S+)\t/__label__$1 /' $f > ${f%.tsv}.fasttext
done
```

```
export FASTTEXT=PATH-TO-FASTTEXT
```

Defaults, sentiment (~47%, majority baseline level)

```
$FASTTEXT supervised -input sentiment/train.fasttext -output sentiment.model
$FASTTEXT test sentiment.model.bin sentiment/dev.fasttext
```

Defaults, topic (~27%, majority baseline is 24%)

```
$FASTTEXT supervised -input topic/train.fasttext -output topic.model
$FASTTEXT test topic.model.bin topic/dev.fasttext
```

More epochs and subwords (~49% and ~24%, i.e. perhaps worse.)

```
for t in sentiment topic; do
    $FASTTEXT supervised -input $t/train.fasttext -output $t.model \
        -minn 3 -maxn 5 -epoch 25
    $FASTTEXT test $t.model.bin $t/dev.fasttext
done
```

FastText Wiki embeddings (~60% and ~62%)

```
wget https://dl.fbaipublicfiles.com/fasttext/vectors-wiki/wiki.et.vec
```

```
for t in sentiment topic; do
    $FASTTEXT supervised -input $t/train.fasttext -output $t.model \
        -pretrainedVectors wiki.et.vec -dim 300
    $FASTTEXT test $t.model.bin $t/dev.fasttext
done
```

More epochs and subwords (~57% and ~68%)

```
for t in sentiment topic; do
    $FASTTEXT supervised -input $t/train.fasttext -output $t.model \
        -pretrainedVectors wiki.et.vec -dim 300 -minn 3 -maxn 5 -epoch 25
    $FASTTEXT test $t.model.bin $t/dev.fasttext
done
```
