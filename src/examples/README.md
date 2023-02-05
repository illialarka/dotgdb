# Insipration Example 

The `Example1.cs` file contains an example program for debugging. The problem of finding the number of islands on the planet. The data structure used for solving is `DisjointSet`.

We want to understand the vertices numbers values of which root search is called recursively.

Build example in debug mode:

```bash
dotnet build ./Example1.cs -c Debug
```

Run the `dotgdb` tool targeting `Example1.dll`:

```bash
cd src/srv
./run.sh
```

Set a breakpoint in the `Find` method on line 21.

```bash
break Example.UnionFind:Find:21
```

Output:
```bash
Breakpoint 1 has been set at 0x01: /Users/illialarka/projects/debuggable/FileSystem/Program.cs, line 21.
```

Add query to the newly placed breakpoint.
```bash
query -id 1 'from params select name, value'
```

Output:
```bash
A query has been added.
```

Start recoding:
```bash
record
```

Output:
```bash
Running recording breakpoints will not stop execution. Are you sure? [Y/N]Y
Running recording.
To stop exeuction hit Ctrl + Z.
1
```

The `dotgdb` will create a csv file named `breakpoint_{request_id}_{method_name}_{line_number}.csv` containing the query results.

The file `breakpoint_1_Find_21.csv`:

<p align="center">
  <img src="https://raw.githubusercontent.com/illialarka/dotgdb/main/docs/imgs/query_result1.png" alt="Query result `from params select name, value">
</p>

1 - expected file name

2 - table with query results