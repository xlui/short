package main

import (
	"fmt"
	"log"
	"net/http"
)

func getHello(w http.ResponseWriter, r *http.Request) {
	_ = r.ParseForm()
	fmt.Println(r.Form)
	fmt.Println("path", r.URL.Path)
	fmt.Println("scheme", r.URL.Scheme)
	fmt.Println(r.Form["key"])
	for key, value := range r.Form {
		fmt.Println("key: ", key)
		fmt.Println("value: ", value)
	}
	_, _ = fmt.Fprintln(w, "Hello xlui!")
}

func main() {
	http.HandleFunc("/", getHello)
	err := http.ListenAndServe("127.0.0.1:8080", nil)
	if err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}
