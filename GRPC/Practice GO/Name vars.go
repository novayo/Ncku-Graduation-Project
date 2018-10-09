package main

import "fmt"

var i, j int = 1, 2                      // the default is 0
var d, python, java = true, false, "no!" // it's fine to ignore type

// 也可以這樣寫
var (
	a int = 1
	b     = 2.2
	c     = float64(a) + b //強制轉型字符、字符串、布爾或數字類型
)

const (
	pi    = 3.14     // const可以是
	Big   = 1 << 100 // bitwise
	Small = Big >> 99
)

func main() {
	z := 3 // := 等於 var，只不過:=只能寫在函式內
	fmt.Println(i, j, d, python, java, z, a, b, c)
	fmt.Println(needInt(Small))
	fmt.Println(needFloat(Small))
	fmt.Println(needFloat(Big))
}

func needInt(x int) int { return x*10 + 1 }
func needFloat(x float64) float64 {
	return x * 0.1
}
