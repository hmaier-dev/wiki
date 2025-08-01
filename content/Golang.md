---
categories:
- coding
title: Golang
---

Go ist eine kompilierte Sprache die von Google entwickelt wurde. 

## Imports

Go mag keine relativen Imports. Daher muss immer der absolute Pfad angeben werden.

```go
import (
    // Module befindet sich in ./pkg/loading
	"github.com/hmaier-dev/contacts_converter/pkg/loading"
    // Falsch wäre:
    "../pkg/loading"
)
```

Ein Underscore stellt eine Blank-Import dar. Das heißt, man selbst greift nicht auf das Module zu, sondern andere 
Module die man importiert hat. Man sieht dies bspw. beim Import eines SQLite-Drivers
```go
import (
    "database/sql"
    _ "github.com/mattn/go-sqlite3" // needed for database/sql when working with sqlite3
)
```

## Schlafende Go-Routine neustarten 

Ich bin heute auf den Fall gestoßen, eine schlafende Go-Routine
neustarten zu müssen. Da man `time.Sleep(d)` nicht unterbrechen, bzw.
nicht zum Aufwecken zwingen kann, benutzt man daher `time.After(d)`.

`time.After(d)` macht einen Channel auf, den man zusammen mit dem
Channel, über welchen man sein Signal senden möchte, an ein
`select`-Statement andockt. `select` hört nun beide Channels ab und
führt bei eintreffen eines Signals, den jeweiligen Logik-Block aus.

``` go

var restartSignal = make(chan bool)
func main() {
    go maintain()
    for{
        time.Sleep(time.Second * 7)
        restartSignal <- true
        fmt.Println("Lets restart!")
        close(restartSignal) // alten Channel schließen
        restartSignal = make(chan bool) //neuen Channel öffnen
        go maintain()
    }
}
func maintain() {
    count := 0
    for{
        count++
        fmt.Printf("Iteration.. %d\n", count)
        select{
            case <-restartSignal:
                return // Funktion beenden
            case <-time.After(time.Second * 3):
                break // Aus select ausbrechen und nächste Iteration einleiten
        }
    }
}

```

## Modules forken
Hat man ein Module was nicht so funktioniert, wie man es möchte, macht man sich einfach einen Fork davon.
Nun hat man die Macht Änderungen um Code vorzunehmen. Sollen diese Änderungen direkt im Hauptprojekt nutzbar sein, kann
man das geforkte Repository klonen und Go dazu bringen, dies zu nutzen. Dies tut man in der `go.mod` mit dem `replace`-Kommando.

```go
require (
	github.com/emersion/go-vcard v0.0.0-00010101000000-000000000000
)

replace github.com/emersion/go-vcard => ../go-vcard

```
Den Pfad des geforkten Repositorys muss man von den root des Hauptprojekts angeben.

## Datenbanken

### Initialzing connection
To work with databases you need
```go
func Init() *sql.DB {
	db, err := sql.Open("sqlite3", "/opt/tool/sqlite.db")
	if err != nil {
		log.Fatal("Failed to connect to database:", err)
	}

	// Create the devices table if it doesn't exist
	createStmt := `
	CREATE TABLE IF NOT EXISTS nice_table (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		important_data TEXT
	);
	`
	_, err = db.Exec(createStmt)
	if err != nil {
		log.Fatal("Failed to create table:", err)
	}
  return db
}
```
Instead of return `*sql.DB` you could also create a global variable.
```go
var db *sql.DB
```
### Scan into struct

```go
func GetDataByID(db *sql.DB, id int)(*data.Entry, error){
	query := `SELECT imei, name, ticket, model, yaml FROM checklists WHERE id = ?`
	row := db.QueryRow(query, id)
	var singleEntry data.Entry

	err := row.Scan(&singleEntry.IMEI, &singleEntry.Name, &singleEntry.Ticket, &singleEntry.Model, &singleEntry.Yaml)
	if err != nil {
		if err == sql.ErrNoRows {
			log.Printf("No entry found for ID %s", id)
			return nil, nil
		}
		log.Fatal("Failed to scan entry:", err)
		return nil, err
	}

	return &singleEntry, nil
}
```


### Select * from table
This is not so easy as you think. Because you need a fixed destination for the values you received by `rows.Scan`.

