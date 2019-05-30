package main

import (
	"encoding/json"
	"fmt"
)

type User struct {
	Id       int    `json:"id"`
	Username string `json:"username"`
	Password string `json:"password"`
}

func main() {
	var user User
	str := `{"id": 1, "username": "xlui", "password": "pass"}`
	_ = json.Unmarshal([]byte(str), &user)
	fmt.Println(user)
}
