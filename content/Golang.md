# Golang 

Go ist eine kompilierte Sprache die von Google entwickelt wurde.

## Typen 

Go stellt alle gängigen Typen bereit. Besonderheiten sind:

-   `byte`: dieser ist ein alias für uint8
-   `rune`: ein alias für int32 welches ein Unicode-Zeichen
    repräsentiert

``` 
package main

func main() {
    println("Hello World")
}
```

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
function seperatly without dependency between them. Different goruntes
communicate via []{#channels}**channels**.

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
