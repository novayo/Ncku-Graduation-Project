package main

import "fmt"

type Vertex struct {
	Lat, Long float64
}

// 創建map
var m = map[string]Vertex{
	// 也可以省略vertex變成"Bell Labs":{}
	"Bell Labs": Vertex{
		40.68433, -74.39967,
	},
	"Google": Vertex{
		37.42202, -122.08408,
	},
}

func main() {
	// 建立map的值
	m = make(map[string]Vertex)
	m["Eric"] = Vertex{
		66.6666, -66.6666,
	}
	fmt.Println(m["Eric"])

	// map操作
	m["Answer"] = Vertex{42, 43}
	fmt.Println("The valu, 43}e:", m["Answer"])

	m["Answer"] = Vertex{48, 49}
	fmt.Println("The value:", m["Answer"])

	delete(m, "Answer")
	fmt.Println("The value:", m["Answer"])

	// 用print去讀取map，會回傳"值"
	// 用var去讀取map，若只有一個變數會回傳"值"，若是兩個 會回傳"值+布林值"
	value, ok := m["Answer"]
	fmt.Println("The value:", value, "Present?", ok)
}
