---
categories:
- Web-Development
title: WebAssembly
description: How to bring fast languages to the browser.
---

Make things in the browser fast, vroom vroom.

## Golang
When building WebAssembly in Go, just have to change the `GOOS` and `GOARCH` variable as following:
```bash
GOOS=js GOARCH=wasm go build -o main.wasm
```
Some parts of the code won't be compatible with the `GOOS=js`. You can exclude them by making a comment a the top of the file:
```go
//go:build !js
```
Now you can try to build again.

- Ressources: https://go.dev/wiki/WebAssembly#getting-started


