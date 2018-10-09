package main

import (
	"fmt"
	"math"
)

func sqrt(x float64) string {
	// 省略()
	if x < 0 {
		return sqrt(-x) + "i"
	}
	return fmt.Sprint(math.Sqrt(x))
}

func pow(x, n, lim float64) float64 {
	// 可以在條件之前執行一個簡單的語句。
	if v := math.Pow(x, n); v < lim {
		return v
	} else if v == lim {
		fmt.Println("v == lim")
	} else {
		fmt.Println("v > lim")
	}
	return lim
}

func main() {
	//fmt.Println(sqrt(2), sqrt(-4))
	fmt.Println(
		pow(3, 2, 9),  // 會先做完這兩個pow內發生的事情(像是print)，
		pow(3, 3, 20), //之後才會顯示return值
	)
}
