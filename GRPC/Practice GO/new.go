package main

import "fmt"

type Vertex struct {
	X, Y int
}

func main() {
	v := new(Vertex) // 等於 var v *Vertex = new(Vertex)
	fmt.Println(v)
	v.X, v.Y = 11, 9 // 與python一樣的寫法
	fmt.Println(v)
}
