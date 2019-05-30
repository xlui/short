package main

import (
	"encoding/json"
	"fmt"
	"log"
)

type User struct {
	Id       int    `json:"id"`
	Username string `json:"username"`
	Password string `json:"password"`
}

func main() {
	u := User{Id: 1, Username: "xlui", Password: "pass"}
	bytes, err := json.Marshal(u)
	if err != nil {
		log.Fatalln("JSON marshal error: ", err)
	}
	fmt.Println(string(bytes))
}
