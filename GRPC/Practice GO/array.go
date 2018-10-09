package main

import "fmt"

func main() {
	var a [2]string
	a[0] = "Hello"
	a[1] = "World"
	fmt.Println(a[0], a[1])
	fmt.Println(a)

	// 等於
	b := []string{"Hello", "World"}
	fmt.Println(b[0], b[1])
	fmt.Println(b)

	p := []int{2, 3, 5, 7, 11, 13}
	fmt.Println("p[1:4] ==", p[1:4])
	fmt.Println("p[:3] ==", p[:3])
	fmt.Println("p[4:] ==", p[4:])
}
