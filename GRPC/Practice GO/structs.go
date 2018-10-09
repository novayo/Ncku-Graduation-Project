package main

import "fmt"

type Vertex struct {
	X int
	Y int
}

func main() {
	// 初始化
	v := Vertex{X: 1}
	v = Vertex{Y: 2}

	// 結構體字段使用點號來訪問。
	v.X = 4

	// Go有指針，但是沒有指針運算。
	// 感覺只能單純做地址訪問
	q := &v

	q.Y = 10
	fmt.Println(v)
}
