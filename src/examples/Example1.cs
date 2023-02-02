namespace Example;

public class UnionFind
{
    private readonly int[] _rank;
    private readonly int[] _root;
    
    public UnionFind(int size)
    {
        _rank = new int[size];
        _root = new int[size];
        
        for(var index = 0; index < size; index++)
        {
            _rank[index] = _root[index] = index;
        }
    }
    
    public int Find(int node)
    {
        if (node == _root[node])
        {
            return node;
        }
        
        return _root[node] = Find(_root[node]);
    }
    
    public bool Union(int first, int second)
    {
        var firstRoot = Find(first);
        var secondRoot = Find(second);
        
        if (firstRoot == secondRoot)
        {
            return false;
        }
        
        if (_rank[firstRoot] > _rank[secondRoot])
        {
            _root[secondRoot] = firstRoot;
        }
        else if (_rank[firstRoot] < _rank[secondRoot])
        {
            _root[firstRoot] = secondRoot;
        }
        else
        {
            _root[firstRoot] = secondRoot;
            _rank[firstRoot] += 1;
        }
            
        return true;
    } 
}

public class Program 
{
    public static void Main()
    {
        var planet = new char[][] {
            new char[] {'1','1','1','1','0'},
            new char[] {'1','1','0','1','0'},
            new char[] {'1','1','0','0','0'},
            new char[] {'0','0','0','0','0'}
        };

        System.Console.WriteLine(NumIslands(planet));
    }

    public static int NumIslands(char[][] grid)
    {
        // x, y
        var directions = new (int, int)[]
        {
            (0, 1),
            (1, 0),
            (0, -1),
            (-1, 0),
        };

        var rows = grid.Length;
        var cols = grid[0].Length;
        var disjointSet = new UnionFind(rows * cols); 
        var components = 0;
        
        for (var index = 0; index < rows; index++)
        {
            for (var jindex = 0; jindex < cols; jindex++)
            {
                if (grid[index][jindex] == '1')
                {
                    components++;
                    var currentNode = index * cols + jindex;
                    foreach ((int x, int y) in directions)
                    {
                        var dx = index + x;
                        var dy = jindex + y;
                        
                        if (dx >= 0 && dy >= 0 && dx < rows && dy < cols && grid[dx][dy] == '1')
                        {
                            if (disjointSet.Union(dx * cols + dy, currentNode))
                            {
                                components--;
                            }
                        }
                    }
                }
            }
        }
        
        return components;
    }
}