package main

import (
	"fmt"
	"math"
)

type Vertex struct {
	X, Y float64
}

// 用struct實現class中的function
func (v *Vertex) getValue() (float64, float64) {
	return v.X, v.Y
}

type myfloat float64

func (f myfloat) abs() float64 {
	if f < 0 {
		return float64(-f)
	}
	return float64(f)
}

func main() {
	v := Vertex{3, 4}
	fmt.Println(v.getValue())

	f := myfloat(-math.Sqrt2)
	fmt.Println(f.abs())
}
