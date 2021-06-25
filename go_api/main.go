package main

// import "github.com/gin-gonic/gin"

import (
	"fmt"
	"database/sql"
	_ "github.com/go-sql-driver/mysql"
	"github.com/gin-gonic/gin"
	"io/ioutil"
)

func HomePage(c *gin.Context){
	c.JSON(200, gin.H{
		"messgae":"Hello",
	})
}

func PostHomePage(c *gin.Context){
	body := c.Request.Body
	value,err := ioutil.ReadAll(body)
	if err != nil{
		fmt.Println(err.Error())
	}
	c.JSON(200, gin.H{
		"message": string(value),
	})
}

func QueryParams(c *gin.Context){
	name := c.Query("name")
	age := c.Query("age")
	c.JSON(200, gin.H{
		"name": name,
		"age": age,
	})
}

func PathParams(c *gin.Context){
	name := c.Param("name")
	age := c.Param("age")
	c.JSON(200, gin.H{
		"name": name,
		"age": age,
	})
}

type Test struct{
	Id int `json:"id"`
	Date string `json:"date"`
	Appeal_no string `json:"appeal_no"`
	Ma_ra_no string `json:"ma_ra_no"`
	Title string `json:"title"`
	Pdf_downloaded string `json:"pdf_downloaded"`
}

func db_connection()(*sql.DB){
	// Database connection
	db, err := sql.Open("mysql","root:Auth@123@tcp(localhost:3306)/authbridge")
	if err != nil{
		panic(err.Error())
	}
	fmt.Println("DB connection created")
	// fmt.Println(reflect.TypeOf(db))
	return db
}

func db_select(c *gin.Context){
	db := db_connection()
	// select query
	results, err := db.Query("SELECT id,date,appeal_no,ma_ra_no,title,pdf_downloaded FROM sat_mumbai_script_search LIMIT 5;")
	if err != nil{
		panic(err.Error())
	}
	var all_responses []interface{}

	for results.Next(){
		var response map[string]string
		response = make(map[string]string)

		var test Test
		err = results.Scan(&test.Id,&test.Date,&test.Appeal_no,&test.Ma_ra_no,&test.Title,&test.Pdf_downloaded)
		if err != nil{
			c.JSON(404, gin.H{
				"message" :err.Error(),
			})
			panic(err.Error())
		}
		response["date"] = test.Date
		response["Appeal_no"] = test.Appeal_no
		all_responses = append(all_responses, response)
	}

	c.JSON(200, all_responses)

	
	fmt.Println(all_responses)
}

func db_insert(){
	db := db_connection()
	// insert query
	insert, err := db.Query("INSERT INTO test (mark) VALUES (1)")
	if err != nil{
		panic(err.Error())
	}
	defer insert.Close()
	defer db.Close()

}

func main(){
	// db_select()
	r := gin.Default()

	
	r.GET("/sat_mumbai",db_select)
	// r.GET("/", HomePage)
	// // r.POST("/", PostHomePage)
	// // r.GET("/query",QueryParams)
	// // r.GET("/path/:name/:age",PathParams)
	r.Run()
}
