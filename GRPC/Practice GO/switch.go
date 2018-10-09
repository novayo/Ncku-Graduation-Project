package main

import (
	"fmt"
	"runtime"
)

func main() {
	fmt.Print("Go runs on ")
	// 可以在條件之前執行一個簡單的語句。
	// switch 的條件從上到下的執行，當匹配成功的時候停止
	switch os := runtime.GOOS; os {
	case "darwin":
		fmt.Println("OS X.")
	case "linux":
		fmt.Println("Linux.")
	default:
		// freebsd, openbsd,
		// plan9, windows...
		fmt.Printf("%s.", os)
	}
}

/* 沒有條件的 switch 同 switch true 一樣。
 * 這一構造使得可以用更清晰的形式來編寫長的 if-then-else 鏈。
 *
 */
