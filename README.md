# dataset_variance
Scripts and statistics for processing and normalizing volumes of MRI data

### Usage

```
python compute_metrics.py [atlas name]  [path to graphs] [output dir] [-f -v]
```

**Flags:**

- `-f`: formatting flag which parses one of two directory structures. If the flag
is absent, the expected structure is `.../atlas/dataset/graph` and if the flag is
present, the expected structure is `.../dataset/atlas/graph`.
- `-v`: toggles verbose output