```go
    db, err := sql.Open("sqlite3", source)
    if err != nil{
        fmt.Println(err)
    }
    rows, err := db.Query("Select * from table;")
    if err != nil{
        log.Fatalf("%#v\n", err)
    } 
    cols, err := rows.Columns()

    if err != nil{
        log.Fatalf("%#v\n", err)
    } 
	rawResult := make([][]byte, len(cols)) // [row][values] -> e.g. row: [[value][value][value]]
	dest := make([]interface{}, len(cols)) // .Scan() needs []any as result type
	allRows := make([][]string, 0)
	for i := range cols {
		dest[i] = &rawResult[i] // mapping dest indices to byte slice
	}
	for rows.Next() {
		err := rows.Scan(dest...)
		if err != nil {
			log.Fatal("problems scanning the database", err)
		}
		singleRow := make([]string, len(cols))
		for i, raw := range rawResult {
			singleRow[i] = string(raw) // from byte to string
			//fmt.Printf("%v -> %v \n", i, singleRow)
		}
		allRows = append(allRows, singleRow)
	}
    
    fmt.Printf("%v\n", allRows)

```
### Error: `Error scanning row: sql: expected 1 destination arguments in Scan, not 3`
Überprüfen, ob du in deinem `SELECT`-Statemnt wirklich 3 Spalten angefragt hast.

### SQL Compiler
There is a library that compiles sql into type-safe code:
 - https://github.com/sqlc-dev/sqlc
Why this, there wouldn't be the need to care about structs in go and about the sql-queries.
I just would write sql and use the queries in go as functions!!

## Commandline Arguments
If you need something quick, without a variable info, just use this snippet:
```go
if len(os.Args) > 1{
    for _ , s := range os.Args[1:]{ // index 0 is the name of the program, so slice it away
        switch s {
        case "--exporter":
            db.Export()
        default:
            fmt.Printf("Argument unknown: %s \n", s)
            os.Exit(0)
        }
    }

}
```
For more complex stuff, use the `flag`-package.

## Windows stuff
If you think about call the powershell from golang like this:
```
cmd := exec.Command("powershell", "-nologo", "-noprofile")
```
There is also a windows-package to make syscalls: https://pkg.go.dev/golang.org/x/sys/windows

## Context 

The `context`-package is used to manage cancellation-signals, deadline
and request-scoped values.

``` go
package main
import (
    "context"
    "fmt"
    "time"
)

func main() {
    // Create a parent context
    parent := context.Background()

    // Create a child context with a deadline set to 100 ms 
    ctx, cancel := context.WithDeadline(parent, time.Now().Add(100*time.Millisecond))
    defer cancel() // Make sure to call cancel to release resources

    select {
    case <-time.After(200 * time.Millisecond):
        fmt.Println("Operation completed") // this won't be reached
    case <-ctx.Done():
        fmt.Println("Operation canceled due to deadline") // this will be reached
    }
}
```

## Go-Routines 

Goroutines make concurrency possible. That means, running two seperate
function seperatly without dependency between them. Different goroutines
communicate via **channels**.

``` go
package main

import (
    "fmt"
    "time"
)

func count(name string) {
    for i := 1; i <= 5; i++ {
        fmt.Println(name, ":", i)
        time.Sleep(100 * time.Millisecond)
    }
}

func main() {
    go count("goroutine")
    count("main function")
    time.Sleep(1 * time.Second)
}
```

## Channels 

They allow safe data exchange and data synchronization between
goroutines without shared memory access.

## gorilla/mux

- https://github.com/gorilla/mux

### `Walk`-Function
If you want to get all `GET`-routes for building a navbar, you can use the Walk funktion.
```golang
type NavItem struct {
    Name string
    Path string
}
var nav []NavItem
func IndexRoute(router *mux.Router){
	router.Walk(func(route *mux.Route, router *mux.Router, ancestors []*mux.Route) error {
		path, _ := route.GetPathTemplate()
        method, _ := route.GetMethods()
		if len(method) > 0 && method[0] == "GET"{
			entry := NavItem{
				Name: path,
				Path: path,
			}
			nav = append(nav, entry)
		}
    return nil
	})
}

```
## Code Analysis
To see flaws in your code-base, you can use [`staticcheck ./...`](https://staticcheck.dev/docs/)(external tool) or `go vet ./...`(part of the go toolchain).

