# qlang

Contains `qlang` implementation.

## Getting started

```bash
cd qlang
python3 cli.py --mode tree --query locals 
```

See also defined examples of queries. 

## qlang CLI 

Contains commands to improve developing process.

### Parameters

* `mode` - specifies handler for a passed query.
* `query` - one of predefined query example.

### Output

The `tree` mode will produce `_expression_tree.png` file with visual representation of query parsing.

For example:

```query
from locals select index, name
```

<p align="center">
  <img src="https://raw.githubusercontent.com/illialarka/dotgdb/master/docs/imgs/expression_tree_example1.png">
</p>

