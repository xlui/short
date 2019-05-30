package main

import (
	"database/sql"
	"log"
	"strconv"

	_ "github.com/mattn/go-sqlite3"
)

func checkErr(err error) {
	if err != nil {
		panic(err)
	}
}

func main() {
	db, err := sql.Open("sqlite3", "data-dev.sqlite3")
	checkErr(err)

	res, err := db.Exec("DROP TABLE IF EXISTS user")
	checkErr(err)
	log.Println("drop table: ", res)

	res, err = db.Exec("CREATE TABLE user(id INT PRIMARY KEY, username VARCHAR(32))")
	checkErr(err)
	log.Println("create table: ", res)

	// 插入数据
	statement, err := db.Prepare("INSERT INTO user(id, username) VALUES (?, ?)")
	checkErr(err)
	res, err = statement.Exec("1", "xlui")
	checkErr(err)
	id, err := res.LastInsertId()
	checkErr(err)
	log.Println("insert: ", id)

	// 更新
	statement, err = db.Prepare("UPDATE user SET username=? WHERE id=?")
	checkErr(err)
	res, err = statement.Exec("new_xlui", 1)
	checkErr(err)
	affect, err := res.RowsAffected()
	log.Println("update: ", affect)

	// 查询
	rows, err := db.Query("SELECT * FROM user")
	checkErr(err)
	for rows.Next() {
		var uid int
		var username string
		err = rows.Scan(&uid, &username)
		checkErr(err)
		log.Println("select: User[id=" + strconv.Itoa(uid) + ", username=" + username + "]")
	}

	// 删除
	statement, err = db.Prepare("DELETE FROM user WHERE id=?")
	checkErr(err)
	res, err = statement.Exec(id)
	checkErr(err)
	affect, err = res.RowsAffected()
	checkErr(err)
	log.Println("delete: ", affect)

	_ = db.Close()
}
