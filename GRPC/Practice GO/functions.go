package main

import (
	"fmt"
)

func add(x int, y int) int {
	return x + y
}

func add_(x, y int) int { // same type is able to unwrite one int
	return x + y
}

func swap(x, y string) (string, string) { // write (string, string) how many
	return y, x // return how many value
}

func split(sum int) (x, y int) { // == func split(sum int) (int, int) {
	x = sum * 4 / 9 //        return x, y
	y = sum - x     //    }
	return
}

func main() {
	fmt.Println(add(42, 13))
	fmt.Println(add_(42, 13))

	a, b := swap("hello", "world")
	fmt.Println(a, b)

	fmt.Println(split(17))
}
