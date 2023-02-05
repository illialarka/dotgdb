# Roadmap 

Contains short roadmap for future projects.

## Features

NOTE: Contains a list of planner features.


1. Condition expressions for `qlang`
   
    To have the ability to filter out query results conditional clauses would be valuable.

    Example:
    ```bash
    from locals select name, value where name = 'node'
    ```

2. Data pipes (formatters) for `qlang`

    To have an ability to format value of specific data types pipes would be valuable. 

    Example:
    ```bash
    from locals select name, value | json where name = 'grid'
    ```

    Applyes JSON formatter to grid, where grid is an object with properties.


TBD