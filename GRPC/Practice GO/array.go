package main

import "fmt"

func main() {
	/***** array *****/
	var a [2]string
	a[0] = "Hello"
	a[1] = "World"
	fmt.Println(a[0], a[1])
	fmt.Println(a)

	/***** slice *****/
	b := []string{"Hello", "World"}
	fmt.Println(b[0], b[1])
	fmt.Println(b)

	p := []int{2, 3, 5, 7, 11, 13}
	fmt.Println("p[1:4] ==", p[1:4])
	fmt.Println("p[:3] ==", p[:3])
	fmt.Println("p[4:] ==", p[4:])

	// 另一種方法建立slice
	a := make([]int, 5)
	printSlice("a", a)
	b := make([]int, 0, 5) //len(b)=0, cap(b)=5
	printSlice("b", b)
	c := b[:2]
	printSlice("c", c)
	d := c[2:5]
	printSlice("d", d)

	var z []int
	fmt.Println(z, len(z), cap(z))
	if z == nil { // 若陣列為空(index(len())以及長度(cap()) = 0) 稱作nil
		fmt.Println("nil!")
	}
}

func printSlice(s string, x []int) {
	fmt.Printf("%s len=%d cap=%d %v\n",
		s, len(x), cap(x), x)
}
