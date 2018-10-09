package main

import "fmt"

func main() {
	sum := 0
	// 省略(), 不支援++i
	// 也可以寫成 for ; sum < 1000; {sum += sum}
	// 或        for  sum < 1000 {sum += sum}
	for i := 0; i < 10; i++ {
		sum += i
	}
	// 因此無窮迴圈只要寫成 for {} 就好
	fmt.Println(sum)
}
