package main

import (
	"fmt"
	"math"
)

func main() {
	// function也可以拿來當作"值"
	hypot := func(x, y float64) float64 {
		return math.Sqrt(x*x + y*y)
	}

	fmt.Println(hypot(3, 4))
}
